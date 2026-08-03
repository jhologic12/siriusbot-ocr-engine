"""
Response Models
---------------
Modelos estándar de respuesta para SiriusBot OCR Engine
"""

from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


# ==================================
# Modelo base
# ==================================

class CamelCaseModel(BaseModel):
    """
    Modelo base para permitir nombres Python
    snake_case y salida JSON camelCase.
    """

    model_config = ConfigDict(
        populate_by_name=True
    )


# ==================================
# Metadata de imagen
# ==================================

class ImageMetadata(CamelCaseModel):

    format: Optional[str] = None

    mode: Optional[str] = None

    width: int = 0

    height: int = 0

    pixels: int = 0

    size_bytes: int = Field(
        default=0,
        alias="sizeBytes"
    )


# ==================================
# Resultado de validación
# ==================================

class ValidationResult(CamelCaseModel):

    valid: bool = True

    errors: List[str] = Field(
        default_factory=list
    )

    warnings: List[str] = Field(
        default_factory=list
    )

    metadata: Optional[ImageMetadata] = None



# ==================================
# Resultado análisis calidad
# ==================================

class QualityResult(CamelCaseModel):

    status: str = "UNKNOWN"

    can_process: bool = Field(
        default=True,
        alias="canProcess"
    )

    width: int = 0

    height: int = 0

    pixels: int = 0

    brightness: float = 0

    contrast: float = 0

    warnings: List[str] = Field(
        default_factory=list
    )



# ==================================
# Resultado procesamiento imagen
# ==================================

class ProcessingResult(CamelCaseModel):

    processed: bool = False

    original_size: int = Field(
        default=0,
        alias="originalSize"
    )

    new_size: int = Field(
        default=0,
        alias="newSize"
    )

    width: int = 0

    height: int = 0



# ==================================
# Resultado OCR
# ==================================

class OCRResult(CamelCaseModel):

    text: str = ""

    confidence: Optional[float] = None



# ==================================
# Respuesta completa Engine
# ==================================

class OCREngineResponse(CamelCaseModel):

    success: bool = True

    validation: Optional[ValidationResult] = None

    quality: Optional[QualityResult] = None

    processing: Optional[ProcessingResult] = None

    ocr: Optional[OCRResult] = None

    message: Optional[str] = None



# ==================================
# Manejo de errores
# ==================================

class ErrorDetail(CamelCaseModel):
    """
    Detalle estándar de error.
    """

    code: str

    message: str



class ErrorResponse(CamelCaseModel):
    """
    Respuesta estándar cuando el Engine
    no puede completar el proceso.
    """

    success: bool = False

    error: ErrorDetail
