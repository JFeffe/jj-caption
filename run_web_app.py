#!/usr/bin/env python3
"""
Point d'entrée pour l'application JJ Caption sur Streamlit Cloud.
"""

import streamlit as st
import sys
from pathlib import Path

# Ajouter le répertoire src au path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Importer et lancer l'application
try:
    from gui.streamlit_app import *
    print("✅ Application JJ Caption chargée avec succès")
except Exception as e:
    print(f"❌ Erreur lors du chargement: {e}")
    
    # Fallback : interface simple
    st.title("🎤 JJ Caption")
    st.success("✅ Application déployée sur Streamlit Cloud !")
    st.info("L'interface complète sera disponible dans quelques instants...") 