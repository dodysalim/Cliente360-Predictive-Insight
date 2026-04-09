"""Tests para modelos de regresión."""
import pytest
import numpy as np
import pandas as pd

from src.models.regression import SpendingPredictor


class TestSpendingPredictor:
    """Tests para SpendingPredictor."""

    def test_model_creation(self):
        """Test creación de modelo."""
        model = SpendingPredictor(algorithm='xgboost')
        assert model.algorithm == 'xgboost'
        assert model.model_name == 'spending_predictor_xgboost'

    def test_invalid_algorithm(self):
        """Test algoritmo inválido."""
        with pytest.raises(ValueError):
            SpendingPredictor(algorithm='invalid')

    def test_predictions_non_negative(self, sample_customer_data):
        """Test que predicciones son no negativas."""
        # Preparar datos simples
        X = sample_customer_data[['edad', 'frecuencia_visita', 'ingresos_mensuales']].fillna(0)
        y = sample_customer_data['promedio_gasto_comida']

        model = SpendingPredictor(algorithm='xgboost')
        model.fit(X, y)

        predictions = model.predict(X)

        # Verificar no negatividad
        assert (predictions >= 0).all()
