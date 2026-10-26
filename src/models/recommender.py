"""Sistema de recomendaciones para clientes."""
from typing import List, Dict, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import NearestNeighbors
import joblib

from src.utils.logger import get_logger

logger = get_logger(__name__)


class CustomerRecommender:
    """Sistema de recomendaciones basado en similitud de perfiles.

    Usa:
    - Similitud coseno para clientes similares
    - KNN para recomendaciones de restaurantes
    """

    def __init__(self, n_neighbors: int = 5, metric: str = 'cosine'):
        self.n_neighbors = n_neighbors
        self.metric = metric

        self._customer_scaler = StandardScaler()
        self._restaurant_scaler = StandardScaler()
        self._customer_knn = None
        self._restaurant_knn = None

        self._customer_features = None
        self._restaurant_features = None
        self._customer_ids = None
        self._restaurant_ids = None

        self._is_fitted_customers = False
        self._is_fitted_restaurants = False

        self.logger = get_logger(__name__)

    def fit_customers(
        self,
        customer_features: pd.DataFrame,
        customer_ids: Optional[pd.Series] = None
    ) -> 'CustomerRecommender':
        """Entrenar modelo de recomendaciones para clientes.

        Args:
            customer_features: DataFrame con features de clientes
            customer_ids: IDs de clientes
        """
        self.logger.info(f"Entrenando recomendador con {len(customer_features)} clientes")

        # Guardar features y IDs
        self._customer_features = customer_features.copy()
        self._customer_ids = customer_ids.values if customer_ids is not None else customer_features.index.values

        # Escalar features
        X_scaled = self._customer_scaler.fit_transform(customer_features)

        # Entrenar KNN
        self._customer_knn = NearestNeighbors(
            n_neighbors=min(self.n_neighbors + 1, len(customer_features)),
            metric=self.metric
        )
        self._customer_knn.fit(X_scaled)
        self._is_fitted_customers = True

        self.logger.info("Recomendador de clientes entrenado")
        return self

    def fit_restaurants(
        self,
        restaurant_features: pd.DataFrame,
        restaurant_ids: Optional[pd.Series] = None
    ) -> 'CustomerRecommender':
        """Entrenar modelo para restaurantes.

        Args:
            restaurant_features: Features de restaurantes
            restaurant_ids: IDs de restaurantes
        """
        self.logger.info(f"Entrenando recomendador de restaurantes con {len(restaurant_features)} items")

        self._restaurant_features = restaurant_features.copy()
        self._restaurant_ids = restaurant_ids.values if restaurant_ids is not None else restaurant_features.index.values

        X_scaled = self._restaurant_scaler.fit_transform(restaurant_features)

        self._restaurant_knn = NearestNeighbors(
            n_neighbors=min(self.n_neighbors, len(restaurant_features)),
            metric='euclidean'
        )
        self._restaurant_knn.fit(X_scaled)
        self._is_fitted_restaurants = True

        self.logger.info("Recomendador de restaurantes entrenado")
        return self

    def get_similar_customers(
        self,
        customer_id,
        n_recommendations: int = 5
    ) -> List[Dict]:
        """Encontrar clientes similares.

        Args:
            customer_id: ID del cliente
            n_recommendations: Cantidad de similares a retornar

        Returns:
            Lista de dicts con id y similitud
        """
        if not self._is_fitted_customers:
            raise ValueError("Modelo de clientes no entrenado")

        # Encontrar índice del cliente
        try:
            customer_idx = np.where(self._customer_ids == customer_id)[0][0]
        except IndexError:
            logger.warning(f"Cliente {customer_id} no encontrado")
            return []

        # Obtener features y escalar
        customer_data = self._customer_features.iloc[[customer_idx]]
        customer_scaled = self._customer_scaler.transform(customer_data)

        # Buscar vecinos
        distances, indices = self._customer_knn.kneighbors(customer_scaled)

        # Preparar resultados (excluir el cliente mismo)
        results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            if self._customer_ids[idx] == customer_id:
                continue

            similarity = 1 - dist  # Convertir distancia a similitud
            results.append({
                'customer_id': self._customer_ids[idx],
                'similarity': round(float(similarity), 4)
            })

            if len(results) >= n_recommendations:
                break

        return results

    def recommend_restaurants(
        self,
        customer_features: pd.DataFrame,
        n_recommendations: int = 5,
        city_filter: Optional[str] = None
    ) -> List[Dict]:
        """Recomendar restaurantes basado en preferencias del cliente.

        Args:
            customer_features: Features del cliente
            n_recommendations: Cantidad de recomendaciones
            city_filter: Filtrar por ciudad

        Returns:
            Lista de restaurantes recomendados
        """
        if not self._is_fitted_restaurants:
            raise ValueError("Modelo de restaurantes no entrenado")

        # Escalar features del cliente
        customer_scaled = self._customer_scaler.transform(customer_features)

        # Buscar restaurantes similares
        distances, indices = self._restaurant_knn.kneighbors(customer_scaled)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            restaurant_id = self._restaurant_ids[idx]
            similarity = 1 / (1 + dist)  # Convertir a score

            result = {
                'restaurant_id': restaurant_id,
                'score': round(float(similarity), 4)
            }

            results.append(result)

            if len(results) >= n_recommendations:
                break

        return results

    def predict_preference_score(
        self,
        customer_features: pd.DataFrame,
        restaurant_features: pd.DataFrame
    ) -> float:
        """Calcular score de preferencia entre cliente y restaurante.

        Args:
            customer_features: Features del cliente
            restaurant_features: Features del restaurante

        Returns:
            Score de similitud (0-1)
        """
        # Escalar ambos vectores
        cust_scaled = self._customer_scaler.transform(customer_features)
        rest_scaled = self._restaurant_scaler.transform(restaurant_features)

        # Calcular similitud coseno
        similarity = cosine_similarity(cust_scaled, rest_scaled)[0][0]

        return float(similarity)

    def get_recommendation_explanation(
        self,
        customer_id,
        recommendation: Dict
    ) -> str:
        """Generar explicación textual de una recomendación.

        Args:
            customer_id: ID del cliente
            recommendation: Recomendación generada

        Returns:
            Explicación textual
        """
        score = recommendation.get('score', 0)

        if score > 0.8:
            level = "altamente compatible"
        elif score > 0.6:
            level = "compatible"
        elif score > 0.4:
            level = "moderadamente compatible"
        else:
            level = "posiblemente de interés"

        return (f"Este restaurante es {level} con sus preferencias "
                f"(score: {score:.2f}). Basado en clientes similares a usted.")

    def save(self, filepath: str) -> None:
        """Guardar modelo."""
        model_data = {
            'customer_scaler': self._customer_scaler,
            'restaurant_scaler': self._restaurant_scaler,
            'customer_knn': self._customer_knn,
            'restaurant_knn': self._restaurant_knn,
            'customer_features': self._customer_features,
            'restaurant_features': self._restaurant_features,
            'customer_ids': self._customer_ids,
            'restaurant_ids': self._restaurant_ids,
            'n_neighbors': self.n_neighbors,
            'metric': self.metric
        }
        joblib.dump(model_data, filepath)
        self.logger.info(f"Recomendador guardado en {filepath}")

    def load(self, filepath: str) -> 'CustomerRecommender':
        """Cargar modelo."""
        model_data = joblib.load(filepath)

        self._customer_scaler = model_data['customer_scaler']
        self._restaurant_scaler = model_data['restaurant_scaler']
        self._customer_knn = model_data['customer_knn']
        self._restaurant_knn = model_data['restaurant_knn']
        self._customer_features = model_data['customer_features']
        self._restaurant_features = model_data['restaurant_features']
        self._customer_ids = model_data['customer_ids']
        self._restaurant_ids = model_data['restaurant_ids']
        self.n_neighbors = model_data['n_neighbors']
        self.metric = model_data['metric']
        self._is_fitted_customers = True
        self._is_fitted_restaurants = True

        self.logger.info(f"Recomendador cargado desde {filepath}")
        return self
