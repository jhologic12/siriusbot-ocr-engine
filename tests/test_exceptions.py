"""
Tests
-----
Excepciones estándar del OCR Engine.
"""

from utils.exceptions import (
    OCRException,
    InvalidImageException,
    LowQualityException,
    OCRProcessingException,
)


def test_base_exception():

    error = OCRException(
        message="Error general"
    )

    assert error.message == "Error general"
    assert error.code == "OCR_ERROR"



def test_invalid_image_exception():

    error = InvalidImageException()

    assert isinstance(
        error,
        OCRException
    )

    assert error.code == "INVALID_IMAGE"



def test_low_quality_exception():

    error = LowQualityException()

    assert isinstance(
        error,
        OCRException
    )

    assert error.code == "LOW_IMAGE_QUALITY"



def test_ocr_processing_exception():

    error = OCRProcessingException()

    assert isinstance(
        error,
        OCRException
    )

    assert error.code == "OCR_PROCESSING_ERROR"
