# Spécifications - Application de Génération de Sous-titres

## 🎯 Objectif Principal
Créer une application qui prend une vidéo H.264 en entrée et produit des sous-titres synchronisés dans la même langue, dans plusieurs formats.

## 📋 Formats de Sortie Requis

### Formats Principaux (Obligatoires)
- **.srt** (SubRip) - Format standard largement supporté
- **.vtt** (WebVTT) - Format web moderne
- **.scc** (Scenarist Closed Captions) - Format broadcast pour malentendants

### Formats Optionnels
- **.ass** (Advanced SubStation Alpha) - Format avancé avec styles
- **.txt** - Format texte simple
- **.json** - Format structuré pour traitement ultérieur

## ⚙️ Architecture Technique

### 1. Transcription Automatique
**Outil principal : Whisper**
- Précis et fonctionne hors ligne
- Gère les accents et le bruit de fond
- Fournit directement les timecodes
- Supporte extraction directe depuis .mp4, .mkv, .mov, etc.

**Commande CLI de base :**
```bash
whisper episode.mp4 --language French --model medium --output_format srt
```

**Options avancées :**
```bash
--task translate  # Pour sous-titres en anglais par exemple
```

### 2. Conversion en Formats Divers

#### Formats Natifs Whisper
- ✅ **.srt** - Produit directement par Whisper
- ✅ **.vtt** - Produit directement par Whisper

#### Formats Requérant Conversion
- **.ass** - Convertissable avec Subtitle Edit ou ffsubsync
- **.scc** - Format complexe basé sur échantillonnage NTSC (29.97 fps), codé en CEA-608

### 3. Outils pour Conversion .scc

#### Option 1 : Subtitle Edit (Windows)
- Ouvre le .srt
- "Save as" → .scc
- Gère positions, couleurs, etc.

#### Option 2 : ccextractor
```bash
ccextractor input.srt -out=scc -o output.scc
```

#### Option 3 : Python avec pycaption
```python
from pycaption import SRTReader, SCCWriter
srt = open("transcript.srt").read()
scc = SCCWriter().write(SRTReader().read(srt))
with open("output.scc", "w") as f:
    f.write(scc)
```

## 🖥️ Architecture de l'Application

### Interface Utilisateur Suggérée
- **Drag & drop** de la vidéo
- **Options configurables :**
  - Langue
  - Format de sortie (.srt, .vtt, .scc, etc.)
  - Correction auto / post-édition
- **Barre de progression** + export final

### Stack Technique Recommandée

| Composant | Outil Recommandé |
|-----------|------------------|
| Transcription | Whisper (Python) |
| Extraction audio | ffmpeg |
| Conversion formats | pycaption, ccextractor, Subtitle Edit |
| GUI (optionnel) | Streamlit (Web), Tkinter (Desktop) |

## 🎁 Fonctionnalités Bonus (Intégration Future)

### Correction Automatique
- **Orthographique** : LanguageTool, Grammalecte
- **Marquage automatique** : [rire], [musique], [applaudissements]

### Prévisualisation
- Prévisualisation dans une vidéo
- Édition en temps réel

## 📁 Structure de Projet Proposée

```
JJ Caption/
├── Documentation/
│   ├── SPECIFICATIONS.md
│   └── TODO.md
├── src/
│   ├── transcription/
│   ├── conversion/
│   ├── gui/
│   └── utils/
├── tests/
├── requirements.txt
├── README.md
└── main.py
```

## 🔧 Dépendances Techniques

### Python
- `openai-whisper` - Transcription
- `pycaption` - Conversion de formats
- `ffmpeg-python` - Traitement vidéo
- `streamlit` ou `tkinter` - Interface utilisateur

### Système
- `ffmpeg` - Extraction audio
- `ccextractor` - Conversion .scc (optionnel)
- `Subtitle Edit` - Conversion avancée (optionnel)

## ❓ Questions pour Affiner les Besoins

1. **Interface utilisateur** : Préférez-vous une interface web (Streamlit) ou desktop (Tkinter) ?
2. **Langues supportées** : Quelles langues doivent être supportées en priorité ?
3. **Qualité de transcription** : Quel modèle Whisper préférez-vous (tiny, base, small, medium, large) ?
4. **Traitement par lot** : L'application doit-elle gérer plusieurs fichiers simultanément ?
5. **Correction manuelle** : Souhaitez-vous une interface d'édition des sous-titres générés ?
6. **Performance** : Préférez-vous la vitesse (modèles plus petits) ou la précision (modèles plus grands) ? 