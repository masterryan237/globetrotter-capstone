from app import create_app

app = create_app()

if __name__ == '__main__':
    print("🌍 GlobeTrotter Travel Assistant")
    print("📡 Démarrage du serveur sur http://localhost:5000")
    print("📚 Documentation des endpoints :")
    print("   POST /register - Créer un compte")
    print("   POST /login - Se connecter")
    print("   GET /destinations - Rechercher des destinations")
    print("   GET /recommendations - Recommandations personnalisées (JWT requis)")
    print("   POST /itineraries - Créer un itinéraire (JWT requis)")
    print("   GET /itineraries - Lister ses itinéraires (JWT requis)")
    print("-" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)