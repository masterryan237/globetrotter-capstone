from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from app.models import load_users, save_users

auth_bp = Blueprint('auth', __name__)

# Clé secrète pour JWT (en production, utilisez une variable d'environnement)
SECRET_KEY = 'globetrotter-secret-change-in-prod'


@auth_bp.route('/register', methods=['POST'])
def register():
    """Enregistre un nouvel utilisateur"""
    data = request.get_json()

    # Validation basique
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username et password requis'}), 400

    username = data['username']
    password = data['password']
    preferences = data.get('preferences', [])

    # Charge les utilisateurs existants
    users = load_users()

    # Vérifie si l'utilisateur existe déjà
    if username in users:
        return jsonify({'error': 'Utilisateur déjà existant'}), 400

    # Crée le nouvel utilisateur
    users[username] = {
        'username': username,
        'password_hash': generate_password_hash(password),
        'preferences': preferences,
        'created_at': datetime.datetime.utcnow().isoformat()
    }

    # Sauvegarde
    save_users(users)

    return jsonify({
        'message': 'Utilisateur créé avec succès',
        'username': username
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Authentifie un utilisateur et retourne un token JWT"""
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username et password requis'}), 400

    username = data['username']
    password = data['password']

    # Charge les utilisateurs
    users = load_users()

    # Vérifie l'utilisateur
    if username not in users:
        return jsonify({'error': 'Utilisateur non trouvé'}), 401

    user = users[username]

    # Vérifie le mot de passe
    if not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Mot de passe incorrect'}), 401

    # Crée le token JWT (expire dans 24h)
    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({
        'message': 'Connexion réussie',
        'token': token,
        'username': username,
        'preferences': user['preferences']
    }), 200


def token_required(f):
    """Décorateur pour protéger les routes avec JWT"""
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Récupère le token du header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'error': 'Token manquant'}), 401

        try:
            # Décode le token
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expiré'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token invalide'}), 401

        return f(current_user, *args, **kwargs)

    return decorated