"""
SiriusBot OCR Engine
--------------------
API principal del microservicio OCR.
"""

import io
import time

from fastapi import FastAPI, UploadFile, File, Request

from fastapi.responses import JSONResponse

from PIL import Image


from services.validator import validate_image

from services.file_security import (
    validate_file_security,
)

from services.preprocessor import (
    preprocess_image,
    image_to_bytes,
)

from services.quality import analyze_quality

from services.ocr import extract_text

from services.response_builder import build_response


from models.response_models import ProcessingResult


from utils.error_handlers import (
    register_exception_handlers,
)

from utils.middleware import (
    observability_middleware,
)

from utils.request_security import (
    validate_request,
)

from utils.metrics import metrics

from utils.telemetry import (
    register_request,
    register_success,
    register_error,
)

app = FastAPI(
    title="SiriusBot OCR Engine",
    description="Microservicio OCR para procesamiento de facturas",
    version="1.0.0",
)


# ==================================
# Observabilidad
# ==================================

app.middleware("http")(observability_middleware)


register_exception_handlers(app)


# ==================================
# Health
# ==================================


@app.get("/")
def root():

    return {
        "service": "SiriusBot OCR Engine",
        "status": "running",
    }


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "siriusbot-ocr-engine",
    }


@app.get("/ready")
def readiness():

    return {
        "status": "ready",
    }


# ==================================
# Metrics endpoint
# ==================================


@app.get("/metrics")
def get_metrics():

    return metrics.get_metrics()


# ==================================
# OCR Pipeline
# ==================================


@app.post("/ocr")
async def process_image(request: Request, file: UploadFile = File(...)):

    start_time = time.perf_counter()

    register_request("POST", "/ocr")

    try:

        await validate_request(request)

        image_bytes = await file.read()

        # ===============================
        # Seguridad del contenido archivo
        # ===============================

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
                        "message": ("Archivo rechazado por validación de seguridad"),
                        "details": security_errors,
                    },
                },
            )

        # ===============================
        # Validación inicial
        # ===============================

        validation = validate_image(image_bytes)

        if not validation.valid:

            register_error("INVALID_IMAGE")

            response = build_response(validation=validation, message="Imagen inválida")

            data = response.model_dump()

            data["error"] = {"code": "INVALID_IMAGE", "message": "Imagen inválida"}

            return JSONResponse(status_code=400, content=data)

        # ===============================
        # Carga imagen
        # ===============================

        image = Image.open(io.BytesIO(image_bytes))

        from services.image_security import (
            validate_image_dimensions,
        )

        image_valid, image_errors = validate_image_dimensions(image)
        if not image_valid:
            register_error("IMAGE_SECURITY_ERROR")

            return JSONResponse(
                status_code=413,
                content={
                    "success": False,
                    "error": {
                        "code": "IMAGE_TOO_LARGE",
                        "message": "Image dimensions exceed security limits",
                        "details": image_errors,
                    },
                },
            )

        # ===============================
        # Preprocesamiento
        # ===============================

        processed_image = preprocess_image(image)

        processed_bytes = image_to_bytes(processed_image)

        # ===============================
        # Análisis calidad
        # ===============================

        quality = analyze_quality(processed_image)

        if not quality.can_process:

            register_error("LOW_QUALITY")

            response = build_response(
                validation=validation, quality=quality, message="Calidad insuficiente"
            )

            data = response.model_dump()

            data["error"] = {"code": "LOW_QUALITY", "message": "Calidad insuficiente"}

            return JSONResponse(status_code=422, content=data)

        # ===============================
        # OCR
        # ===============================

        ocr_result = extract_text(processed_image)

        # ===============================
        # Información procesamiento
        # ===============================

        processing = ProcessingResult(
            processed=True,
            originalSize=len(image_bytes),
            newSize=len(processed_bytes),
            width=processed_image.width,
            height=processed_image.height,
        )

        elapsed = time.perf_counter() - start_time

        metrics.add_processing_time(elapsed)

        metrics.increment("ocr_success")

        register_success(elapsed)

        # ===============================
        # Respuesta exitosa
        # ===============================

        response = build_response(
            validation=validation,
            quality=quality,
            processing=processing,
            ocr=ocr_result,
            message="Proceso completado",
        )

        data = response.model_dump()

        data["error"] = None

        return JSONResponse(status_code=200, content=data)

    except Exception as error:

        metrics.increment("ocr_failed")

        register_error("OCR_EXCEPTION")

        raise error
