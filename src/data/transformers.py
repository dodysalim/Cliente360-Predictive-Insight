"""Transformadores de datos para feature engineering."""
import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Union
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

from src.utils.logger import get_logger, log_execution
from src.utils.exceptions import DataTransformationError

logger = get_logger(__name__)


class DataTransformer:
    """Transformador base de datos."""

    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.onehot_encoder = None
        self._is_fitted = False

    @log_execution()
    def fit_transform(self, df: pd.DataFrame, numeric_cols: List[str],
                      categorical_cols: List[str]) -> pd.DataFrame:
        """Ajustar y transformar datos.

        Args:
            df: DataFrame de entrada
            numeric_cols: Columnas numéricas a escalar
            categorical_cols: Columnas categóricas a codificar

        Returns:
            DataFrame transformado
        """
        df = df.copy()

        # Transformar numéricas
        if numeric_cols:
            df = self._scale_numeric(df, numeric_cols, fit=True)

        # Transformar categóricas
        if categorical_cols:
            df = self._encode_categorical(df, categorical_cols, fit=True)

        self._is_fitted = True
        return df

    @log_execution()
    def transform(self, df: pd.DataFrame, numeric_cols: List[str],
                  categorical_cols: List[str]) -> pd.DataFrame:
        """Transformar datos usando transformadores ajustados.

        Args:
            df: DataFrame de entrada
            numeric_cols: Columnas numéricas
            categorical_cols: Columnas categóricas

        Returns:
            DataFrame transformado
        """
        if not self._is_fitted:
            raise DataTransformationError(
                "El transformador no ha sido ajustado. Llame fit_transform primero."
            )

        df = df.copy()

        if numeric_cols:
            df = self._scale_numeric(df, numeric_cols, fit=False)

        if categorical_cols:
            df = self._encode_categorical(df, categorical_cols, fit=False)

        return df

    def _scale_numeric(self, df: pd.DataFrame, columns: List[str], fit: bool = False) -> pd.DataFrame:
        """Escalar columnas numéricas."""
        df = df.copy()

        existing_cols = [col for col in columns if col in df.columns]
        if not existing_cols:
            return df

        if fit:
            df[existing_cols] = self.scaler.fit_transform(df[existing_cols])
            logger.info(f"Scaler ajustado con columnas: {existing_cols}")
        else:
            df[existing_cols] = self.scaler.transform(df[existing_cols])

        return df

    def _encode_categorical(self, df: pd.DataFrame, columns: List[str], fit: bool = False) -> pd.DataFrame:
        """Codificar columnas categóricas con One-Hot Encoding."""
        df = df.copy()

        for col in columns:
            if col not in df.columns:
                continue

            if fit:
                encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
                encoded = encoder.fit_transform(df[[col]])
                self.label_encoders[col] = encoder

                # Crear nombres de columnas
                categories = encoder.categories_[0]
                new_cols = [f"{col}_{cat}" for cat in categories]

                encoded_df = pd.DataFrame(encoded, columns=new_cols, index=df.index)
                df = pd.concat([df.drop(columns=[col]), encoded_df], axis=1)

                logger.info(f"Columna {col} codificada en {len(new_cols)} columnas")

            else:
                encoder = self.label_encoders.get(col)
                if encoder:
                    encoded = encoder.transform(df[[col]])
                    categories = encoder.categories_[0]
                    new_cols = [f"{col}_{cat}" for cat in categories]
                    encoded_df = pd.DataFrame(encoded, columns=new_cols, index=df.index)
                    df = pd.concat([df.drop(columns=[col]), encoded_df], axis=1)

        return df

    def save(self, filepath: str):
        """Guardar transformador."""
        joblib.dump({
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'is_fitted': self._is_fitted
        }, filepath)
        logger.info(f"Transformador guardado en {filepath}")

    def load(self, filepath: str):
        """Cargar transformador."""
        data = joblib.load(filepath)
        self.scaler = data['scaler']
        self.label_encoders = data['label_encoders']
        self._is_fitted = data['is_fitted']
        logger.info(f"Transformador cargado desde {filepath}")


class FeatureTransformer:
    """Transformador de características especializado para el proyecto."""

    def __init__(self):
        self.logger = get_logger(__name__)

    @log_execution()
    def create_customer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Crear features específicas para análisis de clientes.

        Args:
            df: DataFrame limpio de clientes

        Returns:
            DataFrame con features adicionales
        """
        df = df.copy()

        # 1. Features demográficas
        if 'edad' in df.columns:
            df['es_joven'] = (df['edad'] <= 30).astype(int)
            df['es_adulto_mayor'] = (df['edad'] >= 65).astype(int)

        # 2. Features económicas
        if 'ingresos_mensuales' in df.columns:
            df['ingresos_anuales'] = df['ingresos_mensuales'] * 12
            df['ingreso_diario'] = df['ingresos_mensuales'] / 30

        if all(col in df.columns for col in ['promedio_gasto_comida', 'ingresos_mensuales']):
            df['proporcion_gasto_ingreso'] = np.where(
                df['ingresos_mensuales'] > 0,
                df['promedio_gasto_comida'] / df['ingresos_mensuales'],
                0
            )

        # 3. Features de comportamiento
        if all(col in df.columns for col in ['frecuencia_visita', 'ocio']):
            df['frecuencia_por_ocio'] = df.apply(
                lambda x: x['frecuencia_visita'] * 1.5 if x['ocio'] == 'Sí' else x['frecuencia_visita'],
                axis=1
            )

        # 4. Segmentación socioeconómica
        if all(col in df.columns for col in ['estrato_socioeconomico', 'ingresos_mensuales']):
            estrato_map = {'Bajo': 1, 'Medio': 2, 'Alto': 3, 'Muy Alto': 4}
            df['estrato_numerico'] = df['estrato_socioeconomico'].map(estrato_map).fillna(2)

        # 5. Preferencias alimenticias codificadas
        if 'preferencias_alimenticias' in df.columns:
            pref_dummies = pd.get_dummies(df['preferencias_alimenticias'], prefix='pref')
            df = pd.concat([df, pref_dummies], axis=1)

        # 6. Features de membresía
        if 'membresia_premium' in df.columns:
            df['es_premium'] = (df['membresia_premium'] == 'Sí').astype(int)

        # 7. Features de pago
        if 'tipo_de_pago_mas_usado' in df.columns:
            pago_map = {'Efectivo': 0, 'Tarjeta': 1, 'App': 2}
            df['tipo_pago_cod'] = df['tipo_de_pago_mas_usado'].map(pago_map).fillna(0)

        self.logger.info(f"Features creadas. Total columnas: {len(df.columns)}")
        return df

    @log_execution()
    def create_yelp_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Crear features para datos de Yelp.

        Args:
            df: DataFrame de Yelp

        Returns:
            DataFrame con features adicionales
        """
        df = df.copy()

        # Score de popularidad ponderado
        if all(col in df.columns for col in ['rating', 'review_count']):
            df['weighted_score'] = df['rating'] * np.log1p(df['review_count'])

        # Densidad de reviews
        if 'review_count' in df.columns:
            df['review_density'] = pd.cut(
                df['review_count'],
                bins=[0, 50, 200, 1000, float('inf')],
                labels=[1, 2, 3, 4]
            ).astype(int)

        # Categoría de negocio normalizada
        if 'title' in df.columns:
            df['title_normalized'] = df['title'].str.lower().str.replace(' ', '_')

        return df

    @log_execution()
    def create_combined_features(self, df_customers: pd.DataFrame,
                                  df_yelp: pd.DataFrame) -> pd.DataFrame:
        """Crear features combinando datos de clientes y Yelp.

        Args:
            df_customers: DataFrame de clientes
            df_yelp: DataFrame de Yelp

        Returns:
            DataFrame combinado con features
        """
        # Agrupar datos de Yelp por ciudad
        yelp_by_city = df_yelp.groupby('city').agg({
            'rating': 'mean',
            'review_count': 'mean',
            'weighted_score': 'mean',
            'id': 'count'
        }).rename(columns={'id': 'num_restaurants'})

        # Merge con datos de clientes
        df_combined = df_customers.copy()
        df_combined['ciudad_upper'] = df_combined['ciudad_residencia'].str.upper()

        # Mapeo de oferta de restaurantes
        city_mapping = {
            'MIAMI': 'Miami',
            'NYC': 'New York',
            'NEW YORK': 'New York',
            'BOSTON': 'Boston',
            'CHICAGO': 'Chicago',
            'DENVER': 'Denver',
            'SEATTLE': 'Seattle',
            'DALLAS': 'Dallas',
            'HOUSTON': 'Houston',
            'SAN DIEGO': 'San Diego'
        }

        df_combined['ciudad_mapeada'] = df_combined['ciudad_upper'].map(city_mapping).fillna(df_combined['ciudad_residencia'])

        # Unir con datos de Yelp
        df_combined = df_combined.merge(
            yelp_by_city,
            left_on='ciudad_mapeada',
            right_on='city',
            how='left'
        )

        # Crear indicador de mercado
        df_combined['oferta_vs_demanda'] = np.where(
            df_combined['num_restaurants'].notna(),
            df_combined['num_restaurants'] / df_combined.groupby('ciudad_residencia')['id_persona'].transform('count'),
            0
        )

        return df_combined

    @log_execution()
    def prepare_for_modeling(self, df: pd.DataFrame, target_col: str = 'promedio_gasto_comida',
                           exclude_cols: Optional[List[str]] = None) -> tuple:
        """Preparar datos para modelado ML.

        Args:
            df: DataFrame con todas las features
            target_col: Columna objetivo
            exclude_cols: Columnas a excluir

        Returns:
            Tuple (X, y) listos para modelado
        """
        exclude_cols = exclude_cols or []

        # Identificar columnas no numéricas
        non_numeric = df.select_dtypes(exclude=[np.number]).columns.tolist()
        exclude_cols.extend(non_numeric)

        # Remover target de exclude si está
        if target_col in exclude_cols:
            exclude_cols.remove(target_col)

        # Separar X e y
        feature_cols = [col for col in df.columns
                       if col not in exclude_cols + [target_col, 'id_persona']]

        X = df[feature_cols].fillna(0)
        y = df[target_col] if target_col in df.columns else None

        self.logger.info(f"Datos preparados: X shape {X.shape}, features: {len(feature_cols)}")

        return X, y, feature_cols
