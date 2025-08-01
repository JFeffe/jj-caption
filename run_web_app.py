#!/usr/bin/env python3
"""
Script pour lancer l'interface web Streamlit de JJ Caption.
"""

import subprocess
import sys
import os
from pathlib import Path


def main():
    """Lance l'interface web Streamlit."""
    
    # Vérifier que streamlit est installé
    try:
        import streamlit
        print(f"✅ Streamlit installé: {streamlit.__version__}")
    except ImportError:
        print("❌ Streamlit n'est pas installé. Installation...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        print("✅ Streamlit installé!")
    
    # Chemin vers l'application Streamlit
    app_path = Path(__file__).parent / "src" / "gui" / "streamlit_app.py"
    
    if not app_path.exists():
        print(f"❌ Fichier d'application non trouvé: {app_path}")
        return
    
    print("🚀 Lancement de l'interface web JJ Caption...")
    print("📱 L'interface sera disponible via Streamlit Cloud")
    print("⏹️ Appuyez sur Ctrl+C pour arrêter")
    print("-" * 50)
    
    try:
        # Lancer Streamlit sans contraintes de port pour Streamlit Cloud
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", str(app_path)
        ])
    except KeyboardInterrupt:
        print("\n⏹️ Interface arrêtée par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")


if __name__ == "__main__":
    main() 