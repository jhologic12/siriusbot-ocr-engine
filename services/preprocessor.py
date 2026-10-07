"""
Preprocessor Service
--------------------
Preparación de imágenes para mejorar OCR.
"""

from io import BytesIO

from PIL import (
    Image,
    ImageOps,
)

from config import (
    UPSCALE_WIDTH,
    JPEG_QUALITY,
)



def preprocess_image(
    image: Image.Image,
) -> Image.Image:
    """
    Preprocesa una imagen para mejorar
    la precisión del OCR.

    Pipeline:

    1. Corrección de orientación EXIF
    2. Conversión a RGB
    3. Escalado
    4. Conversión a escala de grises

    Returns:
        PIL.Image
    """

    if image.width == 0 or image.height == 0:

        raise ValueError(
            "La imagen no tiene dimensiones válidas"
        )


    # ==========================
    # Corrección orientación EXIF
    # ==========================

    image = ImageOps.exif_transpose(
        image
    )


    # ==========================
    # Conversión RGB
    # ==========================

    image = image.convert(
        "RGB"
    )


    # ==========================
    # Escalado
    # ==========================

    if image.width < UPSCALE_WIDTH:

        ratio: float = (
            UPSCALE_WIDTH /
            image.width
        )

        new_height: int = int(
            image.height * ratio
        )


        image = image.resize(
            (
                UPSCALE_WIDTH,
                new_height,
            ),
            Image.Resampling.LANCZOS,
        )

    # ==========================
    # Conversión a escala de grises
    # ==========================

    image = image.convert(
        "L"
    )


    return image





def image_to_bytes(
    image: Image.Image,
) -> bytes:
    """
    Convierte una imagen PIL
    a bytes JPEG.
    """

    buffer = BytesIO()


    image.save(
        buffer,
        format="JPEG",
        quality=JPEG_QUALITY,
        optimize=True,
    )


    return buffer.getvalue()
