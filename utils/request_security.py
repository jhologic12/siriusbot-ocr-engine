"""
Request Security Middleware
---------------------------
Protecciones de seguridad para las peticiones HTTP.
"""

from fastapi import HTTPException, Request

from config import MAX_FILE_SIZE


async def validate_request(
    request: Request,
) -> None:
    """
    Valida la petición antes de que sea
    procesada por el OCR Engine.
    """

    content_type = request.headers.get("content-type", "").lower()

    if "multipart/form-data" not in content_type:
        raise HTTPException(
            status_code=415,
            detail="Request must be multipart/form-data",
        )

    content_length = request.headers.get("content-length")

    if content_length:

        if int(content_length) > MAX_FILE_SIZE:

            raise HTTPException(
                status_code=413,
                detail="File exceeds maximum allowed size",
            )
