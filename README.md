# 💎 Cliente360° — InsightReach Analytics
## Plataforma de Inteligencia Predictiva, Segmentación Estratégica y Optimización de Mercado
### *Proyecto Integrador de Nivel Senior Empresarial — Henry Bootcamp*

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
*   **CLV Predictivo**: Proyecciones financieras con >85% de precisión.
*   **Eficiencia en Marketing**: Segmentación algorítmica para optimizar el ROI.
*   **Geomarketing**: Identificación de brechas de oferta externa.

---

## 🔍 Walkthrough Visual: Flujo de Valor

A continuación, se presenta el proceso analítico paso a paso, organizado por áreas de impacto:

### 📊 Fase A: Diagnóstico y Mercado
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

## 📊 Resultados y Dashboard Ejecutivo

El payoff final de toda la tubería analítica es el **Dashboard Integral de Negocio**, donde se consolidan las predicciones financieras con el perfilamiento psicográfico de los clientes.

<p align="center">
  <img src="reports/figures/15_executive_dashboard.png" width="900">
  <br>
  <i>Figura 1: Dashboard Ejecutivo Integral — Consolidación de Inteligencia Predictiva y Segmentación.</i>
</p>

### 💡 Hallazgos Críticos:
- **Impacto Premium**: La membresía aumenta el ticket promedio en un **42%**.
- **Precisión R² de 0.85**: Capacidad predictiva estable para presupuestos anuales.
- **Brechas de Calidad**: 5 zonas identificadas para expansión inmediata basadas en ratings mediocres de la competencia local.

---

## 🏛️ Arquitectura del Motor (SOLID Engineering)

El código ha sido refactorizado bajo estándares industriales:
*   **S (Single Responsibility)**: Módulos específicos e independientes.
*   **O (Open/Closed)**: Arquitectura preparada para el crecimiento.
*   **D (Dependency Inversion)**: Orquestación vía `run_pipeline.py`.

---

## 💾 Guía de Operación

1.  **Instalación**: `pip install -r requirements.txt`
2.  **Seguridad**: Configurar `.env` con las API Keys.
3.  **Ejecución**: `python run_pipeline.py`

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
