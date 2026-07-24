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

def load_data(filename):
    """Charge les données depuis un fichier JSON"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return [] if 'destinations' not in filename else {}
    except json.JSONDecodeError:
        return [] if 'destinations' not in filename else {}

def save_data(data, filename):
    """Sauvegarde les données dans un fichier JSON"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with file_lock:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

# Fonctions spécifiques pour chaque type de données

def load_users():
    return load_data(USERS_FILE)

def save_users(users):
    save_data(users, USERS_FILE)

def load_itineraries():
    return load_data(ITINERARIES_FILE)

def save_itineraries(itineraries):
    save_data(itineraries, ITINERARIES_FILE)

def load_destinations():
    return load_data(DESTINATIONS_FILE)