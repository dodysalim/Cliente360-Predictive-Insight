"""Configuración de logging centralizada."""
import logging
import logging.config
import yaml
from pathlib import Path
from functools import wraps
from typing import Callable, Any


def get_logger(name: str) -> logging.Logger:
    """Obtener logger configurado para un módulo específico.

    Args:
        name: Nombre del módulo/logger

    Returns:
        Logger configurado
    """
    # Cargar configuración YAML (ruta absoluta relativa a este archivo)
    config_path = Path(__file__).parent.parent.parent / "config" / "logging_config.yaml"

    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Crear directorio de logs con ruta absoluta del proyecto
        log_dir = Path(__file__).parent.parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)

        # ── FIX: Resolver rutas de log a absolutas ────────────────────────────
        # dictConfig interpreta paths relativos desde el CWD; cuando se llama
        # desde notebooks/ el handler de ErrorFile falla. Convertimos a absoluta.
        for handler_cfg in config.get('handlers', {}).values():
            if 'filename' in handler_cfg:
                handler_cfg['filename'] = str(log_dir / Path(handler_cfg['filename']).name)

        try:
            logging.config.dictConfig(config)
        except Exception:
            # Fallback: logging básico a consola si la config YAML falla
            logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.INFO)

    return logging.getLogger(name)


def log_execution(logger_name: str = None):
    """Decorador para loggear entrada y salida de funciones.

    Args:
        logger_name: Nombre del logger (default: módulo de la función)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_logger(logger_name or func.__module__)
            func_name = func.__name__

            logger.debug(f"Iniciando ejecución: {func_name}")
            try:
                result = func(*args, **kwargs)
                logger.debug(f"Ejecución exitosa: {func_name}")
                return result
            except Exception as e:
                logger.error(f"Error en {func_name}: {str(e)}", exc_info=True)
                raise

        return wrapper
    return decorator


def log_dataframe_info(df: Any, logger: logging.Logger, name: str = "DataFrame"):
    """Loggear información de un DataFrame.

    Args:
        df: DataFrame de pandas
        logger: Logger a utilizar
        name: Nombre descriptivo del DataFrame
    """
    try:
        shape = df.shape
        memory_usage = df.memory_usage(deep=True).sum() / 1024**2  # MB
        logger.info(
            f"{name} - Shape: {shape}, Memory: {memory_usage:.2f}MB, "
            f"Columns: {list(df.columns)}"
        )
    except Exception as e:
        logger.warning(f"No se pudo obtener info de {name}: {e}")
