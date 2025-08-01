#!/usr/bin/env python3
"""
Interface web Streamlit pour JJ Caption.
"""

import streamlit as st
import os
import tempfile
from pathlib import Path
import sys

# Configuration de la page
st.set_page_config(
    page_title="JJ Caption - Transcription Audio/Vidéo",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre principal
st.title("🎤 JJ Caption")
st.markdown("### Transcription Audio/Vidéo Professionnelle")

# Sidebar avec options
with st.sidebar:
    st.header("⚙️ Options")
    
    # Options de base
    st.subheader("Configuration de base")
    model_size = st.selectbox(
        "Modèle Whisper",
        ["tiny", "base", "small", "medium"],
        index=2,
        help="Plus le modèle est grand, meilleure est la qualité mais plus lent"
    )
    
    language = st.selectbox(
        "Langue",
        ["Auto-détection", "Français", "Anglais", "Espagnol"],
        help="Langue du contenu audio/vidéo"
    )
    
    # Options avancées
    with st.expander("🔧 Options avancées"):
        enable_post_processing = st.checkbox(
            "Post-traitement avancé",
            value=True,
            help="Correction automatique des erreurs de transcription"
        )
        
        condition_on_previous_text = st.checkbox(
            "Utiliser le contexte précédent",
            value=True,
            help="Améliore la cohérence en utilisant les segments précédents"
        )
        
        temperature = st.slider(
            "Température",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.1,
            help="Contrôle la créativité (0.0 = déterministe)"
        )
        
        compression_ratio_threshold = st.slider(
            "Seuil de compression",
            min_value=1.0,
            max_value=5.0,
            value=2.4,
            step=0.1,
            help="Seuil pour détecter les segments compressés"
        )
        
        logprob_threshold = st.slider(
            "Seuil de probabilité",
            min_value=-2.0,
            max_value=0.0,
            value=-1.0,
            step=0.1,
            help="Seuil de confiance pour les mots"
        )
        
        no_speech_threshold = st.slider(
            "Seuil de détection de parole",
            min_value=0.0,
            max_value=1.0,
            value=0.6,
            step=0.1,
            help="Seuil pour détecter les segments sans parole"
        )

# Zone principale
st.markdown("---")

# Zone de téléchargement
st.subheader("📁 Télécharger un fichier audio/vidéo")
uploaded_file = st.file_uploader(
    "Choisissez un fichier audio ou vidéo",
    type=['mp3', 'wav', 'mp4', 'avi', 'mov', 'mkv', 'flv'],
    help="Formats supportés : MP3, WAV, MP4, AVI, MOV, MKV, FLV"
)

# Options de sortie
st.subheader("📤 Formats de sortie")
col1, col2, col3 = st.columns(3)

with col1:
    srt_enabled = st.checkbox("SRT", value=True)
    vtt_enabled = st.checkbox("VTT", value=True)

with col2:
    txt_enabled = st.checkbox("TXT (Diffusion)", value=True)
    json_enabled = st.checkbox("JSON", value=False)

with col3:
    ass_enabled = st.checkbox("ASS", value=False)
    scc_enabled = st.checkbox("SCC", value=False)

# Bouton de transcription
if uploaded_file is not None:
    st.markdown("---")
    
    # Afficher les informations du fichier
    file_details = {
        "Nom": uploaded_file.name,
        "Type": uploaded_file.type,
        "Taille": f"{uploaded_file.size / (1024*1024):.2f} MB"
    }
    
    st.subheader("📋 Informations du fichier")
    for key, value in file_details.items():
        st.write(f"**{key}:** {value}")
    
    # Bouton de transcription
    if st.button("🎤 Commencer la transcription", type="primary"):
        try:
            # Créer un fichier temporaire
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            # Afficher le statut
            with st.spinner("🔄 Transcription en cours..."):
                st.info("⚠️ **Mode démonstration** : L'application est en cours de configuration pour Streamlit Cloud.")
                st.info("La transcription complète sera disponible une fois le déploiement finalisé.")
                
                # Simulation de progression
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(101):
                    progress_bar.progress(i)
                    if i < 30:
                        status_text.text("📥 Téléchargement du modèle Whisper...")
                    elif i < 60:
                        status_text.text("🎵 Analyse du fichier audio...")
                    elif i < 90:
                        status_text.text("📝 Transcription en cours...")
                    else:
                        status_text.text("✅ Finalisation...")
                
                st.success("🎉 Transcription terminée ! (Mode démonstration)")
                
                # Afficher un exemple de résultat
                st.subheader("📄 Exemple de résultat (Mode démonstration)")
                
                # Exemple SRT
                if srt_enabled:
                    with st.expander("📄 Fichier SRT (exemple)"):
                        st.code("""1
00:00:00,000 --> 00:00:03,500
Bonjour et bienvenue dans cette démonstration

2
00:00:03,500 --> 00:00:07,200
de JJ Caption, votre outil de transcription

3
00:00:07,200 --> 00:00:10,800
audio et vidéo professionnel.
""")
                
                # Exemple TXT
                if txt_enabled:
                    with st.expander("📄 Fichier TXT pour diffusion (exemple)"):
                        st.code("""'**************************************************

\\ Title: demonstration.txt

\\ Version: 1.0
\\ Channel: F1C1
\\ Rate: 30d
\\ Type: LTC

\\ Generated By: JJ Caption
\\ CaptionFile: demonstration.txt
\\ MediaFile: uploaded_file.mp4

\\ Author: JJ Caption
\\ Owner: 

\\ Date: August 1, 2025
\\ Time: 8:30:00 PM

'**************************************************


\\ TC:  10:00:00;00 ¶÷142C
\\ TC:  10:00:00;00 ¶÷1426÷142D÷1470Bonjour et bienvenue§00
\\ TC:  10:00:03;15 ¶÷1426÷142D÷1470dans cette démonstration§00
""")
                
        except Exception as e:
            st.error(f"❌ Erreur lors de la transcription : {str(e)}")
            st.info("💡 **Conseil** : Vérifiez que le fichier n'est pas corrompu et réessayez.")

else:
    # Instructions
    st.info("💡 **Instructions :**")
    st.markdown("""
    1. **Téléchargez** un fichier audio ou vidéo dans la zone ci-dessus
    2. **Configurez** les options dans la sidebar
    3. **Sélectionnez** les formats de sortie souhaités
    4. **Cliquez** sur "Commencer la transcription"
    
    **Formats supportés :** MP3, WAV, MP4, AVI, MOV, MKV, FLV
    **Taille maximale :** 200 MB
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🎤 JJ Caption - Transcription Audio/Vidéo Professionnelle</p>
    <p>Version 1.0 | Développé avec ❤️</p>
</div>
""", unsafe_allow_html=True) 