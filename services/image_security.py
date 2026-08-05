"""
Image Security
--------------
Protección contra imágenes maliciosas
tipo Image Bomb.
"""

from PIL import Image

from utils.constants import (
    MAX_IMAGE_PIXELS,
    MAX_IMAGE_WIDTH,
    MAX_IMAGE_HEIGHT,
)


def validate_image_dimensions(
    image: Image.Image,
):
    """
    Valida dimensiones de una imagen.
    """

    width, height = image.size


    errors = []


    pixels = width * height


    if pixels > MAX_IMAGE_PIXELS:

        errors.append(
            "Image exceeds maximum pixel limit"
        )


    if width > MAX_IMAGE_WIDTH:

        errors.append(
            "Image width exceeds limit"
        )


    if height > MAX_IMAGE_HEIGHT:

        errors.append(
            "Image height exceeds limit"
        )


    return (
        len(errors) == 0,
        errors,
    )