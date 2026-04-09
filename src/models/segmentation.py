"""Modelos de segmentación de clientes."""
from typing import Optional, Dict, List, Tuple
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import joblib

from src.utils.logger import get_logger
from src.utils.exceptions import ModelTrainingError

logger = get_logger(__name__)


class CustomerSegmentation:
    """Segmentación de clientes usando clustering.

    Soporta:
    - K-Means (default)
    - DBSCAN
    """

    def __init__(
        self,
        algorithm: str = "kmeans",
        n_clusters: int = 4,
        random_state: int = 42,
        **kwargs
    ):
        self.algorithm = algorithm
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.model_params = kwargs

        self._model = None
        self._scaler = StandardScaler()
        self._pca = None
        self._is_fitted = False
        self._feature_names = None
        self._cluster_profiles = None

        self.logger = get_logger(f"{self.__class__.__name__}.{algorithm}")

    def fit(self, X: pd.DataFrame, apply_pca: bool = False,
            pca_components: int = 2) -> 'CustomerSegmentation':
        """Entrenar modelo de segmentación.

        Args:
            X: Features para clustering
            apply_pca: Si aplicar PCA antes de clustering
            pca_components: Número de componentes PCA
        """
        self.logger.info(f"Entrenando segmentación con {self.algorithm}")

        try:
            X_scaled = self._scaler.fit_transform(X)
            self._feature_names = list(X.columns)

            # Aplicar PCA opcionalmente
            if apply_pca:
                self._pca = PCA(n_components=pca_components)
                X_scaled = self._pca.fit_transform(X_scaled)
                self.logger.info(f"PCA aplicado: {pca_components} componentes")

            # Crear y entrenar modelo
            if self.algorithm == "kmeans":
                self._model = KMeans(
                    n_clusters=self.n_clusters,
                    random_state=self.random_state,
                    n_init=10,
                    **self.model_params
                )
            elif self.algorithm == "dbscan":
                self._model = DBSCAN(**self.model_params)
            else:
                raise ValueError(f"Algoritmo no soportado: {self.algorithm}")

            labels = self._model.fit_predict(X_scaled)
            self._is_fitted = True

            # Calcular perfiles de clusters
            self._calculate_cluster_profiles(X, labels)

            self.logger.info(f"Segmentación completada: {len(set(labels))} clusters")

        except Exception as e:
            raise ModelTrainingError(f"Error en segmentación: {str(e)}")

        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Asignar clientes a clusters."""
        if not self._is_fitted:
            raise ValueError("Modelo no entrenado")

        X_scaled = self._scaler.transform(X)

        if self._pca:
            X_scaled = self._pca.transform(X_scaled)

        if self.algorithm == "kmeans":
            return self._model.predict(X_scaled)
        else:
            # Para DBSCAN usar nearest neighbor
            return self._model.fit_predict(X_scaled)

    def _calculate_cluster_profiles(self, X: pd.DataFrame, labels: np.ndarray):
        """Calcular perfiles descriptivos de cada cluster."""
        X['cluster'] = labels

        profiles = {}
        for cluster_id in sorted(set(labels)):
            if cluster_id == -1:  # Ruido en DBSCAN
                continue

            cluster_data = X[X['cluster'] == cluster_id]
            profiles[int(cluster_id)] = {
                'size': len(cluster_data),
                'percentage': len(cluster_data) / len(X) * 100,
                'mean_values': cluster_data.mean().to_dict(),
                'std_values': cluster_data.std().to_dict()
            }

        X.drop('cluster', axis=1, inplace=True)
        self._cluster_profiles = profiles

    def get_cluster_profiles(self) -> Dict:
        """Obtener perfiles de clusters."""
        return self._cluster_profiles

    def get_cluster_centers(self) -> Optional[np.ndarray]:
        """Obtener centroides (solo K-Means)."""
        if hasattr(self._model, 'cluster_centers_'):
            return self._model.cluster_centers_
        return None

    def get_inertia(self) -> Optional[float]:
        """Obtener inercia (solo K-Means)."""
        if hasattr(self._model, 'inertia_'):
            return self._model.inertia_
        return None

    def find_optimal_clusters(self, X: pd.DataFrame, max_k: int = 10) -> Tuple[int, List[float]]:
        """Encontrar número óptimo de clusters usando método del codo.

        Args:
            X: Features
            max_k: Máximo número de clusters a probar

        Returns:
            Tupla (k_optimo, lista_inercias)
        """
        X_scaled = self._scaler.fit_transform(X)

        inertias = []
        for k in range(1, max_k + 1):
            kmeans = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
            kmeans.fit(X_scaled)
            inertias.append(kmeans.inertia_)

        # Encontrar codo (punto de inflexión)
        # Simple: donde la diferencia empieza a ser pequeña
        diffs = np.diff(inertias)
        diffs2 = np.diff(diffs)

        if len(diffs2) > 0:
            optimal_k = np.argmax(diffs2) + 2
        else:
            optimal_k = 3

        return optimal_k, inertias

    def save(self, filepath: str) -> None:
        """Guardar modelo."""
        model_data = {
            'model': self._model,
            'scaler': self._scaler,
            'pca': self._pca,
            'algorithm': self.algorithm,
            'n_clusters': self.n_clusters,
            'feature_names': self._feature_names,
            'cluster_profiles': self._cluster_profiles
        }
        joblib.dump(model_data, filepath)
        self.logger.info(f"Modelo guardado en {filepath}")

    def load(self, filepath: str) -> 'CustomerSegmentation':
        """Cargar modelo."""
        model_data = joblib.load(filepath)

        self._model = model_data['model']
        self._scaler = model_data['scaler']
        self._pca = model_data.get('pca')
        self.algorithm = model_data['algorithm']
        self.n_clusters = model_data['n_clusters']
        self._feature_names = model_data['feature_names']
        self._cluster_profiles = model_data['cluster_profiles']
        self._is_fitted = True

        self.logger.info(f"Modelo cargado desde {filepath}")
        return self
