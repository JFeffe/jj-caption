# 🚀 JJ Caption - Guide de Déploiement

## 📋 Options de Déploiement

### **🌐 Option 1 : Déploiement Web (Recommandé)**
- ✅ Accessible partout
- ✅ Pas d'installation côté client
- ✅ Mises à jour automatiques
- ✅ Interface moderne

### **💻 Option 2 : Application Desktop**
- ✅ Performance maximale
- ✅ Fonctionne hors ligne
- ✅ Pas de coût serveur

---

## 🌐 Déploiement Web

### **A. Streamlit Cloud (Gratuit - Recommandé)**

#### **Étape 1 : Préparer le repository**
```bash
# Créer un repository GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/votre-username/jj-caption.git
git push -u origin main
```

#### **Étape 2 : Déployer sur Streamlit Cloud**
1. Allez sur [share.streamlit.io](https://share.streamlit.io)
2. Connectez-vous avec GitHub
3. Sélectionnez votre repository
4. Cliquez "Deploy"
5. Votre app sera disponible en 2 minutes !

**URL finale :** `https://jj-caption-votre-username.streamlit.app`

### **B. Heroku (Payant - Professionnel)**

#### **Étape 1 : Installer Heroku CLI**
```bash
# Windows
winget install Heroku.HerokuCLI

# Ou télécharger depuis heroku.com
```

#### **Étape 2 : Déployer**
```bash
# Login
heroku login

# Créer l'app
heroku create jj-caption-app

# Déployer
git push heroku main

# Ouvrir
heroku open
```

### **C. VPS/Cloud (AWS, Azure, GCP)**

#### **Avec Docker (Recommandé)**
```bash
# Construire l'image
docker build -t jj-caption .

# Lancer le conteneur
docker run -d -p 8501:8501 --name jj-caption jj-caption

# Ou avec docker-compose
docker-compose up -d
```

#### **Sans Docker**
```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'app
streamlit run run_web_app.py --server.port=8501 --server.address=0.0.0.0
```

---

## 💻 Application Desktop

### **A. PyInstaller (Simple)**

#### **Étape 1 : Installer PyInstaller**
```bash
pip install pyinstaller
```

#### **Étape 2 : Créer l'exécutable**
```bash
# Version simple
pyinstaller --onefile run_web_app.py

# Version avec interface
pyinstaller --onefile --windowed --name "JJ Caption" run_web_app.py

# Version complète
pyinstaller --onefile --windowed --add-data "src;src" --name "JJ Caption" run_web_app.py
```

#### **Étape 3 : Distribuer**
- L'exécutable sera dans `dist/JJ Caption.exe`
- Partagez le fichier .exe

### **B. Electron (Professionnel)**

#### **Étape 1 : Créer l'app Electron**
```bash
# Initialiser le projet
npm init -y
npm install electron electron-builder

# Créer main.js
```

#### **Étape 2 : Configurer le build**
```json
{
  "scripts": {
    "start": "electron .",
    "build": "electron-builder"
  },
  "build": {
    "appId": "com.jjcaption.app",
    "productName": "JJ Caption",
    "directories": {
      "output": "dist"
    }
  }
}
```

---

## 🔧 Configuration Avancée

### **Variables d'Environnement**
```bash
# .env
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
WHISPER_MODEL=medium
FFMPEG_PATH=/usr/bin/ffmpeg
```

### **Nginx (Reverse Proxy)**
```nginx
server {
    listen 80;
    server_name jj-caption.votre-domaine.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

---

## 📊 Comparaison des Options

| Critère | Web | Desktop |
|---------|-----|---------|
| **Facilité d'usage** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Performance** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Coût** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Mises à jour** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Accessibilité** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Confidentialité** | ⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🎯 Recommandation Finale

### **Pour commencer : Streamlit Cloud**
- ✅ Gratuit
- ✅ Déploiement en 5 minutes
- ✅ Interface professionnelle
- ✅ Mises à jour automatiques

### **Pour production : VPS + Docker**
- ✅ Contrôle total
- ✅ Performance optimale
- ✅ Coût raisonnable
- ✅ Scalabilité

### **Pour usage local : PyInstaller**
- ✅ Simple à distribuer
- ✅ Fonctionne hors ligne
- ✅ Pas de coût serveur

---

## 🚀 Démarrage Rapide

### **Option Web (Recommandée)**
```bash
# 1. Push sur GitHub
git push origin main

# 2. Déployer sur Streamlit Cloud
# → Allez sur share.streamlit.io
# → Connectez votre repo
# → Deploy !

# 3. Votre app est en ligne !
```

### **Option Desktop**
```bash
# 1. Créer l'exécutable
pyinstaller --onefile --windowed run_web_app.py

# 2. Distribuer dist/JJ Caption.exe
# → Partagez le fichier .exe
```

---

## 🎉 Votre JJ Caption est prêt !

**Choisissez votre option et déployez ! 🚀** 