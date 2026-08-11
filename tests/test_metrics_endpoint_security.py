"""
Pruebas de seguridad para el endpoint de métricas.
"""

import importlib

from fastapi.testclient import TestClient


def load_app(app_env: str, monkeypatch):
    """
    Carga la aplicación FastAPI con el entorno indicado.
    """

    monkeypatch.setenv("APP_ENV", app_env)

    import config
    import app

    importlib.reload(config)
    importlib.reload(app)

    return app.app


def test_metrics_endpoint_enabled_in_development(monkeypatch):
    """El endpoint de métricas debe estar disponible en desarrollo."""

    application = load_app("development", monkeypatch)
    client = TestClient(application)

    response = client.get("/api/v1/metrics")

    assert response.status_code == 200


def test_metrics_endpoint_disabled_in_production(monkeypatch):
    """El endpoint de métricas no debe estar disponible en producción."""

    application = load_app("production", monkeypatch)
    client = TestClient(application)

    response = client.get("/api/v1/metrics")

    assert response.status_code == 404
