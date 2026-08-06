"""
Error Handlers
--------------
Manejadores globales de errores HTTP
del SiriusBot OCR Engine.
"""

from fastapi import (
    Request,
    FastAPI,
)

from fastapi.responses import JSONResponse


from utils.exceptions import (
    OCRException,
)

# ==================================cle
# Handler principal OCR
# ==================================


# pylint: disable=unused-argument
async def ocr_exception_handler(
    request: Request,
    exc: OCRException,
):
    """
    Convierte excepciones OCR controladas
    en respuestas HTTP estándar.
    """

    status_code = 500

    if exc.code == "INVALID_IMAGE":

        status_code = 400

    elif exc.code == "LOW_IMAGE_QUALITY":

        status_code = 422

    elif exc.code == "OCR_TIMEOUT":

        status_code = 504

    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message,
            },
        },
    )


# ==================================
# Registro FastAPI
# ==================================


def register_exception_handlers(
    app: FastAPI,
):
    """
    Registra handlers globales
    del OCR Engine.
    """

    app.add_exception_handler(
        OCRException,
        ocr_exception_handler,
    )
