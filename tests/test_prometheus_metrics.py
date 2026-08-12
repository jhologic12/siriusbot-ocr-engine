"""
Pruebas de métricas Prometheus.
"""

from fastapi.testclient import TestClient

from app import app

from utils.prometheus_metrics import (
    register_ocr_processing_time,
    register_ocr_success,
    register_request,
)

client = TestClient(app)


def test_prometheus_metrics_endpoint():
    """
    Verifica que el endpoint Prometheus
    esté disponible.
    """

    response = client.get("/api/v1/metrics/prometheus")

    assert response.status_code == 200

    assert "text/plain" in response.headers["content-type"]


def test_prometheus_metrics_contains_application_metrics():
    """
    Verifica que las métricas propias
    del OCR Engine sean expuestas.
    """

    register_request(
        "GET",
        "/test-prometheus",
    )

    register_ocr_success()

    register_ocr_processing_time(
        0.25,
    )

    response = client.get("/api/v1/metrics/prometheus")

    content = response.text

    assert "ocr_http_requests_total" in content

    assert "ocr_processing_success_total" in content

    assert "ocr_processing_duration_seconds" in content


def test_prometheus_request_metric_has_labels():
    """
    Verifica que las métricas HTTP
    expongan sus labels correctamente.
    """

    register_request(
        "POST",
        "/api/v1/ocr",
    )

    response = client.get("/api/v1/metrics/prometheus")

    content = response.text

    assert 'method="POST"' in content

    assert 'path="/api/v1/ocr"' in content
