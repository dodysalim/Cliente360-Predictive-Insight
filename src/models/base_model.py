"""Clases base para modelos ML (Principio SOLID: OCP, LSP)."""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple
import pickle
import joblib
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator

from src.utils.logger import get_logger
from src.utils.exceptions import ModelTrainingError, ModelPredictionError

logger = get_logger(__name__)


class BaseModel(ABC):
    """Clase base abstracta para todos los modelos.

    Implementa el patrón Template Method para entrenamiento y predicción.
    """

    def __init__(self, model_name: str = "base_model", random_state: int = 42):
        self.model_name = model_name
        self.random_state = random_state
        self._model = None
        self._is_fitted = False
        self._feature_names = None
        self._metrics = {}
        self.logger = get_logger(f"{self.__class__.__name__}.{model_name}")

    @abstractmethod
    def _create_model(self) -> BaseEstimator:
        """Factory method para crear el modelo específico."""
        pass

    @abstractmethod
    def fit(self, X: pd.DataFrame, y: pd.Series = None) -> 'BaseModel':
        """Entrenar el modelo."""
        pass

    @abstractmethod
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Realizar predicciones."""
        pass

    def _validate_input(self, X: pd.DataFrame) -> pd.DataFrame:
        """Validar datos de entrada."""
        if X is None or X.empty:
            raise ValueError("Datos de entrada vacíos")

        # Manejar valores infinitos
        X = X.replace([np.inf, -np.inf], np.nan)

        # Manejar valores nulos
        if X.isnull().any().any():
            self.logger.warning("Valores nulos encontrados, imputando con 0")
            X = X.fillna(0)

        return X

    def _check_fitted(self):
        """Verificar que el modelo esté entrenado."""
        if not self._is_fitted:
            raise ModelPredictionError(
                f"El modelo {self.model_name} no ha sido entrenado. Llame fit() primero."
            )

    def get_feature_importance(self) -> Optional[pd.DataFrame]:
        """Obtener importancia de features si está disponible."""
        if self._model is None:
            return None

        try:
            importance = self._model.feature_importances_
            return pd.DataFrame({
                'feature': self._feature_names,
                'importance': importance
            }).sort_values('importance', ascending=False)
        except AttributeError:
            try:
                importance = self._model.coef_
                if len(importance.shape) > 1:
                    importance = np.abs(importance).mean(axis=0)
                return pd.DataFrame({
                    'feature': self._feature_names,
                    'importance': importance
                }).sort_values('importance', ascending=False)
            except AttributeError:
                return None

    def save(self, filepath: str) -> None:
        """Guardar modelo entrenado."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        model_data = {
            'model': self._model,
            'model_name': self.model_name,
            'is_fitted': self._is_fitted,
            'feature_names': self._feature_names,
            'metrics': self._metrics,
            'random_state': self.random_state
        }

        joblib.dump(model_data, filepath)
        self.logger.info(f"Modelo guardado en {filepath}")

    def load(self, filepath: str) -> 'BaseModel':
        """Cargar modelo entrenado."""
        if not Path(filepath).exists():
            raise FileNotFoundError(f"Archivo no encontrado: {filepath}")

        model_data = joblib.load(filepath)

        self._model = model_data['model']
        self.model_name = model_data['model_name']
        self._is_fitted = model_data['is_fitted']
        self._feature_names = model_data['feature_names']
        self._metrics = model_data['metrics']
        self.random_state = model_data.get('random_state', 42)

        self.logger.info(f"Modelo cargado desde {filepath}")
        return self

    def get_metrics(self) -> Dict[str, float]:
        """Obtener métricas del modelo."""
        return self._metrics.copy()


class RegressionModel(BaseModel):
    """Clase base para modelos de regresión."""

    def __init__(self, model_name: str = "regression", random_state: int = 42):
        super().__init__(model_name, random_state)

    def fit(self, X: pd.DataFrame, y: pd.Series) -> 'RegressionModel':
        """Entrenar modelo de regresión."""
        self.logger.info(f"Entrenando modelo {self.model_name}")

        try:
            X = self._validate_input(X)
            self._feature_names = list(X.columns)

            self._model = self._create_model()
            self._model.fit(X, y)
            self._is_fitted = True

            self.logger.info(f"Modelo {self.model_name} entrenado exitosamente")

        except Exception as e:
            raise ModelTrainingError(
                f"Error entrenando {self.model_name}: {str(e)}",
                model_name=self.model_name
            )

        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predecir valores continuos."""
        self._check_fitted()
        X = self._validate_input(X)

        try:
            predictions = self._model.predict(X)
            # Asegurar valores no negativos para gastos
            predictions = np.maximum(predictions, 0)
            return predictions
        except Exception as e:
            raise ModelPredictionError(
                f"Error en predicción: {str(e)}",
                model_name=self.model_name
            )


class ClassificationModel(BaseModel):
    """Clase base para modelos de clasificación."""

    def __init__(self, model_name: str = "classifier", random_state: int = 42):
        super().__init__(model_name, random_state)
        self._classes = None

    def fit(self, X: pd.DataFrame, y: pd.Series) -> 'ClassificationModel':
        """Entrenar modelo de clasificación."""
        self.logger.info(f"Entrenando clasificador {self.model_name}")

        try:
            X = self._validate_input(X)
            self._feature_names = list(X.columns)

            self._model = self._create_model()
            self._model.fit(X, y)
            self._is_fitted = True
            self._classes = self._model.classes_

            self.logger.info(f"Clasificador entrenado con clases: {self._classes}")

        except Exception as e:
            raise ModelTrainingError(
                f"Error entrenando clasificador: {str(e)}",
                model_name=self.model_name
            )

        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predecir clases."""
        self._check_fitted()
        X = self._validate_input(X)

        try:
            return self._model.predict(X)
        except Exception as e:
            raise ModelPredictionError(
                f"Error en clasificación: {str(e)}",
                model_name=self.model_name
            )

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Predecir probabilidades de clase."""
        self._check_fitted()
        X = self._validate_input(X)

        try:
            return self._model.predict_proba(X)
        except AttributeError:
            self.logger.warning("Modelo no soporta predict_proba")
            return None
