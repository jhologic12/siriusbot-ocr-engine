"""
Pruebas unitarias para el servicio de preprocesamiento.
"""

from io import BytesIO

from PIL import Image

from services.preprocessor import (
    preprocess_image,
    image_to_bytes,
)


TEST_IMAGE = "tests/invoices/test_invoice.jpg"


def test_preprocess_image():
    """
    Debe abrir la imagen, preprocesarla y devolver
    una imagen PIL válida.
    """

    original = Image.open(TEST_IMAGE)

    processed = preprocess_image(original)

    assert isinstance(processed, Image.Image)

    assert processed.mode == "RGB"

    assert processed.width >= original.width

    assert processed.height >= original.height


def test_image_to_bytes():
    """
    Debe convertir correctamente una imagen a bytes JPEG.
    """

    image = Image.open(TEST_IMAGE)

    processed = preprocess_image(image)

    image_bytes = image_to_bytes(processed)

    assert isinstance(image_bytes, bytes)

    assert len(image_bytes) > 0


def test_processed_image_can_be_opened():
    """
    Los bytes generados deben representar
    una imagen JPEG válida.
    """

    image = Image.open(TEST_IMAGE)

    processed = preprocess_image(image)

    image_bytes = image_to_bytes(processed)

    reconstructed = Image.open(BytesIO(image_bytes))

    assert reconstructed.format == "JPEG"

    assert reconstructed.mode == "RGB"

    assert reconstructed.width == processed.width

    assert reconstructed.height == processed.height


def test_processed_image_is_not_smaller():
    """
    Después del preprocesamiento la imagen
    no debería perder resolución.
    """

    original = Image.open(TEST_IMAGE)

    processed = preprocess_image(original)

    assert processed.width >= original.width

    assert processed.height >= original.height


def test_processed_bytes_are_reasonable():
    """
    El JPEG generado debe tener un tamaño coherente.
    """

    image = Image.open(TEST_IMAGE)

    processed = preprocess_image(image)

    image_bytes = image_to_bytes(processed)

    assert len(image_bytes) > 20000
