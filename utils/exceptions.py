"""
Exceptions
-----------
Excepciones estándar del SiriusBot OCR Engine.
"""


# ==================================
# Excepción base OCR Engine
# ==================================

class OCRException(Exception):
    """
    Excepción base para errores controlados
    del motor OCR.
    """

    def __init__(
        self,
        message: str,
        code: str = "OCR_ERROR"
    ):
        self.message = message
        self.code = code

        super().__init__(message)



# ==================================
# Imagen inválida
# ==================================

class InvalidImageException(OCRException):
    """
    Error cuando la imagen no puede
    ser procesada.
    """

    def __init__(
        self,
        message: str = "Imagen inválida",
        code: str = "INVALID_IMAGE"
    ):
        super().__init__(
            message=message,
            code=code
        )



# ==================================
# Calidad insuficiente
# ==================================

class LowQualityException(OCRException):
    """
    Error cuando la imagen tiene
    calidad insuficiente para OCR.
    """

    def __init__(
        self,
        message: str = "Calidad de imagen insuficiente",
        code: str = "LOW_IMAGE_QUALITY"
    ):
        super().__init__(
            message=message,
            code=code
        )



# ==================================
# Error procesamiento OCR
# ==================================

class OCRProcessingException(OCRException):
    """
    Error durante la ejecución
    del motor OCR.
    """

    def __init__(
        self,
        message: str = "Error procesando OCR",
        code: str = "OCR_PROCESSING_ERROR"
    ):
        super().__init__(
            message=message,
            code=code
        )
