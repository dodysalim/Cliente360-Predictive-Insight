"""Cargadores de datos con manejo robusto de excepciones."""
import pandas as pd
import requests
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, Any, List
import json

from config.settings import Settings
from src.utils.exceptions import DataLoadError, APIConnectionError, APIRateLimitError
from src.utils.logger import get_logger, log_execution
from src.utils.validators import DataValidator

logger = get_logger(__name__)


class BaseDataLoader(ABC):
    """Clase base abstracta para cargadores de datos (Principio SOLID: LSP, ISP)."""

    def __init__(self, validator: Optional[DataValidator] = None):
        self.validator = validator
        self._data = None

    @abstractmethod
    def load(self, source: Any, **kwargs) -> pd.DataFrame:
        """Método abstracto para cargar datos."""
        pass

    def validate(self, df: pd.DataFrame) -> bool:
        """Validar datos cargados."""
        if self.validator:
            return self.validator.validate_columns(df)
        return True


class CustomerDataLoader(BaseDataLoader):
    """Cargador de datos de clientes desde CSV."""

    def __init__(self, validator: Optional[DataValidator] = None):
        super().__init__(validator)
        self.expected_columns = Settings.CUSTOMERS_COLUMNS

    @log_execution()
    def load(self, file_path: str, encoding: str = 'utf-8', **kwargs) -> pd.DataFrame:
        """Cargar datos de clientes desde archivo CSV.

        Args:
            file_path: Ruta al archivo CSV
            encoding: Codificación del archivo
            **kwargs: Argumentos adicionales para pd.read_csv

        Returns:
            DataFrame con datos de clientes

        Raises:
            DataLoadError: Si hay error al cargar el archivo
        """
        try:
            path = Path(file_path)
            if not path.exists():
                raise DataLoadError(
                    f"Archivo no encontrado: {file_path}",
                    file_path=str(file_path)
                )

            logger.info(f"Cargando datos de clientes desde: {file_path}")

            df = pd.read_csv(
                path,
                encoding=encoding,
                low_memory=False,
                **kwargs
            )

            logger.info(f"Datos cargados exitosamente: {len(df)} filas, {len(df.columns)} columnas")

            # Validar columnas esperadas
            if self.validator:
                self.validator.validate_columns(df)

            self._data = df
            return df

        except pd.errors.EmptyDataError:
            error_msg = f"El archivo está vacío: {file_path}"
            logger.error(error_msg)
            raise DataLoadError(error_msg, file_path=str(file_path))

        except pd.errors.ParserError as e:
            error_msg = f"Error de parseo en {file_path}: {str(e)}"
            logger.error(error_msg)
            raise DataLoadError(error_msg, file_path=str(file_path))

        except Exception as e:
            error_msg = f"Error inesperado al cargar {file_path}: {str(e)}"
            logger.error(error_msg)
            raise DataLoadError(error_msg, file_path=str(file_path))

    @log_execution()
    def load_from_raw(self, filename: str = "base_datos_restaurantes_USA_v2 (1).csv") -> pd.DataFrame:
        """Cargar archivo desde directorio raw."""
        file_path = Settings.RAW_DATA_DIR / filename
        return self.load(file_path)


class YelpDataLoader(BaseDataLoader):
    """Cargador de datos de Yelp desde CSV."""

    def __init__(self, validator: Optional[DataValidator] = None):
        super().__init__(validator)
        self.expected_columns = Settings.YELP_COLUMNS

    @log_execution()
    def load(self, file_path: str, **kwargs) -> pd.DataFrame:
        """Cargar datos de Yelp desde archivo CSV.

        Args:
            file_path: Ruta al archivo CSV
            **kwargs: Argumentos adicionales

        Returns:
            DataFrame con datos de Yelp
        """
        try:
            path = Path(file_path)
            logger.info(f"Cargando datos de Yelp desde: {file_path}")

            df = pd.read_csv(path, low_memory=False, **kwargs)

            logger.info(f"Datos de Yelp cargados: {len(df)} filas")
            self._data = df
            return df

        except Exception as e:
            error_msg = f"Error al cargar datos de Yelp: {str(e)}"
            logger.error(error_msg)
            raise DataLoadError(error_msg, file_path=str(file_path))

    @log_execution()
    def load_from_external(self, filename: str = "yelp_restaurants (2).csv") -> pd.DataFrame:
        """Cargar archivo desde directorio external."""
        file_path = Settings.EXTERNAL_DATA_DIR / filename
        return self.load(file_path)


class APIDataLoader:
    """Cargador de datos desde API Yelp con retry logic y rate limiting."""

    def __init__(self):
        self.api_key = Settings.YELP_API_KEY
        self.client_id = Settings.YELP_CLIENT_ID
        self.base_url = Settings.YELP_BASE_URL
        self.timeout = Settings.API_TIMEOUT
        self.max_retries = Settings.API_MAX_RETRIES
        self._last_request_time = 0

        if not Settings.validate_api_credentials():
            logger.warning("Credenciales de API no configuradas correctamente")

    def _get_headers(self) -> Dict[str, str]:
        """Obtener headers para autenticación."""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def _apply_rate_limit(self):
        """Aplicar rate limiting entre requests."""
        current_time = time.time()
        time_since_last = current_time - self._last_request_time

        if time_since_last < Settings.API_RATE_LIMIT_PERIOD:
            sleep_time = Settings.API_RATE_LIMIT_PERIOD - time_since_last
            time.sleep(sleep_time)

        self._last_request_time = time.time()

    @log_execution()
    def fetch_businesses(
        self,
        location: str,
        term: str = "restaurants",
        limit: int = 50,
        offset: int = 0,
        categories: Optional[str] = None
    ) -> List[Dict]:
        """Obtener negocios de Yelp API.

        Args:
            location: Ubicación (ciudad)
            term: Término de búsqueda
            limit: Límite de resultados (máx 50)
            offset: Offset para paginación
            categories: Categorías separadas por coma

        Returns:
            Lista de negocios

        Raises:
            APIConnectionError: Si hay error de conexión
            APIRateLimitError: Si se excede el rate limit
        """
        endpoint = f"{self.base_url}/businesses/search"

        params = {
            'location': location,
            'term': term,
            'limit': min(limit, 50),
            'offset': offset
        }

        if categories:
            params['categories'] = categories

        for attempt in range(self.max_retries):
            try:
                self._apply_rate_limit()

                logger.debug(f"Request {attempt + 1}/{self.max_retries}: {endpoint}")

                response = requests.get(
                    endpoint,
                    headers=self._get_headers(),
                    params=params,
                    timeout=self.timeout
                )

                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 60))
                    logger.warning(f"Rate limit alcanzado. Esperando {retry_after}s")
                    raise APIRateLimitError(retry_after=retry_after)

                response.raise_for_status()

                data = response.json()
                businesses = data.get('businesses', [])

                logger.info(f"Obtenidos {len(businesses)} negocios de Yelp")
                return businesses

            except APIRateLimitError:
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Backoff exponencial
                else:
                    raise

            except requests.exceptions.RequestException as e:
                logger.error(f"Error de conexión: {str(e)}")
                if attempt == self.max_retries - 1:
                    raise APIConnectionError(
                        f"Error al conectar con API después de {self.max_retries} intentos: {str(e)}"
                    )
                time.sleep(2 ** attempt)

        return []

    @log_execution()
    def fetch_business_details(self, business_id: str) -> Dict:
        """Obtener detalles de un negocio específico.

        Args:
            business_id: ID del negocio

        Returns:
            Diccionario con detalles del negocio
        """
        endpoint = f"{self.base_url}/businesses/{business_id}"

        try:
            self._apply_rate_limit()

            response = requests.get(
                endpoint,
                headers=self._get_headers(),
                timeout=self.timeout
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error obteniendo detalles de negocio {business_id}: {str(e)}")
            raise APIConnectionError(f"Error al obtener detalles: {str(e)}")

    @log_execution()
    def fetch_reviews(self, business_id: str, limit: int = 3) -> List[Dict]:
        """Obtener reviews de un negocio.

        Args:
            business_id: ID del negocio
            limit: Cantidad de reviews

        Returns:
            Lista de reviews
        """
        endpoint = f"{self.base_url}/businesses/{business_id}/reviews"

        try:
            self._apply_rate_limit()

            response = requests.get(
                endpoint,
                headers=self._get_headers(),
                params={'limit': limit},
                timeout=self.timeout
            )

            response.raise_for_status()
            data = response.json()
            return data.get('reviews', [])

        except requests.exceptions.RequestException as e:
            logger.error(f"Error obteniendo reviews: {str(e)}")
            return []
