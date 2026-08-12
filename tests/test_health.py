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

    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "siriusbot-ocr-engine"


def test_ready_endpoint():
    """
    Verifica que /ready responde correctamente
    cuando todas las dependencias están disponibles.
    """

    response = client.get("/api/v1/ready")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ready"

    assert "checks" in data

    assert data["checks"]["tesseract"] == "ready"
    assert data["checks"]["ocr_language"] == "ready"


def test_ready_endpoint_when_dependency_is_unavailable(monkeypatch):
    """
    Verifica que /ready responda 503 cuando
    una dependencia necesaria no está disponible.
    """

    monkeypatch.setattr(
        "api.v1.health.check_readiness",
        lambda: {
            "tesseract": "ready",
            "ocr_language": "unavailable",
        },
    )

    response = client.get("/api/v1/ready")

    assert response.status_code == 503

    data = response.json()

    assert data["status"] == "not_ready"
    assert data["checks"]["tesseract"] == "ready"
    assert data["checks"]["ocr_language"] == "unavailable"
