"""
Interface web Streamlit pour JJ Caption.
"""

import streamlit as st
import os
import tempfile
from pathlib import Path
from typing import List, Dict, Any
import sys

# Ajouter le répertoire src au path
current_dir = Path(__file__).parent
src_dir = current_dir.parent
sys.path.insert(0, str(src_dir))

from transcription.whisper_handler import WhisperHandler
from conversion.format_converter import FormatConverter


def create_streamlit_app():
    """Crée l'application Streamlit."""
    
    # Configuration de la page
    st.set_page_config(
        page_title="JJ Caption - Générateur de Sous-titres",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Titre principal
    st.title("🎬 JJ Caption - Générateur de Sous-titres Automatique")
    st.markdown("---")
    
    # Sidebar pour les paramètres
    with st.sidebar:
        st.header("⚙️ Paramètres")
        
        # Modèle Whisper
        model_options = ["tiny", "base", "small", "medium", "large"]
        selected_model = st.selectbox(
            "Modèle Whisper",
            model_options,
            index=4,  # large par défaut pour usage professionnel
            help="Plus le modèle est grand, plus la transcription est précise mais lente"
        )
        
        # Langue
        language_options = [
            "French", "English", "Spanish", "German", "Italian", 
            "Portuguese", "Dutch", "Russian", "Chinese", "Japanese",
            "Korean", "Arabic", "Hindi", "Turkish", "Polish"
        ]
        selected_language = st.selectbox(
            "Langue du contenu",
            language_options,
            index=0,  # French par défaut
            help="Langue principale du contenu audio/vidéo"
        )
        
        # Type de tâche
        task_options = ["transcribe", "translate"]
        selected_task = st.selectbox(
            "Type de tâche",
            task_options,
            index=0,
            help="transcribe: garde la langue originale, translate: traduit en anglais"
        )
        
        # Formats de sortie
        format_options = ["srt", "vtt", "scc", "ass", "txt", "json"]
        selected_formats = st.multiselect(
            "Formats de sortie",
            format_options,
            default=["srt"],
            help="Sélectionnez un ou plusieurs formats"
        )
        
        st.markdown("---")
        
        # Options avancées
        st.subheader("🔧 Options Avancées")
        
        # Post-traitement
        enable_post_processing = st.checkbox(
            "Post-traitement avancé",
            value=True,
            help="Améliore la qualité avec correction d'erreurs et ponctuation"
        )
        
        # Options Whisper avancées
        with st.expander("⚙️ Options Whisper avancées"):
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
                help="0.0 = déterministe, 1.0 = créatif"
            )
            
            compression_ratio_threshold = st.slider(
                "Seuil de compression",
                min_value=0.0,
                max_value=10.0,
                value=2.4,
                step=0.1,
                help="Contrôle la compression du texte"
            )
            
            logprob_threshold = st.slider(
                "Seuil de probabilité",
                min_value=-5.0,
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
        
        st.markdown("---")
        
        # Informations sur les modèles
        st.subheader("📊 Informations Modèles")
        model_info = {
            "tiny": "39M - Très rapide, précision limitée",
            "base": "74M - Rapide, bonne précision",
            "small": "244M - Équilibré",
            "medium": "769M - Recommandé",
            "large": "1550M - Très précis, lent"
        }
        st.info(f"**{selected_model.title()}**: {model_info[selected_model]}")
        
        # Informations sur le format TXT professionnel
        if "txt" in selected_formats:
            st.info("📺 **Format TXT**: Génère un fichier de diffusion professionnel avec timecodes LTC")
    
    # Zone principale
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📁 Upload de fichier")
        
        # Upload de fichier
        uploaded_file = st.file_uploader(
            "Choisissez un fichier vidéo ou audio",
            type=['mp4', 'mkv', 'mov', 'avi', 'wmv', 'mp3', 'wav', 'm4a', 'flac'],
            help="Formats supportés: MP4, MKV, MOV, AVI, WMV, MP3, WAV, M4A, FLAC"
        )
        
        if uploaded_file is not None:
            # Afficher les informations du fichier
            file_size = uploaded_file.size / (1024 * 1024)  # MB
            st.info(f"📄 **Fichier**: {uploaded_file.name}")
            st.info(f"📏 **Taille**: {file_size:.2f} MB")
            st.info(f"🎯 **Type**: {uploaded_file.type}")
            
            # Bouton de traitement
            if st.button("🚀 Lancer la transcription", type="primary"):
                # Récupérer les options avancées
                advanced_options = {
                    "enable_post_processing": enable_post_processing,
                    "condition_on_previous_text": condition_on_previous_text,
                    "temperature": temperature,
                    "compression_ratio_threshold": compression_ratio_threshold,
                    "logprob_threshold": logprob_threshold,
                    "no_speech_threshold": no_speech_threshold
                }
                process_file(uploaded_file, selected_model, selected_language, selected_task, selected_formats, advanced_options)
    
    with col2:
        st.header("📋 Formats supportés")
        
        format_descriptions = {
            "srt": "SubRip - Format standard",
            "vtt": "WebVTT - Format web moderne",
            "scc": "Scenarist - Format broadcast",
            "ass": "Advanced SubStation - Format avancé",
            "txt": "Texte simple",
            "json": "Format structuré"
        }
        
        for fmt, desc in format_descriptions.items():
            st.markdown(f"**{fmt.upper()}**: {desc}")
        
        st.markdown("---")
        
        st.header("ℹ️ Aide")
        st.markdown("""
        1. **Upload** votre fichier vidéo/audio
        2. **Configurez** les paramètres dans la sidebar
        3. **Cliquez** sur "Lancer la transcription"
        4. **Téléchargez** les fichiers générés
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**JJ Caption** - Générateur de sous-titres automatique avec Whisper | "
        "Développé avec ❤️ en Python"
    )


def process_file(uploaded_file, model: str, language: str, task: str, formats: List[str], advanced_options: Dict[str, Any]):
    """Traite le fichier uploadé avec options avancées."""
    
    # Créer un fichier temporaire
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name
    
    try:
        # Barre de progression
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Initialisation
        status_text.text("🔄 Initialisation du modèle Whisper...")
        progress_bar.progress(10)
        
        whisper_handler = WhisperHandler(model_name=model)
        converter = FormatConverter()
        
        # Transcription avec options avancées
        status_text.text("🎬 Transcription en cours...")
        progress_bar.progress(30)
        
        if advanced_options["enable_post_processing"]:
            # Utiliser les options avancées
            result = whisper_handler.transcribe_with_options(
                input_path=tmp_path,
                language=language,
                task=task,
                condition_on_previous_text=advanced_options["condition_on_previous_text"],
                temperature=advanced_options["temperature"],
                compression_ratio_threshold=advanced_options["compression_ratio_threshold"],
                logprob_threshold=advanced_options["logprob_threshold"],
                no_speech_threshold=advanced_options["no_speech_threshold"]
            )
            
            # Post-traitement
            status_text.text("🔧 Application du post-traitement...")
            progress_bar.progress(50)
            result = whisper_handler.post_process_transcription(result)
        else:
            # Transcription standard
            result = whisper_handler.transcribe(
                input_path=tmp_path,
                language=language,
                task=task
            )
        
        progress_bar.progress(70)
        
        # Génération des fichiers
        status_text.text("💾 Génération des fichiers...")
        
        generated_files = []
        
        for i, output_format in enumerate(formats):
            # Créer un fichier temporaire pour la sortie
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{output_format}") as output_tmp:
                output_path = output_tmp.name
            
            try:
                if output_format == "srt":
                    whisper_handler.save_srt(result, output_path)
                elif output_format == "vtt":
                    whisper_handler.save_vtt(result, output_path)
                elif output_format == "txt":
                    whisper_handler.save_txt(result, output_path, tmp_path)
                elif output_format == "json":
                    whisper_handler.save_json(result, output_path)
                elif output_format in ["scc", "ass"]:
                    # Sauvegarder d'abord en SRT temporaire
                    temp_srt = output_path.replace(f".{output_format}", ".srt")
                    whisper_handler.save_srt(result, temp_srt)
                    
                    # Convertir vers le format cible
                    if output_format == "scc":
                        converter.srt_to_scc(temp_srt, output_path)
                    elif output_format == "ass":
                        converter.srt_to_ass(temp_srt, output_path)
                    
                    # Supprimer le fichier temporaire
                    os.unlink(temp_srt)
                
                generated_files.append((output_path, output_format))
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la génération du format {output_format}: {e}")
        
        progress_bar.progress(100)
        status_text.text("✅ Traitement terminé!")
        
        # Afficher les fichiers générés
        st.success("🎉 Transcription terminée avec succès!")
        
        st.subheader("📁 Fichiers générés")
        
        for file_path, file_format in generated_files:
            if os.path.exists(file_path):
                # Lire le contenu du fichier
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                # Nom du fichier original sans extension
                original_name = Path(uploaded_file.name).stem
                
                # Créer le bouton de téléchargement
                st.download_button(
                    label=f"📥 Télécharger {original_name}.{file_format}",
                    data=file_content,
                    file_name=f"{original_name}.{file_format}",
                    mime="text/plain"
                )
                
                # Afficher un aperçu pour les formats texte
                if file_format in ["srt", "vtt", "txt"]:
                    with st.expander(f"Aperçu {file_format.upper()}"):
                        st.code(file_content[:1000] + "..." if len(file_content) > 1000 else file_content)
        
        # Nettoyer les fichiers temporaires
        for file_path, _ in generated_files:
            try:
                os.unlink(file_path)
            except:
                pass
    
    except Exception as e:
        st.error(f"❌ Erreur lors du traitement: {e}")
        st.error("Vérifiez que le fichier est valide et que tous les paramètres sont corrects.")
    
    finally:
        # Nettoyer le fichier temporaire d'entrée
        try:
            os.unlink(tmp_path)
        except:
            pass


if __name__ == "__main__":
    create_streamlit_app() 