"""Wrappers para endpoints específicos de Yelp API."""
from typing import List, Dict, Optional
from .client import YelpClient
from src.utils.logger import get_logger, log_execution

logger = get_logger(__name__)


class BusinessEndpoints:
    """Endpoints para negocios/businesses."""

    def __init__(self, client: YelpClient):
        self.client = client

    @log_execution()
    def search(
        self,
        location: str,
        term: str = "restaurants",
        limit: int = 50,
        offset: int = 0,
        categories: Optional[str] = None,
        price: Optional[str] = None,
        sort_by: str = "best_match",
        radius: Optional[int] = None
    ) -> Dict:
        """Buscar negocios.

        Args:
            location: Ubicación (ciudad, código postal, etc.)
            term: Término de búsqueda (restaurants, food, etc.)
            limit: Máximo 50
            offset: Para paginación
            categories: Categorías separadas por coma
            price: 1, 2, 3, 4 (separados por coma para múltiples)
            sort_by: best_match, rating, review_count, distance
            radius: Radio en metros (máx 40000)

        Returns:
            Respuesta JSON de la API
        """
        params = {
            'location': location,
            'term': term,
            'limit': min(limit, 50),
            'offset': offset,
            'sort_by': sort_by
        }

        if categories:
            params['categories'] = categories
        if price:
            params['price'] = price
        if radius:
            params['radius'] = min(radius, 40000)

        return self.client.get('businesses/search', params=params)

    @log_execution()
    def get_details(self, business_id: str) -> Dict:
        """Obtener detalles de un negocio.

        Args:
            business_id: ID del negocio

        Returns:
            Detalles del negocio
        """
        return self.client.get(f'businesses/{business_id}')

    @log_execution()
    def search_all_pages(
        self,
        location: str,
        term: str = "restaurants",
        max_results: int = 200,
        **kwargs
    ) -> List[Dict]:
        """Buscar negocios paginando automáticamente.

        Args:
            location: Ubicación
            term: Término de búsqueda
            max_results: Máximo de resultados a obtener
            **kwargs: Argumentos adicionales para search

        Returns:
            Lista de negocios
        """
        all_businesses = []
        offset = 0
        limit = 50

        while len(all_businesses) < max_results:
            response = self.search(
                location=location,
                term=term,
                limit=limit,
                offset=offset,
                **kwargs
            )

            businesses = response.get('businesses', [])
            if not businesses:
                break

            all_businesses.extend(businesses)

            # Verificar si hay más páginas
            total = response.get('total', 0)
            if offset + limit >= total or offset + limit >= max_results:
                break

            offset += limit

        logger.info(f"Obtenidos {len(all_businesses)} negocios de {location}")
        return all_businesses[:max_results]


class ReviewEndpoints:
    """Endpoints para reviews."""

    def __init__(self, client: YelpClient):
        self.client = client

    @log_execution()
    def get_reviews(
        self,
        business_id: str,
        limit: int = 3,
        sort_by: str = "newest"
    ) -> Dict:
        """Obtener reviews de un negocio.

        Args:
            business_id: ID del negocio
            limit: Cantidad de reviews (máx 3 por request)
            sort_by: newest, oldest, rating

        Returns:
            Reviews del negocio
        """
        params = {
            'limit': min(limit, 3),
            'sort_by': sort_by
        }

        return self.client.get(f'businesses/{business_id}/reviews', params=params)


class AutocompleteEndpoints:
    """Endpoints de autocompletado."""

    def __init__(self, client: YelpClient):
        self.client = client

    def autocomplete(self, text: str, latitude: Optional[float] = None,
                     longitude: Optional[float] = None) -> Dict:
        """Autocompletar búsquedas.

        Args:
            text: Texto parcial
            latitude: Latitud opcional
            longitude: Longitud opcional

        Returns:
            Sugerencias de autocompletado
        """
        params = {'text': text}
        if latitude and longitude:
            params['latitude'] = latitude
            params['longitude'] = longitude

        return self.client.get('autocomplete', params=params)


class CategoryEndpoints:
    """Endpoints de categorías."""

    def __init__(self, client: YelpClient):
        self.client = client

    def get_categories(self, locale: str = "en_US") -> Dict:
        """Obtener todas las categorías disponibles.

        Args:
            locale: Locale para nombres de categorías

        Returns:
            Lista de categorías
        """
        params = {'locale': locale}
        return self.client.get('categories', params=params)

    def get_category_details(self, alias: str, locale: str = "en_US") -> Dict:
        """Obtener detalles de una categoría.

        Args:
            alias: Alias de la categoría
            locale: Locale

        Returns:
            Detalles de la categoría
        """
        params = {'locale': locale}
        return self.client.get(f'categories/{alias}', params=params)


class EventEndpoints:
    """Endpoints para eventos."""

    def __init__(self, client: YelpClient):
        self.client = client

    def search_events(
        self,
        location: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        categories: Optional[str] = None,
        limit: int = 50
    ) -> Dict:
        """Buscar eventos.

        Args:
            location: Ubicación
            start_date: Fecha inicio (YYYY-MM-DD)
            end_date: Fecha fin (YYYY-MM-DD)
            categories: Categorías
            limit: Límite de resultados

        Returns:
            Eventos encontrados
        """
        params = {'limit': limit}

        if location:
            params['location'] = location
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        if categories:
            params['categories'] = categories

        return self.client.get('events', params=params)

    def get_event_details(self, event_id: str) -> Dict:
        """Obtener detalles de un evento.

        Args:
            event_id: ID del evento

        Returns:
            Detalles del evento
        """
        return self.client.get(f'events/{event_id}')
