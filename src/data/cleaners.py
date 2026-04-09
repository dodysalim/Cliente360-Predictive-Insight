"""Limpiadores de datos con principios SOLID."""
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import Optional, Dict, List, Any
import re

from src.utils.exceptions import DataTransformationError
from src.utils.logger import get_logger, log_execution

logger = get_logger(__name__)


class DataCleaner(ABC):
    """Clase base abstracta para limpieza de datos."""

    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self._cleaning_log = []

    @abstractmethod
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Método abstracto de limpieza."""
        pass

    def _log_operation(self, operation: str, details: Dict[str, Any]):
        """Registrar operación de limpieza."""
        self._cleaning_log.append({'operation': operation, 'details': details})
        self.logger.info(f"{operation}: {details}")

    def get_cleaning_log(self) -> List[Dict]:
        """Obtener log de operaciones de limpieza."""
        return self._cleaning_log.copy()


class CustomerDataCleaner(DataCleaner):
    """Limpiador especializado para datos de clientes."""

    def __init__(self):
        super().__init__()
        self.numeric_columns = ['edad', 'frecuencia_visita', 'promedio_gasto_comida', 'ingresos_mensuales']
        self.categorical_columns = ['genero', 'ciudad_residencia', 'estrato_socioeconomico',
                                     'ocio', 'consume_licor', 'preferencias_alimenticias',
                                     'membresia_premium', 'tipo_de_pago_mas_usado']

    @log_execution()
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Pipeline completo de limpieza de datos de clientes.

        Args:
            df: DataFrame con datos crudos

        Returns:
            DataFrame limpio
        """
        self.logger.info(f"Iniciando limpieza de {len(df)} registros de clientes")

        df_clean = df.copy()

        # Aplicar pasos de limpieza
        df_clean = self._standardize_column_names(df_clean)
        df_clean = self._clean_numeric_columns(df_clean)
        df_clean = self._clean_categorical_columns(df_clean)
        df_clean = self._handle_missing_values(df_clean)
        df_clean = self._remove_duplicates(df_clean)
        df_clean = self._handle_outliers(df_clean)
        df_clean = self._create_derived_features(df_clean)

        self.logger.info(f"Limpieza completada: {len(df_clean)} registros finales")
        return df_clean

    def _standardize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Estandarizar nombres de columnas."""
        df = df.copy()
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        self._log_operation("standardize_columns", {"columns": list(df.columns)})
        return df

    def _clean_numeric_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpiar columnas numéricas."""
        df = df.copy()

        for col in self.numeric_columns:
            if col in df.columns:
                # Convertir a numérico
                df[col] = pd.to_numeric(df[col], errors='coerce')

                # Limpiar edad (valores extremos como 300)
                if col == 'edad':
                    invalid_age = df[col] > 120
                    count = invalid_age.sum()
                    if count > 0:
                        df.loc[invalid_age, col] = np.nan
                        self._log_operation("clean_age", {"invalid_values": int(count)})

                # Limpiar ingresos (valores negativos)
                if col in ['ingresos_mensuales', 'promedio_gasto_comida']:
                    negative = df[col] < 0
                    if negative.sum() > 0:
                        df.loc[negative, col] = np.nan
                        self._log_operation(f"clean_{col}", {"negative_values": int(negative.sum())})

        return df

    def _clean_categorical_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpiar columnas categóricas."""
        df = df.copy()

        # Mapear valores inconsistentes
        mappings = {
            'genero': {
                'M': 'Masculino',
                'F': 'Femenino',
                'm': 'Masculino',
                'f': 'Femenino'
            },
            'ocio': {
                'Si': 'Sí',
                'si': 'Sí',
                'No': 'No',
                'no': 'No'
            },
            'consume_licor': {
                'Si': 'Sí',
                'si': 'Sí',
                'No': 'No',
                'no': 'No'
            },
            'membresia_premium': {
                'Si': 'Sí',
                'si': 'Sí',
                'No': 'No',
                'no': 'No'
            }
        }

        for col, mapping in mappings.items():
            if col in df.columns:
                df[col] = df[col].replace(mapping)

        # Limpiar texto
        for col in ['nombre', 'apellido', 'ciudad_residencia']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.title()

        return df

    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Manejar valores faltantes."""
        df = df.copy()
        missing_before = df.isnull().sum().sum()

        # Edad: imputar con mediana
        if 'edad' in df.columns:
            median_age = df['edad'].median()
            df['edad'].fillna(median_age, inplace=True)

        # Categóricas: imputar con 'Desconocido'
        for col in self.categorical_columns:
            if col in df.columns:
                df[col] = df[col].fillna('Desconocido')

        # Numéricas: imputar con 0 o mediana según el caso
        for col in ['frecuencia_visita', 'promedio_gasto_comida']:
            if col in df.columns:
                df[col].fillna(0, inplace=True)

        # Correos y teléfonos: permitir nulos
        if 'correo_electronico' in df.columns:
            df['correo_electronico'] = df['correo_electronico'].replace('', np.nan)

        missing_after = df.isnull().sum().sum()
        self._log_operation("handle_missing", {
            "missing_before": int(missing_before),
            "missing_after": int(missing_after)
        })

        return df

    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Eliminar duplicados basados en ID."""
        df = df.copy()

        if 'id_persona' in df.columns:
            duplicates = df.duplicated(subset=['id_persona']).sum()
            df = df.drop_duplicates(subset=['id_persona'], keep='first')

            if duplicates > 0:
                self._log_operation("remove_duplicates", {"removed": int(duplicates)})

        return df

    def _handle_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Manejar outliers usando IQR."""
        df = df.copy()

        for col in self.numeric_columns:
            if col in df.columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()

                # Solo cap en extremos, no eliminar
                df[col] = df[col].clip(lower=0, upper=upper_bound * 2)

                if outliers > 0:
                    self._log_operation("cap_outliers", {"column": col, "outliers": int(outliers)})

        return df

    def _create_derived_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Crear características derivadas."""
        df = df.copy()

        # Grupos de edad
        if 'edad' in df.columns:
            df['grupo_edad'] = pd.cut(
                df['edad'],
                bins=[0, 25, 35, 50, 65, 150],
                labels=['18-25', '26-35', '36-50', '51-65', '65+']
            )

        # Categorización de ingresos
        if 'ingresos_mensuales' in df.columns:
            df['categoria_ingresos'] = pd.cut(
                df['ingresos_mensuales'],
                bins=[0, 2000, 5000, 10000, float('inf')],
                labels=['Bajo', 'Medio', 'Alto', 'Muy Alto']
            )

        # Gasto por visita (si aplica)
        if all(col in df.columns for col in ['promedio_gasto_comida', 'frecuencia_visita']):
            df['gasto_por_visita'] = np.where(
                df['frecuencia_visita'] > 0,
                df['promedio_gasto_comida'] / df['frecuencia_visita'],
                0
            )

        self._log_operation("create_features", {"new_columns": ['grupo_edad', 'categoria_ingresos', 'gasto_por_visita']})

        return df


class YelpDataCleaner(DataCleaner):
    """Limpiador especializado para datos de Yelp."""

    def __init__(self):
        super().__init__()

    @log_execution()
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Pipeline de limpieza para datos de Yelp."""
        self.logger.info(f"Iniciando limpieza de {len(df)} registros de Yelp")

        df_clean = df.copy()

        df_clean = self._clean_price(df_clean)
        df_clean = self._clean_ratings(df_clean)
        df_clean = self._clean_coordinates(df_clean)
        df_clean = self._remove_duplicates(df_clean)
        df_clean = self._create_features(df_clean)

        self.logger.info(f"Limpieza de Yelp completada: {len(df_clean)} registros")
        return df_clean

    def _clean_price(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpiar columna de precio."""
        df = df.copy()

        if 'price' in df.columns:
            # Mapear precios
            price_map = {
                '$': 'Bajo',
                '$$': 'Medio',
                '$$$': 'Alto',
                '$$$$': 'Muy Alto',
                'No especificado': 'No especificado'
            }
            df['price_category'] = df['price'].map(price_map).fillna('No especificado')

            self._log_operation("clean_price", {"categories": df['price_category'].value_counts().to_dict()})

        return df

    def _clean_ratings(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpiar ratings."""
        df = df.copy()

        if 'rating' in df.columns:
            df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
            df['rating'] = df['rating'].clip(1, 5)

        if 'review_count' in df.columns:
            df['review_count'] = pd.to_numeric(df['review_count'], errors='coerce').fillna(0)

        return df

    def _clean_coordinates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpiar coordenadas geográficas."""
        df = df.copy()

        for col in ['coordinates_latitude', 'coordinates_longitude']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Eliminar registros sin coordenadas válidas
        if 'coordinates_latitude' in df.columns and 'coordinates_longitude' in df.columns:
            invalid_coords = df['coordinates_latitude'].isna() | df['coordinates_longitude'].isna()
            if invalid_coords.sum() > 0:
                self._log_operation("remove_invalid_coords", {"removed": int(invalid_coords.sum())})
                df = df[~invalid_coords]

        return df

    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Eliminar duplicados por business ID."""
        df = df.copy()

        if 'id' in df.columns:
            duplicates = df.duplicated(subset=['id']).sum()
            df = df.drop_duplicates(subset=['id'], keep='first')

            if duplicates > 0:
                self._log_operation("remove_yelp_duplicates", {"removed": int(duplicates)})

        return df

    def _create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Crear características derivadas."""
        df = df.copy()

        # Categoría de popularidad
        if 'review_count' in df.columns:
            df['popularidad'] = pd.cut(
                df['review_count'],
                bins=[0, 50, 200, 1000, float('inf')],
                labels=['Baja', 'Media', 'Alta', 'Muy Alta']
            )

        # Categoría de calidad
        if 'rating' in df.columns:
            df['calidad'] = pd.cut(
                df['rating'],
                bins=[0, 3.0, 4.0, 4.5, 5.0],
                labels=['Regular', 'Buena', 'Muy Buena', 'Excelente']
            )

        return df
