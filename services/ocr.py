"""
OCR Service
-----------
Ejecuta reconocimiento de texto usando Tesseract.
"""

import pytesseract

from PIL import Image

from config import (
    OCR_LANGUAGE,
    OCR_CONFIG,
)

from models.response_models import OCRResult



def extract_text(
    image: Image.Image,
) -> OCRResult:
    """
    Ejecuta OCR sobre una imagen.

    Obtiene:
    - Texto reconocido
    - Confianza promedio del OCR

    Returns:
        OCRResult
    """


    # ==========================
    # Extracción de texto
    # ==========================

    text: str = pytesseract.image_to_string(
        image,
        lang=OCR_LANGUAGE,
        config=OCR_CONFIG,
    )


    # ==========================
    # Cálculo de confianza
    # ==========================

    data = pytesseract.image_to_data(
        image,
        lang=OCR_LANGUAGE,
        config=OCR_CONFIG,
        output_type=pytesseract.Output.DICT,
    )


    confidences = []


    for confidence in data["conf"]:

        try:

            value = float(confidence)

            if value >= 0:

                confidences.append(value)

        except ValueError:

            continue



    confidence = None


    if confidences:

        confidence = round(
            sum(confidences) / len(confidences),
            2,
        )


    return OCRResult(
        text=text.strip(),
        confidence=confidence,
    )
