"""Generador de reportes."""
from typing import Dict, Any, Optional
from pathlib import Path
import pandas as pd
import json
from datetime import datetime

from config.settings import Settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ReportGenerator:
    """Generador de reportes del proyecto."""

    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = Path(output_dir) if output_dir else Settings.REPORTS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = get_logger(__name__)

    def generate_data_report(self, df: pd.DataFrame, title: str = "Data Report") -> str:
        """Generar reporte de calidad de datos.

        Args:
            df: DataFrame a reportar
            title: Título del reporte

        Returns:
            Ruta del archivo generado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data_report_{timestamp}.html"
        filepath = self.output_dir / filename

        # Calcular estadísticas
        report_data = {
            'title': title,
            'timestamp': datetime.now().isoformat(),
            'shape': df.shape,
            'columns': []
        }

        for col in df.columns:
            col_data = {
                'name': col,
                'dtype': str(df[col].dtype),
                'missing': int(df[col].isnull().sum()),
                'missing_pct': round(df[col].isnull().sum() / len(df) * 100, 2),
                'unique': int(df[col].nunique())
            }

            if pd.api.types.is_numeric_dtype(df[col]):
                col_data['stats'] = {
                    'mean': round(float(df[col].mean()), 2),
                    'std': round(float(df[col].std()), 2),
                    'min': round(float(df[col].min()), 2),
                    'max': round(float(df[col].max()), 2),
                    'median': round(float(df[col].median()), 2)
                }
            else:
                col_data['top_values'] = df[col].value_counts().head(5).to_dict()

            report_data['columns'].append(col_data)

        # Generar HTML simple
        html = self._generate_html_report(report_data)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        self.logger.info(f"Reporte de datos generado: {filepath}")
        return str(filepath)

    def generate_model_report(
        self,
        model_results: Dict[str, Any],
        title: str = "Model Report"
    ) -> str:
        """Generar reporte de modelos.

        Args:
            model_results: Resultados de modelos
            title: Título del reporte

        Returns:
            Ruta del archivo generado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"model_report_{timestamp}.json"
        filepath = self.output_dir / filename

        report_data = {
            'title': title,
            'timestamp': datetime.now().isoformat(),
            'results': model_results
        }

        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)

        self.logger.info(f"Reporte de modelos generado: {filepath}")
        return str(filepath)

    def generate_executive_summary(
        self,
        data_summary: Dict[str, Any],
        model_summary: Dict[str, Any],
        filename: str = "executive_summary.md"
    ) -> str:
        """Generar resumen ejecutivo.

        Args:
            data_summary: Resumen de datos
            model_summary: Resumen de modelos
            filename: Nombre del archivo

        Returns:
            Ruta del archivo generado
        """
        filepath = self.output_dir / filename

        content = f"""# Resumen Ejecutivo - Proyecto Cliente 360°

**Fecha:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Datos

- **Registros de clientes:** {data_summary.get('total_customers', 'N/A')}
- **Features:** {data_summary.get('n_features', 'N/A')}
- **Ciudades analizadas:** {data_summary.get('n_cities', 'N/A')}

## Modelos Entrenados

### 1. Regresión (Predicción de Gasto)
- **R² Score:** {model_summary.get('regression_r2', 'N/A')}
- **MAE:** {model_summary.get('regression_mae', 'N/A')}

### 2. Segmentación (Clusters)
- **Número de clusters:** {model_summary.get('n_clusters', 'N/A')}
- **Silhouette Score:** {model_summary.get('silhouette', 'N/A')}

### 3. Sistema de Recomendaciones
- **Clientes en sistema:** {model_summary.get('n_customers_rec', 'N/A')}

## Hallazgos Clave

{model_summary.get('key_findings', 'Sin hallazgos registrados')}

## Próximos Pasos

1. Desplegar modelos en producción
2. Integrar con sistema CRM
3. Monitorear métricas de negocio
"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        self.logger.info(f"Resumen ejecutivo generado: {filepath}")
        return str(filepath)

    def _generate_html_report(self, data: Dict) -> str:
        """Generar HTML básico para reporte."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{data['title']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #4CAF50; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .metric {{ font-weight: bold; color: #2196F3; }}
            </style>
        </head>
        <body>
            <h1>{data['title']}</h1>
            <p><strong>Fecha:</strong> {data['timestamp']}</p>
            <p><strong>Dimensiones:</strong> {data['shape'][0]} filas × {data['shape'][1]} columnas</p>

            <h2>Resumen de Columnas</h2>
            <table>
                <tr>
                    <th>Columna</th>
                    <th>Tipo</th>
                    <th>Nulos</th>
                    <th>% Nulos</th>
                    <th>Únicos</th>
                    <th>Estadísticas</th>
                </tr>
        """

        for col in data['columns']:
            stats_str = ""
            if 'stats' in col:
                stats = col['stats']
                stats_str = f"Mean: {stats['mean']}, Std: {stats['std']}"

            html += f"""
                <tr>
                    <td>{col['name']}</td>
                    <td>{col['dtype']}</td>
                    <td>{col['missing']}</td>
                    <td>{col['missing_pct']}%</td>
                    <td>{col['unique']}</td>
                    <td>{stats_str}</td>
                </tr>
            """

        html += """
            </table>
        </body>
        </html>
        """

        return html

    def generate_insights_report(
        self,
        insights: Dict[str, Any],
        filename: str = "insights_report.md"
    ) -> str:
        """Generar reporte de insights."""
        filepath = self.output_dir / filename

        content = f"""# Reporte de Insights

**Generado:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Insights Principales

"""

        for category, items in insights.items():
            content += f"\n### {category}\n\n"
            for item in items:
                content += f"- {item}\n"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        self.logger.info(f"Reporte de insights generado: {filepath}")
        return str(filepath)
