from flask import Blueprint, jsonify
from app.auth import token_required
from app.models import load_users, load_destinations

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/recommendations', methods=['GET'])
@token_required
def get_recommendations(current_user):
    """Retourne des recommandations basées sur les préférences utilisateur"""
    # Charge les données
    users = load_users()
    destinations = load_destinations()
    
    # Récupère les préférences de l'utilisateur
    user = users.get(current_user)
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    preferences = user.get('preferences', [])
    
    if not preferences:
        return jsonify({
            'message': 'Aucune préférence définie. Voici nos destinations populaires.',
            'recommendations': destinations.get('destinations', [])[:5]
        }), 200
    
    # Algorithme simple de recommandation basé sur les tags
    all_destinations = destinations.get('destinations', [])
    scored_destinations = []
    
    for dest in all_destinations:
        # Calcule un score basé sur le nombre de préférences qui matchent
        dest_tags = [t.lower() for t in dest.get('tags', [])]
        matching_tags = [p for p in preferences if p.lower() in dest_tags]
        score = len(matching_tags)
        
        if score > 0:
            scored_destinations.append({
                **dest,
                'match_score': score,
                'matching_preferences': matching_tags
            })
    
    # Trie par score décroissant
    scored_destinations.sort(key=lambda x: x['match_score'], reverse=True)
    
    return jsonify({
        'user_preferences': preferences,
        'count': len(scored_destinations),
        'recommendations': scored_destinations
    }), 200