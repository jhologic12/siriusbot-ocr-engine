"""
API principal del microservicio OCR.
"""

from fastapi import FastAPI

from api.v1.health import router as health_router
from api.v1.metrics import router as metrics_router
from api.v1.ocr import router as ocr_router

from utils.error_handlers import register_exception_handlers
from utils.middleware import observability_middleware

app = FastAPI(
    title="SiriusBot OCR Engine",
    description="Microservicio OCR para procesamiento de facturas",
    version="1.0.0",
)


# ==================================
# API Versioning
# ==================================

app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"],
)

app.include_router(
    metrics_router,
    prefix="/api/v1",
    tags=["Metrics"],
)

app.include_router(
    ocr_router,
    prefix="/api/v1",
    tags=["OCR"],
)

# ==================================
# Observabilidad
# ==================================

app.middleware("http")(observability_middleware)


# ==================================
# Exception handlers
# ==================================

register_exception_handlers(app)


# ==================================
# Root endpoint
# ==================================


@app.get("/")
def root():
    """
    Endpoint raíz del servicio.
    """
    return {
        "service": "SiriusBot OCR Engine",
        "status": "running",
        "version": "1.0.0",
    }
