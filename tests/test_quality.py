"""
Pruebas unitarias para el análisis de calidad de imágenes.
"""

from PIL import Image

from services.preprocessor import preprocess_image
from services.quality import analyze_quality
from models.response_models import QualityResult


TEST_IMAGE = "tests/invoices/test_invoice.jpg"


def test_analyze_quality_returns_quality_result():
    """
    Debe devolver una instancia de QualityResult.
    """

    image = Image.open(TEST_IMAGE)

    image = preprocess_image(image)

    quality = analyze_quality(image)

    assert isinstance(quality, QualityResult)


def test_quality_dimensions():
    """
    Las dimensiones deben ser válidas.
    """

    image = Image.open(TEST_IMAGE)

    image = preprocess_image(image)

    quality = analyze_quality(image)

    assert quality.width > 0

    assert quality.height > 0

    assert quality.pixels == quality.width * quality.height


def test_quality_metrics():
    """
    Brillo y contraste deben estar en rangos válidos.
    """

    image = Image.open(TEST_IMAGE)

    image = preprocess_image(image)

    quality = analyze_quality(image)

    assert 0 <= quality.brightness <= 255

    assert quality.contrast >= 0


def test_quality_status():
    """
    El estado debe ser uno de los permitidos.
    """

    image = Image.open(TEST_IMAGE)

    image = preprocess_image(image)

    quality = analyze_quality(image)

    assert quality.status in [
        "GOOD",
        "WARNING",
        "BAD",
    ]


def test_can_process_is_boolean():
    """
    can_process debe ser booleano.
    """

    image = Image.open(TEST_IMAGE)

    image = preprocess_image(image)

    quality = analyze_quality(image)

    assert isinstance(
        quality.can_process,
        bool,
    )


def test_warnings_is_list():
    """
    warnings siempre debe ser una lista.
    """

    image = Image.open(TEST_IMAGE)

    image = preprocess_image(image)

    quality = analyze_quality(image)

    assert isinstance(
        quality.warnings,
        list,
    )


def test_invoice_quality_is_good():
    """
    La factura de prueba debe ser procesable.
    """

    image = Image.open(TEST_IMAGE)

    image = preprocess_image(image)

    quality = analyze_quality(image)

    assert quality.can_process is True

    assert quality.status in [
        "GOOD",
        "WARNING",
    ]
