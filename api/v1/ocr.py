"""
OCR endpoints para la API v1.
"""

import secrets

import config
from fastapi import (
    APIRouter,
    Depends,
    File,
    Header,
    HTTPException,
    Request,
    UploadFile,
)

from services.ocr_pipeline import execute_ocr_pipeline

router = APIRouter()


def verify_api_key(
    x_api_key: str | None = Header(
        default=None,
        alias="X-API-Key",
    ),
) -> None:
    """Valida la clave API cuando está configurada."""

    expected_key = config.OCR_API_KEY

    # En desarrollo y pruebas puede omitirse la clave.
    if expected_key is None:
        return

    if (
        not x_api_key
        or not secrets.compare_digest(
            x_api_key.encode("utf-8"),
            expected_key.encode("utf-8"),
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas",
        )


@router.post(
    "/ocr",
    dependencies=[Depends(verify_api_key)],
)
async def process_image(
    request: Request,
    file: UploadFile = File(...),
):
    """
    Procesa una imagen enviada al motor OCR.

    Ejecuta validaciones de seguridad,
    preprocesamiento, análisis de calidad
    y extracción de texto.
    """

    return await execute_ocr_pipeline(
        request,
        file,
    )
