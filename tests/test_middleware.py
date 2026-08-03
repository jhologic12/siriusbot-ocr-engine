"""
Middleware Tests
----------------
Pruebas del middleware de observabilidad.
"""


from fastapi import FastAPI
from fastapi.testclient import TestClient


from utils.middleware import (
    observability_middleware,
)



app = FastAPI()



app.middleware(
    "http"
)(
    observability_middleware
)



@app.get("/test")
def health_test_endpoint():

    return {
        "message": "ok"
    }



client = TestClient(app)



def test_endpoint():

    """
    Verifica que el middleware
    no rompe el endpoint.
    """

    response = client.get(
        "/test"
    )


    assert response.status_code == 200



def test_request_id_header():

    """
    Verifica que el middleware
    agrega X-Request-ID.
    """

    response = client.get(
        "/test"
    )


    assert response.status_code == 200


    assert (
        "X-Request-ID"
        in response.headers
    )


    assert (
        len(response.headers["X-Request-ID"])
        > 0
    )



def test_response_body():

    """
    Verifica que el middleware
    conserva la respuesta original.
    """

    response = client.get(
        "/test"
    )


    assert response.json() == {
        "message": "ok"
    }
