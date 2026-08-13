"""
Pipeline principal de procesamiento OCR.
"""

import io
import time

from PIL import Image

from fastapi import UploadFile, Request
from fastapi.responses import JSONResponse

from models.response_models import ProcessingResult

from services.file_security import validate_file_security
from services.image_security import validate_image_dimensions
from services.ocr import extract_text
from services.preprocessor import (
    preprocess_image,
    image_to_bytes,
)
from services.quality import analyze_quality
from services.response_builder import build_response
from services.validator import validate_image

from utils.metrics import metrics

from utils.request_security import (
    read_upload_with_limit,
    validate_request,
)

from utils.telemetry import (
    register_error,
    register_request,
    register_success,
)

from utils.prometheus_metrics import (
    register_ocr_success,
    register_ocr_failure,
    register_ocr_processing_time,
)


async def execute_ocr_pipeline(
    request: Request,
    file: UploadFile,
):
    """
    Ejecuta el pipeline completo de procesamiento OCR.

    Incluye:
    - Validación HTTP.
    - Seguridad del archivo.
    - Validación de imagen.
    - Preprocesamiento.
    - Análisis de calidad.
    - OCR.
    - Construcción de respuesta.
    """

    start_time = time.perf_counter()

    register_request("POST", "/ocr")

    try:
        await validate_request(request)

        image_bytes = await read_upload_with_limit(file)

        file_valid, security_errors = validate_file_security(
            file.filename,
            image_bytes,
        )

        if not file_valid:
            register_error("FILE_SECURITY_ERROR")

            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": {
                        "code": "FILE_SECURITY_ERROR",
                        "message": "Archivo rechazado por validación de seguridad",
                        "details": security_errors,
                    },
                },
            )

        validation = validate_image(image_bytes)

        if not validation.valid:

            register_error("INVALID_IMAGE")

            response = build_response(
                validation=validation,
                message="Imagen inválida",
            )

            data = response.model_dump(by_alias=True)

            data["error"] = {
                "code": "INVALID_IMAGE",
            }

            return JSONResponse(
                status_code=400,
                content=data,
            )

        image = Image.open(io.BytesIO(image_bytes))

        image_valid, image_errors = validate_image_dimensions(image)

        if not image_valid:

            register_error("IMAGE_SECURITY_ERROR")

            return JSONResponse(
                status_code=413,
                content={
                    "success": False,
                    "error": {
                        "code": "IMAGE_TOO_LARGE",
                        "details": image_errors,
                    },
                },
            )

        processed_image = preprocess_image(image)

        processed_bytes = image_to_bytes(processed_image)

        quality = analyze_quality(processed_image)

        if not quality.can_process:

            register_error("LOW_QUALITY")

            response = build_response(
                validation=validation,
                quality=quality,
                message="Calidad insuficiente",
            )

            return JSONResponse(
                status_code=422,
                content=response.model_dump(by_alias=True),
            )

        ocr_start_time = time.perf_counter()

        ocr_result = extract_text(processed_image)

        ocr_elapsed = time.perf_counter() - ocr_start_time

        register_ocr_processing_time(ocr_elapsed)

        processing = ProcessingResult(
            processed=True,
            originalSize=len(image_bytes),
            newSize=len(processed_bytes),
            width=processed_image.width,
            height=processed_image.height,
        )

        elapsed = time.perf_counter() - start_time

        metrics.add_processing_time(elapsed)

        register_success()
        register_ocr_success()

        response = build_response(
            validation=validation,
            quality=quality,
            processing=processing,
            ocr=ocr_result,
            message="Proceso completado",
        )

        data = response.model_dump(by_alias=True)

        data["error"] = None

        return JSONResponse(
            status_code=200,
            content=data,
        )

    except Exception as error:

        metrics.increment("ocr_failed")

        register_error("OCR_EXCEPTION")
        register_ocr_failure()

        raise error
