"""Configuración global del proyecto."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class Settings:
    """Configuración centralizada del proyecto."""

    # Rutas base
    ROOT_DIR = Path(__file__).parent.parent.absolute()
    DATA_DIR = ROOT_DIR / "data"
    RAW_DATA_DIR = DATA_DIR / "raw"
    EXTERNAL_DATA_DIR = DATA_DIR / "external"
    INTERIM_DATA_DIR = DATA_DIR / "interim"
    PROCESSED_DATA_DIR = DATA_DIR / "processed"
    REPORTS_DIR = ROOT_DIR / "reports"
    NOTEBOOKS_DIR = ROOT_DIR / "notebooks"

    # Credenciales API Yelp
    YELP_CLIENT_ID = os.getenv('CLIENTE_ID', '')
    YELP_API_KEY = os.getenv('API_KEY', '')
    YELP_BASE_URL = "https://api.yelp.com/v3"

    # Configuración de API
    API_TIMEOUT = 30
    API_MAX_RETRIES = 3
    API_RATE_LIMIT_CALLS = 5
    API_RATE_LIMIT_PERIOD = 1  # segundos

    # Configuración de ML
    RANDOM_STATE = 42
    TEST_SIZE = 0.2
    CV_FOLDS = 5

    # Columnas esperadas en datasets
    CUSTOMERS_COLUMNS = [
        'id_persona', 'nombre', 'apellido', 'edad', 'genero',
        'ciudad_residencia', 'estrato_socioeconomico', 'frecuencia_visita',
        'promedio_gasto_comida', 'ocio', 'consume_licor',
        'preferencias_alimenticias', 'membresia_premium',
        'telefono_contacto', 'correo_electronico', 'tipo_de_pago_mas_usado',
        'ingresos_mensuales'
    ]

    YELP_COLUMNS = [
        'alias', 'title', 'id', 'name', 'price', 'rating',
        'review_count', 'distance', 'coordinates_latitude',
        'coordinates_longitude', 'location_address1', 'city'
    ]

    @classmethod
    def ensure_directories(cls):
        """Crear directorios necesarios si no existen."""
        directories = [
            cls.DATA_DIR,
            cls.RAW_DATA_DIR,
            cls.EXTERNAL_DATA_DIR,
            cls.INTERIM_DATA_DIR,
            cls.PROCESSED_DATA_DIR,
            cls.REPORTS_DIR,
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def validate_api_credentials(cls) -> bool:
        """Validar que las credenciales de API estén configuradas."""
        return bool(cls.YELP_API_KEY and cls.YELP_CLIENT_ID)
