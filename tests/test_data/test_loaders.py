"""Tests para loaders."""
import pytest
import pandas as pd
from pathlib import Path

from src.data.loaders import CustomerDataLoader, CustomerDataCleaner


class TestCustomerDataLoader:
    """Tests para CustomerDataLoader."""

    def test_cleaner_creates_expected_features(self, sample_customer_data):
        """Test que el cleaner crea features esperadas."""
        cleaner = CustomerDataCleaner()
        df_clean = cleaner.clean(sample_customer_data)

        # Verificar que se crearon features
        assert 'edad_grupo' in df_clean.columns
        assert 'grupo_edad' in df_clean.columns or 'edad_grupo' in df_clean.columns

    def test_cleaner_handles_nulls(self, sample_customer_data):
        """Test manejo de nulos."""
        cleaner = CustomerDataCleaner()
        df_clean = cleaner.clean(sample_customer_data)

        # Verificar que no hay edades imposibles
        assert (df_clean['edad'] <= 120).all()

    def test_cleaner_removes_duplicates(self, sample_customer_data):
        """Test eliminación de duplicados."""
        # Crear duplicados
        df_dup = pd.concat([sample_customer_data, sample_customer_data.iloc[[0]]])

        cleaner = CustomerDataCleaner()
        df_clean = cleaner.clean(df_dup)

        # Verificar que se eliminaron duplicados
        assert len(df_clean) < len(df_dup)
