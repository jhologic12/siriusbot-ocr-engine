"""
Tests del endpoint OCR para protección
contra Image Bomb.
"""

import io

from PIL import Image

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_ocr_rejects_image_with_excessive_pixels():
    """
    El endpoint debe rechazar una imagen
    que supere el límite de píxeles.
    """

    image = Image.new(
        "RGB",
        (6000, 5000),
    )

    image_bytes = io.BytesIO()

    image.save(
        image_bytes,
        format="PNG",
    )

    image_bytes.seek(0)

    response = client.post(
        "/api/v1/ocr",
        files={
            "file": (
                "bomb.png",
                image_bytes,
                "image/png",
            )
        },
    )

    assert response.status_code == 413

    data = response.json()

    assert data["error"]["code"] == "IMAGE_TOO_LARGE"


def test_ocr_accepts_safe_image():
    """
    El endpoint debe aceptar una imagen
    dentro de los límites permitidos.
    """

    image = Image.new(
        "RGB",
        (1000, 800),
    )

    image_bytes = io.BytesIO()

    image.save(
        image_bytes,
        format="PNG",
    )

    image_bytes.seek(0)

    response = client.post(
        "/api/v1/ocr",
        files={
            "file": (
                "invoice.png",
                image_bytes,
                "image/png",
            )
        },
    )

    assert response.status_code != 400
