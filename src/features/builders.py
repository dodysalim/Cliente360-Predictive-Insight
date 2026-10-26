"""Constructores de features."""
from typing import List, Dict, Optional
import pandas as pd
import numpy as np

from src.utils.logger import get_logger

logger = get_logger(__name__)


class CustomerFeatureBuilder:
    """Constructor de features para datos de clientes."""

    def __init__(self):
        self.logger = get_logger(__name__)
        self._features_created = []

    def build_all_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Crear todas las features para clientes.

        Args:
            df: DataFrame limpio de clientes

        Returns:
            DataFrame con features adicionales
        """
        df = df.copy()

        # Features demográficas
        df = self._build_demographic_features(df)

        # Features económicas
        df = self._build_economic_features(df)

        # Features de comportamiento
        df = self._build_behavioral_features(df)

        # Features de preferencias
        df = self._build_preference_features(df)

        # Features de engagement
        df = self._build_engagement_features(df)

        self.logger.info(f"Features creadas: {len(self._features_created)}")
        return df

    def _build_demographic_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Features demográficas."""
        df = df.copy()

        if 'edad' in df.columns:
            # Grupos de edad
            df['edad_grupo'] = pd.cut(
                df['edad'],
                bins=[0, 25, 35, 50, 65, 150],
                labels=['18-25', '26-35', '36-50', '51-65', '65+']
            )

            # Indicadores
            df['es_joven'] = (df['edad'] <= 30).astype(int)
            df['es_adulto'] = ((df['edad'] > 30) & (df['edad'] < 65)).astype(int)
            df['es_adulto_mayor'] = (df['edad'] >= 65).astype(int)

            # Edad al cuadrado (para relaciones no lineales)
            df['edad_squared'] = df['edad'] ** 2

            self._features_created.extend(['edad_grupo', 'es_joven', 'es_adulto', 'es_adulto_mayor', 'edad_squared'])

        if 'genero' in df.columns:
            df['es_masculino'] = (df['genero'] == 'Masculino').astype(int)
            df['es_femenino'] = (df['genero'] == 'Femenino').astype(int)
            self._features_created.extend(['es_masculino', 'es_femenino'])

        return df

    def _build_economic_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Features económicas."""
        df = df.copy()

        if 'ingresos_mensuales' in df.columns:
            # Ingresos anuales
            df['ingresos_anuales'] = df['ingresos_mensuales'] * 12

            # Ingreso diario
            df['ingreso_diario'] = df['ingresos_mensuales'] / 30

            # Categorías de ingreso
            df['categoria_ingreso'] = pd.cut(
                df['ingresos_mensuales'],
                bins=[0, 2000, 5000, 10000, float('inf')],
                labels=['Bajo', 'Medio', 'Alto', 'Muy Alto']
            )

            # Log de ingresos (para distribuciones sesgadas)
            df['log_ingresos'] = np.log1p(df['ingresos_mensuales'])

            self._features_created.extend(['ingresos_anuales', 'ingreso_diario', 'categoria_ingreso', 'log_ingresos'])

        # Estrato socioeconómico numérico
        if 'estrato_socioeconomico' in df.columns:
            estrato_map = {'Bajo': 1, 'Medio': 2, 'Alto': 3, 'Muy Alto': 4}
            df['estrato_num'] = df['estrato_socioeconomico'].map(estrato_map).fillna(2)
            self._features_created.append('estrato_num')

        # Relación gasto-ingreso
        if all(col in df.columns for col in ['promedio_gasto_comida', 'ingresos_mensuales']):
            df['proporcion_gasto_ingreso'] = np.where(
                df['ingresos_mensuales'] > 0,
                df['promedio_gasto_comida'] / df['ingresos_mensuales'],
                0
            )
            df['proporcion_gasto_ingreso'] = df['proporcion_gasto_ingreso'].clip(0, 1)
            self._features_created.append('proporcion_gasto_ingreso')

        return df

    def _build_behavioral_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Features de comportamiento."""
        df = df.copy()

        if 'frecuencia_visita' in df.columns:
            # Categorías de frecuencia
            df['frecuencia_categoria'] = pd.cut(
                df['frecuencia_visita'],
                bins=[-1, 0, 2, 5, 10, float('inf')],
                labels=['No visita', 'Baja', 'Media', 'Alta', 'Muy Alta']
            )

            # Indicadores
            df['visitante_frecuente'] = (df['frecuencia_visita'] >= 5).astype(int)
            df['no_visitante'] = (df['frecuencia_visita'] == 0).astype(int)

            self._features_created.extend(['frecuencia_categoria', 'visitante_frecuente', 'no_visitante'])

        # Gasto por visita
        if all(col in df.columns for col in ['promedio_gasto_comida', 'frecuencia_visita']):
            df['gasto_por_visita'] = np.where(
                df['frecuencia_visita'] > 0,
                df['promedio_gasto_comida'] / df['frecuencia_visita'],
                0
            )
            self._features_created.append('gasto_por_visita')

        # Interacción frecuencia-ocio
        if all(col in df.columns for col in ['frecuencia_visita', 'ocio']):
            df['frecuencia_ajustada_ocio'] = df.apply(
                lambda x: x['frecuencia_visita'] * 1.3 if x['ocio'] == 'Sí' else x['frecuencia_visita'],
                axis=1
            )
            self._features_created.append('frecuencia_ajustada_ocio')

        # Consumo de licor
        if 'consume_licor' in df.columns:
            df['consume_licor_bin'] = (df['consume_licor'] == 'Sí').astype(int)
            self._features_created.append('consume_licor_bin')

        return df

    def _build_preference_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Features de preferencias alimenticias."""
        df = df.copy()

        if 'preferencias_alimenticias' in df.columns:
            # One-hot encoding para preferencias
            pref_dummies = pd.get_dummies(df['preferencias_alimenticias'], prefix='pref')
            df = pd.concat([df, pref_dummies], axis=1)

            # Indicadores específicos
            df['es_vegetariano'] = (df['preferencias_alimenticias'] == 'Vegetariano').astype(int)
            df['es_vegano'] = (df['preferencias_alimenticias'] == 'Vegano').astype(int)
            df['prefiere_mariscos'] = (df['preferencias_alimenticias'] == 'Mariscos').astype(int)

            self._features_created.extend(list(pref_dummies.columns) + ['es_vegetariano', 'es_vegano', 'prefiere_mariscos'])

        return df

    def _build_engagement_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Features de engagement/membresía."""
        df = df.copy()

        if 'membresia_premium' in df.columns:
            df['es_premium'] = (df['membresia_premium'] == 'Sí').astype(int)
            self._features_created.append('es_premium')

        if 'tipo_de_pago_mas_usado' in df.columns:
            pago_map = {'Efectivo': 0, 'Tarjeta': 1, 'App': 2}
            df['tipo_pago_num'] = df['tipo_de_pago_mas_usado'].map(pago_map).fillna(0)

            # One-hot para tipos de pago
            pago_dummies = pd.get_dummies(df['tipo_de_pago_mas_usado'], prefix='pago')
            df = pd.concat([df, pago_dummies], axis=1)

            self._features_created.extend(['tipo_pago_num'] + list(pago_dummies.columns))

        # Score de engagement compuesto
        engagement_cols = ['frecuencia_visita', 'promedio_gasto_comida', 'es_premium']
        if all(col in df.columns for col in engagement_cols):
            # Normalizar componentes
            df['engagement_score'] = (
                (df['frecuencia_visita'] / df['frecuencia_visita'].max()) * 0.4 +
                (df['promedio_gasto_comida'] / df['promedio_gasto_comida'].max()) * 0.4 +
                df['es_premium'] * 0.2
            )
            self._features_created.append('engagement_score')

        return df

    def get_feature_names(self) -> List[str]:
        """Obtener lista de features creadas."""
        return self._features_created.copy()


class YelpFeatureBuilder:
    """Constructor de features para datos de Yelp."""

    def __init__(self):
        self.logger = get_logger(__name__)

    def build_all_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Crear todas las features para Yelp.

        Args:
            df: DataFrame de Yelp

        Returns:
            DataFrame con features adicionales
        """
        df = df.copy()

        # Features de calidad
        df = self._build_quality_features(df)

        # Features de popularidad
        df = self._build_popularity_features(df)

        # Features de ubicación
        df = self._build_location_features(df)

        # Features de categorías
        df = self._build_category_features(df)

        return df

    def _build_quality_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Features de calidad."""
        df = df.copy()

        if 'rating' in df.columns:
            # Categoría de calidad
            df['calidad_categoria'] = pd.cut(
                df['rating'],
                bins=[0, 3.0, 4.0, 4.5, 5.0],
                labels=['Regular', 'Buena', 'Muy Buena', 'Excelente']
            )

            # Score ponderado con número de reviews
            if 'review_count' in df.columns:
                df['weighted_quality_score'] = df['rating'] * np.log1p(df['review_count'])

        return df

    def _build_popularity_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Features de popularidad."""
        df = df.copy()

        if 'review_count' in df.columns:
            # Categoría de popularidad
            df['popularidad_categoria'] = pd.cut(
                df['review_count'],
                bins=[0, 50, 200, 1000, float('inf')],
                labels=['Baja', 'Media', 'Alta', 'Muy Alta']
            )

            # Log de reviews
            df['log_reviews'] = np.log1p(df['review_count'])

        return df

    def _build_location_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Features de ubicación."""
        df = df.copy()

        # Agrupar por ciudad
        if 'city' in df.columns:
            city_counts = df['city'].value_counts()
            df['restaurantes_en_ciudad'] = df['city'].map(city_counts)

        return df

    def _build_category_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Features de categorías."""
        df = df.copy()

        if 'title' in df.columns:
            # Top categorías
            top_cats = df['title'].value_counts().head(10).index
            df['es_categoria_popular'] = df['title'].isin(top_cats).astype(int)

        return df
