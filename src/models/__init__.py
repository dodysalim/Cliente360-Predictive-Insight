"""Módulo de modelos ML."""
from .base_model import BaseModel, RegressionModel, ClassificationModel
from .regression import SpendingPredictor
from .segmentation import CustomerSegmentation
from .recommender import CustomerRecommender
from .evaluation import ModelEvaluator

__all__ = [
    'BaseModel',
    'RegressionModel',
    'ClassificationModel',
    'SpendingPredictor',
    'CustomerSegmentation',
    'CustomerRecommender',
    'ModelEvaluator',
]
