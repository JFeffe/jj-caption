"""
Convertisseur de formats de sous-titres.
"""

import os
import logging
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from pycaption import SRTReader, SCCWriter, WebVTTReader, DFXPReader

logger = logging.getLogger(__name__)


class FormatConverter:
    """
    Convertisseur entre différents formats de sous-titres.
    """
    
    def __init__(self):
        """Initialise le convertisseur."""
        self.supported_formats = {
            'srt': 'SubRip',
            'vtt': 'WebVTT', 
            'scc': 'Scenarist Closed Captions',
            'ass': 'Advanced SubStation Alpha',
            'txt': 'Plain Text',
            'json': 'JSON'
        }
    
    def srt_to_vtt(self, input_path: str, output_path: str) -> None:
        """
        Convertit un fichier SRT en VTT.
        
        Args:
            input_path: Chemin du fichier SRT
            output_path: Chemin de sortie VTT
        """
        try:
            logger.info(f"Conversion SRT vers VTT: {input_path} -> {output_path}")
            
            with open(input_path, 'r', encoding='utf-8') as f:
                srt_content = f.read()
            
            # Utiliser pycaption pour la conversion
            reader = SRTReader()
            captions = reader.read(srt_content)
            
            # Écrire en format VTT
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("WEBVTT\n\n")
                
                for i, caption in enumerate(captions.get_captions("en-US"), 1):
                    start_time = self._format_timestamp_vtt(caption.start)
                    end_time = self._format_timestamp_vtt(caption.end)
                    text = caption.get_text()
                    
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{text}\n\n")
            
            logger.info("Conversion SRT vers VTT terminée")
            
        except Exception as e:
            logger.error(f"Erreur lors de la conversion SRT vers VTT: {e}")
            raise
    
    def srt_to_scc(self, input_path: str, output_path: str) -> None:
        """
        Convertit un fichier SRT en SCC.
        
        Args:
            input_path: Chemin du fichier SRT
            output_path: Chemin de sortie SCC
        """
        try:
            logger.info(f"Conversion SRT vers SCC: {input_path} -> {output_path}")
            
            with open(input_path, 'r', encoding='utf-8') as f:
                srt_content = f.read()
            
            # Utiliser pycaption pour la conversion
            reader = SRTReader()
            captions = reader.read(srt_content)
            
            writer = SCCWriter()
            scc_content = writer.write(captions)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(scc_content)
            
            logger.info("Conversion SRT vers SCC terminée")
            
        except Exception as e:
            logger.error(f"Erreur lors de la conversion SRT vers SCC: {e}")
            raise
    
    def srt_to_ass(self, input_path: str, output_path: str) -> None:
        """
        Convertit un fichier SRT en ASS.
        
        Args:
            input_path: Chemin du fichier SRT
            output_path: Chemin de sortie ASS
        """
        try:
            logger.info(f"Conversion SRT vers ASS: {input_path} -> {output_path}")
            
            # Lire le fichier SRT
            segments = self._parse_srt(input_path)
            
            # Écrire en format ASS
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("[Script Info]\n")
                f.write("Title: Generated Subtitles\n")
                f.write("ScriptType: v4.00+\n")
                f.write("WrapStyle: 0\n")
                f.write("ScaledBorderAndShadow: yes\n")
                f.write("YCbCr Matrix: TV.601\n\n")
                
                f.write("[V4+ Styles]\n")
                f.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
                f.write("Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1\n\n")
                
                f.write("[Events]\n")
                f.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
                
                for segment in segments:
                    start_time = self._format_timestamp_ass(segment['start'])
                    end_time = self._format_timestamp_ass(segment['end'])
                    text = segment['text'].replace('\n', '\\N')
                    
                    f.write(f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{text}\n")
            
            logger.info("Conversion SRT vers ASS terminée")
            
        except Exception as e:
            logger.error(f"Erreur lors de la conversion SRT vers ASS: {e}")
            raise
    
    def srt_to_txt(self, input_path: str, output_path: str) -> None:
        """
        Convertit un fichier SRT en TXT (texte simple).
        
        Args:
            input_path: Chemin du fichier SRT
            output_path: Chemin de sortie TXT
        """
        try:
            logger.info(f"Conversion SRT vers TXT: {input_path} -> {output_path}")
            
            segments = self._parse_srt(input_path)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                for segment in segments:
                    f.write(f"{segment['text']}\n")
            
            logger.info("Conversion SRT vers TXT terminée")
            
        except Exception as e:
            logger.error(f"Erreur lors de la conversion SRT vers TXT: {e}")
            raise
    
    def srt_to_json(self, input_path: str, output_path: str) -> None:
        """
        Convertit un fichier SRT en JSON.
        
        Args:
            input_path: Chemin du fichier SRT
            output_path: Chemin de sortie JSON
        """
        try:
            logger.info(f"Conversion SRT vers JSON: {input_path} -> {output_path}")
            
            segments = self._parse_srt(input_path)
            
            data = {
                "format": "srt",
                "segments": segments
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info("Conversion SRT vers JSON terminée")
            
        except Exception as e:
            logger.error(f"Erreur lors de la conversion SRT vers JSON: {e}")
            raise
    
    def _parse_srt(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Parse un fichier SRT et retourne les segments.
        
        Args:
            file_path: Chemin du fichier SRT
            
        Returns:
            Liste des segments avec start, end, text
        """
        segments = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern pour parser SRT
        pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n([\s\S]*?)(?=\n\n|\n\d+\n|$)'
        matches = re.findall(pattern, content)
        
        for match in matches:
            index = int(match[0])
            start_time = self._parse_timestamp(match[1])
            end_time = self._parse_timestamp(match[2])
            text = match[3].strip()
            
            segments.append({
                'index': index,
                'start': start_time,
                'end': end_time,
                'text': text
            })
        
        return segments
    
    def _parse_timestamp(self, timestamp: str) -> float:
        """
        Parse un timestamp SRT en secondes.
        
        Args:
            timestamp: Timestamp au format HH:MM:SS,mmm
            
        Returns:
            Temps en secondes
        """
        time_str, millisecs = timestamp.split(',')
        hours, minutes, seconds = map(int, time_str.split(':'))
        millisecs = int(millisecs)
        
        return hours * 3600 + minutes * 60 + seconds + millisecs / 1000
    
    def _format_timestamp_vtt(self, seconds: float) -> str:
        """
        Formate un timestamp en format VTT.
        
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
    
    def _format_timestamp_ass(self, seconds: float) -> str:
        """
        Formate un timestamp en format ASS.
        
        Args:
            seconds: Temps en secondes
            
        Returns:
            Timestamp formaté
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        centisecs = int((seconds % 1) * 100)
        
        return f"{hours}:{minutes:02d}:{secs:02d}.{centisecs:02d}"
    
    def get_supported_formats(self) -> Dict[str, str]:
        """
        Retourne les formats supportés.
        
        Returns:
            Dictionnaire des formats supportés
        """
        return self.supported_formats.copy()
    
    def convert(self, input_path: str, output_path: str, input_format: str = None, output_format: str = None) -> None:
        """
        Convertit un fichier entre formats.
        
        Args:
            input_path: Chemin du fichier d'entrée
            output_path: Chemin du fichier de sortie
            input_format: Format d'entrée (auto-détecté si None)
            output_format: Format de sortie (déduit de l'extension si None)
        """
        # Auto-détection des formats
        if input_format is None:
            input_format = Path(input_path).suffix.lower()[1:]
        
        if output_format is None:
            output_format = Path(output_path).suffix.lower()[1:]
        
        # Validation des formats
        if input_format not in self.supported_formats:
            raise ValueError(f"Format d'entrée non supporté: {input_format}")
        
        if output_format not in self.supported_formats:
            raise ValueError(f"Format de sortie non supporté: {output_format}")
        
        # Conversion
        if input_format == 'srt':
            if output_format == 'vtt':
                self.srt_to_vtt(input_path, output_path)
            elif output_format == 'scc':
                self.srt_to_scc(input_path, output_path)
            elif output_format == 'ass':
                self.srt_to_ass(input_path, output_path)
            elif output_format == 'txt':
                self.srt_to_txt(input_path, output_path)
            elif output_format == 'json':
                self.srt_to_json(input_path, output_path)
            else:
                raise ValueError(f"Conversion {input_format} vers {output_format} non implémentée")
        else:
            raise ValueError(f"Format d'entrée {input_format} non supporté pour la conversion") 