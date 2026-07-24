import json
import os
from threading import Lock

# Verrou pour éviter les problèmes de concurrence
file_lock = Lock()

# Chemins des fichiers
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
ITINERARIES_FILE = os.path.join(DATA_DIR, 'itineraries.json')
DESTINATIONS_FILE = os.path.join(DATA_DIR, 'destinations.json')

def load_data(filename, default=None):
    """Charge les données depuis un fichier JSON"""
    if default is None:
        default = {}
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_data(data, filename):
    """Sauvegarde les données dans un fichier JSON"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with file_lock:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

# Fonctions spécifiques pour chaque type de données

def load_users():
    """Charge les utilisateurs - retourne TOUJOURS un dictionnaire"""
    return load_data(USERS_FILE, default={})

def save_users(users):
    save_data(users, USERS_FILE)

def load_itineraries():
    """Charge les itinéraires - retourne TOUJOURS une liste"""
    return load_data(ITINERARIES_FILE, default=[])

def save_itineraries(itineraries):
    save_data(itineraries, ITINERARIES_FILE)

def load_destinations():
    return load_data(DESTINATIONS_FILE, default={})