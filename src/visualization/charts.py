"""Constructor de gráficos."""
from typing import Optional, List, Dict, Any
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from config.settings import Settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Configuración global de estilo
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")


class ChartBuilder:
    """Constructor de gráficos para el proyecto."""

    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = Path(output_dir) if output_dir else Settings.REPORTS_DIR / "figures"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = get_logger(__name__)

    def save_figure(self, filename: str, **kwargs):
        """Guardar figura actual."""
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight', **kwargs)
        self.logger.info(f"Figura guardada: {filepath}")
        plt.close()

    def plot_distribution(
        self,
        df: pd.DataFrame,
        column: str,
        title: Optional[str] = None,
        filename: Optional[str] = None,
        kde: bool = True
    ):
        """Graficar distribución de variable."""
        fig, ax = plt.subplots(figsize=(10, 6))

        sns.histplot(data=df, x=column, kde=kde, ax=ax)
        ax.set_title(title or f"Distribución de {column}")
        ax.set_xlabel(column)
        ax.set_ylabel("Frecuencia")

        if filename:
            self.save_figure(filename)
        else:
            plt.show()

    def plot_correlation_matrix(
        self,
        df: pd.DataFrame,
        columns: Optional[List[str]] = None,
        title: str = "Matriz de Correlación",
        filename: Optional[str] = None
    ):
        """Graficar matriz de correlación."""
        if columns:
            df = df[columns]

        # Solo columnas numéricas
        numeric_df = df.select_dtypes(include=[np.number])

        if numeric_df.empty:
            logger.warning("No hay columnas numéricas para correlación")
            return

        fig, ax = plt.subplots(figsize=(12, 10))

        corr = numeric_df.corr()
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax)
        ax.set_title(title)

        if filename:
            self.save_figure(filename)
        else:
            plt.show()

    def plot_categorical_distribution(
        self,
        df: pd.DataFrame,
        column: str,
        title: Optional[str] = None,
        filename: Optional[str] = None,
        top_n: Optional[int] = None
    ):
        """Graficar distribución de variable categórica."""
        fig, ax = plt.subplots(figsize=(12, 6))

        value_counts = df[column].value_counts()
        if top_n:
            value_counts = value_counts.head(top_n)

        value_counts.plot(kind='bar', ax=ax)
        ax.set_title(title or f"Distribución de {column}")
        ax.set_xlabel(column)
        ax.set_ylabel("Frecuencia")
        plt.xticks(rotation=45, ha='right')

        if filename:
            self.save_figure(filename)
        else:
            plt.show()

    def plot_scatter(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        hue: Optional[str] = None,
        title: Optional[str] = None,
        filename: Optional[str] = None
    ):
        """Graficar scatter plot."""
        fig, ax = plt.subplots(figsize=(10, 6))

        sns.scatterplot(data=df, x=x, y=y, hue=hue, ax=ax, alpha=0.6)
        ax.set_title(title or f"{y} vs {x}")

        if filename:
            self.save_figure(filename)
        else:
            plt.show()

    def plot_boxplot(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        title: Optional[str] = None,
        filename: Optional[str] = None
    ):
        """Graficar boxplot."""
        fig, ax = plt.subplots(figsize=(10, 6))

        sns.boxplot(data=df, x=x, y=y, ax=ax)
        ax.set_title(title or f"{y} por {x}")
        plt.xticks(rotation=45, ha='right')

        if filename:
            self.save_figure(filename)
        else:
            plt.show()

    def plot_clustering(
        self,
        X: np.ndarray,
        labels: np.ndarray,
        title: str = "Clusters",
        filename: Optional[str] = None
    ):
        """Visualizar clusters."""
        fig, ax = plt.subplots(figsize=(10, 8))

        scatter = ax.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', alpha=0.6)
        ax.set_title(title)
        ax.set_xlabel("Componente 1")
        ax.set_ylabel("Componente 2")
        plt.colorbar(scatter, ax=ax, label='Cluster')

        if filename:
            self.save_figure(filename)
        else:
            plt.show()

    def plot_feature_importance(
        self,
        importance_df: pd.DataFrame,
        top_n: int = 15,
        title: str = "Importancia de Features",
        filename: Optional[str] = None
    ):
        """Graficar importancia de features."""
        fig, ax = plt.subplots(figsize=(10, 8))

        top_features = importance_df.head(top_n)
        sns.barplot(data=top_features, y='feature', x='importance', ax=ax)
        ax.set_title(title)
        ax.set_xlabel("Importancia")
        ax.set_ylabel("Feature")

        if filename:
            self.save_figure(filename)
        else:
            plt.show()

    def plot_prediction_vs_actual(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        title: str = "Predicciones vs Valores Reales",
        filename: Optional[str] = None
    ):
        """Graficar predicciones vs reales."""
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.scatter(y_true, y_pred, alpha=0.5)
        ax.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()],
               'r--', lw=2, label='Perfecto')
        ax.set_xlabel("Valores Reales")
        ax.set_ylabel("Predicciones")
        ax.set_title(title)
        ax.legend()

        if filename:
            self.save_figure(filename)
        else:
            plt.show()

    def plot_eda_dashboard(self, df: pd.DataFrame, save: bool = True):
        """Crear dashboard de EDA completo."""
        self.logger.info("Generando dashboard de EDA")

        # 1. Distribución de edad
        self.plot_distribution(df, 'edad', filename="01_distribucion_edad.png" if save else None)

        # 2. Distribución de gasto
        self.plot_distribution(df, 'promedio_gasto_comida',
                               filename="02_distribucion_gasto.png" if save else None)

        # 3. Gasto por estrato
        if 'estrato_socioeconomico' in df.columns:
            self.plot_boxplot(df, 'estrato_socioeconomico', 'promedio_gasto_comida',
                            filename="03_gasto_por_estrato.png" if save else None)

        # 4. Distribución de preferencias
        if 'preferencias_alimenticias' in df.columns:
            self.plot_categorical_distribution(df, 'preferencias_alimenticias',
                                               filename="04_preferencias.png" if save else None)

        # 5. Correlaciones
        numeric_cols = ['edad', 'promedio_gasto_comida', 'frecuencia_visita', 'ingresos_mensuales']
        available_cols = [c for c in numeric_cols if c in df.columns]
        if len(available_cols) >= 3:
            self.plot_correlation_matrix(df, available_cols,
                                        filename="05_correlaciones.png" if save else None)

        self.logger.info("Dashboard generado")
