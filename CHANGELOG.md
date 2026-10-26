# Changelog

Todos los cambios relevantes de este proyecto se documentan aquí.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y [Versionado Semántico](https://semver.org/lang/es/).

## [1.1.0] - 2026-10-26

### 🔧 Mantenimiento

- **Corregido:** el ETL buscaba el CSV de Yelp en `data/external` y lo omitía en silencio; ahora usa `data/raw` como respaldo y carga los 463 registros (200 establecimientos únicos).
- Nueva prueba automatizada del cargador de Yelp (7 pruebas en total).
- Dependencias separadas en `requirements.txt` (ejecución) y `requirements-dev.txt` (desarrollo); se eliminaron paquetes sin uso.
- CI instala desde `requirements-dev.txt`.
- Licencia MIT, insignias de CI y versión en el README.

