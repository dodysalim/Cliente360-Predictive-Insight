"""Excepciones personalizadas del proyecto."""


class ProyectoIntegradorError(Exception):
    """Excepción base para todos los errores del proyecto."""

    def __init__(self, message: str, error_code: str = None, details: dict = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}

    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class DataLoadError(ProyectoIntegradorError):
    """Error al cargar datos."""

    def __init__(self, message: str, file_path: str = None, **kwargs):
        super().__init__(message, error_code="DATA_LOAD_ERROR", **kwargs)
        self.file_path = file_path


class DataValidationError(ProyectoIntegradorError):
    """Error de validación de datos."""

    def __init__(self, message: str, validation_errors: list = None, **kwargs):
        super().__init__(message, error_code="DATA_VALIDATION_ERROR", **kwargs)
        self.validation_errors = validation_errors or []


class DataTransformationError(ProyectoIntegradorError):
    """Error en transformación de datos."""

    def __init__(self, message: str, column: str = None, **kwargs):
        super().__init__(message, error_code="DATA_TRANSFORMATION_ERROR", **kwargs)
        self.column = column


class APIConnectionError(ProyectoIntegradorError):
    """Error de conexión con API."""

    def __init__(self, message: str, status_code: int = None, **kwargs):
        super().__init__(message, error_code="API_CONNECTION_ERROR", **kwargs)
        self.status_code = status_code


class APIRateLimitError(ProyectoIntegradorError):
    """Error de rate limiting de API."""

    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = None, **kwargs):
        super().__init__(message, error_code="API_RATE_LIMIT", **kwargs)
        self.retry_after = retry_after


class APIAuthenticationError(ProyectoIntegradorError):
    """Error de autenticación en API."""

    def __init__(self, message: str = "Authentication failed", **kwargs):
        super().__init__(message, error_code="API_AUTH_ERROR", **kwargs)


class ModelTrainingError(ProyectoIntegradorError):
    """Error durante entrenamiento de modelo."""

    def __init__(self, message: str, model_name: str = None, **kwargs):
        super().__init__(message, error_code="MODEL_TRAINING_ERROR", **kwargs)
        self.model_name = model_name


class ModelPredictionError(ProyectoIntegradorError):
    """Error durante predicción de modelo."""

    def __init__(self, message: str, model_name: str = None, **kwargs):
        super().__init__(message, error_code="MODEL_PREDICTION_ERROR", **kwargs)
        self.model_name = model_name


class ConfigurationError(ProyectoIntegradorError):
    """Error de configuración."""

    def __init__(self, message: str, config_key: str = None, **kwargs):
        super().__init__(message, error_code="CONFIG_ERROR", **kwargs)
        self.config_key = config_key
