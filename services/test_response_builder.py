"""
Tests para Response Builder Service.
"""

from services.response_builder import build_response

from models.response_models import (
    OCREngineResponse,
    ValidationResult,
    QualityResult,
    ProcessingResult,
    OCRResult,
)



def test_build_response_returns_engine_response():
    """
    Debe devolver un OCREngineResponse.
    """

    response = build_response()


    assert isinstance(
        response,
        OCREngineResponse,
    )



def test_build_response_with_validation():
    """
    Debe incluir resultado de validación.
    """

    validation = ValidationResult(
        valid=True,
    )


    response = build_response(
        validation=validation,
    )


    assert response.validation == validation

    assert response.success is True



def test_build_response_invalid_validation():
    """
    Una validación fallida debe marcar success=False.
    """

    validation = ValidationResult(
        valid=False,
        errors=[
            "Imagen inválida"
        ],
    )


    response = build_response(
        validation=validation,
    )


    assert response.success is False



def test_build_response_full_pipeline():
    """
    Debe ensamblar todos los componentes OCR.
    """

    validation = ValidationResult(
        valid=True,
    )


    quality = QualityResult(
        status="GOOD",
        can_process=True,
    )


    processing = ProcessingResult(
        processed=True,
    )


    ocr = OCRResult(
        text="Factura prueba",
    )


    response = build_response(
        validation=validation,
        quality=quality,
        processing=processing,
        ocr=ocr,
        message="Proceso completado",
    )


    assert response.validation == validation

    assert response.quality == quality

    assert response.processing == processing

    assert response.ocr == ocr

    assert response.message == "Proceso completado"

    assert response.success is True
