"""Pipeline de ML para entrenamiento y predicción."""
from typing import Optional, Dict, Any, List
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from config.settings import Settings
from src.models.regression import SpendingPredictor
from src.models.segmentation import CustomerSegmentation
from src.models.recommender import CustomerRecommender
from src.models.evaluation import ModelEvaluator
from src.features.selectors import FeatureSelector
from src.utils.logger import get_logger

logger = get_logger(__name__)


class MLPipeline:
    """Pipeline completo de Machine Learning."""

    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.logger = get_logger(__name__)

        # Componentes
        self.feature_selector = FeatureSelector(random_state=random_state)
        self.regression_model = None
        self.segmentation_model = None
        self.recommender_model = None
        self.evaluator = ModelEvaluator()

        # Estado
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.selected_features = None

    def run(
        self,
        df: pd.DataFrame,
        target_col: str = 'promedio_gasto_comida',
        train_regression: bool = True,
        train_segmentation: bool = True,
        train_recommender: bool = True,
        save_models: bool = True
    ) -> Dict[str, Any]:
        """Ejecutar pipeline ML completo.

        Args:
            df: DataFrame con features
            target_col: Columna objetivo
            train_regression: Entrenar modelo de regresión
            train_segmentation: Entrenar modelo de segmentación
            train_recommender: Entrenar modelo de recomendaciones
            save_models: Guardar modelos entrenados

        Returns:
            Dict con resultados y métricas
        """
        self.logger.info("=" * 60)
        self.logger.info("INICIANDO PIPELINE ML")
        self.logger.info("=" * 60)

        results = {}

        try:
            # 1. Preparar datos
            self._prepare_data(df, target_col)

            # 2. Seleccionar features
            self._select_features(target_col)

            # 3. Entrenar regresión
            if train_regression:
                results['regression'] = self._train_regression()

            # 4. Entrenar segmentación
            if train_segmentation:
                results['segmentation'] = self._train_segmentation()

            # 5. Entrenar recomendador
            if train_recommender:
                results['recommender'] = self._train_recommender()

            # 6. Guardar modelos
            if save_models:
                self._save_models(results)

            self.logger.info("=" * 60)
            self.logger.info("PIPELINE ML COMPLETADO")
            self.logger.info("=" * 60)

            return results

        except Exception as e:
            self.logger.error(f"Error en pipeline ML: {str(e)}")
            raise

    def _prepare_data(self, df: pd.DataFrame, target_col: str):
        """Preparar datos para entrenamiento."""
        self.logger.info("ML - Fase 1: PREPARACIÓN DE DATOS")

        # Seleccionar solo columnas numéricas
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        # Remover target de features
        feature_cols = [c for c in numeric_cols if c != target_col]

        X = df[feature_cols].fillna(0)
        y = df[target_col] if target_col in df.columns else None

        # Split train/test
        if y is not None:
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                X, y,
                test_size=Settings.TEST_SIZE,
                random_state=self.random_state
            )
            self.logger.info(f"Train: {len(self.X_train)}, Test: {len(self.X_test)}")
        else:
            self.X_train = X
            self.X_test = X.iloc[:int(len(X) * 0.2)]

    def _select_features(self, target_col: str):
        """Seleccionar features óptimas."""
        self.logger.info("ML - Fase 2: SELECCIÓN DE FEATURES")

        if self.y_train is not None:
            self.selected_features = self.feature_selector.select_combined(
                self.X_train, self.y_train
            )
        else:
            # Si no hay target, usar todas las features
            self.selected_features = list(self.X_train.columns)

        self.logger.info(f"Features seleccionadas: {len(self.selected_features)}")

    def _train_regression(self) -> Dict[str, Any]:
        """Entrenar modelo de regresión."""
        self.logger.info("ML - Fase 3: ENTRENAMIENTO DE REGRESIÓN")

        # Usar XGBoost
        self.regression_model = SpendingPredictor(algorithm='xgboost')

        X_train_sel = self.X_train[self.selected_features]
        X_test_sel = self.X_test[self.selected_features]

        self.regression_model.fit(X_train_sel, self.y_train)

        # Evaluar
        y_pred = self.regression_model.predict(X_test_sel)
        metrics = self.evaluator.evaluate_regression(
            self.y_test.values, y_pred, model_name='xgboost_spending'
        )

        # Feature importance
        importance = self.regression_model.get_feature_importance()

        return {
            'model': self.regression_model,
            'metrics': metrics,
            'feature_importance': importance.to_dict() if importance is not None else {}
        }

    def _train_segmentation(self) -> Dict[str, Any]:
        """Entrenar modelo de segmentación."""
        self.logger.info("ML - Fase 4: SEGMENTACIÓN DE CLIENTES")

        self.segmentation_model = CustomerSegmentation(
            algorithm='kmeans',
            n_clusters=4,
            random_state=self.random_state
        )

        # Usar subset de features para clustering
        seg_features = [f for f in self.selected_features
                       if f not in ['id_persona', 'es_joven', 'es_adulto', 'es_adulto_mayor']][:10]

        X_seg = self.X_train[seg_features].fillna(0)

        self.segmentation_model.fit(X_seg, apply_pca=True, pca_components=2)

        # Evaluar
        labels = self.segmentation_model.predict(X_seg)
        metrics = self.evaluator.evaluate_clustering(
            X_seg.values, labels, model_name='kmeans_segments'
        )

        # Perfiles de clusters
        profiles = self.segmentation_model.get_cluster_profiles()

        return {
            'model': self.segmentation_model,
            'metrics': metrics,
            'cluster_profiles': profiles
        }

    def _train_recommender(self) -> Dict[str, Any]:
        """Entrenar sistema de recomendaciones."""
        self.logger.info("ML - Fase 5: SISTEMA DE RECOMENDACIONES")

        self.recommender_model = CustomerRecommender(n_neighbors=5)

        # Entrenar con features seleccionadas
        rec_features = [f for f in self.selected_features if 'pref_' in f or 'engagement' in f][:5]
        if len(rec_features) < 3:
            rec_features = self.selected_features[:5]

        X_rec = self.X_train[rec_features].fillna(0)

        self.recommender_model.fit_customers(X_rec)

        return {
            'model': self.recommender_model,
            'n_customers': len(X_rec),
            'features_used': rec_features
        }

    def _save_models(self, results: Dict[str, Any]):
        """Guardar modelos entrenados."""
        self.logger.info("ML - Fase 6: GUARDANDO MODELOS")

        models_dir = Path(Settings.ROOT_DIR) / "models"
        models_dir.mkdir(exist_ok=True)

        if self.regression_model:
            self.regression_model.save(str(models_dir / "regression_model.joblib"))

        if self.segmentation_model:
            self.segmentation_model.save(str(models_dir / "segmentation_model.joblib"))

        if self.recommender_model:
            self.recommender_model.save(str(models_dir / "recommender_model.joblib"))

        # Guardar feature selector
        import joblib
        joblib.dump(self.selected_features, str(models_dir / "selected_features.joblib"))

        self.logger.info(f"Modelos guardados en: {models_dir}")

    def get_evaluation_report(self) -> str:
        """Generar reporte de evaluación."""
        return self.evaluator.generate_report()
