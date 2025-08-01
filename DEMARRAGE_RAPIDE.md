# 🚀 JJ Caption - Démarrage Rapide

## ⚡ Utilisation Immédiate

### 1. **Interface Web (Recommandée)**
```bash
python run_web_app.py
```
- Ouvrez http://localhost:8501
- Glissez-déposez votre vidéo
- Configurez les options dans la sidebar
- Cliquez "Lancer la transcription"
- Téléchargez les fichiers générés

### 2. **Script Simple (Rapide)**
```bash
# Transcription basique
python transcribe_video.py votre_video.mp4

# Formats multiples
python transcribe_video.py votre_video.mp4 srt,txt,vtt

# Modèle spécifique
python transcribe_video.py votre_video.mp4 srt,txt medium
```

### 3. **Interface CLI (Avancée)**
```bash
# Aide
python main.py --help

# Transcription avec options
python main.py votre_video.mp4 --language French --output srt,txt,vtt
```

---

## 🎯 Exemples Concrets

### **Vidéo YouTube**
```bash
python transcribe_video.py video_youtube.mp4 srt
# → Génère video_youtube.srt
```

### **Diffusion TV**
```bash
python transcribe_video.py emission_tv.mp4 txt
# → Génère emission_tv.txt (format professionnel LTC)
```

### **Usage Professionnel**
```bash
python transcribe_video.py video_pro.mp4 srt,txt,vtt medium
# → Génère 3 fichiers avec modèle medium
```

---

## 📁 Formats Disponibles

| Format | Usage | Commande |
|--------|-------|----------|
| **SRT** | YouTube, lecteurs vidéo | `srt` |
| **TXT** | Diffusion TV, broadcast | `txt` |
| **VTT** | Web, streaming | `vtt` |
| **SCC** | Broadcast professionnel | `scc` |
| **ASS** | Édition avancée | `ass` |
| **JSON** | Traitement automatique | `json` |

---

## ⚙️ Options Avancées

### **Modèles Whisper**
- **Tiny** : Rapide, tests (39M)
- **Base** : Équilibré (74M)
- **Small** : Recommandé (244M)
- **Medium** : Professionnel (769M) ⭐
- **Large** : Maximum qualité (1550M)

### **Post-traitement**
- ✅ Correction automatique d'erreurs françaises
- ✅ Amélioration de la ponctuation
- ✅ Fusion des segments courts
- ✅ Amélioration du contexte

### **Format TXT Professionnel**
- ⏰ Timecodes LTC : `10:00:00;00`
- 📺 Codes de contrôle : `¶÷142C`
- 🎯 Segmentation intelligente
- 📋 En-tête complet

---

## 🔧 Dépannage Rapide

### **Erreur "FFmpeg non trouvé"**
```bash
winget install Gyan.FFmpeg
```

### **Erreur "Module transcription"**
```bash
python test_quick.py
```

### **Mémoire insuffisante**
```bash
python transcribe_video.py video.mp4 srt tiny
```

---

## 📊 Performance

| Durée Vidéo | Modèle | Temps Estimé |
|-------------|--------|--------------|
| 1 minute | Tiny | 30 secondes |
| 10 minutes | Medium | 5 minutes |
| 1 heure | Large | 30 minutes |

---

## 🎉 C'est Parti !

**Votre première transcription :**
```bash
# Test rapide
python transcribe_video.py Test_Vid/smpts-3_ep11_20250702_pk01_hd_29i.mp4 srt,txt
```

**Interface web :**
```bash
python run_web_app.py
# → http://localhost:8501
```

**Bonne transcription ! 🎬✨** 