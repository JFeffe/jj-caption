# JJ Caption - Générateur de Sous-titres Automatique

Une application Python pour générer automatiquement des sous-titres synchronisés à partir de vidéos H.264 dans plusieurs formats.

## 🎯 Fonctionnalités

- **Transcription automatique** avec Whisper (OpenAI)
- **Formats de sortie multiples** : .srt, .vtt, .scc, .ass, .txt, .json
- **Interface utilisateur intuitive** (Streamlit ou Tkinter)
- **Support multi-langues**
- **Traitement hors ligne**

## 📋 Prérequis Système

### Windows
1. **Python 3.8+** : [Télécharger Python](https://www.python.org/downloads/)
2. **FFmpeg** : [Télécharger FFmpeg](https://ffmpeg.org/download.html)
   - Ajouter FFmpeg au PATH système
3. **Git** (optionnel) : [Télécharger Git](https://git-scm.com/)

### macOS
```bash
# Avec Homebrew
brew install python ffmpeg

# Ou avec MacPorts
sudo port install python3 ffmpeg
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip ffmpeg
```

## 🚀 Installation

### 1. Cloner le projet
```bash
git clone <repository-url>
cd JJ-Caption
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Tester l'installation
```bash
python -c "import whisper; print('Whisper installé avec succès!')"
```

## 🎮 Utilisation

### Interface Web (Streamlit)
```bash
streamlit run src/gui/streamlit_app.py
```

### Interface Desktop (Tkinter)
```bash
python src/gui/tkinter_app.py
```

### Ligne de commande
```bash
python main.py --input video.mp4 --output subtitles.srt --language French
```

## 📁 Structure du Projet

```
JJ Caption/
├── Documentation/          # Documentation du projet
│   ├── SPECIFICATIONS.md  # Spécifications détaillées
│   └── TODO.md           # Plan d'implémentation
├── src/                   # Code source
│   ├── transcription/     # Module de transcription
│   ├── conversion/        # Module de conversion de formats
│   ├── gui/              # Interfaces utilisateur
│   └── utils/            # Utilitaires
├── tests/                # Tests unitaires
├── requirements.txt       # Dépendances Python
├── README.md            # Ce fichier
└── main.py              # Point d'entrée principal
```

## 🔧 Configuration

### Variables d'environnement
Créer un fichier `.env` :
```env
# Modèle Whisper par défaut (tiny, base, small, medium, large)
WHISPER_MODEL=medium

# Langue par défaut
DEFAULT_LANGUAGE=French

# Dossier de sortie par défaut
OUTPUT_DIR=./output

# Logging
LOG_LEVEL=INFO
```

## 📊 Formats Supportés

### Formats d'entrée
- **Vidéo** : .mp4, .mkv, .mov, .avi, .wmv
- **Audio** : .mp3, .wav, .m4a, .flac

### Formats de sortie
- **.srt** (SubRip) - Format standard
- **.vtt** (WebVTT) - Format web moderne
- **.scc** (Scenarist) - Format broadcast
- **.ass** (Advanced SubStation) - Format avancé
- **.txt** - Format texte simple
- **.json** - Format structuré

## 🎯 Exemples d'utilisation

### Transcription simple
```python
from src.transcription.whisper_handler import WhisperHandler

handler = WhisperHandler()
subtitles = handler.transcribe("video.mp4", language="French")
handler.save_srt(subtitles, "output.srt")
```

### Conversion de formats
```python
from src.conversion.format_converter import FormatConverter

converter = FormatConverter()
converter.srt_to_vtt("input.srt", "output.vtt")
converter.srt_to_scc("input.srt", "output.scc")
```

## 🧪 Tests

### Lancer tous les tests
```bash
pytest tests/
```

### Tests avec couverture
```bash
pytest --cov=src tests/
```

## 🐛 Dépannage

### Erreur FFmpeg
```
Error: ffmpeg not found
```
**Solution** : Installer FFmpeg et l'ajouter au PATH

### Erreur Whisper
```
Error: No module named 'whisper'
```
**Solution** : Réinstaller avec `pip install openai-whisper`

### Erreur mémoire
```
Error: CUDA out of memory
```
**Solution** : Utiliser un modèle plus petit (tiny, base, small)

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- [OpenAI Whisper](https://github.com/openai/whisper) - Transcription automatique
- [FFmpeg](https://ffmpeg.org/) - Traitement audio/vidéo
- [pycaption](https://github.com/pbs/pycaption) - Conversion de formats
- [Streamlit](https://streamlit.io/) - Interface web

## 📞 Support

Pour toute question ou problème :
- Ouvrir une issue sur GitHub
- Consulter la documentation dans `Documentation/`
- Vérifier les logs d'erreur 