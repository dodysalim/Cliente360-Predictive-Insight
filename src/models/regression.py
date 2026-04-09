"""Modelos de regresión para predicción de gasto."""
from typing import Optional, Dict, Any
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge, Lasso
import xgboost as xgb

from src.models.base_model import RegressionModel
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SpendingPredictor(RegressionModel):
    """Predictor de gasto promedio de clientes.

    Soporta múltiples algoritmos:
    - xgboost (default)
    - random_forest
    - gradient_boosting
    - ridge
    - lasso
    """

    def __init__(
        self,
        algorithm: str = "xgboost",
        random_state: int = 42,
        **kwargs
    ):
        self.algorithm = algorithm
        self.model_params = kwargs
        model_name = f"spending_predictor_{algorithm}"
        super().__init__(model_name, random_state)

    def _create_model(self):
        """Factory method para crear el modelo específico."""
        models = {
            'xgboost': xgb.XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=self.random_state,
                **self.model_params
            ),
            'random_forest': RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=self.random_state,
                **self.model_params
            ),
            'gradient_boosting': GradientBoostingRegressor(
                n_estimators=100,
                max_depth=4,
                random_state=self.random_state,
                **self.model_params
            ),
            'ridge': Ridge(
                alpha=1.0,
                random_state=self.random_state,
                **self.model_params
            ),
            'lasso': Lasso(
                alpha=0.1,
                random_state=self.random_state,
                **self.model_params
            )
        }

        if self.algorithm not in models:
            raise ValueError(f"Algoritmo no soportado: {self.algorithm}. "
                           f"Use uno de: {list(models.keys())}")

        return models[self.algorithm]

    def fit(self, X: pd.DataFrame, y: pd.Series) -> 'SpendingPredictor':
        """Entrenar predictor de gasto."""
        super().fit(X, y)

        # Calcular métricas básicas
        predictions = self.predict(X)
        from sklearn.metrics import mean_absolute_error, r2_score

        self._metrics = {
            'r2_train': r2_score(y, predictions),
            'mae_train': mean_absolute_error(y, predictions),
            'mean_actual': y.mean(),
            'mean_predicted': predictions.mean()
        }

        self.logger.info(f"Métricas de entrenamiento: R²={self._metrics['r2_train']:.4f}")
        return self

    def get_prediction_interval(
        self,
        X: pd.DataFrame,
        confidence: float = 0.95
    ) -> tuple:
        """Obtener intervalo de confianza para predicciones.

        Args:
            X: Features
            confidence: Nivel de confianza (0.9, 0.95, 0.99)

        Returns:
            Tuple (lower_bound, upper_bound)
        """
        self._check_fitted()

        predictions = self.predict(X)

        # Estimación de error basada en residuals del entrenamiento
        # Esto es una aproximación simple
        std_error = predictions * 0.15  # Asumir 15% de error

        from scipy import stats
        z_score = stats.norm.ppf((1 + confidence) / 2)

        margin = z_score * std_error
        lower = predictions - margin
        upper = predictions + margin

        return lower, upper
