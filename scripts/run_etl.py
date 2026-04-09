"""Script para ejecutar pipeline ETL."""
import sys
import argparse
from pathlib import Path

# Añadir directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pipeline.etl_pipeline import ETLPipeline
from src.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """Punto de entrada principal."""
    parser = argparse.ArgumentParser(description='Ejecutar pipeline ETL')
    parser.add_argument(
        '--no-save',
        action='store_true',
        help='No guardar archivos intermedios'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Modo verbose'
    )

    args = parser.parse_args()

    try:
        logger.info("=" * 60)
        logger.info("EJECUTANDO SCRIPT RUN_ETL.PY")
        logger.info("=" * 60)

        # Crear y ejecutar pipeline
        pipeline = ETLPipeline()
        final_data = pipeline.run(save_intermediate=not args.no_save)

        # Mostrar reporte
        report = pipeline.get_report()

        print("\n" + "=" * 60)
        print("REPORTE ETL")
        print("=" * 60)
        print(f"Clientes crudos: {report['raw_customers']}")
        print(f"Clientes limpios: {report['clean_customers']}")
        print(f"Yelp crudos: {report['raw_yelp']}")
        print(f"Yelp limpios: {report['clean_yelp']}")
        print(f"Features finales: {report['final_features']}")
        print(f"Registros finales: {report['final_rows']}")
        print("=" * 60)

        logger.info("ETL completado exitosamente")
        return 0

    except Exception as e:
        logger.error(f"Error ejecutando ETL: {str(e)}")
        raise


if __name__ == "__main__":
    sys.exit(main())
