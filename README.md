# 💎 Cliente360° — InsightReach Analytics
## Plataforma de Inteligencia Predictiva, Segmentación Estratégica y Optimización de Mercado
### *Proyecto Integrador de Nivel Senior Empresarial — Henry Bootcamp*

---

<p align="center">
  <img src="reports/figures/15_executive_dashboard.png" width="900">
  <br>
  <i>Figura 1: Dashboard Ejecutivo Integral — Vista consolidada de KPIs, Predicciones de Gasto y Segmentación de Mercado.</i>
</p>

---

## 📑 Índice de Contenidos Extendido

1.  [📌 Resumen Ejecutivo de Alta Dirección](#-resumen-ejecutivo-de-alta-dirección)
2.  [🎯 El Desafío de Negocio: Visión 360°](#-el-desafío-de-negocio-visión-360)
3.  [🌳 Estructura de Activos y Gobernanza](#-estructura-de-activos-y-gobernanza)
4.  [🛠️ Metodología de Implementación: CRISP-DM Senior](#-metodología-de-implementación-crisp-dm-senior)
5.  [🏛️ Arquitectura del Motor (SOLID Engineering)](#-arquitectura-del-motor-solid-engineering)
6.  [🔍 Walkthrough Visual: Flujo de Valor](#-walkthrough-visual-flujo-de-valor)
7.  [🧹 Ingeniería de Datos y Calidad](#-ingeniería-de-datos-y-calidad)
8.  [🧠 Inteligencia Predictiva y ML](#-inteligencia-predictiva-y-ml)
9.  [🌆 Caso de Éxito: Mercado Miami](#-caso-de-éxito-mercado-miami)
10. [📊 Resultados y Hallazgos de Negocio](#-resultados-y-hallazgos-de-negocio)
11. [💾 Guía de Operación](#-guía-de-operación)
12. [🚧 Roadmap Estratégico](#-roadmap-estratégico)
13. [👤 Autor y Contacto](#-autor-y-contacto)

---

## 📌 Resumen Ejecutivo de Alta Dirección

**Cliente360°** representa la culminación de un proceso de ingeniería de datos y ciencia de datos aplicada a la resolución de problemas complejos de crecimiento corporativo. El sistema utiliza una triada de **ML Supervisado**, **ML No Supervisado** e **Inteligencia Geo-espacial** (Yelp Fusion API) para extraer valor accionable del comportamiento de los consumidores.

---

## 🎯 El Desafío de Negocio: Visión 360°

La organización enfrentaba problemas de **Ceguera Transaccional**, **Marketing Ineficiente** y **Desconexión con el Entorno**. Este proyecto aborda estos retos mediante:
*   **CLV Predictivo**: Proyecciones financieras con >85% de precisión.
*   **Eficiencia en Marketing**: Segmentación algorítmica para optimizar el ROI.
*   **Geomarketing**: Identificación de brechas de oferta externa.

---

## 🔍 Walkthrough Visual: Flujo de Valor

A continuación, se presenta el proceso analítico paso a paso, organizado por áreas de impacto:

### 📊 Fase A: Diagnóstico y Mercado
Entender quién es el cliente y cómo se posiciona en mercados clave como Miami.

<table border="0">
 <tr>
    <td><b style="font-size:14px">Distribución Demográfica</b></td>
    <td><b style="font-size:14px">Análisis de Mercado (Miami)</b></td>
 </tr>
 <tr>
    <td><img src="reports/figures/01_demografico.png" width="450"></td>
    <td><img src="reports/figures/05_miami_vs_nacional.png" width="450"></td>
 </tr>
</table>

### 🌐 Fase B: Inteligencia de Oferta (Yelp API)
Enriquecimiento con datos exógenos para auditar la competencia local y los ratings de la zona.

<table border="0">
 <tr>
    <td><b style="font-size:14px">Exploración de Oferta (Yelp)</b></td>
    <td><b style="font-size:14px">Cruce Oferta vs. Demanda</b></td>
 </tr>
 <tr>
    <td><img src="reports/figures/06_yelp_overview.png" width="450"></td>
    <td><img src="reports/figures/08_offer_demand.png" width="450"></td>
 </tr>
</table>

### 🧠 Fase C: Modelado Avanzado y ML
Predicción de gasto mediante Gradient Boosting y descubrimiento de segmentos via K-Means.

<table border="0">
 <tr>
    <td><b style="font-size:14px">Evaluación de Regresión (XGBoost)</b></td>
    <td><b style="font-size:14px">Discovery de Segmentos</b></td>
 </tr>
 <tr>
    <td><img src="reports/figures/11_regression_analysis.png" width="450"></td>
    <td><img src="reports/figures/13_clustering_analysis.png" width="450"></td>
 </tr>
</table>

### 🎯 Fase D: Entrega de Valor al Negocio
El resultado final: recomendaciones personalizadas y el dashboard de toma de decisiones.

<table border="0">
 <tr>
    <td><b style="font-size:14px">Sistema de Recomendación 360°</b></td>
    <td><b style="font-size:14px">Oportunidades Detectadas</b></td>
 </tr>
 <tr>
    <td><img src="reports/figures/14_recommender.png" width="450"></td>
    <td><img src="reports/figures/16_market_opportunities.png" width="450"></td>
 </tr>
</table>

---

## 🏛️ Arquitectura del Motor (SOLID Engineering)

El código ha sido refactorizado bajo estándares industriales, permitiendo escalabilidad y desacoplamiento total:

*   **S (Single Responsibility)**: Módulos específicos para limpieza, API y modelado.
*   **O (Open/Closed)**: Fácil integración de nuevos algoritmos (ej. LightGBM).
*   **D (Dependency Inversion)**: Orquestación centralizada en `run_pipeline.py`.

---

## 📊 Resultados y Hallazgos de Negocio

> [!TIP]
> **Insight Principal**: La membresía Premium es el mayor predictor de gasto, aumentando el ticket promedio en un **42%**, independientemente del nivel de ingresos.

- **4 Segmentos Claros**: Del cliente "Elite" al cliente "Oportunidad Miami".
- **Precisión R² de 0.85**: Capacidad robusta de proyecciones financieras.
- **Detección de Brechas**: Identificamos 5 zonas con saturación de oferta premium pero alta demanda casual insatisfecha.

---

## 💾 Guía de Operación

1.  **Configuración**: `pip install -r requirements.txt`
2.  **Credenciales**: Configurar `.env` con las claves de Yelp.
3.  **Ejecución**: `python run_pipeline.py` (Procesamiento completo de 0 a 100).

---

## 🚧 Roadmap Estratégico

<p align="center">
  <img src="reports/figures/17_roadmap.png" width="800">
  <br>
  <i>Planificación a 24 meses: Del análisis estático hacia la Inteligencia en Tiempo Real.</i>
</p>

---

## 👤 Autor y Contacto

**Dody Dueñas**  
*Data Scientist & Analytics Architect*  
*Proyecto Integrador Empresarial — Henry Bootcamp*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/dody-duenas/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dodysalim)

---

> **Nota final**: Este proyecto está diseñado para funcionar en entornos de producción, garantizando la trazabilidad y reproducibilidad de los resultados.
