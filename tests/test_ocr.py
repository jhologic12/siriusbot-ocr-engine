"""
Tests para servicio OCR.
"""

from PIL import Image

from services.ocr import extract_text
from services.preprocessor import preprocess_image

from models.response_models import OCRResult


TEST_IMAGE = "tests/invoices/test_invoice.jpg"



def test_extract_text_returns_ocr_result():
    """
    Debe devolver un OCRResult.
    """

    image = Image.open(TEST_IMAGE)

    result = extract_text(image)

    assert isinstance(
        result,
        OCRResult
    )



def test_extract_text_not_empty():
    """
    OCR debe generar texto.
    """

    image = Image.open(TEST_IMAGE)

    result = extract_text(image)

    assert result.text != ""

    assert len(result.text) > 10



def test_invoice_contains_expected_words():
    """
    La factura debe contener términos esperados.
    """

    image = Image.open(TEST_IMAGE)

    image = preprocess_image(image)

    result = extract_text(image)


    text = result.text.lower()


    assert any(
        word in text
        for word in [
            "factura",
            "invoice",
            "total",
            "iva",
            "fecha"
        ]
    )



def test_ocr_result_structure():
    """
    Valida estructura del resultado OCR.
    """

    image = Image.open(TEST_IMAGE)

    result = extract_text(image)


    assert isinstance(
        result.text,
        str
    )


    if result.confidence is not None:

        assert (
            0 <= result.confidence <= 100
        )
