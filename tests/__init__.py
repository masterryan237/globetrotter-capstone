from flask import Flask
from flask_cors import CORS


def create_app():
    """Application Factory Pattern"""
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = 'globetrotter-secret-change-in-prod'

    # Enable CORS pour les appels cross-origin
    CORS(app)

    # Register blueprints (routes)
    from app.auth import auth_bp
    from app.destinations import destinations_bp
    from app.recommendations import recommendations_bp
    from app.itineraries import itineraries_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(destinations_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(itineraries_bp)

    return app