"""Pruebas de autenticación del endpoint OCR."""

from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

import config
from app import app


client = TestClient(app, headers={"host": "localhost"})
TEST_API_KEY = "test-only-secret"


def test_ocr_without_api_key_returns_401(monkeypatch):
    monkeypatch.setattr(config, "OCR_API_KEY", TEST_API_KEY)

    response = client.post(
        "/api/v1/ocr",
        files={"file": ("test.jpg", b"image", "image/jpeg")},
    )

    assert response.status_code == 401


def test_ocr_with_invalid_api_key_returns_401(monkeypatch):
    monkeypatch.setattr(config, "OCR_API_KEY", TEST_API_KEY)

    response = client.post(
        "/api/v1/ocr",
        headers={"X-API-Key": "wrong-key"},
        files={"file": ("test.jpg", b"image", "image/jpeg")},
    )

    assert response.status_code == 401


def test_ocr_with_valid_api_key_continues_processing(monkeypatch):
    monkeypatch.setattr(config, "OCR_API_KEY", TEST_API_KEY)

    expected_response = {
        "success": True,
        "ocr": {"text": "test", "confidence": 90},
        "message": "Proceso completado",
    }

    with patch(
        "api.v1.ocr.execute_ocr_pipeline",
        new_callable=AsyncMock,
        return_value=expected_response,
    ) as mock_pipeline:
        response = client.post(
            "/api/v1/ocr",
            headers={"X-API-Key": TEST_API_KEY},
            files={"file": ("test.jpg", b"image", "image/jpeg")},
        )

    assert response.status_code == 200
    assert response.json() == expected_response
    mock_pipeline.assert_awaited_once()


def test_health_endpoint_remains_public(monkeypatch):
    monkeypatch.setattr(config, "OCR_API_KEY", TEST_API_KEY)

    response = client.get("/api/v1/health")

    assert response.status_code == 200
