"""Cliente HTTP para Yelp API con manejo robusto de errores."""
import requests
import time
from typing import Optional, Dict, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config.settings import Settings
from src.utils.exceptions import APIConnectionError, APIRateLimitError, APIAuthenticationError
from src.utils.logger import get_logger

logger = get_logger(__name__)


class YelpClient:
    """Cliente seguro para Yelp Fusion API.

    Implementa:
    - Retry automático con backoff exponencial
    - Rate limiting
    - Manejo de errores específicos
    - Logging detallado
    """

    def __init__(self):
        self.api_key = Settings.YELP_API_KEY
        self.client_id = Settings.YELP_CLIENT_ID
        self.base_url = Settings.YELP_BASE_URL
        self.timeout = Settings.API_TIMEOUT

        self._session = requests.Session()
        self._last_request_time = 0
        self._request_count = 0

        # Configurar retry strategy
        self._setup_retry_strategy()

        # Validar credenciales
        if not self._validate_credentials():
            logger.error("Credenciales de API no válidas")
            raise APIAuthenticationError("API_KEY o CLIENT_ID no configurados")

    def _setup_retry_strategy(self):
        """Configurar estrategia de retry con backoff."""
        retry_strategy = Retry(
            total=Settings.API_MAX_RETRIES,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self._session.mount("http://", adapter)
        self._session.mount("https://", adapter)

    def _validate_credentials(self) -> bool:
        """Validar que las credenciales estén configuradas."""
        return bool(self.api_key and self.client_id)

    def _get_headers(self) -> Dict[str, str]:
        """Obtener headers de autenticación."""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def _apply_rate_limit(self):
        """Aplicar rate limiting simple."""
        current_time = time.time()
        time_since_last = current_time - self._last_request_time

        if time_since_last < Settings.API_RATE_LIMIT_PERIOD:
            sleep_time = Settings.API_RATE_LIMIT_PERIOD - time_since_last
            logger.debug(f"Rate limiting: esperando {sleep_time:.2f}s")
            time.sleep(sleep_time)

        self._last_request_time = time.time()
        self._request_count += 1

    def request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Realizar request HTTP con manejo de errores.

        Args:
            method: Método HTTP
            endpoint: Endpoint (ej: 'businesses/search')
            **kwargs: Argumentos adicionales para requests

        Returns:
            JSON response como diccionario

        Raises:
            APIConnectionError: Si hay error de conexión
            APIRateLimitError: Si se excede rate limit
            APIAuthenticationError: Si hay error de autenticación
        """
        url = f"{self.base_url}/{endpoint}"

        # Aplicar headers por defecto
        headers = self._get_headers()
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))

        try:
            # Rate limiting
            self._apply_rate_limit()

            logger.debug(f"{method} {url}")

            response = self._session.request(
                method=method,
                url=url,
                headers=headers,
                timeout=self.timeout,
                **kwargs
            )

            # Manejar errores HTTP
            if response.status_code == 401:
                raise APIAuthenticationError("Token de autenticación inválido")

            if response.status_code == 403:
                raise APIAuthenticationError("Sin permisos para acceder a este recurso")

            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                raise APIRateLimitError(
                    f"Rate limit excedido. Retry-After: {retry_after}s",
                    retry_after=retry_after
                )

            response.raise_for_status()

            logger.debug(f"Response {response.status_code}: {len(response.content)} bytes")
            return response.json()

        except requests.exceptions.Timeout:
            logger.error(f"Timeout en request a {url}")
            raise APIConnectionError(f"Timeout después de {self.timeout}s", status_code=408)

        except requests.exceptions.ConnectionError as e:
            logger.error(f"Error de conexión: {str(e)}")
            raise APIConnectionError(f"Error de conexión: {str(e)}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Error en request: {str(e)}")
            raise APIConnectionError(f"Error en request: {str(e)}")

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """GET request simplificado."""
        return self.request('GET', endpoint, params=params)

    def close(self):
        """Cerrar sesión HTTP."""
        self._session.close()
        logger.info(f"Cliente cerrado. Total requests: {self._request_count}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
