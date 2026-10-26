"""Selectores de features."""
from typing import List, Optional, Dict
import pandas as pd
import numpy as np
from sklearn.feature_selection import (
    SelectKBest,
    f_regression,
    mutual_info_regression,
    RFE,
    SelectFromModel
)
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

from src.utils.logger import get_logger

logger = get_logger(__name__)


class FeatureSelector:
    """Selector de features para modelado."""

    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self._selected_features = []
        self._feature_scores = {}
        self.logger = get_logger(__name__)

    def select_correlation(
        self,
        df: pd.DataFrame,
        target: str,
        threshold: float = 0.05
    ) -> List[str]:
        """Seleccionar features por correlación.

        Args:
            df: DataFrame con features y target
            target: Nombre columna target
            threshold: Umbral mínimo de correlación absoluta

        Returns:
            Lista de features seleccionadas
        """
        # Solo columnas numéricas
        numeric_df = df.select_dtypes(include=[np.number])

        if target not in numeric_df.columns:
            logger.warning(f"Target {target} no es numérico, omitiendo selección por correlación")
            return []

        correlations = numeric_df.corr()[target].abs().sort_values(ascending=False)
        selected = correlations[correlations > threshold].index.tolist()
        selected.remove(target) if target in selected else None

        self._feature_scores['correlation'] = correlations.drop(target, errors='ignore').to_dict()
        self.logger.info(f"Correlación: {len(selected)} features seleccionadas")

        return selected

    def select_k_best(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        k: int = 10,
        score_func = f_regression
    ) -> List[str]:
        """Seleccionar k mejores features.

        Args:
            X: Features
            y: Target
            k: Cantidad de features
            score_func: Función de scoring

        Returns:
            Lista de features seleccionadas
        """
        selector = SelectKBest(score_func=score_func, k=k)
        selector.fit(X, y)

        selected = X.columns[selector.get_support()].tolist()
        scores = selector.scores_

        self._feature_scores['k_best'] = dict(zip(X.columns, scores))
        self.logger.info(f"K-best: {len(selected)} features seleccionadas")

        return selected

    def select_rfe(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        n_features: int = 10,
        step: int = 1
    ) -> List[str]:
        """Seleccionar con Recursive Feature Elimination.

        Args:
            X: Features
            y: Target
            n_features: Cantidad de features a seleccionar
            step: Paso de eliminación

        Returns:
            Lista de features seleccionadas
        """
        estimator = RandomForestRegressor(
            n_estimators=50,
            random_state=self.random_state
        )

        selector = RFE(
            estimator=estimator,
            n_features_to_select=n_features,
            step=step
        )

        selector.fit(X, y)
        selected = X.columns[selector.support_].tolist()
        rankings = dict(zip(X.columns, selector.ranking_))

        self._feature_scores['rfe'] = rankings
        self.logger.info(f"RFE: {len(selected)} features seleccionadas")

        return selected

    def select_importance(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        threshold: str = 'median'
    ) -> List[str]:
        """Seleccionar por importancia de Random Forest.

        Args:
            X: Features
            y: Target
            threshold: Umbral de selección ('mean', 'median', o float)

        Returns:
            Lista de features seleccionadas
        """
        estimator = RandomForestRegressor(
            n_estimators=100,
            random_state=self.random_state
        )
        estimator.fit(X, y)

        importances = estimator.feature_importances_
        selector = SelectFromModel(estimator, threshold=threshold, prefit=True)

        selected = X.columns[selector.get_support()].tolist()

        self._feature_scores['importance'] = dict(zip(X.columns, importances))
        self.logger.info(f"Importancia: {len(selected)} features seleccionadas")

        return selected

    def select_combined(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        methods: List[str] = ['correlation', 'k_best', 'importance'],
        min_votes: int = 2
    ) -> List[str]:
        """Combinar múltiples métodos de selección.

        Args:
            X: Features
            y: Target
            methods: Lista de métodos a usar
            min_votes: Mínimo de métodos que deben seleccionar la feature

        Returns:
            Lista de features seleccionadas por consenso
        """
        votes = {}

        for method in methods:
            if method == 'correlation':
                # Para correlación necesitamos el DataFrame completo
                temp_df = X.copy()
                temp_df['target'] = y
                selected = self.select_correlation(temp_df, 'target')
            elif method == 'k_best':
                selected = self.select_k_best(X, y)
            elif method == 'rfe':
                selected = self.select_rfe(X, y)
            elif method == 'importance':
                selected = self.select_importance(X, y)
            else:
                continue

            for feat in selected:
                votes[feat] = votes.get(feat, 0) + 1

        # Seleccionar features con suficientes votos
        final_selected = [f for f, v in votes.items() if v >= min_votes]
        final_selected = sorted(final_selected, key=lambda x: votes[x], reverse=True)

        self._selected_features = final_selected
        self.logger.info(f"Combinado: {len(final_selected)} features seleccionadas")

        return final_selected

    def get_feature_importance_df(self) -> pd.DataFrame:
        """Obtener DataFrame con importancia de features."""
        if not self._feature_scores:
            return pd.DataFrame()

        df = pd.DataFrame(self._feature_scores)
        return df.sort_values(by=df.columns[0], ascending=False)

    def remove_high_correlation(
        self,
        X: pd.DataFrame,
        threshold: float = 0.95
    ) -> List[str]:
        """Eliminar features altamente correlacionadas.

        Args:
            X: Features
            threshold: Umbral de correlación

        Returns:
            Lista de features no correlacionadas
        """
        corr_matrix = X.corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))

        to_drop = [column for column in upper.columns
                  if any(upper[column] > threshold)]

        selected = [c for c in X.columns if c not in to_drop]

        self.logger.info(f"Correlación alta: {len(to_drop)} features eliminadas")
        return selected

    def get_selected_features(self) -> List[str]:
        """Obtener lista de features seleccionadas."""
        return self._selected_features.copy()
