"""Evaluación de modelos ML."""
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    mean_absolute_percentage_error,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    silhouette_score,
    calinski_harabasz_score,
    davies_bouldin_score
)
import matplotlib.pyplot as plt
import seaborn as sns

from src.utils.logger import get_logger

logger = get_logger(__name__)


class ModelEvaluator:
    """Evaluador de modelos de ML."""

    def __init__(self):
        self.metrics_history = []
        self.logger = get_logger(__name__)

    def evaluate_regression(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        model_name: str = "model"
    ) -> Dict[str, float]:
        """Evaluar modelo de regresión.

        Args:
            y_true: Valores reales
            y_pred: Predicciones
            model_name: Nombre del modelo

        Returns:
            Dict con métricas
        """
        metrics = {
            'model': model_name,
            'r2': r2_score(y_true, y_pred),
            'mae': mean_absolute_error(y_true, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
            'mape': mean_absolute_percentage_error(y_true, y_pred),
            'mean_actual': np.mean(y_true),
            'mean_predicted': np.mean(y_pred),
            'std_actual': np.std(y_true),
            'std_predicted': np.std(y_pred)
        }

        self.logger.info(f"Métricas {model_name}: R²={metrics['r2']:.4f}, MAE={metrics['mae']:.2f}")

        self.metrics_history.append({**metrics, 'type': 'regression'})
        return metrics

    def evaluate_classification(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        model_name: str = "classifier",
        average: str = 'weighted'
    ) -> Dict[str, float]:
        """Evaluar modelo de clasificación.

        Args:
            y_true: Valores reales
            y_pred: Predicciones
            model_name: Nombre del modelo
            average: Método de promedio

        Returns:
            Dict con métricas
        """
        metrics = {
            'model': model_name,
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average=average, zero_division=0),
            'recall': recall_score(y_true, y_pred, average=average, zero_division=0),
            'f1': f1_score(y_true, y_pred, average=average, zero_division=0)
        }

        self.logger.info(f"Métricas {model_name}: Acc={metrics['accuracy']:.4f}, F1={metrics['f1']:.4f}")

        self.metrics_history.append({**metrics, 'type': 'classification'})
        return metrics

    def evaluate_clustering(
        self,
        X: np.ndarray,
        labels: np.ndarray,
        model_name: str = "clustering"
    ) -> Dict[str, float]:
        """Evaluar modelo de clustering.

        Args:
            X: Features
            labels: Labels de clusters
            model_name: Nombre del modelo

        Returns:
            Dict con métricas
        """
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

        if n_clusters < 2:
            return {'model': model_name, 'n_clusters': n_clusters, 'silhouette': None}

        metrics = {
            'model': model_name,
            'n_clusters': n_clusters,
            'silhouette': silhouette_score(X, labels),
            'calinski_harabasz': calinski_harabasz_score(X, labels),
            'davies_bouldin': davies_bouldin_score(X, labels)
        }

        self.logger.info(
            f"Métricas {model_name}: Silhouette={metrics['silhouette']:.4f}, "
            f"Clusters={n_clusters}"
        )

        self.metrics_history.append({**metrics, 'type': 'clustering'})
        return metrics

    def plot_regression_results(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        save_path: Optional[str] = None
    ) -> None:
        """Visualizar resultados de regresión.

        Args:
            y_true: Valores reales
            y_pred: Predicciones
            save_path: Ruta para guardar figura
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Scatter plot: Predicciones vs Reales
        axes[0].scatter(y_true, y_pred, alpha=0.5)
        axes[0].plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()],
                    'r--', lw=2)
        axes[0].set_xlabel('Valores Reales')
        axes[0].set_ylabel('Predicciones')
        axes[0].set_title('Predicciones vs Valores Reales')

        # Residuales
        residuals = y_true - y_pred
        axes[1].scatter(y_pred, residuals, alpha=0.5)
        axes[1].axhline(y=0, color='r', linestyle='--')
        axes[1].set_xlabel('Predicciones')
        axes[1].set_ylabel('Residuales')
        axes[1].set_title('Análisis de Residuales')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Figura guardada en {save_path}")

        plt.close()

    def plot_confusion_matrix(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        labels: Optional[List[str]] = None,
        save_path: Optional[str] = None
    ) -> None:
        """Visualizar matriz de confusión.

        Args:
            y_true: Valores reales
            y_pred: Predicciones
            labels: Labels de clases
            save_path: Ruta para guardar
        """
        cm = confusion_matrix(y_true, y_pred)

        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=labels, yticklabels=labels)
        plt.xlabel('Predicción')
        plt.ylabel('Real')
        plt.title('Matriz de Confusión')

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        plt.close()

    def compare_models(self, metrics_list: List[Dict[str, Any]]) -> pd.DataFrame:
        """Comparar múltiples modelos.

        Args:
            metrics_list: Lista de métricas de diferentes modelos

        Returns:
            DataFrame con comparación
        """
        return pd.DataFrame(metrics_list)

    def get_best_model(
        self,
        metrics_list: List[Dict[str, Any]],
        metric: str = 'r2',
        higher_is_better: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Encontrar mejor modelo según métrica.

        Args:
            metrics_list: Lista de métricas
            metric: Métrica a comparar
            higher_is_better: Si mayor es mejor

        Returns:
            Métricas del mejor modelo
        """
        if not metrics_list:
            return None

        sorted_models = sorted(
            metrics_list,
            key=lambda x: x.get(metric, float('-inf') if higher_is_better else float('inf')),
            reverse=higher_is_better
        )

        return sorted_models[0]

    def generate_report(self, save_path: Optional[str] = None) -> str:
        """Generar reporte de evaluación.

        Args:
            save_path: Ruta para guardar reporte

        Returns:
            Texto del reporte
        """
        report = ["=" * 60, "REPORTE DE EVALUACIÓN DE MODELOS", "=" * 60, ""]

        for i, metrics in enumerate(self.metrics_history, 1):
            report.append(f"\nModelo {i}: {metrics.get('model', 'N/A')}")
            report.append(f"Tipo: {metrics.get('type', 'N/A')}")
            report.append("-" * 40)

            for key, value in metrics.items():
                if key not in ['model', 'type']:
                    if isinstance(value, float):
                        report.append(f"  {key}: {value:.4f}")
                    else:
                        report.append(f"  {key}: {value}")

        report_text = "\n".join(report)

        if save_path:
            with open(save_path, 'w') as f:
                f.write(report_text)

        return report_text
