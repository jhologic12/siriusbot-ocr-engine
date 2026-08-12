"""
Health endpoints
----------------
Endpoints de disponibilidad del SiriusBot OCR Engine.
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from utils.health import (
    check_readiness,
    is_ready,
)

router = APIRouter()


@router.get("/health")
def health():
    """
    Verifica que el servicio esté disponible.
    """

    return {
        "status": "healthy",
        "service": "siriusbot-ocr-engine",
    }


@router.get("/ready")
def readiness():
    """
    Verifica que el servicio esté listo para procesar OCR.
    """

    checks = check_readiness()

    if is_ready(checks):
        return {
            "status": "ready",
            "checks": checks,
        }

    return JSONResponse(
        status_code=503,
        content={
            "status": "not_ready",
            "checks": checks,
        },
    )
