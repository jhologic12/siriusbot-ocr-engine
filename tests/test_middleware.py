"""
Middleware Tests
----------------
Pruebas del middleware de observabilidad.
"""

import pytest

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from utils.middleware import observability_middleware

app = FastAPI()


app.middleware("http")(observability_middleware)


@app.get("/test")
def health_test_endpoint():
    """
    Endpoint de prueba utilizado
    por los tests del middleware.
    """

    return {"message": "ok"}


client = TestClient(app)


def test_endpoint():
    """
    Verifica que el middleware
    no rompe el endpoint.
    """

    response = client.get("/test")

    assert response.status_code == 200


def test_request_id_header():
    """
    Verifica que el middleware
    agrega X-Request-ID.
    """

    response = client.get("/test")

    assert response.status_code == 200

    assert "X-Request-ID" in response.headers

    assert len(response.headers["X-Request-ID"]) > 0


def test_response_body():
    """
    Verifica que el middleware
    conserva la respuesta original.
    """

    response = client.get("/test")

    assert response.json() == {"message": "ok"}


@pytest.mark.anyio
async def test_middleware_exception(caplog):
    """
    Verifica que el middleware
    relanza la excepción cuando
    call_next falla.
    """

    request = Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/test",
            "headers": [],
        }
    )

    async def failing_call_next(request):
        raise RuntimeError("Simulated failure")

    with caplog.at_level("ERROR"):

        with pytest.raises(RuntimeError):

            await observability_middleware(
                request,
                failing_call_next,
            )

    messages = [record.message for record in caplog.records]

    assert "request_failed" in messages


def test_request_generates_structured_log(caplog):
    """
    Verifica que el middleware genera
    logs estructurados.
    """

    with caplog.at_level("INFO"):
        response = client.get("/test")

    assert response.status_code == 200

    messages = [record.message for record in caplog.records]

    assert "request_started" in messages


def test_request_generates_completed_log(caplog):
    """
    Verifica que el middleware genera
    un log estructurado al completar
    una petición.
    """

    with caplog.at_level("INFO"):
        response = client.get("/test")

    assert response.status_code == 200

    messages = [record.message for record in caplog.records]

    assert "request_completed" in messages
