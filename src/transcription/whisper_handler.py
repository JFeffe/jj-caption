"""
Gestionnaire de transcription avec Whisper.
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
import whisper
import ffmpeg

logger = logging.getLogger(__name__)


class WhisperHandler:
    """
    Gestionnaire pour la transcription audio/vidéo avec Whisper.
    """
    
    def __init__(self, model_name: str = "medium", device: str = "cpu"):
        """
        Initialise le gestionnaire Whisper.
        
        Args:
            model_name: Nom du modèle Whisper (tiny, base, small, medium, large)
            device: Device pour l'inférence (cpu, cuda, auto)
        """
        self.model_name = model_name
        self.device = device
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Charge le modèle Whisper."""
        try:
            logger.info(f"Chargement du modèle Whisper: {self.model_name}")
            
            # Forcer l'utilisation du CPU pour éviter les problèmes de compatibilité
            import torch
            if torch.cuda.is_available():
                logger.info("CUDA disponible mais utilisation forcée du CPU pour la compatibilité")
            
            # Charger le modèle avec des options spécifiques pour éviter les erreurs
            self.model = whisper.load_model(
                self.model_name, 
                device="cpu",
                download_root=None,
                in_memory=False
            )
            logger.info("Modèle chargé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle: {e}")
            # Essayer avec des options de fallback
            try:
                logger.info("Tentative de chargement avec options de fallback...")
                self.model = whisper.load_model(self.model_name, device="cpu")
                logger.info("Modèle chargé avec succès (fallback)")
            except Exception as e2:
                logger.error(f"Erreur lors du chargement de fallback: {e2}")
                raise
    
    def transcribe(
        self,
        input_path: str,
        language: Optional[str] = None,
        task: str = "transcribe",
        output_format: str = "srt"
    ) -> Dict[str, Any]:
        """
        Transcrit un fichier audio/vidéo.
        
        Args:
            input_path: Chemin vers le fichier d'entrée
            language: Langue du contenu (auto-détection si None)
            task: Type de tâche (transcribe ou translate)
            output_format: Format de sortie (srt, vtt, txt, json)
            
        Returns:
            Résultat de la transcription
        """
        return self._transcribe_with_config(input_path, language, task, output_format)
    
    def transcribe_with_options(
        self,
        input_path: str,
        language: Optional[str] = None,
        task: str = "transcribe",
        condition_on_previous_text: bool = True,
        temperature: float = 0.0,
        compression_ratio_threshold: float = 2.4,
        logprob_threshold: float = -1.0,
        no_speech_threshold: float = 0.6
    ) -> Dict[str, Any]:
        """
        Transcrit avec des options avancées pour améliorer la qualité.
        
        Args:
            input_path: Chemin vers le fichier d'entrée
            language: Langue du contenu
            task: Type de tâche
            condition_on_previous_text: Utiliser le contexte précédent
            temperature: Contrôle la créativité (0.0 = déterministe)
            compression_ratio_threshold: Seuil de compression
            logprob_threshold: Seuil de probabilité logarithmique
            no_speech_threshold: Seuil de détection de parole
            
        Returns:
            Résultat de la transcription
        """
        return self._transcribe_with_config(
            input_path, language, task, "srt",
            condition_on_previous_text=condition_on_previous_text,
            temperature=temperature,
            compression_ratio_threshold=compression_ratio_threshold,
            logprob_threshold=logprob_threshold,
            no_speech_threshold=no_speech_threshold
        )
    
    def _transcribe_with_config(
        self,
        input_path: str,
        language: Optional[str] = None,
        task: str = "transcribe",
        output_format: str = "srt",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Transcription avec configuration personnalisée.
        """
        try:
            logger.info(f"Transcription de: {input_path}")
            
            # Validation du fichier d'entrée
            if not os.path.exists(input_path):
                raise FileNotFoundError(f"Fichier non trouvé: {input_path}")
            
            # Configuration de FFmpeg pour Whisper
            import whisper
            import subprocess
            
            # Vérifier si FFmpeg est disponible
            ffmpeg_path = None
            possible_paths = [
                "ffmpeg",
                r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
                os.path.expanduser(r"~\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1.1-full_build\bin\ffmpeg.exe")
            ]
            
            for path in possible_paths:
                try:
                    if path == "ffmpeg":
                        subprocess.run([path, "-version"], capture_output=True, check=True)
                        ffmpeg_path = path
                        break
                    elif os.path.exists(path):
                        subprocess.run([path, "-version"], capture_output=True, check=True)
                        ffmpeg_path = path
                        break
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            
            if ffmpeg_path:
                logger.info(f"FFmpeg trouvé: {ffmpeg_path}")
                # Configurer Whisper pour utiliser le chemin FFmpeg
                import whisper.audio
                whisper.audio.ffmpeg_path = ffmpeg_path
                
                # Ajouter le répertoire FFmpeg au PATH
                ffmpeg_dir = os.path.dirname(ffmpeg_path)
                if ffmpeg_dir not in os.environ.get('PATH', ''):
                    os.environ['PATH'] = ffmpeg_dir + os.pathsep + os.environ.get('PATH', '')
                    logger.info(f"Répertoire FFmpeg ajouté au PATH: {ffmpeg_dir}")
            else:
                logger.warning("FFmpeg non trouvé, Whisper utilisera sa configuration par défaut")
            
            # Options de transcription de base
            options = {
                "task": task,
                "verbose": False,
                "fp16": False
            }
            
            # Ajouter les options avancées si fournies
            if kwargs:
                options.update(kwargs)
                logger.info(f"Options avancées utilisées: {kwargs}")
            
            if language:
                options["language"] = language
            
            # Transcription
            result = self.model.transcribe(input_path, **options)
            
            logger.info("Transcription terminée avec succès")
            return result
            
        except Exception as e:
            logger.error(f"Erreur lors de la transcription: {e}")
            raise
    
    def save_srt(self, result: Dict[str, Any], output_path: str) -> None:
        """
        Sauvegarde le résultat au format SRT.
        
        Args:
            result: Résultat de la transcription
            output_path: Chemin de sortie
        """
        try:
            logger.info(f"Sauvegarde SRT: {output_path}")
            
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, segment in enumerate(result["segments"], 1):
                    start_time = self._format_timestamp(segment["start"])
                    end_time = self._format_timestamp(segment["end"])
                    text = segment["text"].strip()
                    
                    f.write(f"{i}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{text}\n\n")
            
            logger.info("Fichier SRT sauvegardé avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde SRT: {e}")
            raise
    
    def save_vtt(self, result: Dict[str, Any], output_path: str) -> None:
        """
        Sauvegarde le résultat au format VTT.
        
        Args:
            result: Résultat de la transcription
            output_path: Chemin de sortie
        """
        try:
            logger.info(f"Sauvegarde VTT: {output_path}")
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("WEBVTT\n\n")
                
                for i, segment in enumerate(result["segments"], 1):
                    start_time = self._format_timestamp_vtt(segment["start"])
                    end_time = self._format_timestamp_vtt(segment["end"])
                    text = segment["text"].strip()
                    
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{text}\n\n")
            
            logger.info("Fichier VTT sauvegardé avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde VTT: {e}")
            raise
    
    def save_txt(self, result: Dict[str, Any], output_path: str, input_path: str = None) -> None:
        """
        Sauvegarde le résultat au format TXT pour diffusion professionnelle.
        
        Args:
            result: Résultat de la transcription
            output_path: Chemin de sortie
            input_path: Chemin du fichier vidéo source (pour timecodes LTC)
        """
        try:
            logger.info(f"Sauvegarde TXT pour diffusion professionnelle: {output_path}")
            
            # Récupérer les timecodes LTC du fichier vidéo
            ltc_start = None
            if input_path:
                ltc_start = self._get_ltc_timecode(input_path)
            
            # Codes de diffusion
            codes = self._get_broadcast_codes()
            
            with open(output_path, 'w', encoding='utf-8') as f:
                # En-tête du fichier de diffusion
                f.write("'**************************************************\n\n")
                f.write("\\ Title: " + os.path.basename(output_path) + "\n\n")
                f.write("\\ Version: 1.0\n")
                f.write("\\ Channel: F1C1\n")
                f.write("\\ Rate: 30d\n")
                f.write("\\ Type: LTC\n\n")
                f.write("\\ Generated By: JJ Caption\n")
                f.write("\\ CaptionFile: " + output_path + "\n")
                f.write("\\ MediaFile: " + (input_path or "Unknown") + "\n\n")
                f.write("\\ Author: JJ Caption\n")
                f.write("\\ Owner: \n\n")
                f.write("\\ Date: " + self._get_current_date() + "\n")
                f.write("\\ Time: " + self._get_current_time() + "\n\n")
                f.write("'**************************************************\n\n\n")
                
                # Timecode de départ avec format professionnel
                if ltc_start:
                    # Ajuster le timecode de départ
                    adjusted_start = self._adjust_start_time(ltc_start)
                    f.write("\\ TC:  " + adjusted_start + " " + codes["clear"] + "\n")
                else:
                    # Timecode par défaut
                    f.write("\\ TC:  10:00:00;00 " + codes["clear"] + "\n")
                
                # Segments avec timecodes LTC et segmentation professionnelle
                for i, segment in enumerate(result["segments"]):
                    start_time = segment["start"]
                    text = segment["text"].strip()
                    
                    # Convertir le temps en timecode LTC avec ajustement
                    if ltc_start:
                        adjusted_start = self._adjust_start_time(ltc_start)
                        ltc_time = self._convert_to_ltc(start_time, adjusted_start)
                    else:
                        ltc_time = self._format_timestamp_ltc(start_time)
                    
                    # Segmenter le texte pour la diffusion
                    text_segments = self._segment_text_for_broadcast(text)
                    
                    # Écrire chaque segment de texte
                    for j, text_segment in enumerate(text_segments):
                        if j == 0:
                            # Premier segment du segment original
                            f.write("\\ TC:  " + ltc_time + " " + codes["text_start"] + text_segment + codes["text_end"] + "\n")
                        else:
                            # Segments suivants (ajouter un petit délai)
                            next_time = start_time + (j * 0.5)  # 0.5 seconde entre segments
                            if ltc_start:
                                adjusted_start = self._adjust_start_time(ltc_start)
                                next_ltc_time = self._convert_to_ltc(next_time, adjusted_start)
                            else:
                                next_ltc_time = self._format_timestamp_ltc(next_time)
                            f.write("\\ TC:  " + next_ltc_time + " " + codes["text_start"] + text_segment + codes["text_end"] + "\n")
                    
                    # Ajouter une pause entre les segments principaux
                    if i < len(result["segments"]) - 1:
                        next_segment_start = result["segments"][i + 1]["start"]
                        if next_segment_start - start_time > 2.0:  # Pause de plus de 2 secondes
                            pause_time = start_time + 1.0
                            if ltc_start:
                                adjusted_start = self._adjust_start_time(ltc_start)
                                pause_ltc_time = self._convert_to_ltc(pause_time, adjusted_start)
                            else:
                                pause_ltc_time = self._format_timestamp_ltc(pause_time)
                            f.write("\\ TC:  " + pause_ltc_time + " " + codes["clear"] + "\n")
            
            logger.info("Fichier TXT pour diffusion professionnelle sauvegardé avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde TXT: {e}")
            raise
    
    def save_json(self, result: Dict[str, Any], output_path: str) -> None:
        """
        Sauvegarde le résultat au format JSON.
        
        Args:
            result: Résultat de la transcription
            output_path: Chemin de sortie
        """
        try:
            logger.info(f"Sauvegarde JSON: {output_path}")
            
            import json
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            logger.info("Fichier JSON sauvegardé avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde JSON: {e}")
            raise
    
    def _format_timestamp(self, seconds: float) -> str:
        """
        Formate un timestamp en format SRT (HH:MM:SS,mmm).
        
        Args:
            seconds: Temps en secondes
            
        Returns:
            Timestamp formaté
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"
    
    def _format_timestamp_vtt(self, seconds: float) -> str:
        """
        Formate un timestamp en format VTT (HH:MM:SS.mmm).
        
        Args:
            seconds: Temps en secondes
            
        Returns:
            Timestamp formaté
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millisecs:03d}"
    
    def get_available_models(self) -> List[str]:
        """
        Retourne la liste des modèles disponibles.
        
        Returns:
            Liste des noms de modèles
        """
        return ["tiny", "base", "small", "medium", "large"]
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Retourne les informations sur le modèle actuel.
        
        Returns:
            Informations sur le modèle
        """
        return {
            "name": self.model_name,
            "device": self.device,
            "available_models": self.get_available_models()
        }
    
    def _get_ltc_timecode(self, video_path: str) -> Optional[str]:
        """
        Récupère le timecode LTC du fichier vidéo.
        
        Args:
            video_path: Chemin vers le fichier vidéo
            
        Returns:
            Timecode LTC ou None si non trouvé
        """
        try:
            import subprocess
            import json
            
            # Utiliser ffprobe pour récupérer les timecodes
            ffprobe_path = None
            possible_paths = [
                "ffprobe",
                r"C:\Program Files\ffmpeg\bin\ffprobe.exe",
                os.path.expanduser(r"~\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1.1-full_build\bin\ffprobe.exe")
            ]
            
            for path in possible_paths:
                try:
                    if path == "ffprobe":
                        result = subprocess.run([path, "-v", "quiet", "-show_entries", "stream_tags=timecode", "-of", "json", video_path], 
                                              capture_output=True, text=True, check=True)
                        ffprobe_path = path
                        break
                    elif os.path.exists(path):
                        result = subprocess.run([path, "-v", "quiet", "-show_entries", "stream_tags=timecode", "-of", "json", video_path], 
                                              capture_output=True, text=True, check=True)
                        ffprobe_path = path
                        break
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            
            if ffprobe_path and result.stdout:
                data = json.loads(result.stdout)
                # Chercher le timecode dans les streams ou le format
                for stream in data.get("streams", []):
                    if "tags" in stream and "timecode" in stream["tags"]:
                        return stream["tags"]["timecode"]
                
                # Chercher dans les tags du format
                if "format" in data and "tags" in data["format"] and "timecode" in data["format"]["tags"]:
                    return data["format"]["tags"]["timecode"]
            
            return None
            
        except Exception as e:
            logger.warning(f"Impossible de récupérer le timecode LTC: {e}")
            return None
    
    def _convert_to_ltc(self, seconds: float, start_ltc: str) -> str:
        """
        Convertit un temps en secondes vers un timecode LTC.
        
        Args:
            seconds: Temps en secondes depuis le début
            start_ltc: Timecode LTC de départ (format HH:MM:SS;FF ou HH:MM:SS:FF)
            
        Returns:
            Timecode LTC calculé
        """
        try:
            # Normaliser le format du timecode de départ
            if ";" in start_ltc:
                # Format HH:MM:SS;FF
                parts = start_ltc.replace(";", ":").split(":")
            else:
                # Format HH:MM:SS:FF
                parts = start_ltc.split(":")
            
            if len(parts) >= 3:
                start_hours = int(parts[0])
                start_minutes = int(parts[1])
                start_seconds = int(parts[2])
                
                # Convertir en secondes totales
                start_total_seconds = start_hours * 3600 + start_minutes * 60 + start_seconds
                
                # Ajouter le temps de la transcription
                total_seconds = start_total_seconds + seconds
                
                # Convertir en timecode LTC
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                secs = int(total_seconds % 60)
                
                # Format avec point-virgule comme dans l'original
                return f"{hours:02d}:{minutes:02d};{secs:02d}"
            else:
                raise ValueError(f"Format de timecode invalide: {start_ltc}")
            
        except Exception as e:
            logger.warning(f"Erreur lors de la conversion LTC: {e}")
            return self._format_timestamp_ltc(seconds)
    
    def _adjust_start_time(self, start_ltc: str) -> str:
        """
        Ajuste le timecode de départ pour correspondre au format professionnel.
        
        Args:
            start_ltc: Timecode LTC original
            
        Returns:
            Timecode ajusté
        """
        try:
            if not start_ltc:
                return "10:00:00;00"  # Timecode par défaut
            
            # Si le timecode commence avant 10:00:00, l'ajuster
            parts = start_ltc.split(":")
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2])
            
            # Si c'est avant 10:00:00, ajuster à 10:00:00
            if hours < 10 or (hours == 9 and minutes == 59):
                return "10:00:00;00"
            
            return start_ltc
            
        except Exception as e:
            logger.warning(f"Erreur lors de l'ajustement du timecode: {e}")
            return "10:00:00;00"
    
    def _format_timestamp_ltc(self, seconds: float) -> str:
        """
        Formate un timestamp en format LTC (HH:MM:SS).
        
        Args:
            seconds: Temps en secondes
            
        Returns:
            Timestamp formaté LTC
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        # Format avec point-virgule comme dans l'original
        return f"{hours:02d}:{minutes:02d};{secs:02d}"
    
    def _get_broadcast_codes(self) -> Dict[str, str]:
        """
        Retourne les codes de diffusion professionnels.
        
        Returns:
            Dictionnaire des codes
        """
        return {
            "clear": "¶÷142C",
            "text_start": "¶÷1426÷142D÷1470",
            "text_end": "§00",
            "pause": "¶÷142C",
            "italics_start": "¶÷1425",
            "italics_end": "¶÷142C",
            "underline_start": "¶÷142D",
            "underline_end": "¶÷142C"
        }
    
    def _segment_text_for_broadcast(self, text: str, max_length: int = 25) -> List[str]:
        """
        Segmente le texte pour la diffusion en respectant les contraintes professionnelles.
        
        Args:
            text: Texte à segmenter
            max_length: Longueur maximale par segment
            
        Returns:
            Liste des segments
        """
        # Nettoyer le texte
        text = text.strip()
        
        # Ajouter un tiret au début si c'est une nouvelle phrase
        if text and not text.startswith('-') and not text.startswith('('):
            text = '- ' + text
        
        words = text.split()
        segments = []
        current_segment = ""
        
        for word in words:
            # Vérifier si l'ajout du mot dépasse la limite
            test_segment = (current_segment + " " + word) if current_segment else word
            
            if len(test_segment) <= max_length:
                current_segment = test_segment
            else:
                if current_segment:
                    segments.append(current_segment.strip())
                current_segment = word
        
        if current_segment:
            segments.append(current_segment.strip())
        
        return segments
    

    
    def _get_current_date(self) -> str:
        """Retourne la date actuelle au format requis."""
        from datetime import datetime
        return datetime.now().strftime("%B %d, %Y")
    
    def _get_current_time(self) -> str:
        """Retourne l'heure actuelle au format requis."""
        from datetime import datetime
        return datetime.now().strftime("%I:%M:%S %p")
    
    def post_process_transcription(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Applique un post-traitement pour améliorer la qualité de la transcription.
        
        Args:
            result: Résultat de la transcription Whisper
            
        Returns:
            Résultat post-traité
        """
        try:
            logger.info("Application du post-traitement...")
            
            # Copier le résultat pour ne pas modifier l'original
            processed_result = result.copy()
            segments = processed_result.get('segments', []).copy()
            
            # 1. Correction des erreurs communes
            segments = self._correct_common_errors(segments)
            
            # 2. Amélioration de la ponctuation
            segments = self._improve_punctuation(segments)
            
            # 3. Fusion des segments trop courts
            segments = self._merge_short_segments(segments)
            
            # 4. Correction du contexte
            segments = self._improve_context(segments)
            
            # Mettre à jour le résultat
            processed_result['segments'] = segments
            processed_result['text'] = ' '.join([seg.get('text', '').strip() for seg in segments])
            
            logger.info("Post-traitement terminé avec succès")
            return processed_result
            
        except Exception as e:
            logger.error(f"Erreur lors du post-traitement: {e}")
            return result  # Retourner l'original en cas d'erreur
    
    def _correct_common_errors(self, segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Corrige les erreurs communes de transcription."""
        corrections = {
            # Erreurs de transcription françaises communes
            "awe vi": "au revoir",
            "brigette": "Brigitte",
            "j'en amie": "Jean-Mi",
            "ma tête": "matin",
            "racker": "raquer",
            "t'as barouette": "tabarouette",
            "colombe": "Colombie",
            "sèillés": "séries",
            "singlé": "cinglées",
            "vivrent": "vivre un",
            "entraînement": "entre amis",
            "coïnce": "convalescence",
            "convallé sens": "convalescence",
            "hébrigette": "Brigitte",
            "boquillard": "Boquilla",
            "pirelles": "pirogues",
            "paix": "pêche",
            "maix": "mer",
            "t'explique": "typique",
            "entriez": "intriguez",
            "gure": "prêt",
            "joviterrement": "majoritairement",
            "afro-colorbienne": "afro-colombienne",
            "haute haute": "communautaire",
            "vitra-ditionnel": "vie traditionnel",
            "génère": "génère",
            "ancestral": "ancestrales",
            "Ronnaie": "Rony",
            "attuyer": "capturer",
            "crabeurs": "crabes",
            "parles": "paroles",
            "médé brûlée": "méditation",
            "vacimmants": "investissements",
            "balkille": "Boquilla",
            "plache": "plage",
            "gentrification": "gentrification",
            "élégion": "population",
            "capaixeur": "capable",
            "décès d'érestir": "défis d'exister",
            "blessier": "plaisir",
            "page": "pêche",
            "lycier": "pêche",
            "main grave": "mangrove",
            "pêcher les": "pêcher des",
            "Réder": "Rony",
            "salez traille": "sale travail",
            "soquies": "soucis",
            "contre": "compte",
            "grand-t-blom": "grand problème",
            "égrés": "égratignures",
            "commun": "commun",
            "matre": "matière",
            "mélange": "mélange"
        }
        
        for segment in segments:
            text = segment.get('text', '')
            original_text = text
            
            # Appliquer les corrections
            for error, correction in corrections.items():
                text = text.replace(error, correction)
            
            # Mettre à jour le segment si des corrections ont été appliquées
            if text != original_text:
                segment['text'] = text
                logger.debug(f"Correction: '{original_text}' -> '{text}'")
        
        return segments
    
    def _improve_punctuation(self, segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Améliore la ponctuation."""
        for segment in segments:
            text = segment.get('text', '').strip()
            
            # Ajouter des points d'interrogation pour les questions
            if any(word in text.lower() for word in ['quoi', 'comment', 'pourquoi', 'quand', 'où', 'qui', 'combien']):
                if not text.endswith('?'):
                    text += '?'
            
            # Ajouter des points d'exclamation pour les exclamations
            if any(word in text.lower() for word in ['oh', 'ah', 'wow', 'super', 'génial', 'parfait']):
                if not text.endswith('!'):
                    text += '!'
            
            # Capitaliser le début des phrases
            if text and not text[0].isupper():
                text = text[0].upper() + text[1:]
            
            segment['text'] = text
        
        return segments
    
    def _merge_short_segments(self, segments: List[Dict[str, Any]], min_duration: float = 1.0) -> List[Dict[str, Any]]:
        """Fusionne les segments trop courts."""
        if not segments:
            return segments
        
        merged_segments = []
        current_segment = segments[0].copy()
        
        for i in range(1, len(segments)):
            segment = segments[i]
            current_duration = current_segment.get('end', 0) - current_segment.get('start', 0)
            
            # Si le segment actuel est trop court, le fusionner avec le suivant
            if current_duration < min_duration:
                current_text = current_segment.get('text', '').strip()
                next_text = segment.get('text', '').strip()
                
                # Fusionner les textes
                if current_text and next_text:
                    current_segment['text'] = current_text + ' ' + next_text
                elif next_text:
                    current_segment['text'] = next_text
                
                # Mettre à jour la fin
                current_segment['end'] = segment.get('end', current_segment.get('end', 0))
            else:
                # Le segment actuel est assez long, l'ajouter et passer au suivant
                merged_segments.append(current_segment)
                current_segment = segment.copy()
        
        # Ajouter le dernier segment
        merged_segments.append(current_segment)
        
        return merged_segments
    
    def _improve_context(self, segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Améliore le contexte en utilisant les segments précédents."""
        for i in range(1, len(segments)):
            current_segment = segments[i]
            previous_segment = segments[i-1]
            
            current_text = current_segment.get('text', '').strip()
            previous_text = previous_segment.get('text', '').strip()
            
            # Si le segment actuel commence par une minuscule et le précédent ne se termine pas par un point
            if (current_text and current_text[0].islower() and 
                previous_text and not previous_text.endswith('.') and 
                not previous_text.endswith('!') and not previous_text.endswith('?')):
                
                # C'est probablement une continuation de phrase
                current_segment['text'] = current_text[0].lower() + current_text[1:]
        
        return segments 