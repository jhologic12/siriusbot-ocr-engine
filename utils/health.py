"""
Health checks del SiriusBot OCR Engine.
"""

import pytesseract

from config import OCR_LANGUAGE


def check_tesseract() -> bool:
    """
    Verifica que Tesseract OCR esté disponible.
    """

    try:
        pytesseract.get_tesseract_version()
        return True

    except Exception:
        return False


def check_ocr_language() -> bool:
    """
    Verifica que el idioma configurado para OCR
    esté disponible en Tesseract.
    """

    try:
        languages = pytesseract.get_languages(config="")
        return OCR_LANGUAGE in languages

    except Exception:
        return False


def check_readiness() -> dict[str, str]:
    """
    Ejecuta las comprobaciones necesarias para determinar
    si el servicio está listo para procesar OCR.
    """

    tesseract_ready = check_tesseract()
    language_ready = check_ocr_language()

    return {
        "tesseract": "ready"
        if tesseract_ready
        else "unavailable",
        "ocr_language": "ready"
        if language_ready
        else "unavailable",
    }


def is_ready(checks: dict[str, str]) -> bool:
    """
    Determina si todas las dependencias necesarias
    están disponibles.
    """

    return all(
        status == "ready"
        for status in checks.values()
    )
