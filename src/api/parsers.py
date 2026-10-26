"""Parsers para transformar respuestas de API a DataFrames."""
import pandas as pd
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

from src.utils.logger import get_logger

logger = get_logger(__name__)


class YelpResponseParser(ABC):
    """Parser base para respuestas de Yelp API."""

    @abstractmethod
    def parse(self, response: Dict) -> pd.DataFrame:
        """Parsear respuesta a DataFrame."""
        pass

    @abstractmethod
    def parse_list(self, items: List[Dict]) -> pd.DataFrame:
        """Parsear lista de items a DataFrame."""
        pass


class BusinessParser(YelpResponseParser):
    """Parser para datos de negocios."""

    def __init__(self):
        self.logger = get_logger(__name__)

    def parse(self, response: Dict) -> pd.DataFrame:
        """Parsear respuesta de búsqueda de negocios.

        Args:
            response: Respuesta JSON de la API

        Returns:
            DataFrame con datos estructurados
        """
        businesses = response.get('businesses', [])
        total = response.get('total', 0)
        region = response.get('region', {})

        self.logger.info(f"Parseando {len(businesses)} negocios de {total} totales")

        return self.parse_list(businesses)

    def parse_list(self, businesses: List[Dict]) -> pd.DataFrame:
        """Parsear lista de negocios.

        Args:
            businesses: Lista de dicts con datos de negocios

        Returns:
            DataFrame con datos estructurados
        """
        if not businesses:
            return pd.DataFrame()

        parsed_records = []

        for business in businesses:
            try:
                record = self._parse_business(business)
                parsed_records.append(record)
            except Exception as e:
                self.logger.warning(f"Error parseando negocio {business.get('id')}: {e}")
                continue

        df = pd.DataFrame(parsed_records)
        self.logger.info(f"Parseados {len(df)} negocios exitosamente")
        return df

    def _parse_business(self, business: Dict) -> Dict:
        """Parsear un negocio individual.

        Args:
            business: Dict con datos del negocio

        Returns:
            Dict estructurado
        """
        # Extraer categorías
        categories = business.get('categories', [])
        category_aliases = [cat.get('alias', '') for cat in categories]
        category_titles = [cat.get('title', '') for cat in categories]

        # Extraer ubicación
        location = business.get('location', {})
        coordinates = business.get('coordinates', {})

        # Parsear precio
        price = business.get('price', '')
        price_numeric = len(price) if price else None

        record = {
            'id': business.get('id'),
            'name': business.get('name'),
            'alias': ', '.join(category_aliases) if category_aliases else None,
            'title': ', '.join(category_titles) if category_titles else None,
            'price': price if price else 'No especificado',
            'price_numeric': price_numeric,
            'rating': business.get('rating'),
            'review_count': business.get('review_count'),
            'distance': business.get('distance'),
            'url': business.get('url'),
            'phone': business.get('phone'),
            'display_phone': business.get('display_phone'),
            'is_closed': business.get('is_closed'),
            'image_url': business.get('image_url'),
            # Coordenadas
            'coordinates_latitude': coordinates.get('latitude'),
            'coordinates_longitude': coordinates.get('longitude'),
            # Ubicación
            'location_address1': location.get('address1'),
            'location_address2': location.get('address2'),
            'location_address3': location.get('address3'),
            'city': location.get('city'),
            'zip_code': location.get('zip_code'),
            'country': location.get('country'),
            'state': location.get('state'),
            'display_address': ', '.join(location.get('display_address', [])) if location.get('display_address') else None,
            # Transacciones
            'transactions': ', '.join(business.get('transactions', [])) if business.get('transactions') else None,
        }

        return record

    def parse_details(self, details: Dict) -> Dict:
        """Parsear detalles extendidos de un negocio.

        Args:
            details: Respuesta de get_details

        Returns:
            Dict con datos extendidos
        """
        base = self._parse_business(details)

        # Datos adicionales de details
        extended = {
            **base,
            'hours': details.get('hours', []),
            'special_hours': details.get('special_hours'),
            'photos': details.get('photos', []),
            'is_claimed': details.get('is_claimed'),
            'messaging': details.get('messaging'),
        }

        return extended


class ReviewParser(YelpResponseParser):
    """Parser para reviews."""

    def parse(self, response: Dict) -> pd.DataFrame:
        """Parsear respuesta de reviews."""
        reviews = response.get('reviews', [])
        total = response.get('total', 0)
        possible_languages = response.get('possible_languages', [])

        self.logger.info(f"Parseando {len(reviews)} reviews (total posible: {total})")

        return self.parse_list(reviews)

    def parse_list(self, reviews: List[Dict]) -> pd.DataFrame:
        """Parsear lista de reviews."""
        if not reviews:
            return pd.DataFrame()

        parsed_records = []

        for review in reviews:
            try:
                record = self._parse_review(review)
                parsed_records.append(record)
            except Exception as e:
                self.logger.warning(f"Error parseando review: {e}")
                continue

        return pd.DataFrame(parsed_records)

    def _parse_review(self, review: Dict) -> Dict:
        """Parsear un review individual."""
        user = review.get('user', {})

        return {
            'review_id': review.get('id'),
            'text': review.get('text'),
            'rating': review.get('rating'),
            'time_created': review.get('time_created'),
            'url': review.get('url'),
            'user_id': user.get('id'),
            'user_name': user.get('name'),
            'user_image_url': user.get('image_url'),
        }


class CategoryParser(YelpResponseParser):
    """Parser para categorías."""

    def parse(self, response: Dict) -> pd.DataFrame:
        """Parsear respuesta de categorías."""
        categories = response.get('categories', [])
        return self.parse_list(categories)

    def parse_list(self, categories: List[Dict]) -> pd.DataFrame:
        """Parsear lista de categorías."""
        if not categories:
            return pd.DataFrame()

        records = []
        for cat in categories:
            records.append({
                'alias': cat.get('alias'),
                'title': cat.get('title'),
                'parent_aliases': ', '.join(cat.get('parent_aliases', [])),
                'country_whitelist': ', '.join(cat.get('country_whitelist', [])),
                'country_blacklist': ', '.join(cat.get('country_blacklist', [])),
            })

        return pd.DataFrame(records)


class EventParser(YelpResponseParser):
    """Parser para eventos."""

    def parse(self, response: Dict) -> pd.DataFrame:
        """Parsear respuesta de eventos."""
        events = response.get('events', [])
        return self.parse_list(events)

    def parse_list(self, events: List[Dict]) -> pd.DataFrame:
        """Parsear lista de eventos."""
        if not events:
            return pd.DataFrame()

        records = []
        for event in events:
            try:
                business = event.get('business', {})
                records.append({
                    'event_id': event.get('id'),
                    'name': event.get('name'),
                    'description': event.get('description'),
                    'category': event.get('category'),
                    'is_free': event.get('is_free'),
                    'is_canceled': event.get('is_canceled'),
                    'tickets_url': event.get('tickets_url'),
                    'interested_count': event.get('interested_count'),
                    'attending_count': event.get('attending_count'),
                    'business_id': business.get('id'),
                    'business_name': business.get('name'),
                    'start_date': event.get('time_start'),
                    'end_date': event.get('time_end'),
                    'cost': event.get('cost'),
                    'cost_max': event.get('cost_max'),
                })
            except Exception as e:
                self.logger.warning(f"Error parseando evento: {e}")
                continue

        return pd.DataFrame(records)


def save_to_csv(df: pd.DataFrame, filepath: str, **kwargs):
    """Guardar DataFrame a CSV con logging.

    Args:
        df: DataFrame a guardar
        filepath: Ruta del archivo
        **kwargs: Argumentos adicionales para to_csv
    """
    try:
        df.to_csv(filepath, index=False, **kwargs)
        logger.info(f"Guardados {len(df)} registros en {filepath}")
    except Exception as e:
        logger.error(f"Error guardando CSV: {e}")
        raise
