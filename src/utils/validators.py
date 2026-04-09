"""Validadores de datos."""
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from .exceptions import DataValidationError
from .logger import get_logger

logger = get_logger(__name__)


class DataValidator:
    """Validador de calidad de datos."""

    def __init__(self, required_columns: Optional[List[str]] = None):
        """Inicializar validador.

        Args:
            required_columns: Columnas requeridas en el dataset
        """
        self.required_columns = required_columns or []
        self.validation_errors = []

    def validate_columns(self, df: pd.DataFrame) -> bool:
        """Validar que existan todas las columnas requeridas.

        Args:
            df: DataFrame a validar

        Returns:
            True si todas las columnas existen

        Raises:
            DataValidationError: Si faltan columnas
        """
        missing = [col for col in self.required_columns if col not in df.columns]

        if missing:
            error_msg = f"Columnas faltantes: {missing}"
            logger.error(error_msg)
            raise DataValidationError(error_msg, validation_errors=missing)

        logger.debug(f"Validación de columnas exitosa: {len(self.required_columns)} columnas")
        return True

    def validate_types(self, df: pd.DataFrame, expected_types: Dict[str, type]) -> bool:
        """Validar tipos de datos.

        Args:
            df: DataFrame a validar
            expected_types: Diccionario {columna: tipo_esperado}

        Returns:
            True si los tipos son correctos
        """
        type_errors = []

        for column, expected_type in expected_types.items():
            if column in df.columns:
                actual_type = df[column].dtype
                if not np.issubdtype(actual_type, expected_type):
                    type_errors.append({
                        'column': column,
                        'expected': expected_type.__name__,
                        'actual': str(actual_type)
                    })

        if type_errors:
            error_msg = f"Tipos incorrectos: {type_errors}"
            logger.error(error_msg)
            raise DataValidationError(error_msg, validation_errors=type_errors)

        return True

    def validate_nulls(self, df: pd.DataFrame, max_null_ratio: float = 0.3) -> Dict[str, float]:
        """Validar porcentaje de valores nulos.

        Args:
            df: DataFrame a validar
            max_null_ratio: Ratio máximo permitido de nulos

        Returns:
            Diccionario con columnas que exceden el umbral
        """
        null_ratios = df.isnull().mean()
        high_null_cols = null_ratios[null_ratios > max_null_ratio].to_dict()

        if high_null_cols:
            logger.warning(f"Columnas con alto porcentaje de nulos (>{max_null_ratio*100}%): {high_null_cols}")

        return high_null_cols

    def validate_duplicates(self, df: pd.DataFrame, subset: Optional[List[str]] = None) -> int:
        """Validar y reportar duplicados.

        Args:
            df: DataFrame a validar
            subset: Columnas para identificar duplicados

        Returns:
            Número de duplicados encontrados
        """
        duplicates = df.duplicated(subset=subset).sum()

        if duplicates > 0:
            logger.warning(f"Se encontraron {duplicates} registros duplicados")
        else:
            logger.debug("No se encontraron duplicados")

        return duplicates

    def validate_range(self, df: pd.DataFrame, column: str, min_val: Any, max_val: Any) -> bool:
        """Validar que valores estén dentro de un rango.

        Args:
            df: DataFrame a validar
            column: Nombre de la columna
            min_val: Valor mínimo permitido
            max_val: Valor máximo permitido

        Returns:
            True si todos los valores están en rango
        """
        if column not in df.columns:
            logger.warning(f"Columna {column} no existe para validación de rango")
            return False

        out_of_range = df[(df[column] < min_val) | (df[column] > max_val)]

        if len(out_of_range) > 0:
            logger.warning(
                f"{len(out_of_range)} valores fuera de rango en {column} "
                f"(esperado: {min_val}-{max_val})"
            )
            return False

        return True

    def validate_categories(self, df: pd.DataFrame, column: str, allowed_values: List[str]) -> bool:
        """Validar valores categóricos permitidos.

        Args:
            df: DataFrame a validar
            column: Nombre de la columna
            allowed_values: Lista de valores permitidos

        Returns:
            True si todos los valores están permitidos
        """
        if column not in df.columns:
            return False

        invalid = df[~df[column].isin(allowed_values)][column].unique()

        if len(invalid) > 0:
            logger.warning(f"Valores inválidos en {column}: {invalid}")
            return False

        return True

    def get_quality_report(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generar reporte completo de calidad de datos.

        Args:
            df: DataFrame a analizar

        Returns:
            Diccionario con métricas de calidad
        """
        report = {
            'shape': df.shape,
            'total_cells': df.size,
            'missing_values': df.isnull().sum().sum(),
            'missing_percentage': (df.isnull().sum().sum() / df.size) * 100,
            'duplicates': df.duplicated().sum(),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
            'columns': {}
        }

        for col in df.columns:
            report['columns'][col] = {
                'dtype': str(df[col].dtype),
                'missing': int(df[col].isnull().sum()),
                'unique': int(df[col].nunique()),
            }

            if pd.api.types.is_numeric_dtype(df[col]):
                report['columns'][col]['min'] = float(df[col].min()) if not pd.isna(df[col].min()) else None
                report['columns'][col]['max'] = float(df[col].max()) if not pd.isna(df[col].max()) else None
                report['columns'][col]['mean'] = float(df[col].mean()) if not pd.isna(df[col].mean()) else None

        logger.info(f"Reporte de calidad generado: {report['shape'][0]} filas, {report['shape'][1]} columnas")
        return report
