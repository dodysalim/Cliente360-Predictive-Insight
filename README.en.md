<p align="center"><img src="https://dodysalim.github.io/assets/project-covers/cliente360.webp" alt="Cliente360" width="100%"></p>

<h1 align="center">Cliente360</h1>

<p align="center"><b>Data cleaning, segmentation and models to understand customers and market opportunities.</b></p>

<p align="center"><img src="https://img.shields.io/badge/Henry_·_Capstone_project-75E6CE?style=for-the-badge&labelColor=0b1222" alt="Henry · Capstone project"></p>

<p align="center">
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="pandas"> <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white" alt="scikit-learn"> <img src="https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white" alt="Jupyter"> <img src="https://img.shields.io/badge/Power_BI-F2C811?style=flat-square&logoColor=black" alt="Power BI">
</p>

<p align="center"><a href="https://dodysalim.github.io/"><b>🌐 Portfolio</b></a> · <a href="README.md"><b>🇪🇸 Versión en español</b></a></p>

---

## 📌 At a glance

| | |
| --- | --- |
| **🎯 Problem** | Identify customer profiles and what conclusions the data coverage really supports. |
| **🛠️ Solution** | Staged ETL pipeline, feature engineering, regression and clustering. |
| **📈 Deliverables** | Executive report and a 5-page Power BI dashboard. |
| **🧪 Quality** | 7 automated tests, including the Yelp loader fixed in v1.1.0. |

## 🏗️ Architecture

```mermaid
flowchart LR
    RAW[(CSV de clientes<br/>30.000 registros)] --> LD[loaders]
    YELP[(Yelp · Miami)] --> LD
    LD --> CL[cleaners] --> TR[transformers]
    TR --> FB[features/builders<br/>+ selectors] --> MD[models<br/>regresión y clustering]
    MD --> EV[evaluation]
    TR --> PROC[(data/processed)]
    PROC --> PBI[Power BI · 5 páginas]
    EV --> RPT[Informe ejecutivo]
```

## 🚀 How to run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python scripts/run_etl.py --no-save
python -m pytest tests -q
```

## ⚖️ Scope

Training data; no realized business impact is claimed. Yelp coverage is Miami only (200 unique venues).

---

<p align="center">
<b>Dody Dueñas Remache</b> · Data Analyst / Data Scientist · Guayaquil, Ecuador (remote LATAM)<br>
<a href="https://dodysalim.github.io/">Portfolio</a> · <a href="https://github.com/dodysalim">GitHub</a> · <a href="https://www.linkedin.com/in/dody-duenas/">LinkedIn</a> · <a href="mailto:dodydurema67@gmail.com">dodydurema67@gmail.com</a>
</p>
