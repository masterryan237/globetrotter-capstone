# Image Python officielle
FROM python:3.9-slim

# Définit le répertoire de travail
WORKDIR /app

# Copie les dépendances
COPY requirements.txt .

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie le code source
COPY app/ ./app/
COPY data/ ./data/

# Expose le port
EXPOSE 5000

# Définit les variables d'environnement
ENV FLASK_DEBUG=0
ENV PORT=5000

# Commande pour lancer l'application
CMD ["python", "app/main.py"]