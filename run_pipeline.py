import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os
from pathlib import Path
import time
import sys

PROJECT_ROOT = Path(__file__).parent.resolve()
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)

def run_notebook(nb_name):
    nb_path = NOTEBOOKS_DIR / nb_name
    print(f"\n--- Ejecutando: {nb_name}")
    start_time = time.time()
    
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
        
    ep = ExecutePreprocessor(timeout=1200, kernel_name='python3')
    
    try:
        ep.preprocess(nb, {'metadata': {'path': str(PROJECT_ROOT)}})
        with open(nb_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        elapsed = time.time() - start_time
        print(f"EXITO: {nb_name} ({elapsed:.1f}s)")
        return True
    except Exception as e:
        # LOG PRIMERO
        error_msg = str(e)
        with open(LOGS_DIR / "pipeline_error_final.log", "a", encoding="utf-8") as f:
            f.write(f"\nError en {nb_name} a las {time.ctime()}:\n{error_msg}\n")
        
        # PRINT DESPUES (SEGURO)
        print(f"ERROR en {nb_name}. Revisa pipeline_error_final.log")
        return False

def main():
    notebooks = ["01_exploratory_data_analysis.ipynb", "02_api_integration.ipynb", "03_feature_engineering.ipynb", "04_modeling.ipynb", "05_insights_and_recommendations.ipynb"]
    print("INICIANDO ANALISIS")
    for nb in notebooks:
        if not run_notebook(nb):
            sys.exit(1)
    print("COMPLETO")

if __name__ == "__main__":
    main()
