"""Configuración de pytest."""
import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def sample_customer_data():
    """Datos de clientes de ejemplo."""
    return pd.DataFrame({
        'id_persona': ['1', '2', '3', '4', '5'],
        'nombre': ['Juan', 'Maria', 'Pedro', 'Ana', 'Luis'],
        'apellido': ['Perez', 'Garcia', 'Lopez', 'Martinez', 'Sanchez'],
        'edad': [25, 35, 45, 55, 65],
        'genero': ['Masculino', 'Femenino', 'Masculino', 'Femenino', 'Masculino'],
        'ciudad_residencia': ['Miami', 'NYC', 'Boston', 'Miami', 'Chicago'],
        'estrato_socioeconomico': ['Alto', 'Medio', 'Bajo', 'Alto', 'Medio'],
        'frecuencia_visita': [5, 3, 1, 8, 0],
        'promedio_gasto_comida': [50.0, 30.0, 15.0, 75.0, 0.0],
        'ocio': ['Sí', 'No', 'Sí', 'Sí', 'No'],
        'consume_licor': ['No', 'Sí', 'No', 'Sí', 'No'],
        'preferencias_alimenticias': ['Carnes', 'Vegetariano', 'Mariscos', 'Carnes', 'Vegano'],
        'membresia_premium': ['Sí', 'No', 'No', 'Sí', 'No'],
        'telefono_contacto': ['123', '456', None, '789', ''],
        'correo_electronico': ['a@b.com', None, 'c@d.com', 'e@f.com', ''],
        'tipo_de_pago_mas_usado': ['Tarjeta', 'Efectivo', 'App', 'Tarjeta', 'Efectivo'],
        'ingresos_mensuales': [5000, 3000, 1500, 8000, 2000]
    })


@pytest.fixture
def sample_yelp_data():
    """Datos de Yelp de ejemplo."""
    return pd.DataFrame({
        'alias': ['italian', 'mexican', 'japanese'],
        'title': ['Italian', 'Mexican', 'Japanese'],
        'id': ['rest1', 'rest2', 'rest3'],
        'name': ['Bella Italia', 'Tacos Express', 'Sushi Palace'],
        'price': ['$$', '$', '$$$'],
        'rating': [4.5, 4.0, 4.8],
        'review_count': [100, 50, 200],
        'distance': [1000.0, 2000.0, 500.0],
        'coordinates_latitude': [25.76, 25.77, 25.78],
        'coordinates_longitude': [-80.19, -80.20, -80.21],
        'location_address1': ['123 Main', '456 Oak', '789 Pine'],
        'city': ['Miami', 'Miami', 'Miami']
    })
