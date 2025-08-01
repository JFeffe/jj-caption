#!/usr/bin/env python3
"""
Script de démonstration des fonctionnalités de JJ Caption.
"""

import os
import sys
import logging
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from transcription.whisper_handler import WhisperHandler
from conversion.format_converter import FormatConverter


def setup_logging():
    """Configure le logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('demo_features.log', encoding='utf-8')
        ]
    )


def demo_transcription():
    """Démonstration de la transcription."""
    logger = logging.getLogger(__name__)
    
    video_path = "Test_Vid/smpts-3_ep11_20250702_pk01_hd_29i.mp4"
    
    if not os.path.exists(video_path):
        logger.error(f"Fichier vidéo non trouvé: {video_path}")
        return None
    
    logger.info("🎬 Démonstration de la transcription Whisper")
    logger.info("=" * 50)
    
    try:
        # Initialiser Whisper
        whisper_handler = WhisperHandler(model_name="tiny")
        
        # Transcrire le fichier
        logger.info("Transcription en cours...")
        result = whisper_handler.transcribe(
            input_path=video_path,
            language="French",
            task="transcribe"
        )
        
        logger.info(f"✅ Transcription réussie: {len(result.get('segments', []))} segments")
        return result, video_path
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la transcription: {e}")
        return None


def demo_formats(result, video_path):
    """Démonstration de tous les formats de sortie."""
    logger = logging.getLogger(__name__)
    
    logger.info("\n📝 Démonstration des formats de sortie")
    logger.info("=" * 50)
    
    try:
        whisper_handler = WhisperHandler()
        converter = FormatConverter()
        
        base_name = video_path.replace('.mp4', '')
        
        # 1. Format SRT (SubRip)
        logger.info("1. Génération du format SRT...")
        srt_path = f"{base_name}_demo.srt"
        whisper_handler.save_srt(result, srt_path)
        logger.info(f"   ✅ SRT généré: {srt_path}")
        
        # 2. Format VTT (WebVTT)
        logger.info("2. Génération du format VTT...")
        vtt_path = f"{base_name}_demo.vtt"
        whisper_handler.save_vtt(result, vtt_path)
        logger.info(f"   ✅ VTT généré: {vtt_path}")
        
        # 3. Format TXT pour diffusion (avec timecodes LTC)
        logger.info("3. Génération du format TXT pour diffusion...")
        txt_path = f"{base_name}_demo.txt"
        whisper_handler.save_txt(result, txt_path, video_path)
        logger.info(f"   ✅ TXT pour diffusion généré: {txt_path}")
        
        # 4. Format JSON
        logger.info("4. Génération du format JSON...")
        json_path = f"{base_name}_demo.json"
        whisper_handler.save_json(result, json_path)
        logger.info(f"   ✅ JSON généré: {json_path}")
        
        # 5. Format ASS (Advanced SubStation Alpha)
        logger.info("5. Conversion vers le format ASS...")
        ass_path = f"{base_name}_demo.ass"
        converter.srt_to_ass(srt_path, ass_path)
        logger.info(f"   ✅ ASS généré: {ass_path}")
        
        # 6. Format SCC (Scenarist Closed Captions)
        logger.info("6. Conversion vers le format SCC...")
        scc_path = f"{base_name}_demo.scc"
        converter.srt_to_scc(srt_path, scc_path)
        logger.info(f"   ✅ SCC généré: {scc_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la génération des formats: {e}")
        return False


def demo_timecodes(video_path):
    """Démonstration de la récupération des timecodes LTC."""
    logger = logging.getLogger(__name__)
    
    logger.info("\n⏰ Démonstration des timecodes LTC")
    logger.info("=" * 50)
    
    try:
        whisper_handler = WhisperHandler()
        
        # Récupérer le timecode LTC
        ltc_timecode = whisper_handler._get_ltc_timecode(video_path)
        
        if ltc_timecode:
            logger.info(f"✅ Timecode LTC trouvé: {ltc_timecode}")
            logger.info("   Ce timecode est automatiquement utilisé dans le format TXT pour diffusion")
        else:
            logger.warning("⚠️ Aucun timecode LTC trouvé dans le fichier vidéo")
            logger.info("   Le format TXT utilisera des timecodes calculés")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des timecodes: {e}")
        return False


def show_file_info():
    """Affiche les informations sur les fichiers générés."""
    logger = logging.getLogger(__name__)
    
    logger.info("\n📁 Informations sur les fichiers générés")
    logger.info("=" * 50)
    
    demo_files = [
        "Test_Vid/smpts-3_ep11_20250702_pk01_hd_29i_demo.srt",
        "Test_Vid/smpts-3_ep11_20250702_pk01_hd_29i_demo.vtt",
        "Test_Vid/smpts-3_ep11_20250702_pk01_hd_29i_demo.txt",
        "Test_Vid/smpts-3_ep11_20250702_pk01_hd_29i_demo.json",
        "Test_Vid/smpts-3_ep11_20250702_pk01_hd_29i_demo.ass",
        "Test_Vid/smpts-3_ep11_20250702_pk01_hd_29i_demo.scc"
    ]
    
    for file_path in demo_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            size_kb = size / 1024
            logger.info(f"✅ {os.path.basename(file_path)}: {size_kb:.1f} KB")
        else:
            logger.warning(f"❌ {os.path.basename(file_path)}: Non trouvé")


def main():
    """Fonction principale de démonstration."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("🚀 Démonstration des fonctionnalités JJ Caption")
    logger.info("=" * 60)
    
    # 1. Démonstration de la transcription
    result_data = demo_transcription()
    if not result_data:
        logger.error("❌ Impossible de continuer sans transcription")
        return
    
    result, video_path = result_data
    
    # 2. Démonstration des timecodes LTC
    demo_timecodes(video_path)
    
    # 3. Démonstration de tous les formats
    if demo_formats(result, video_path):
        # 4. Afficher les informations sur les fichiers
        show_file_info()
        
        logger.info("\n🎉 Démonstration terminée avec succès!")
        logger.info("📋 Tous les formats de sous-titres ont été générés")
        logger.info("⏰ Les timecodes LTC ont été récupérés et utilisés")
        logger.info("🔧 Le système est prêt pour la production!")
    else:
        logger.error("❌ Erreur lors de la démonstration des formats")


if __name__ == "__main__":
    main() 