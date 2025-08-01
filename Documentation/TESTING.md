# 🧪 Guide de Tests - JJ Caption

Ce guide explique comment tester l'application JJ Caption de différentes manières.

## 📋 Prérequis

### Installation des dépendances de test
```bash
pip install pytest pytest-cov
pip install openai-whisper pycaption streamlit ffmpeg-python
```

### Vérification de l'installation
```bash
python -c "import pytest; print('✅ pytest installé')"
python -c "import whisper; print('✅ whisper installé')"
python -c "import streamlit; print('✅ streamlit installé')"
```

## 🚀 Méthodes de Test

### 1. Tests Rapides (Recommandé pour commencer)

```bash
# Tests basiques sans Whisper
python -m pytest tests/test_basic.py -v

# Tests rapides (sans les tests lents)
python tests/run_tests.py fast

# Tests unitaires uniquement
python tests/run_tests.py unit
```

### 2. Tests Complets

```bash
# Tous les tests
python tests/run_tests.py all

# Tests d'intégration
python tests/run_tests.py integration

# Tests lents (avec Whisper)
python tests/run_tests.py slow
```

### 3. Tests Spécifiques

```bash
# Test d'un fichier spécifique
python -m pytest tests/test_basic.py -v

# Test d'une classe spécifique
python -m pytest tests/test_basic.py::TestBasicStructure -v

# Test d'une méthode spécifique
python -m pytest tests/test_basic.py::TestBasicStructure::test_file_structure -v
```

### 4. Tests avec Couverture

```bash
# Tests avec rapport de couverture
python -m pytest tests/ --cov=src --cov-report=html

# Afficher la couverture dans le terminal
python -m pytest tests/ --cov=src --cov-report=term-missing
```

## 📊 Types de Tests

### ✅ Tests Basiques (test_basic.py)
- **Structure du projet** : Vérifie que tous les fichiers nécessaires existent
- **Imports** : Teste que les modules peuvent être importés
- **CLI** : Teste l'interface en ligne de commande
- **FormatConverter** : Teste les conversions de formats

### ✅ Tests Unitaires
- **WhisperHandler** : Tests de transcription (nécessite Whisper)
- **FormatConverter** : Tests de conversion de formats
- **Main CLI** : Tests de l'interface en ligne de commande

### ✅ Tests d'Intégration
- **Workflow complet** : Transcription + conversion
- **Formats multiples** : Test de tous les formats de sortie
- **Gestion d'erreurs** : Test des cas d'erreur

### ✅ Tests de Performance
- **Tests lents** : Tests avec Whisper (marqués `@pytest.mark.slow`)
- **Tests rapides** : Tests sans Whisper

## 🎯 Tests Recommandés par Priorité

### 1. **Démarrage Rapide** (2 minutes)
```bash
python -m pytest tests/test_basic.py -v
```
✅ Vérifie que l'installation fonctionne

### 2. **Tests de Conversion** (5 minutes)
```bash
python -m pytest tests/test_format_converter.py -v
```
✅ Teste les conversions de formats sans Whisper

### 3. **Tests CLI** (1 minute)
```bash
python -m pytest tests/test_main.py -v
```
✅ Teste l'interface en ligne de commande

### 4. **Tests Complets** (10-30 minutes)
```bash
python tests/run_tests.py all
```
✅ Tests complets avec Whisper

## 🔧 Dépannage

### Problème : "ModuleNotFoundError"
```bash
# Solution : Ajouter src au path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
# Ou sur Windows :
set PYTHONPATH=%PYTHONPATH%;%CD%\src
```

### Problème : "RuntimeError" avec Whisper
```bash
# Solution : Utiliser un modèle plus petit
export WHISPER_MODEL=tiny
# Ou dans le code :
handler = WhisperHandler(model_name='tiny')
```

### Problème : "ffmpeg not found"
```bash
# Solution : Installer ffmpeg
# Windows : Télécharger depuis https://ffmpeg.org/
# Linux : sudo apt install ffmpeg
# Mac : brew install ffmpeg
```

## 📈 Interprétation des Résultats

### ✅ Tests Réussis
```
================================================= 9 passed, 1 skipped in 5.11s =================================================
```
- **Passed** : Tests qui fonctionnent
- **Skipped** : Tests ignorés (dépendances manquantes)
- **Failed** : Tests qui échouent

### ❌ Tests Échoués
```
FAILED tests/test_whisper_handler.py::TestWhisperHandler::test_init - RuntimeError
```
- Vérifiez les dépendances
- Consultez les logs d'erreur
- Testez avec des modèles plus petits

## 🎁 Tests Avancés

### Test avec un Fichier Vidéo Réel
```bash
# Créer un fichier de test
python -c "
import tempfile
import subprocess
# Créer un fichier vidéo de test
subprocess.run(['ffmpeg', '-f', 'lavfi', '-i', 'testsrc=duration=5:size=320x240:rate=1', 'test_video.mp4'])
"

# Tester avec le fichier
python main.py test_video.mp4 --model tiny --formats srt,vtt
```

### Test de Performance
```bash
# Test avec différents modèles
for model in tiny base small medium large; do
    echo "Testing $model model..."
    time python -c "from src.transcription.whisper_handler import WhisperHandler; WhisperHandler('$model')"
done
```

## 📝 Ajout de Nouveaux Tests

### 1. Créer un nouveau fichier de test
```python
# tests/test_nouveau.py
import pytest

def test_nouvelle_fonctionnalite():
    """Test d'une nouvelle fonctionnalité."""
    assert True  # Votre test ici
```

### 2. Marquer les tests
```python
@pytest.mark.slow  # Test lent
@pytest.mark.unit  # Test unitaire
@pytest.mark.integration  # Test d'intégration
def test_avec_marqueur():
    pass
```

### 3. Exécuter les nouveaux tests
```bash
python -m pytest tests/test_nouveau.py -v
```

## 🚀 Intégration Continue

### GitHub Actions (exemple)
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    - name: Run tests
      run: |
        python -m pytest tests/ --cov=src --cov-report=xml
```

## 📊 Métriques de Qualité

### Couverture de Code
```bash
# Générer un rapport HTML
python -m pytest tests/ --cov=src --cov-report=html
# Ouvrir htmlcov/index.html dans un navigateur
```

### Performance
```bash
# Mesurer le temps d'exécution
python -m pytest tests/ --durations=10
```

## 🎯 Objectifs de Test

- **Couverture** : > 80% du code testé
- **Performance** : Tests rapides < 30 secondes
- **Fiabilité** : Tests stables et reproductibles
- **Maintenabilité** : Tests clairs et documentés

---

**💡 Conseil** : Commencez toujours par les tests basiques (`test_basic.py`) pour vérifier que l'installation fonctionne, puis passez aux tests plus complexes. 