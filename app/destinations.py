from flask import Blueprint, request, jsonify
from app.models import load_destinations

destinations_bp = Blueprint('destinations', __name__)


@destinations_bp.route('/destinations', methods=['GET'])
def search_destinations():
    """Recherche des destinations avec filtres optionnels"""
    destinations = load_destinations()

    # Récupère les paramètres de filtre
    tag = request.args.get('tag')
    max_cost = request.args.get('max_cost', type=float)

    results = destinations.get('destinations', [])

    # Applique les filtres
    if tag:
        results = [d for d in results if tag.lower() in [t.lower() for t in d.get('tags', [])]]

    if max_cost is not None:
        results = [d for d in results if d.get('cost_per_day', float('inf')) <= max_cost]

    return jsonify({
        'count': len(results),
        'destinations': results
    }), 200