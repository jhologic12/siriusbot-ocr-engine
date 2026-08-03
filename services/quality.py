"""
Análisis de calidad de imágenes para OCR.
"""

from PIL import Image, ImageStat

from config import (
    MIN_PIXELS,
    MIN_CONTRAST,
    MIN_BRIGHTNESS,
    MAX_BRIGHTNESS,
)

from models.response_models import QualityResult



def analyze_quality(
    image: Image.Image,
) -> QualityResult:
    """
    Analiza si una imagen tiene calidad suficiente
    para ejecutar OCR.
    """

    gray = image.convert(
        "L"
    )

    stat = ImageStat.Stat(
        gray
    )


    width: int = image.width

    height: int = image.height

    pixels: int = width * height


    brightness: float = stat.mean[0]

    contrast: float = stat.stddev[0]


    warnings: list[str] = []


    status: str = "GOOD"

    can_process: bool = True


    # ==========================
    # Resolución
    # ==========================

    if pixels < MIN_PIXELS:

        status = "WARNING"

        warnings.append(
            "Resolución baja"
        )


    if pixels < (MIN_PIXELS // 2):

        status = "BAD"

        can_process = False

        warnings.append(
            "Imagen demasiado pequeña"
        )


    # ==========================
    # Brillo
    # ==========================

    if brightness < MIN_BRIGHTNESS:

        status = "WARNING"

        warnings.append(
            "Imagen oscura"
        )


    elif brightness > MAX_BRIGHTNESS:

        status = "WARNING"

        warnings.append(
            "Imagen demasiado clara"
        )


    # ==========================
    # Contraste
    # ==========================

    if contrast < MIN_CONTRAST:

        status = "WARNING"

        warnings.append(
            "Contraste bajo"
        )


    return QualityResult(

        status=status,

        can_process=can_process,

        width=width,

        height=height,

        pixels=pixels,

        brightness=round(
            brightness,
            2
        ),

        contrast=round(
            contrast,
            2
        ),

        warnings=warnings,
    )
