"""Pipeline ETL para procesamiento de datos."""
from typing import Optional, Dict, Any
from pathlib import Path
import pandas as pd

from config.settings import Settings
from src.data.loaders import CustomerDataLoader, YelpDataLoader
from src.data.cleaners import CustomerDataCleaner, YelpDataCleaner
from src.data.transformers import FeatureTransformer
from src.features.builders import CustomerFeatureBuilder
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ETLPipeline:
    """Pipeline completo de Extracción, Transformación y Carga."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = get_logger(__name__)

        # Componentes
        self.customer_loader = CustomerDataLoader()
        self.yelp_loader = YelpDataLoader()
        self.customer_cleaner = CustomerDataCleaner()
        self.yelp_cleaner = YelpDataCleaner()
        self.feature_builder = CustomerFeatureBuilder()
        self.transformer = FeatureTransformer()

        # Estado
        self.raw_customers = None
        self.raw_yelp = None
        self.clean_customers = None
        self.clean_yelp = None
        self.final_data = None

    def run(self, save_intermediate: bool = True) -> pd.DataFrame:
        """Ejecutar pipeline ETL completo.

        Args:
            save_intermediate: Guardar archivos intermedios

        Returns:
            DataFrame final procesado
        """
        self.logger.info("=" * 60)
        self.logger.info("INICIANDO PIPELINE ETL")
        self.logger.info("=" * 60)

        try:
            # 1. Extracción
            self._extract()

            # 2. Transformación (Limpieza)
            self._transform()

            # 3. Feature Engineering
            self._build_features()

            # 4. Carga (Guardar resultados)
            if save_intermediate:
                self._load()

            self.logger.info("=" * 60)
            self.logger.info("PIPELINE ETL COMPLETADO EXITOSAMENTE")
            self.logger.info("=" * 60)

            return self.final_data

        except Exception as e:
            self.logger.error(f"Error en pipeline ETL: {str(e)}")
            raise

    def _extract(self):
        """Extracción de datos."""
        self.logger.info("ETL - Fase 1: EXTRACCIÓN")

        # Cargar datos de clientes
        self.raw_customers = self.customer_loader.load_from_raw()
        self.logger.info(f"Clientes extraídos: {len(self.raw_customers)} registros")

        # Cargar datos de Yelp
        try:
            self.raw_yelp = self.yelp_loader.load_from_external()
            self.logger.info(f"Yelp extraído: {len(self.raw_yelp)} registros")
        except Exception as e:
            self.logger.warning(f"No se pudieron cargar datos de Yelp: {e}")
            self.raw_yelp = None

    def _transform(self):
        """Transformación y limpieza."""
        self.logger.info("ETL - Fase 2: TRANSFORMACIÓN")

        # Limpiar clientes
        self.clean_customers = self.customer_cleaner.clean(self.raw_customers)
        self.logger.info(f"Clientes limpios: {len(self.clean_customers)} registros")

        # Limpiar Yelp
        if self.raw_yelp is not None:
            self.clean_yelp = self.yelp_cleaner.clean(self.raw_yelp)
            self.logger.info(f"Yelp limpio: {len(self.clean_yelp)} registros")

    def _build_features(self):
        """Feature Engineering."""
        self.logger.info("ETL - Fase 3: FEATURE ENGINEERING")

        # Crear features para clientes
        self.final_data = self.feature_builder.build_all_features(self.clean_customers)
        self.logger.info(f"Features creadas: {len(self.final_data.columns)} columnas totales")

    def _load(self):
        """Carga/G保存 de datos procesados."""
        self.logger.info("ETL - Fase 4: CARGA")

        # Guardar datos procesados
        output_path = Settings.PROCESSED_DATA_DIR / "customers_processed.csv"
        self.final_data.to_csv(output_path, index=False)
        self.logger.info(f"Datos guardados en: {output_path}")

        # Guardar log de limpieza
        cleaning_log = {
            'customer_log': self.customer_cleaner.get_cleaning_log(),
            'yelp_log': self.yelp_cleaner.get_cleaning_log() if self.clean_yelp is not None else []
        }

        import json
        log_path = Settings.PROCESSED_DATA_DIR / "cleaning_log.json"
        with open(log_path, 'w') as f:
            json.dump(cleaning_log, f, indent=2, default=str)

    def get_report(self) -> Dict[str, Any]:
        """Generar reporte del pipeline."""
        report = {
            'raw_customers': len(self.raw_customers) if self.raw_customers is not None else 0,
            'clean_customers': len(self.clean_customers) if self.clean_customers is not None else 0,
            'raw_yelp': len(self.raw_yelp) if self.raw_yelp is not None else 0,
            'clean_yelp': len(self.clean_yelp) if self.clean_yelp is not None else 0,
            'final_features': len(self.final_data.columns) if self.final_data is not None else 0,
            'final_rows': len(self.final_data) if self.final_data is not None else 0,
            'cleaning_log': self.customer_cleaner.get_cleaning_log()
        }
        return report
