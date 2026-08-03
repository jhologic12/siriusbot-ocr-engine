"""
Tests Validator Service
-----------------------

Pruebas automáticas del servicio de validación de imágenes.
"""

import os

from services.validator import validate_image


# Imagen real de prueba
TEST_IMAGE = "tests/invoices/test_invoice.jpg"


def test_validate_real_invoice():
    """
    Valida una imagen real de factura.
    """

    assert os.path.exists(
        TEST_IMAGE
    ), f"No existe la imagen {TEST_IMAGE}"


    # Leer imagen como bytes

    with open(
        TEST_IMAGE,
        "rb"
    ) as file:

        image_bytes = file.read()


    # Ejecutar validator

    result = validate_image(
        image_bytes
    )


    # Validaciones esperadas

    assert result.valid is True

    assert result.metadata is not None

    assert result.metadata.width > 0

    assert result.metadata.height > 0


    print("\nResultado Validator:")

    print(
        result.model_dump_json(
            indent=2
        )
    )



def test_invalid_image():
    """
    Verifica rechazo de archivo inválido.
    """

    fake_image = b"esto no es una imagen"


    result = validate_image(
        fake_image
    )


    assert result.valid is False

    assert len(
        result.errors
    ) > 0
