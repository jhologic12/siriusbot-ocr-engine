"""
Tests
-----
Manejadores globales de errores HTTP.
"""

import asyncio

from fastapi.responses import JSONResponse

from utils.error_handlers import (
    ocr_exception_handler,
)

from utils.exceptions import (
    InvalidImageException,
    LowQualityException,
    OCRProcessingException,
)



def run_handler(exception):

    return asyncio.run(
        ocr_exception_handler(
            request=None,
            exc=exception
        )
    )



def test_invalid_image_handler():

    response = run_handler(
        InvalidImageException()
    )

    assert isinstance(
        response,
        JSONResponse
    )

    assert response.status_code == 400



def test_low_quality_handler():

    response = run_handler(
        LowQualityException()
    )

    assert response.status_code == 422



def test_processing_error_handler():

    response = run_handler(
        OCRProcessingException()
    )

    assert response.status_code == 500



def test_error_response_structure():

    response = run_handler(
        InvalidImageException(
            message="Archivo corrupto"
        )
    )

    body = response.body.decode()


    assert "INVALID_IMAGE" in body

    assert "Archivo corrupto" in body
