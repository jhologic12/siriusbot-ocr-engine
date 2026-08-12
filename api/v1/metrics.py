"""
Metrics endpoint para la API v1.
"""

from fastapi import APIRouter
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from utils.metrics import metrics

router = APIRouter()


@router.get("/metrics")
def get_metrics():
    """
    Retorna las métricas del servicio.
    """
    return metrics.get_metrics()


@router.get(
    "/metrics/prometheus",
    include_in_schema=True,
)
def get_prometheus_metrics():
    """
    Retorna las métricas en formato Prometheus.
    """

    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
