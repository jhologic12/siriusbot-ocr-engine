"""
Metrics endpoint para la API v1.
"""

from fastapi import APIRouter

from utils.metrics import metrics

router = APIRouter()


@router.get("/metrics")
def get_metrics():
    """
    Retorna las métricas del servicio.
    """
    return metrics.get_metrics()
