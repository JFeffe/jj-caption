#!/usr/bin/env python3
"""
Point d'entrée principal de l'application JJ Caption.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from transcription.whisper_handler import WhisperHandler
from conversion.format_converter import FormatConverter


def setup_logging(level: str = "INFO") -> None:
    """
    Configure le logging.
    
    Args:
        level: Niveau de logging
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('jj_caption.log', encoding='utf-8')
        ]
    )


def validate_input_file(file_path: str) -> bool:
    """
    Valide le fichier d'entrée.
    
    Args:
        file_path: Chemin du fichier
        
    Returns:
        True si le fichier est valide
    """
    path = Path(file_path)
    
    if not path.exists():
        print(f"❌ Erreur: Le fichier {file_path} n'existe pas")
        return False
    
    if not path.is_file():
        print(f"❌ Erreur: {file_path} n'est pas un fichier")
        return False
    
    # Vérifier l'extension
    supported_extensions = {'.mp4', '.mkv', '.mov', '.avi', '.wmv', '.mp3', '.wav', '.m4a', '.flac'}
    if path.suffix.lower() not in supported_extensions:
        print(f"❌ Erreur: Format de fichier non supporté: {path.suffix}")
        print(f"Formats supportés: {', '.join(supported_extensions)}")
        return False
    
    return True


def get_output_path(input_path: str, output_format: str, output_dir: Optional[str] = None) -> str:
    """
    Génère le chemin de sortie.
    
    Args:
        input_path: Chemin du fichier d'entrée
        output_format: Format de sortie
        output_dir: Répertoire de sortie (optionnel)
        
    Returns:
        Chemin de sortie
    """
    input_path = Path(input_path)
    
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        return str(output_dir / f"{input_path.stem}.{output_format}")
    else:
        return str(input_path.parent / f"{input_path.stem}.{output_format}")


def main():
    """Fonction principale."""
    parser = argparse.ArgumentParser(
        description="JJ Caption - Générateur de sous-titres automatique",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python main.py video.mp4 --language French --output srt
  python main.py video.mp4 --language French --output vtt,scc,ass
  python main.py video.mp4 --model medium --output-dir ./subtitles
        """
    )
    
    parser.add_argument(
        "input",
        help="Chemin vers le fichier vidéo/audio"
    )
    
    parser.add_argument(
        "--language", "-l",
        default="French",
        help="Langue du contenu (défaut: French)"
    )
    
    parser.add_argument(
        "--model", "-m",
        default="medium",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Modèle Whisper à utiliser (défaut: medium)"
    )
    
    parser.add_argument(
        "--output", "-o",
        default="srt",
        help="Format(s) de sortie (srt, vtt, scc, ass, txt, json). Séparer par des virgules pour plusieurs formats"
    )
    
    parser.add_argument(
        "--output-dir", "-d",
        help="Répertoire de sortie (optionnel)"
    )
    
    parser.add_argument(
        "--task",
        default="transcribe",
        choices=["transcribe", "translate"],
        help="Type de tâche (défaut: transcribe)"
    )
    
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Niveau de logging (défaut: INFO)"
    )
    
    args = parser.parse_args()
    
    # Configuration du logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    logger.info("🚀 Démarrage de JJ Caption")
    
    # Validation du fichier d'entrée
    if not validate_input_file(args.input):
        sys.exit(1)
    
    try:
        # Initialisation des composants
        logger.info(f"📝 Initialisation du modèle Whisper: {args.model}")
        whisper_handler = WhisperHandler(model_name=args.model)
        
        converter = FormatConverter()
        
        # Transcription
        logger.info(f"🎬 Transcription de: {args.input}")
        result = whisper_handler.transcribe(
            input_path=args.input,
            language=args.language,
            task=args.task
        )
        
        # Génération des formats de sortie
        output_formats = [fmt.strip() for fmt in args.output.split(",")]
        
        for output_format in output_formats:
            output_path = get_output_path(args.input, output_format, args.output_dir)
            
            logger.info(f"💾 Sauvegarde au format {output_format.upper()}: {output_path}")
            
            if output_format == "srt":
                whisper_handler.save_srt(result, output_path)
            elif output_format == "vtt":
                whisper_handler.save_vtt(result, output_path)
            elif output_format == "txt":
                whisper_handler.save_txt(result, output_path, args.input)
            elif output_format == "json":
                whisper_handler.save_json(result, output_path)
            elif output_format in ["scc", "ass"]:
                # Sauvegarder d'abord en SRT temporaire
                temp_srt = get_output_path(args.input, "srt", args.output_dir)
                whisper_handler.save_srt(result, temp_srt)
                
                # Convertir vers le format cible
                if output_format == "scc":
                    converter.srt_to_scc(temp_srt, output_path)
                elif output_format == "ass":
                    converter.srt_to_ass(temp_srt, output_path)
                
                # Supprimer le fichier temporaire
                Path(temp_srt).unlink(missing_ok=True)
            else:
                logger.warning(f"⚠️ Format non supporté ignoré: {output_format}")
        
        logger.info("✅ Traitement terminé avec succès!")
        
        # Afficher les fichiers générés
        print("\n📁 Fichiers générés:")
        for output_format in output_formats:
            if output_format in ["srt", "vtt", "txt", "json", "scc", "ass"]:
                output_path = get_output_path(args.input, output_format, args.output_dir)
                if Path(output_path).exists():
                    print(f"  ✅ {output_path}")
        
    except KeyboardInterrupt:
        logger.info("⏹️ Traitement interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Erreur lors du traitement: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 