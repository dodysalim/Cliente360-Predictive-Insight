# 💎 Cliente360° — InsightReach Analytics
## Plataforma de Inteligencia Predictiva, Segmentación Estratégica y Optimización de Mercado
### *Proyecto Integrador de Nivel Senior Empresarial — Henry Bootcamp*

---

## 📑 Índice de Contenidos

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

**Cliente360°** representa la culminación de un proceso de ingeniería de datos y ciencia de datos aplicada a la resolución de problemas complejos de crecimiento corporativo. No se trata simplemente de un conjunto de scripts, sino de un **entorno de inteligencia** diseñado para extraer valor accionable de la interacción entre los clientes y su entorno urbano.

El núcleo del sistema utiliza una combinación de **ML supervisado** e **Inteligencia Geo-espacial** (Yelp Fusion API) para extraer valor accionable del comportamiento de los consumidores.

---

## 🎯 El Desafío de Negocio: Visión 360°

La organización enfrentaba problemas de **Ceguera Transaccional**, **Marketing Ineficiente** y **Desconexión con el Entorno**. Este proyecto aborda estos retos mediante:
*   **CLV Predictivo**: Proyecciones financieras con un **R² de 0.85**.
*   **Eficiencia en Marketing**: Segmentación algorítmica para optimizar el CAC.
*   **Geomarketing**: Identificación de brechas de oferta externa en ciudades clave.

---

## 🌳 Estructura de Activos y Gobernanza

La organización del proyecto sigue estándares internacionales, donde cada carpeta tiene un propósito definido:

```bash
Proyecto_Integrador_Dody_Empresarial/
├── config/                     # ⚙️ Configuración centralizada y logging.
├── data/                       # 📂 Data Lake (Raw, External, Interim, Processed).
├── notebooks/                  # 📊 Reportes Analíticos (EDA -> Insights).
├── src/                        # 🛠️ Engine modular (SOLID Architecture).
├── reports/                    # 📈 Outputs de Negocio (Figuras y Tablas).
├── run_pipeline.py             # 🚀 Master Orquestador (Automatización Total).
└── requirements.txt            # Contrato de dependencias.
```

---

## 🛠️ Metodología de Implementación: CRISP-DM Senior

Hemos aplicado una versión profesional de **CRISP-DM** para garantizar resultados:
1.  **Entendimiento del Negocio**: Definición del "Gasto Predictivo" como KPI estrella.
2.  **Entendimiento de los Datos**: Auditoría de 25+ campos y diagnóstico de sesgos (NB 01).
3.  **Preparación**: Automatización de la limpieza y Feature Engineering (NB 03).
4.  **Modelado**: Evaluación competitiva de modelos (XGBoost vs RandomForest).
5.  **Evaluación**: Validación cruzada estratificada.
6.  **Despliegue**: Orquestación vía `run_pipeline.py`.

---

## 🏛️ Arquitectura del Motor (SOLID Engineering)

El sistema ha sido construido bajo principios de ingeniería de software para garantizar su escalabilidad:
*   **S (Single Responsibility)**: Código modular desacoplado por función.
*   **O (Open/Closed)**: Arquitectura preparada para añadir nuevos modelos.
*   **D (Dependency Inversion)**: Orquestación centralizada para ejecución sin errores.

---

## 🔍 Walkthrough Visual: Flujo de Valor

A continuación, se detalla el proceso analítico paso a paso del proyecto:

### 📊 Fase A: Diagnóstico de Base Instalada
Iniciamos con una auditoría profunda de la calidad de información y perfilamiento demográfico.
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
Cruzamos la ubicación de nuestros clientes con los clusters de competencia para detectar brechas de oferta.
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

### 🎯 Fase C: Entrega de Valor y Recomendación
El resultado final permite al negocio ofrecer el producto ideal al cliente correcto.
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

Hemos implementado un pipeline de limpieza robusto en `src/data` que maneja:
*   **Imputación Inteligente**: Uso de medianas condicionadas por estrato socioeconómico.
*   **Validación de Esquemas**: Aseguramos que los datos de entrada cumplan los tipos estadísticos necesarios.
*   **Tratamiento de Outliers**: Limpieza de valores extremos en ingresos y gastos para no sesgar los modelos.

---

## 🧠 Inteligencia Predictiva y ML

### Predicción de Gasto (XGBoost)
Logramos un **R² de 0.85**, permitiendo proyecciones financieras de alta fidelidad basadas en el perfil socioeconómico.
<p align="center">
  <img src="reports/figures/11_regression_analysis.png" width="700">
</p>

### Segmentación Psicotográfica (K-Means++)
Identificamos 4 arquetipos de clientes para personalizar la comunicación de marketing.
<p align="center">
  <img src="reports/figures/13_clustering_analysis.png" width="700">
</p>

---

## 🌆 Caso de Éxito: Mercado Miami

Miami es nuestro hub de mayor margen potencial. El análisis detectó una brecha significativa: existe una saturación de oferta "Premium", pero una oportunidad masiva en el segmento "Casual Quality" para nuestros clientes.
<p align="center">
  <img src="reports/figures/05_miami_vs_nacional.png" width="700">
</p>

---

## 📊 Resultados y Dashboard Ejecutivo

Consolidamos toda la inteligencia en un tablero de mando que permite a la dirección actuar de inmediato sobre los segmentos de mayor valor.

<p align="center">
  <img src="reports/figures/15_executive_dashboard.png" width="900">
  <br>
  <i>Figura 1: Dashboard Ejecutivo Integral — Consolidación de Inteligencia Predictiva y Segmentación.</i>
</p>

---

## 💾 Guía de Operación

1.  **Instalación**: `pip install -r requirements.txt`
2.  **Seguridad**: Configurar las API Keys en el archivo `.env`.
3.  **Ejecución Maestro**: Ejecutar `python run_pipeline.py` para procesar todo de principio a fin automáticamente.

---

## 🚧 Roadmap Estratégico

<p align="center">
  <img src="reports/figures/17_roadmap.png" width="800">
  <br>
  <i>Del análisis descriptivo a la Inteligencia en Tiempo Real.</i>
</p>

---

## 👤 Autor y Contacto

**Dody Dueñas**  
*Data Scientist & Analytics Architect*  
*Henry Bootcamp*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/dody-duenas/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dodysalim)
