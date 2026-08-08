"""
Servicio centralizado de observabilidad
del SiriusBot OCR Engine.
"""

from utils.metrics import metrics
from utils.logger import get_logger

logger = get_logger("telemetry")


def register_request(
    method: str,
    path: str,
):
    """
    Registra una petición OCR recibida.
    """

    logger.info(
        f"REQUEST {method} {path}"
    )


def register_success():
    """
    Registra un procesamiento OCR exitoso.
    """

    metrics.increment("ocr_success")


def register_error(
    error_type: str,
):
    """
    Registra un error ocurrido durante
    el procesamiento OCR.
    """

    metrics.increment("ocr_failed")

    metrics.increment(error_type)

    logger.error(
        f"ERROR {error_type}"
    )


def get_telemetry():
    """
    Retorna estado actual
    de métricas del Engine.
    """

    return metrics.get_metrics()


def reset_telemetry():
    """
    Limpia métricas.
    """

    metrics.reset()
