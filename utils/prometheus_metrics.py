"""
Métricas Prometheus del SiriusBot OCR Engine.
"""

from prometheus_client import Counter, Histogram

# ============================================================
# HTTP metrics
# ============================================================

REQUESTS_TOTAL = Counter(
    "ocr_http_requests_total",
    "Total de peticiones HTTP recibidas por el OCR Engine.",
    ["method", "path"],
)

REQUESTS_COMPLETED = Counter(
    "ocr_http_requests_completed_total",
    "Total de peticiones HTTP completadas.",
    ["method", "path", "status_code"],
)

REQUESTS_FAILED = Counter(
    "ocr_http_requests_failed_total",
    "Total de peticiones HTTP que terminaron con excepción.",
    ["method", "path"],
)

REQUEST_DURATION = Histogram(
    "ocr_http_request_duration_seconds",
    "Duración de las peticiones HTTP en segundos.",
    ["method", "path"],
)


# ============================================================
# OCR metrics
# ============================================================

OCR_SUCCESS = Counter(
    "ocr_processing_success_total",
    "Total de procesamientos OCR exitosos.",
)

OCR_FAILED = Counter(
    "ocr_processing_failed_total",
    "Total de procesamientos OCR fallidos.",
)

OCR_PROCESSING_DURATION = Histogram(
    "ocr_processing_duration_seconds",
    "Duración del procesamiento OCR en segundos.",
)


# ============================================================
# Helper functions
# ============================================================


def register_request(
    method: str,
    path: str,
):
    """
    Registra una petición HTTP recibida.
    """

    REQUESTS_TOTAL.labels(
        method=method,
        path=path,
    ).inc()


def register_request_completed(
    method: str,
    path: str,
    status_code: int,
    duration: float,
):
    """
    Registra una petición HTTP completada.
    """

    REQUESTS_COMPLETED.labels(
        method=method,
        path=path,
        status_code=str(status_code),
    ).inc()

    REQUEST_DURATION.labels(
        method=method,
        path=path,
    ).observe(duration)


def register_request_failed(
    method: str,
    path: str,
):
    """
    Registra una petición HTTP que terminó
    con una excepción.
    """

    REQUESTS_FAILED.labels(
        method=method,
        path=path,
    ).inc()


def register_ocr_success():
    """
    Registra un procesamiento OCR exitoso.
    """

    OCR_SUCCESS.inc()


def register_ocr_failure():
    """
    Registra un procesamiento OCR fallido.
    """

    OCR_FAILED.inc()


def register_ocr_processing_time(
    duration: float,
):
    """
    Registra la duración de un procesamiento OCR.
    """

    OCR_PROCESSING_DURATION.observe(duration)
