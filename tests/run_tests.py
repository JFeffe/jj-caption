#!/usr/bin/env python3
"""
Script de lancement des tests pour JJ Caption.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_tests(test_type="all", verbose=True):
    """Lance les tests selon le type spécifié."""
    
    # Vérifier que pytest est installé
    try:
        import pytest
    except ImportError:
        print("❌ pytest n'est pas installé.")
        print("Installez-le avec: pip install pytest pytest-cov")
        return False
    
    # Options de base
    cmd = [sys.executable, "-m", "pytest"]
    
    if verbose:
        cmd.append("-v")
    
    # Ajouter la couverture de code
    cmd.extend(["--cov=src", "--cov-report=term-missing"])
    
    # Sélectionner les tests selon le type
    if test_type == "unit":
        print("🧪 Lancement des tests unitaires...")
        cmd.extend(["-m", "unit"])
    elif test_type == "integration":
        print("🔗 Lancement des tests d'intégration...")
        cmd.extend(["-m", "integration"])
    elif test_type == "fast":
        print("⚡ Lancement des tests rapides (sans les tests lents)...")
        cmd.extend(["-m", "not slow"])
    elif test_type == "slow":
        print("🐌 Lancement des tests lents...")
        cmd.extend(["-m", "slow"])
    elif test_type == "cli":
        print("💻 Lancement des tests CLI...")
        cmd.extend(["-m", "cli"])
    elif test_type == "gui":
        print("🖥️ Lancement des tests GUI...")
        cmd.extend(["-m", "gui"])
    else:
        print("🧪 Lancement de tous les tests...")
    
    # Ajouter le répertoire des tests
    cmd.append("tests/")
    
    print(f"Commande: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ Tous les tests ont réussi!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Certains tests ont échoué (code: {e.returncode})")
        return False


def run_specific_test(test_file):
    """Lance un test spécifique."""
    test_path = Path("tests") / test_file
    
    if not test_path.exists():
        print(f"❌ Fichier de test non trouvé: {test_path}")
        return False
    
    print(f"🧪 Lancement du test spécifique: {test_file}")
    
    cmd = [
        sys.executable, "-m", "pytest",
        str(test_path),
        "-v",
        "--tb=short"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ Test réussi!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Test échoué (code: {e.returncode})")
        return False


def show_test_help():
    """Affiche l'aide pour les tests."""
    print("""
🧪 JJ Caption - Script de Tests

Usage:
    python tests/run_tests.py [option]

Options:
    all          - Tous les tests (défaut)
    unit         - Tests unitaires uniquement
    integration  - Tests d'intégration uniquement
    fast         - Tests rapides (sans les tests lents)
    slow         - Tests lents uniquement
    cli          - Tests CLI uniquement
    gui          - Tests GUI uniquement
    help         - Affiche cette aide

Exemples:
    python tests/run_tests.py fast
    python tests/run_tests.py unit
    python tests/run_tests.py test_whisper_handler.py

Tests disponibles:
    ✅ test_whisper_handler.py - Tests pour WhisperHandler
    ✅ test_format_converter.py - Tests pour FormatConverter
    ✅ test_main.py - Tests pour l'interface CLI
    ✅ test_integration.py - Tests d'intégration complets
    """)


def main():
    """Fonction principale."""
    if len(sys.argv) < 2:
        print("🧪 Lancement de tous les tests...")
        success = run_tests("all")
    else:
        option = sys.argv[1].lower()
        
        if option == "help":
            show_test_help()
            return
        
        # Vérifier si c'est un fichier de test spécifique
        if option.endswith('.py'):
            success = run_specific_test(option)
        else:
            success = run_tests(option)
    
    if success:
        print("\n🎉 Tests terminés avec succès!")
        sys.exit(0)
    else:
        print("\n💥 Tests terminés avec des erreurs.")
        sys.exit(1)


if __name__ == "__main__":
    main() 