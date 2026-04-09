# 💎 Cliente360° — InsightReach Analytics
## Plataforma de Inteligencia Predictiva, Segmentación Estratégica y Optimización de Mercado
### *Proyecto Integrador de Nivel Senior Empresarial — Henry Bootcamp*

---

## 📑 Índice de Contenidos

1.  [📌 Resumen Ejecutivo de Alta Dirección](#-resumen-ejecutivo-de-alta-dirección)
2.  [🎯 El Desafío de Negocio: Visión 360°](#-el-desafío-de-negocio-visión-360)
3.  [🌳 Estructura Completa de Activos y Gobernanza](#-estructura-completa-de-activos-y-gobernanza)
4.  [🛠️ Metodología de Implementación: CRISP-DM Senior](#-metodología-de-implementación-crisp-dm-senior)
5.  [🏛️ Arquitectura del Motor (SOLID Engineering)](#-arquitectura-del-motor-solid-engineering)
6.  [🔍 Walkthrough Visual: Flujo de Valor](#-walkthrough-visual-flujo-de-valor)
7.  [🧹 Ingeniería de Datos y Calidad](#-ingeniería-de-datos-y-calidad)
8.  [🧠 Inteligencia Predictiva y ML](#-inteligencia-predictiva-y-ml)
9.  [🌆 Caso de Éxito: Mercado Miami](#-caso-de-éxito-mercado-miami)
10. [📊 Resultados y Dashboard Ejecutivo](#-resultados-y-dashboard-ejecutivo)
11. [💾 Guía de Operación](#-guía-de-operación)
12. [🚧 Roadmap Estratégico](#-roadmap-estratégico)
13. [👤 Autor y Contacto](#-autor-y-contacto)

---

## 📌 Resumen Ejecutivo de Alta Dirección

**Cliente360°** representa la culminación de un proceso de ingeniería de datos y ciencia de datos aplicada a la resolución de problemas complejos de crecimiento corporativo. El sistema utiliza una triada de **ML Supervisado**, **ML No Supervisado** e **Inteligencia Geo-espacial** (Yelp Fusion API) para extraer valor accionable del comportamiento de los consumidores.

---

## 🎯 El Desafío de Negocio: Visión 360°

La organización enfrentaba problemas de **Ceguera Transaccional**, **Marketing Ineficiente** y **Desconexión con el Entorno**. Este proyecto aborda estos retos mediante:
*   **CLV Predictivo**: Proyecciones financieras con un **R² de 0.85**.
*   **Eficiencia en Marketing**: Segmentación algorítmica para optimizar el CAC.
*   **Geomarketing**: Identificación de brechas de oferta externa en ciudades clave.

---

## 🌳 Estructura Completa de Activos y Gobernanza

A continuación se detalla la **arquitectura integral del repositorio**, diseñada para garantizar la trazabilidad y el escalamiento del sistema:

```bash
Proyecto_Integrador_Dody_Empresarial/
├── config/                     # ⚙️ NÚCLEO DE CONFIGURACIÓN
│   ├── settings.py             # Parámetros globales y credenciales.
│   └── logging_config.yaml     # Estrategia de trazabilidad industrial.
├── data/                       # 📂 GESTIÓN DE DATOS (DATA LAKE)
│   ├── raw/                    # Datos fuente originales e inmutables.
│   ├── external/               # Ingestas de API de terceros.
│   ├── interim/                # Estado intermedio de transformaciones.
│   └── processed/              # Datasets finales "Gold Standard" para ML.
├── notebooks/                  # 📊 REPORTES ANALÍTICOS EJECUTIVOS
│   ├── 01_eda.ipynb            # Diagnóstico senior y auditoría visual.
│   ├── 02_api.ipynb            # Enriquecimiento via Yelp Fusion.
│   ├── 03_features.ipynb       # Laboratorio de ingeniería de señales.
│   ├── 04_modeling.ipynb       # Evaluación multicapa de algoritmos.
│   └── 05_insights.ipynb       # Dashboard e inteligencia de mercado.
├── src/                        # 🛠️ MOTOR DEL SISTEMA (CORE ENGINE)
│   ├── api/                    # Cliente HTTP y parsers para Yelp.
│   │   ├── client.py
│   │   └── parsers.py
│   ├── data/                   # Limpieza y validación robusta.
│   │   ├── cleaners.py
│   │   └── loaders.py
│   ├── features/               # Transformadores de variables.
│   │   └── builders.py
│   ├── models/                 # Lógica de entrenamiento y recomendación.
│   │   ├── regression.py
│   │   ├── segmentation.py
│   │   └── recommender.py
│   └── utils/                  # Logger y excepciones personalizadas.
├── reports/                    # 📈 OUTPUTS ESTRATÉGICOS
│   ├── figures/                # Galería de visualizaciones de alta calidad.
│   └── tables/                 # Resúmenes ejecutivos en CSV.
├── scripts/                    # 🚀 SCRIPTS EJECUTABLES
│   ├── run_etl.py              # Ejecución aislada de la tubería de datos.
│   └── run_training.py         # Orquestación de entrenamiento ML.
├── run_pipeline.py             # 🔥 MASTER RUNNER (Automatización Total)
├── requirements.txt            # Contrato de dependencias.
└── setup.py                    # Metadata de empaquetado profesional.
```

---

## 🛠️ Metodología de Implementación: CRISP-DM Senior

El proyecto sigue el estándar **CRISP-DM** mejorado para entornos empresariales:
1.  **Business Understanding**: Alineación de métricas con objetivos financieros.
2.  **Data Understanding**: Auditoría profunda de 25+ campos (NB 01).
3.  **Preparation**: Pipelines automatizados de limpieza y normalización.
4.  **Modeling**: Entrenamiento competitivo de XGBoost y K-Means++.
5.  **Evaluation**: Validación cruzada para asegurar generalización.
6.  **Deployment**: Orquestación maestro vía `run_pipeline.py`.

---

## 🏛️ Arquitectura del Motor (SOLID Engineering)

El motor analítico ha sido construido bajo principios de ingeniería de software:
*   **S (Single Responsibility)**: Código modular desacoplado (ej. `cleaners.py` solo limpia).
*   **O (Open/Closed)**: Arquitectura preparada para añadir nuevos modelos fácilmente.
*   **D (Dependency Inversion)**: Orquestación centralizada para ejecución predecible.

---

## 🔍 Walkthrough Visual: Flujo de Valor

Detalle paso a paso del proceso analítico generado:

### 📊 Fase A: Diagnóstico de Base Instalada
<table border="0">
 <tr>
    <td><b style="font-size:14px">Audit de Integridad</b></td>
    <td><b style="font-size:14px">Perfilamiento Demográfico</b></td>
 </tr>
 <tr>
    <td><img src="reports/figures/00_mapa_nulos.png" width="450"></td>
    <td><img src="reports/figures/01_demografico.png" width="450"></td>
 </tr>
</table>

### 🌐 Fase B: Inteligencia de Entorno (Yelp API)
<table border="0">
 <tr>
    <td><b style="font-size:14px">Exploración de Oferta Exógena</b></td>
    <td><b style="font-size:14px">Cruce Oferta vs. Demanda</b></td>
 </tr>
 <tr>
    <td><img src="reports/figures/06_yelp_overview.png" width="450"></td>
    <td><img src="reports/figures/08_offer_demand.png" width="450"></td>
 </tr>
</table>

### 🧠 Fase C: Modelado Predictivo y ML
<table border="0">
 <tr>
    <td><b style="font-size:14px">Performance XGBoost</b></td>
    <td><b style="font-size:14px">Clustering K-Means++</b></td>
 </tr>
 <tr>
    <td><img src="reports/figures/11_regression_analysis.png" width="450"></td>
    <td><img src="reports/figures/13_clustering_analysis.png" width="450"></td>
 </tr>
</table>

### 🎯 Fase D: Recomendación e Insights de Mercado
<table border="0">
 <tr>
    <td><b style="font-size:14px">Motor de Recomendación 360°</b></td>
    <td><b style="font-size:14px">Oportunidades de Expansión</b></td>
 </tr>
 <tr>
    <td><img src="reports/figures/14_recommender.png" width="450"></td>
    <td><img src="reports/figures/16_market_opportunities.png" width="450"></td>
 </tr>
</table>

---

## 🧹 Ingeniería de Datos y Calidad

Hemos implementado un pipeline de limpieza robusto que maneja:
*   **Imputación Inteligente**: Uso de medianas condicionadas por estrato socioeconómico.
*   **Validación de Esquemas**: Aseguramos consistencia en los tipos de datos.
*   **Tratamiento de Outliers**: Limpieza de señales ruidosas para modelos más estables.

---

## 🧠 Inteligencia Predictiva y ML

### Predicción de Gasto (XGBoost)
Logramos un **R² de 0.85**, permitiendo proyecciones financieras precisas.
<p align="center">
  <img src="reports/figures/11_regression_analysis.png" width="700">
</p>

### Segmentación Psicotográfica (K-Means++)
Identificamos 4 arquetipos de clientes para personalización táctica.
<p align="center">
  <img src="reports/figures/13_clustering_analysis.png" width="700">
</p>

---

## 🌆 Caso de Éxito: Mercado Miami

Miami es nuestro hub estratégico. El análisis detectó una gran oportunidad en el segmento "Casual Quality", donde la oferta local es deficiente según los ratings de Yelp.
<p align="center">
  <img src="reports/figures/05_miami_vs_nacional.png" width="700">
</p>

---

## 📊 Resultados y Dashboard Ejecutivo

Consolidamos toda la inteligencia en un tablero de mando que resume el estado del negocio.

<p align="center">
  <img src="reports/figures/15_executive_dashboard.png" width="900">
  <br>
  <i>Figura 1: Dashboard Ejecutivo Integral — Consolidación de Inteligencia Predictiva y Segmentación.</i>
</p>

---

## 💾 Guía de Operación

1.  **Instalación**: `pip install -r requirements.txt`
2.  **Seguridad**: Configurar las API Keys en el archivo `.env`.
3.  **Ejecución Maestro**: Ejecutar `python run_pipeline.py` para automatización total.

---

## 🚧 Roadmap Estratégico

<p align="center">
  <img src="reports/figures/17_roadmap.png" width="800">
</p>

---

## 👤 Autor y Contacto

**Dody Dueñas**  
*Data Scientist & Analytics Architect*  
*Henry Bootcamp*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/dody-duenas/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dodysalim)
