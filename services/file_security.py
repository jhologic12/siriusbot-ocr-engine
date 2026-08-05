"""
File Security Service
---------------------
Validación de seguridad del contenido real del archivo.
"""

from pathlib import Path

import magic

from utils.constants import (
    ALLOWED_IMAGE_MIME_TYPES,
    ALLOWED_IMAGE_EXTENSIONS,
)


def validate_file_security(
    filename: str,
    file_bytes: bytes,
) -> tuple[bool, list[str]]:
    """
    Valida seguridad básica del archivo.

    Verifica:
    - Extensión permitida
    - MIME real del contenido
    - Correspondencia extensión/MIME
    """

    errors: list[str] = []


    # ==========================
    # Extensión
    # ==========================

    extension = (
        Path(filename)
        .suffix
        .lower()
    )


    if extension not in ALLOWED_IMAGE_EXTENSIONS:

        errors.append(
            f"Extensión no permitida: {extension}"
        )


    # ==========================
    # MIME real
    # ==========================

    detected_mime = magic.from_buffer(
        file_bytes,
        mime=True
    )


    if detected_mime not in ALLOWED_IMAGE_MIME_TYPES:

        errors.append(
            f"MIME no permitido: {detected_mime}"
        )


    # ==========================
    # Validación extensión MIME
    # ==========================

    mime_extension_map = {

        ".jpg": {
            "image/jpeg"
        },

        ".jpeg": {
            "image/jpeg"
        },

        ".png": {
            "image/png"
        },

        ".webp": {
            "image/webp"
        },
    }


    allowed_mimes = mime_extension_map.get(
        extension,
        set()
    )


    if detected_mime not in allowed_mimes:

        errors.append(
            (
                "Extensión no coincide con "
                f"MIME real ({extension} -> {detected_mime})"
            )
        )


    return (
        len(errors) == 0,
        errors,
    )