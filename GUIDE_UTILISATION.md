# 🎬 JJ Caption - Guide d'Utilisation

## 📋 Table des Matières
1. [Installation](#installation)
2. [Interface Web](#interface-web)
3. [Ligne de Commande](#ligne-de-commande)
4. [Formats Supportés](#formats-supportés)
5. [Options Avancées](#options-avancées)
6. [Exemples d'Utilisation](#exemples-dutilisation)
7. [Dépannage](#dépannage)

---

## 🚀 Installation

### Prérequis
- Python 3.8 ou plus récent
- FFmpeg (installé automatiquement via WinGet sur Windows)

### Installation des dépendances
```bash
pip install -r requirements.txt
```

---

## 🌐 Interface Web

### Lancement
```bash
python run_web_app.py
```
L'interface sera disponible à l'adresse : **http://localhost:8501**

### Utilisation
1. **Upload** : Glissez-déposez votre fichier vidéo/audio
2. **Configuration** : Ajustez les paramètres dans la sidebar
3. **Transcription** : Cliquez sur "Lancer la transcription"
4. **Téléchargement** : Récupérez les fichiers générés

### Options Avancées (Interface Web)
- ✅ **Post-traitement avancé** : Correction automatique d'erreurs
- ⚙️ **Options Whisper** : Température, seuils, contexte
- 📺 **Format TXT professionnel** : Timecodes LTC pour diffusion

---

## 💻 Ligne de Commande

### Script Simple
```bash
# Transcription basique
python transcribe_video.py video.mp4

# Formats multiples
python transcribe_video.py video.mp4 srt,txt,vtt

# Modèle spécifique
python transcribe_video.py video.mp4 srt,txt medium
```

### Interface CLI Complète
```bash
# Transcription avec options
python main.py video.mp4 --language French --output srt,txt,vtt

# Modèle et répertoire de sortie
python main.py video.mp4 --model medium --output-dir ./subtitles

# Aide
python main.py --help
```

---

## 📁 Formats Supportés

### Formats de Sortie
| Format | Description | Usage |
|--------|-------------|-------|
| **SRT** | SubRip standard | Lecteurs vidéo, YouTube |
| **VTT** | WebVTT moderne | Web, streaming |
| **TXT** | Diffusion professionnelle | Broadcast, TV |
| **SCC** | Scenarist | Broadcast professionnel |
| **ASS** | Advanced SubStation | Édition avancée |
| **JSON** | Données structurées | Traitement automatique |

### Format TXT Professionnel
Le format TXT génère des fichiers de diffusion avec :
- ⏰ **Timecodes LTC** : Format `HH:MM:SS;FF`
- 📺 **Codes de contrôle** : `¶÷142C`, `¶÷1426÷142D÷1470`
- 🎯 **Segmentation intelligente** : Pauses et découpage optimal
- 📋 **En-tête professionnel** : Métadonnées complètes

---

## 🔧 Options Avancées

### Post-traitement
- **Correction d'erreurs** : Dictionnaire de corrections françaises
- **Amélioration ponctuation** : Points, virgules, majuscules
- **Fusion segments** : Regroupement des segments courts
- **Contexte** : Amélioration de la cohérence

### Options Whisper
| Paramètre | Description | Valeur Recommandée |
|-----------|-------------|-------------------|
| **Temperature** | Créativité (0.0 = déterministe) | 0.0 |
| **Condition on Previous** | Utilise le contexte précédent | True |
| **Compression Ratio** | Seuil de compression | 2.4 |
| **Logprob Threshold** | Seuil de confiance | -1.0 |
| **No Speech Threshold** | Détection de parole | 0.6 |

### Modèles Whisper
| Modèle | Taille | Vitesse | Précision | Usage |
|--------|--------|---------|-----------|-------|
| **Tiny** | 39M | ⚡⚡⚡ | ⭐⭐ | Tests rapides |
| **Base** | 74M | ⚡⚡ | ⭐⭐⭐ | Usage général |
| **Small** | 244M | ⚡ | ⭐⭐⭐⭐ | Recommandé |
| **Medium** | 769M | 🐌 | ⭐⭐⭐⭐⭐ | Professionnel |
| **Large** | 1550M | 🐌🐌 | ⭐⭐⭐⭐⭐ | Maximum qualité |

---

## 📝 Exemples d'Utilisation

### Exemple 1 : Vidéo YouTube
```bash
# Transcription simple pour YouTube
python transcribe_video.py video_youtube.mp4 srt

# Résultat : video_youtube.srt
```

### Exemple 2 : Diffusion TV
```bash
# Format professionnel pour diffusion
python transcribe_video.py emission_tv.mp4 txt

# Résultat : emission_tv.txt (format LTC)
```

### Exemple 3 : Projet multilingue
```bash
# Transcription en français
python main.py video.mp4 --language French --output srt,txt

# Traduction en anglais
python main.py video.mp4 --language French --task translate --output srt
```

### Exemple 4 : Traitement par lot
```bash
# Script pour traiter plusieurs vidéos
for video in *.mp4; do
    python transcribe_video.py "$video" srt,txt
done
```

---

## 🔍 Dépannage

### Problèmes Courants

#### ❌ "FFmpeg non trouvé"
```bash
# Windows (WinGet)
winget install Gyan.FFmpeg

# Ou téléchargement manuel
# https://ffmpeg.org/download.html
```

#### ❌ "Erreur PyTorch"
```bash
# Réinstaller PyTorch
pip uninstall torch torchaudio
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

#### ❌ "Modèle non trouvé"
```bash
# Le modèle sera téléchargé automatiquement
# Vérifiez votre connexion internet
```

#### ❌ "Mémoire insuffisante"
```bash
# Utiliser un modèle plus petit
python transcribe_video.py video.mp4 srt tiny

# Ou fermer d'autres applications
```

### Logs et Debug
```bash
# Activer les logs détaillés
python main.py video.mp4 --log-level DEBUG

# Vérifier les logs
tail -f jj_caption.log
```

---

## 🎯 Conseils d'Optimisation

### Performance
- **Modèle Tiny** : Pour les tests rapides
- **Modèle Medium** : Pour la production
- **Modèle Large** : Pour la qualité maximale

### Qualité
- **Post-traitement** : Toujours activé pour le français
- **Context** : Améliore la cohérence
- **Température 0.0** : Résultats déterministes

### Formats
- **SRT** : Compatibilité maximale
- **TXT** : Diffusion professionnelle
- **VTT** : Web moderne
- **JSON** : Traitement automatique

---

## 📞 Support

### Fichiers de Log
- `jj_caption.log` : Logs détaillés
- `pytest.ini` : Configuration des tests

### Tests
```bash
# Lancer tous les tests
python -m pytest tests/

# Test spécifique
python -m pytest tests/test_whisper_handler.py
```

### Documentation
- `Documentation/SPECIFICATIONS.md` : Spécifications techniques
- `Documentation/TESTING.md` : Guide de test
- `Documentation/TODO.md` : Roadmap

---

## 🎉 Félicitations !

Vous maîtrisez maintenant JJ Caption ! 

**Prochaines étapes :**
1. Testez avec vos propres vidéos
2. Explorez les options avancées
3. Intégrez dans vos workflows
4. Partagez vos retours d'expérience

**Bonne transcription ! 🎬✨** 