"""
Tests Image Security
--------------------

Validación contra Image Bomb.

Prueba:
- imágenes normales
- exceso de píxeles
- ancho máximo
- alto máximo
"""

from PIL import Image

from services.image_security import (
    validate_image_dimensions,
)


def test_accept_normal_image():
    """
    Imagen dentro de límites permitidos.
    """

    image = Image.new(
        "RGB",
        (1200, 1200),
    )


    valid, errors = validate_image_dimensions(
        image
    )


    assert valid is True
    assert errors == []



def test_reject_excessive_pixels():
    """
    Imagen que supera el límite total
    de píxeles.
    """

    image = Image.new(
        "RGB",
        (6000, 5000),
    )


    valid, errors = validate_image_dimensions(
        image
    )


    assert valid is False

    assert (
        "Image exceeds maximum pixel limit"
        in errors
    )



def test_reject_excessive_width():
    """
    Imagen con ancho excesivo.
    """

    image = Image.new(
        "RGB",
        (12000, 500),
    )


    valid, errors = validate_image_dimensions(
        image
    )


    assert valid is False

    assert (
        "Image width exceeds limit"
        in errors
    )



def test_reject_excessive_height():
    """
    Imagen con altura excesiva.
    """

    image = Image.new(
        "RGB",
        (500, 12000),
    )


    valid, errors = validate_image_dimensions(
        image
    )


    assert valid is False

    assert (
        "Image height exceeds limit"
        in errors
    )