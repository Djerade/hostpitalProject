# Utilisation de l'image Python officielle
FROM python:3.10-slim

# Définition du répertoire de travail
WORKDIR /app

# Copie des fichiers nécessaires
COPY requirements.txt requirements.txt
COPY app/ ./app/

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposition du port pour Flask
EXPOSE 5000

# Lancement de l'application Flask
CMD ["python3", "app/main.py"]
