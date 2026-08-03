"""
HTTP Middleware
---------------
Middleware global para observabilidad
del SiriusBot OCR Engine.
"""

import time

from fastapi import Request

from utils.logger import get_logger
from utils.metrics import metrics

from utils.request_context import (
    generate_request_id,
    clear_request_id,
)


logger = get_logger(__name__)


async def observability_middleware(
    request: Request,
    call_next,
):
    """
    Middleware encargado de:

    - Crear Request ID
    - Medir tiempo
    - Registrar logs
    - Actualizar métricas
    """


    request_id = generate_request_id()

    start_time = time.time()


    logger.info(
        f"[{request_id}] "
        f"Request iniciado "
        f"{request.method} {request.url.path}"
    )


    metrics.increment(
        "requests_total"
    )


    try:

        response = await call_next(
            request
        )


        elapsed = (
            time.time()
            - start_time
        )


        metrics.add_processing_time(
            elapsed
        )


        metrics.increment(
            "requests_success"
        )


        response.headers[
            "X-Request-ID"
        ] = request_id


        logger.info(
            f"[{request_id}] "
            f"Request completado "
            f"status={response.status_code} "
            f"time={elapsed:.4f}s"
        )


        return response


    except Exception as exc:


        metrics.increment(
            "requests_failed"
        )


        logger.exception(
            f"[{request_id}] "
            f"Error procesando request: {exc}"
        )


        raise


    finally:

        clear_request_id()
