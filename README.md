<p align="center"><img src="https://dodysalim.github.io/assets/project-covers/cliente360.webp" alt="Cliente360" width="100%"></p>

<h1 align="center">Cliente360</h1>

<p align="center"><b>Limpieza, segmentación y modelos para entender clientes y oportunidades de mercado.</b></p>

<p align="center">
<img src="https://img.shields.io/badge/Henry_%C2%B7_Proyecto_integrador-75E6CE?style=for-the-badge&labelColor=0b1222" alt="Henry · Proyecto integrador">
</p>

<p align="center">
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="pandas"> <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white" alt="scikit-learn"> <img src="https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white" alt="Jupyter"> <img src="https://img.shields.io/badge/Power_BI-F2C811?style=flat-square&logoColor=black" alt="Power BI">
</p>

<p align="center">
<a href="https://github.com/dodysalim/Cliente360-Predictive-Insight/actions"><img src="https://github.com/dodysalim/Cliente360-Predictive-Insight/actions/workflows/local-tests.yml/badge.svg" alt="CI"></a> <img src="https://img.shields.io/badge/versión-1.1.0-8F7BFF?style=flat-square" alt="Versión 1.1.0"> <img src="https://img.shields.io/badge/licencia-MIT-30405B?style=flat-square" alt="Licencia MIT">
</p>

<p align="center"><a href="https://dodysalim.github.io/"><b>🌐 Portafolio</b></a> · <a href="docs/PORTFOLIO_CASE.md"><b>📄 Caso de estudio</b></a> · <a href="docs/VALIDATION.md"><b>✅ Verificación</b></a></p>

---

## 📌 Resumen en 30 segundos

| | |
| --- | --- |
| **🎯 Problema** | Identificar perfiles de clientes y qué conclusiones permite realmente la cobertura de los datos. |
| **🛠️ Solución** | Pipeline ETL, ingeniería de características, regresión y clustering, organizado por etapas. |
| **📈 Entregables** | Informe ejecutivo y dashboard Power BI de 5 páginas. |
| **🧪 Calidad** | 7 pruebas automatizadas de carga, datos y regresión. |
| **👤 Autor** | Dody Dueñas Remache. |

## ❓ La pregunta de negocio

¿Qué perfiles aparecen entre los clientes y qué conclusiones permite realmente la cobertura de los datos?

## ✨ Qué incluye

- ETL, ingeniería de características, regresión y clustering.
- Notebooks por etapa, comparativas de modelos y tablas procesadas.
- Informe ejecutivo y dashboard Power BI con cinco páginas.

## 🚀 Cómo ejecutarlo

Usa Python 3.11 o 3.12 en un entorno independiente. Desde la raíz:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
# Para pruebas y desarrollo:
python -m pip install -r requirements-dev.txt
```

Después de configurar los datos:

```bash
python -m pytest tests -q
# Para ejecutar los notebooks completos, con sus datos disponibles:
python run_pipeline.py
```

## 🗂️ Datos y configuración

Datos y resultados procesados presentes. La cobertura de Yelp utilizada en Power BI corresponde a Miami, con 200 establecimientos únicos; no permite comparar otras ciudades con Yelp.

## 📊 Power BI · PC y móvil

[Archivos e instrucciones](powerbi/README.md). Descarga el repositorio completo y abre `powerbi/Abrir-PowerBI.bat` en Windows; después pulsa **Actualizar**. Incluye A4 horizontal a tamaño real (100 %) y diseño móvil vertical. El archivo `.pbip` necesita sus carpetas Report, SemanticModel y data.

## 🧭 Estructura del repositorio

| Ruta | Qué contiene |
| --- | --- |
| [notebooks/](notebooks/) | Exploración y modelado |
| [src/](src/) | Componentes del pipeline |
| [data/processed/](data/processed/) | Resultados procesados |
| [reports/](reports/) | Tablas, figuras e informe |
| [tests/](tests/) | Pruebas de carga y regresión |

## ✅ Calidad y alcance

Siete pruebas aprobadas, incluida la del cargador de Yelp. Las tablas y el modelo Power BI se verificaron en la entrega de BI anterior.

No se volvió a ejecutar aquí la cadena completa de cinco notebooks. Los clientes son datos de formación; no se afirma impacto comercial realizado.

Para repetir las pruebas desde la raíz:

```bash
python -m pytest tests -q
```

## 👥 Autoría

Proyecto académico Henry. Dody Salim Dueñas Remache.

[Documentación anterior](docs/ORIGINAL_README.md), conservada como referencia histórica.

---

<p align="center">
<b>Dody Dueñas Remache</b> · Analista de Datos / Data Scientist<br>
<a href="https://dodysalim.github.io/">Portafolio</a> · <a href="https://github.com/dodysalim">GitHub</a> · <a href="https://www.linkedin.com/in/dody-duenas/">LinkedIn</a> · <a href="mailto:dodydurema67@gmail.com">dodydurema67@gmail.com</a>
</p>
