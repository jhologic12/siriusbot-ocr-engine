"""
OCR endpoints para la API v1.
"""

from fastapi import APIRouter, File, Request, UploadFile

from services.ocr_pipeline import execute_ocr_pipeline

router = APIRouter()


@router.post("/ocr")
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
