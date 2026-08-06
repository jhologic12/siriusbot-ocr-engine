"""
Health Check Tests
Pruebas de endpoints de disponibilidad del servicio.
"""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health_endpoint():
    """
    Verifica que /health responde correctamente.
    """

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"

    assert data["service"] == "siriusbot-ocr-engine"


def test_ready_endpoint():
    """
    Verifica que /ready responde correctamente.
    """

    response = client.get("/ready")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ready"
