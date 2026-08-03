"""
Telemetry Service
-----------------
Servicio centralizado de observabilidad
del SiriusBot OCR Engine.
"""


from utils.metrics import metrics
from utils.logger import get_logger


logger = get_logger(
    "telemetry"
)



def register_request(
    method: str,
    path: str,
):
    """
    Registra una petición recibida.
    """

    metrics.increment(
        "requests_total"
    )


    logger.info(
        f"REQUEST {method} {path}"
    )



def register_success(
    processing_time: float,
):
    """
    Registra una petición exitosa.
    """

    metrics.increment(
        "requests_success"
    )


    metrics.add_processing_time(
        processing_time
    )



def register_error(
    error_type: str,
):
    """
    Registra una petición fallida.
    """

    metrics.increment(
        "requests_error"
    )


    metrics.increment(
        error_type
    )


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
