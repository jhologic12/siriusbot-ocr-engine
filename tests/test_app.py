"""
Pruebas de integración de los endpoints principales
del SiriusBot OCR Engine.
"""

import io
import pytest

from unittest.mock import patch

from fastapi.testclient import TestClient

from PIL import Image, ImageDraw

from app import app

client = TestClient(
    app,
    headers={"host": "localhost"},
)

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
    """
    Verifica el endpoint raíz del servicio.
    """

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["service"] == "SiriusBot OCR Engine"
    assert data["status"] == "running"
    assert data["version"] == "1.0.0"


def test_api_health_endpoint():
    """
    Verifica el endpoint de health check.
    """

    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "siriusbot-ocr-engine"


def test_api_ready_endpoint():
    """
    Verifica el endpoint de readiness.
    """

    response = client.get("/api/v1/ready")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ready"


def test_metrics_endpoint():
    """
    Verifica que el endpoint de métricas
    esté disponible y devuelva las métricas
    principales del servicio.
    """

    response = client.get("/api/v1/metrics")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

    assert "requests_total" in data
    assert "requests_success" in data
    assert "requests_failed" in data
    assert "ocr_success" in data
    assert "ocr_failed" in data
    assert "uptime_seconds" in data
    assert "average_processing_time" in data


def test_request_id_header():
    """
    Verifica que el middleware agregue
    X-Request-ID a las respuestas HTTP.
    """

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"]


def test_ocr_endpoint_with_valid_image():
    """
    Verifica el procesamiento completo de una imagen válida.
    """

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

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True

    assert data["validation"]["valid"] is True

    assert "quality" in data
    assert data["quality"]["canProcess"] is True

    assert data["processing"]["processed"] is True
    assert data["processing"]["originalSize"] > 0
    assert data["processing"]["newSize"] > 0
    assert data["processing"]["width"] > 0
    assert data["processing"]["height"] > 0

    assert "ocr" in data
    assert "text" in data["ocr"]
    assert "confidence" in data["ocr"]

    assert data["message"] == "Proceso completado"


def test_ocr_endpoint_low_quality():
    """
    Verifica que una imagen válida pero con resolución
    insuficiente sea rechazada por el análisis de calidad.
    """

    image = Image.new(
        "RGB",
        (400, 400),
        "white",
    )

    draw = ImageDraw.Draw(image)

    for y in range(0, 400, 10):
        draw.line(
            (0, y, 400, y),
            fill=(y % 256, 50, 100),
            width=3,
        )

    buffer = io.BytesIO()

    image.save(
        buffer,
        format="JPEG",
        quality=95,
    )

    buffer.seek(0)

    response = client.post(
        "/api/v1/ocr",
        files={
            "file": (
                "low-quality.jpg",
                buffer,
                "image/jpeg",
            )
        },
    )

    assert response.status_code == 422

    data = response.json()

    assert data["success"] is True
    assert data["quality"]["status"] == "BAD"
    assert data["quality"]["canProcess"] is False
    assert data["message"] == "Calidad insuficiente"



def test_ocr_endpoint_invalid_file():
    """
    Verifica que un archivo inválido
    sea rechazado por la API.
    """

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

    assert response.status_code == 400

    data = response.json()

    assert data["success"] is False
    assert "error" in data
    assert "code" in data["error"]
    assert "message" in data["error"]



def test_ocr_response_structure():
    """
    Verifica la estructura general de la respuesta OCR.
    """

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

    expected_fields = {
        "success",
        "validation",
        "quality",
        "processing",
        "ocr",
        "message",
        "error",
    }

    assert expected_fields.issubset(data.keys())


def test_security_headers():
    """
    Verifica que la API incluya headers HTTP
    básicos de seguridad.
    """

    response = client.get("/api/v1/health")

    assert response.status_code == 200

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "no-referrer"


def test_ocr_endpoint_invalid_image():
    """
    Verifica que un archivo que supera la validación
    de seguridad pero no contiene una imagen válida
    sea rechazado por la validación de imagen.
    """

    with patch(
        "services.ocr_pipeline.validate_file_security",
        return_value=(True, []),
    ):
        response = client.post(
            "/api/v1/ocr",
            files={
                "file": (
                    "corrupt.jpg",
                    b"contenido que no es una imagen",
                    "image/jpeg",
                )
            },
        )

    assert response.status_code == 400

    data = response.json()

    assert data["success"] is False
    assert data["error"]["code"] == "INVALID_IMAGE"


def test_ocr_endpoint_image_too_large():
    """
    Verifica que una imagen que supera las
    restricciones de dimensiones sea rechazada.
    """

    image = create_test_image()

    with patch(
        "services.ocr_pipeline.validate_image_dimensions",
        return_value=(
            False,
            ["Image exceeds maximum pixel limit"],
        ),
    ):
        response = client.post(
            "/api/v1/ocr",
            files={
                "file": (
                    "large.jpg",
                    image,
                    "image/jpeg",
                )
            },
        )

    assert response.status_code == 413

    data = response.json()

    assert data["success"] is False
    assert data["error"]["code"] == "IMAGE_TOO_LARGE"
    assert "details" in data["error"]


def test_ocr_endpoint_ocr_exception():
    """
    Verifica que una excepción durante OCR sea registrada
    y propagada correctamente.
    """

    image = create_test_image()

    with patch(
        "services.ocr_pipeline.extract_text",
        side_effect=RuntimeError("OCR failure"),
    ):
        with pytest.raises(RuntimeError, match="OCR failure"):
            client.post(
                "/api/v1/ocr",
                files={
                    "file": (
                        "test.jpg",
                        image,
                        "image/jpeg",
                    )
                },
            )
