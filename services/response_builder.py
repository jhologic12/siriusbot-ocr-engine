"""
Response Builder Service
------------------------
Construcción de respuestas estándar del OCR Engine.
"""


from typing import Optional


from models.response_models import (
    OCREngineResponse,
    ValidationResult,
    QualityResult,
    ProcessingResult,
    OCRResult,
)



def build_response(
    validation: Optional[ValidationResult] = None,
    quality: Optional[QualityResult] = None,
    processing: Optional[ProcessingResult] = None,
    ocr: Optional[OCRResult] = None,
    message: Optional[str] = None,
) -> OCREngineResponse:
    """
    Construye una respuesta estándar
    del OCR Engine.
    """


    success = True


    if validation is not None:

        success = validation.valid


    return OCREngineResponse(

        success=success,

        validation=validation,

        quality=quality,

        processing=processing,

        ocr=ocr,

        message=message,
    )
