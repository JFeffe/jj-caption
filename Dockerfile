# JJ Caption - Dockerfile pour déploiement
FROM python:3.9-slim

# Installer FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Exposer le port
EXPOSE 8501

# Commande de démarrage
CMD ["streamlit", "run", "run_web_app.py", "--server.port=8501", "--server.address=0.0.0.0"] 