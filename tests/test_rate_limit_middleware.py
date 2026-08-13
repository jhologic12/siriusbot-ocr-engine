"""
Pruebas de integración del rate limiting en el middleware.
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from utils.middleware import observability_middleware
from utils.rate_limiter import rate_limiter
import pytest


@pytest.fixture(autouse=True)
def restore_rate_limiter_state():
    original_max_requests = rate_limiter.max_requests
    original_window_seconds = rate_limiter.window_seconds

    rate_limiter.reset()

    yield

    rate_limiter.reset()
    rate_limiter.max_requests = original_max_requests
    rate_limiter.window_seconds = original_window_seconds


app = FastAPI()

app.middleware("http")(observability_middleware)


@app.post("/api/v1/ocr")
def ocr_test_endpoint():
    return {"message": "ocr ok"}


@app.get("/api/v1/health")
def health_test_endpoint():
    return {"status": "healthy"}


@app.get("/api/v1/ocr")
def ocr_get_test_endpoint():
    return {"message": "ocr get ok"}


client = TestClient(app)


def reset_rate_limiter():
    """
    Restablece el estado del rate limiter
    antes de cada escenario.
    """

    rate_limiter.reset()
    rate_limiter.max_requests = 1
    rate_limiter.window_seconds = 60


def test_ocr_request_is_allowed():
    reset_rate_limiter()

    response = client.post("/api/v1/ocr")

    assert response.status_code == 200
    assert response.json() == {"message": "ocr ok"}


def test_ocr_request_is_rate_limited_after_limit():
    reset_rate_limiter()

    first_response = client.post("/api/v1/ocr")
    second_response = client.post("/api/v1/ocr")

    assert first_response.status_code == 200
    assert second_response.status_code == 429


def test_rate_limited_response_contains_retry_after():
    reset_rate_limiter()

    client.post("/api/v1/ocr")
    response = client.post("/api/v1/ocr")

    assert response.status_code == 429
    assert "Retry-After" in response.headers
    assert int(response.headers["Retry-After"]) > 0


def test_health_endpoint_is_not_rate_limited():
    reset_rate_limiter()

    client.post("/api/v1/ocr")

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_ocr_is_not_rate_limited():
    reset_rate_limiter()

    client.post("/api/v1/ocr")

    response = client.get("/api/v1/ocr")

    assert response.status_code == 200
    assert response.json() == {"message": "ocr get ok"}


def test_rate_limited_response_contains_standard_headers():
    reset_rate_limiter()

    client.post("/api/v1/ocr")
    response = client.post("/api/v1/ocr")

    assert response.status_code == 429
    assert "X-Request-ID" in response.headers
    assert "X-Content-Type-Options" in response.headers
    assert "X-Frame-Options" in response.headers
    assert "Referrer-Policy" in response.headers
    assert "Retry-After" in response.headers
