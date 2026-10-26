"""Script para entrenar modelos ML."""
import sys
import argparse
from pathlib import Path
import pandas as pd

# Añadir directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pipeline.ml_pipeline import MLPipeline
from src.data.loaders import CustomerDataLoader
from src.data.cleaners import CustomerDataCleaner
from src.features.builders import CustomerFeatureBuilder
from config.settings import Settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


def load_or_process_data(data_path: Path = None) -> pd.DataFrame:
    """Cargar datos procesados o procesar desde raw."""
    processed_path = Settings.PROCESSED_DATA_DIR / "customers_processed.csv"

    if processed_path.exists():
        logger.info(f"Cargando datos procesados desde: {processed_path}")
        return pd.read_csv(processed_path)
    else:
        logger.info("Procesando datos desde raw...")
        loader = CustomerDataLoader()
        cleaner = CustomerDataCleaner()
        builder = CustomerFeatureBuilder()

        df = loader.load_from_raw()
        df = cleaner.clean(df)
        df = builder.build_all_features(df)

        return df


def main():
    """Punto de entrada principal."""
    parser = argparse.ArgumentParser(description='Entrenar modelos ML')
    parser.add_argument(
        '--skip-regression',
        action='store_true',
        help='Omitir entrenamiento de regresión'
    )
    parser.add_argument(
        '--skip-segmentation',
        action='store_true',
        help='Omitir entrenamiento de segmentación'
    )
    parser.add_argument(
        '--skip-recommender',
        action='store_true',
        help='Omitir entrenamiento de recomendaciones'
    )
    parser.add_argument(
        '--no-save',
        action='store_true',
        help='No guardar modelos'
    )

    args = parser.parse_args()

    try:
        logger.info("=" * 60)
        logger.info("EJECUTANDO SCRIPT RUN_TRAINING.PY")
        logger.info("=" * 60)

        # Cargar datos
        df = load_or_process_data()
        logger.info(f"Datos cargados: {len(df)} registros, {len(df.columns)} features")

        # Crear y ejecutar pipeline ML
        pipeline = MLPipeline(random_state=Settings.RANDOM_STATE)
        results = pipeline.run(
            df=df,
            train_regression=not args.skip_regression,
            train_segmentation=not args.skip_segmentation,
            train_recommender=not args.skip_recommender,
            save_models=not args.no_save
        )

        # Mostrar resultados
        print("\n" + "=" * 60)
        print("RESULTADOS DEL ENTRENAMIENTO")
        print("=" * 60)

        if 'regression' in results:
            reg_metrics = results['regression']['metrics']
            print("\n--- REGRESIÓN ---")
            print(f"R² Score: {reg_metrics['r2']:.4f}")
            print(f"MAE: {reg_metrics['mae']:.2f}")
            print(f"RMSE: {reg_metrics['rmse']:.2f}")

        if 'segmentation' in results:
            seg_metrics = results['segmentation']['metrics']
            print("\n--- SEGMENTACIÓN ---")
            print(f"Número de clusters: {seg_metrics['n_clusters']}")
            print(f"Silhouette Score: {seg_metrics['silhouette']:.4f}")

        if 'recommender' in results:
            rec_info = results['recommender']
            print("\n--- RECOMENDACIONES ---")
            print(f"Clientes en sistema: {rec_info['n_customers']}")
            print(f"Features usadas: {len(rec_info['features_used'])}")

        print("=" * 60)

        # Generar reporte de evaluación
        eval_report = pipeline.get_evaluation_report()
        print("\n" + eval_report)

        logger.info("Entrenamiento completado exitosamente")
        return 0

    except Exception as e:
        logger.error(f"Error en entrenamiento: {str(e)}")
        raise


if __name__ == "__main__":
    sys.exit(main())
