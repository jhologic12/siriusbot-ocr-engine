"""
Middleware global para observabilidad
del SiriusBot OCR Engine.
"""

import time

from fastapi import Request
from fastapi.responses import JSONResponse

from utils.rate_limiter import rate_limiter
from utils.logger import get_logger
from utils.metrics import metrics
from utils.request_context import (
    generate_request_id,
    clear_request_id,
)

from utils.prometheus_metrics import (
    register_request as prometheus_register_request,
    register_request_completed,
    register_request_failed,
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
    - Registrar logs estructurados
    - Actualizar métricas
    - Agregar headers de seguridad HTTP
    """

    request_id = generate_request_id()
    start_time = time.time()

    logger.info(
        "request_started",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
        },
    )

    metrics.increment("requests_total")

    prometheus_register_request(
        method=request.method,
        path=request.url.path,
    )

    try:
        if request.method == "POST" and request.url.path == "/api/v1/ocr":
            client_host = request.client.host if request.client else "unknown"

            if not rate_limiter.is_allowed(client_host):
                retry_after = rate_limiter.get_retry_after(client_host)

                response = JSONResponse(
                    status_code=429,
                    content={
                        "success": False,
                        "error": {
                            "code": "RATE_LIMIT_EXCEEDED",
                            "message": "Too many requests",
                        },
                    },
                    headers={
                        "Retry-After": str(retry_after),
                    },
                )
            else:
                response = await call_next(request)
        else:
            response = await call_next(request)

        elapsed = time.time() - start_time

        metrics.add_request_time(elapsed)
        metrics.increment("requests_success")

        register_request_completed(
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration=elapsed,
        )

        # Request tracing
        response.headers["X-Request-ID"] = request_id

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"

        logger.info(
            "request_completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(elapsed * 1000, 2),
            },
        )

        return response
    except Exception:
        metrics.increment("requests_failed")

        register_request_failed(
            method=request.method,
            path=request.url.path,
        )

        logger.exception(
            "request_failed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
            },
        )

        raise

    finally:
        clear_request_id()
