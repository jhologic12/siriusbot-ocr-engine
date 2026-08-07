"""
Health endpoints para la API v1.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    """
    Verifica que el servicio está saludable.
    """
    return {
        "status": "healthy",
        "service": "siriusbot-ocr-engine",
    }


@router.get("/ready")
def readiness():
    """
    Verifica que el servicio está listo para recibir tráfico.
    """
    return {
        "status": "ready",
    }
