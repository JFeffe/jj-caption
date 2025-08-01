#!/usr/bin/env python3
"""
Script simple pour transcrire des vidéos avec JJ Caption.
Utilise toutes les améliorations : format professionnel, post-traitement, etc.
"""

import os
import sys
import logging
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from transcription.whisper_handler import WhisperHandler


def setup_logging():
    """Configure le logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def transcribe_video(video_path: str, output_formats: list = None, model: str = "medium"):
    """
    Transcrit une vidéo avec toutes les améliorations.
    
    Args:
        video_path: Chemin vers la vidéo
        output_formats: Formats de sortie (srt, vtt, txt, etc.)
        model: Modèle Whisper à utiliser
    """
    if output_formats is None:
        output_formats = ["srt", "txt"]
    
    logger = logging.getLogger(__name__)
    
    # Vérifier que le fichier existe
    if not os.path.exists(video_path):
        logger.error(f"❌ Fichier non trouvé: {video_path}")
        return
    
    logger.info(f"🎬 Début de la transcription: {video_path}")
    logger.info(f"📊 Modèle: {model}")
    logger.info(f"📁 Formats: {', '.join(output_formats)}")
    
    try:
        # Initialiser le gestionnaire Whisper
        whisper_handler = WhisperHandler(model_name=model)
        
        # Transcription avec options avancées et post-traitement
        logger.info("🔄 Transcription avec options avancées...")
        result = whisper_handler.transcribe_with_options(
            input_path=video_path,
            language="French",
            condition_on_previous_text=True,
            temperature=0.0,
            compression_ratio_threshold=2.4,
            logprob_threshold=-1.0,
            no_speech_threshold=0.6
        )
        
        # Post-traitement
        logger.info("🔧 Application du post-traitement...")
        result = whisper_handler.post_process_transcription(result)
        
        # Générer les fichiers de sortie
        base_name = Path(video_path).stem
        
        for output_format in output_formats:
            output_path = f"{base_name}.{output_format}"
            
            logger.info(f"💾 Génération du fichier {output_format}...")
            
            if output_format == "srt":
                whisper_handler.save_srt(result, output_path)
            elif output_format == "vtt":
                whisper_handler.save_vtt(result, output_path)
            elif output_format == "txt":
                whisper_handler.save_txt(result, output_path, video_path)
            elif output_format == "json":
                whisper_handler.save_json(result, output_path)
            else:
                logger.warning(f"⚠️ Format non supporté: {output_format}")
                continue
            
            logger.info(f"✅ Fichier généré: {output_path}")
        
        logger.info("🎉 Transcription terminée avec succès!")
        
        # Afficher un aperçu
        logger.info("\n📝 Aperçu de la transcription:")
        for i, segment in enumerate(result["segments"][:3]):
            text = segment.get("text", "").strip()
            start = segment.get("start", 0)
            end = segment.get("end", 0)
            logger.info(f"  {i+1}. [{start:.1f}s-{end:.1f}s] {text}")
        
        if len(result["segments"]) > 3:
            logger.info(f"  ... et {len(result['segments']) - 3} autres segments")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la transcription: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Fonction principale."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    if len(sys.argv) < 2:
        print("""
🎬 JJ Caption - Transcription de vidéos

Usage:
  python transcribe_video.py <chemin_video> [formats] [modèle]

Exemples:
  python transcribe_video.py video.mp4
  python transcribe_video.py video.mp4 srt,txt,vtt
  python transcribe_video.py video.mp4 srt,txt medium

Formats supportés: srt, vtt, txt, json
Modèles: tiny, base, small, medium, large
        """)
        return
    
    video_path = sys.argv[1]
    output_formats = sys.argv[2].split(",") if len(sys.argv) > 2 else ["srt", "txt"]
    model = sys.argv[3] if len(sys.argv) > 3 else "medium"
    
    transcribe_video(video_path, output_formats, model)


if __name__ == "__main__":
    main() 