"""
Validator Service
-----------------
Validación inicial de imágenes para OCR Engine.
"""

from io import BytesIO

from PIL import Image

from config import (
    MIN_FILE_SIZE,
    MAX_FILE_SIZE,
    MIN_WIDTH,
    MIN_HEIGHT,
)

from models.response_models import (
    ValidationResult,
    ImageMetadata,
)


SUPPORTED_FORMATS: tuple[str, ...] = (
    "JPEG",
    "PNG",
    "TIFF",
    "BMP",
    "WEBP",
)



def validate_image(
    image_bytes: bytes
) -> ValidationResult:
    """
    Valida una imagen recibida como bytes.

    Returns:
        ValidationResult
    """

    errors: list[str] = []

    warnings: list[str] = []


    # ==========================
    # Tamaño archivo
    # ==========================

    file_size: int = len(image_bytes)


    if file_size < MIN_FILE_SIZE:

        warnings.append(
            f"Imagen pequeña ({file_size} bytes)"
        )


    if file_size > MAX_FILE_SIZE:

        return ValidationResult(
            valid=False,
            errors=[
                "La imagen supera el tamaño máximo permitido"
            ],
        )


    # ==========================
    # Apertura imagen
    # ==========================

    try:

        image = Image.open(
            BytesIO(image_bytes)
        )

        image.verify()


        image = Image.open(
            BytesIO(image_bytes)
        )


    except Exception as error:

        return ValidationResult(
            valid=False,
            errors=[
                f"Imagen corrupta: {str(error)}"
            ],
        )


    # ==========================
    # Formato
    # ==========================

    image_format = image.format


    if image_format not in SUPPORTED_FORMATS:

        errors.append(
            f"Formato no soportado: {image_format}"
        )


    # ==========================
    # Resolución
    # ==========================

    image_width, image_height = image.size


    if image_width < MIN_WIDTH:

        warnings.append(
            f"Ancho bajo ({image_width}px)"
        )


    if image_height < MIN_HEIGHT:

        warnings.append(
            f"Alto bajo ({image_height}px)"
        )


    # ==========================
    # Metadata
    # ==========================

    metadata = ImageMetadata(

        format=image_format,

        mode=image.mode,

        width=image_width,

        height=image_height,

        pixels=image_width * image_height,

        size_bytes=file_size,
    )


    return ValidationResult(

        valid=len(errors) == 0,

        errors=errors,

        warnings=warnings,

        metadata=metadata,
    )
