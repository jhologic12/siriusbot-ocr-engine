"""
Input Security Service
----------------------
Validaciones de seguridad antes del procesamiento OCR.
"""

from pathlib import Path

from utils.constants import (
    MAX_UPLOAD_SIZE_BYTES,
    ALLOWED_IMAGE_EXTENSIONS,
    ALLOWED_IMAGE_MIME_TYPES,
)

from utils.exceptions import InvalidImageException



def validate_upload_security(
    filename: str,
    content_type: str,
    file_size: int,
):
    """
    Validaciones básicas de seguridad
    del archivo recibido.
    """


    # ==========================
    # Tamaño
    # ==========================

    if file_size > MAX_UPLOAD_SIZE_BYTES:

        raise InvalidImageException(
            message="El archivo supera el tamaño máximo permitido"
        )


    # ==========================
    # Extensión
    # ==========================

    extension = (
        Path(filename)
        .suffix
        .lower()
    )


    if extension not in ALLOWED_IMAGE_EXTENSIONS:

        raise InvalidImageException(
            message="Extensión de archivo no permitida"
        )


    # ==========================
    # MIME declarado
    # ==========================

    if content_type not in ALLOWED_IMAGE_MIME_TYPES:

        raise InvalidImageException(
            message="Tipo de archivo no permitido"
        )


    return True