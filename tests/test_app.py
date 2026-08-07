"""
API Tests
---------
Pruebas de los endpoints principales
del SiriusBot OCR Engine.
"""

import io

from fastapi.testclient import TestClient
from PIL import Image

from app import app

client = TestClient(app)


def create_test_image() -> io.BytesIO:
    """
    Crea una imagen temporal para pruebas.
    """

    image = Image.new(
        "RGB",
        (1000, 1000),
        color="white",
    )

    buffer = io.BytesIO()

    image.save(
        buffer,
        format="JPEG",
    )

    buffer.seek(0)

    return buffer


def test_health_endpoint():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["service"] == "SiriusBot OCR Engine"
    assert data["status"] == "running"


def test_ocr_endpoint_with_valid_image():

    image = create_test_image()

    response = client.post(
        "/api/v1/ocr",
        files={
            "file": (
                "test.jpg",
                image,
                "image/jpeg",
            )
        },
    )

    # Una imagen válida debe responder 200
    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "validation" in data
    assert "quality" in data
    assert "processing" in data
    assert "ocr" in data


def test_ocr_endpoint_invalid_file():

    response = client.post(
        "/api/v1/ocr",
        files={
            "file": (
                "test.txt",
                b"archivo invalido",
                "text/plain",
            )
        },
    )

    # Un archivo inválido debe responder 400
    assert response.status_code == 400

    data = response.json()

    assert data["success"] is False
    assert "error" in data
    assert "code" in data["error"]
    assert "message" in data["error"]


def test_ocr_response_structure():

    image = create_test_image()

    response = client.post(
        "/api/v1/ocr",
        files={
            "file": (
                "invoice.jpg",
                image,
                "image/jpeg",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

    assert "success" in data
    assert "message" in data
