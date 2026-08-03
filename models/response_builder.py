"""
Response Models
---------------
Modelos estándar de respuesta del OCR Engine
"""

from typing import List, Optional
from pydantic import BaseModel


# ==================================
# Metadata de imagen
# ==================================

class ImageMetadata(BaseModel):

    format: Optional[str] = None

    mode: Optional[str] = None

    width: int = 0

    height: int = 0

    pixels: int = 0

    sizeBytes: int = 0



# ==================================
# Resultado de validación
# ==================================

class ValidationResult(BaseModel):

    valid: bool = True

    errors: List[str] = []

    warnings: List[str] = []

    metadata: Optional[ImageMetadata] = None



# ==================================
# Calidad de imagen
# ==================================

class QualityResult(BaseModel):

    status: str = "UNKNOWN"

    canProcess: bool = True

    width: int = 0

    height: int = 0

    pixels: int = 0

    brightness: float = 0

    contrast: float = 0

    warnings: List[str] = []



# ==================================
# Resultado procesamiento
# ==================================

class ProcessingResult(BaseModel):

    processed: bool = False

    originalSize: int = 0

    newSize: int = 0

    width: int = 0

    height: int = 0



# ==================================
# Resultado OCR
# ==================================

class OCRResult(BaseModel):

    text: str = ""

    confidence: Optional[float] = None



# ==================================
# Respuesta principal del Engine
# ==================================

class OCREngineResponse(BaseModel):

    success: bool

    validation: Optional[ValidationResult] = None

    quality: Optional[QualityResult] = None

    processing: Optional[ProcessingResult] = None

    ocr: Optional[OCRResult] = None

    message: Optional[str] = None
