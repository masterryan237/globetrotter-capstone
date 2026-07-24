from flask import Blueprint, request, jsonify
from app.auth import token_required
from app.models import load_itineraries, save_itineraries
import uuid
import datetime

itineraries_bp = Blueprint('itineraries', __name__)


@itineraries_bp.route('/itineraries', methods=['POST'])
@token_required
def create_itinerary(current_user):
    """Crée un nouvel itinéraire"""
    data = request.get_json()

    # Validation
    required_fields = ['title', 'destinations', 'start_date', 'end_date']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Champ requis manquant: {field}'}), 400

    # Charge les itinéraires existants (c'est TOUJOURS une liste maintenant)
    itineraries = load_itineraries()

    # Crée le nouvel itinéraire
    itinerary = {
        'id': str(uuid.uuid4()),
        'user': current_user,
        'title': data['title'],
        'destinations': data['destinations'],
        'start_date': data['start_date'],
        'end_date': data['end_date'],
        'notes': data.get('notes', ''),
        'created_at': datetime.datetime.utcnow().isoformat(),
        'updated_at': datetime.datetime.utcnow().isoformat()
    }

    # Ajoute à la liste
    itineraries.append(itinerary)
    save_itineraries(itineraries)

    return jsonify({
        'message': 'Itinéraire créé avec succès',
        'itinerary': itinerary
    }), 201


@itineraries_bp.route('/itineraries', methods=['GET'])
@token_required
def list_itineraries(current_user):
    """Liste tous les itinéraires de l'utilisateur connecté"""
    itineraries = load_itineraries()

    # Filtre par utilisateur (itineraries est toujours une liste)
    user_itineraries = [i for i in itineraries if i.get('user') == current_user]

    return jsonify({
        'count': len(user_itineraries),
        'itineraries': user_itineraries
    }), 200