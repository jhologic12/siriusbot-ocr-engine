"""
Configuración global del OCR Engine.

SiriusBot OCR Engine
"""

import os


# ==========================
# Runtime Environment
# ==========================

APP_ENV: str = os.getenv("APP_ENV", "development")

VALID_APP_ENVS = {
    "development",
    "test",
    "production",
}

if APP_ENV not in VALID_APP_ENVS:
    raise ValueError(
        f"APP_ENV must be one of: {', '.join(sorted(VALID_APP_ENVS))}"
    )


SERVICE_NAME: str = os.getenv(
    "SERVICE_NAME",
    "SiriusBot OCR Engine",
)


LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

VALID_LOG_LEVELS = {
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
}

if LOG_LEVEL not in VALID_LOG_LEVELS:
    raise ValueError(
        f"LOG_LEVEL must be one of: {', '.join(sorted(VALID_LOG_LEVELS))}"
    )


# ==========================
# OCR
# ==========================

OCR_LANGUAGE: str = "spa"

OCR_ENGINE_MODE: int = 3
"""
Tesseract OCR Engine Mode.
3 = Default automático.
"""

OCR_PAGE_SEGMENT: int = 6
"""
Tesseract Page Segmentation Mode.
6 = Bloque uniforme de texto.
"""

OCR_CONFIG: str = (
    f"--oem {OCR_ENGINE_MODE} "
    f"--psm {OCR_PAGE_SEGMENT}"
)


# ==========================
# OCR Timeout
# ==========================

OCR_TIMEOUT_SECONDS: int = int(
    os.getenv("OCR_TIMEOUT_SECONDS", "15")
)

if OCR_TIMEOUT_SECONDS <= 0:
    raise ValueError(
        "OCR_TIMEOUT_SECONDS must be greater than 0"
    )


# ==========================
# Imagen
# ==========================

MIN_FILE_SIZE: int = 15_000
"""
Tamaño mínimo permitido en bytes.
"""

MAX_FILE_SIZE_MB: int = int(
    os.getenv("MAX_FILE_SIZE_MB", "20")
)

if MAX_FILE_SIZE_MB <= 0:
    raise ValueError(
        "MAX_FILE_SIZE_MB must be greater than 0"
    )

MAX_FILE_SIZE: int = MAX_FILE_SIZE_MB * 1024 * 1024

MIN_WIDTH: int = 800

MIN_HEIGHT: int = 800


# ==========================
# Calidad imagen
# ==========================

MIN_PIXELS: int = 400_000

MIN_CONTRAST: int = 15

MIN_BRIGHTNESS: int = 45

MAX_BRIGHTNESS: int = 250


# ==========================
# Preprocesamiento
# ==========================

UPSCALE_WIDTH: int = 1200

JPEG_QUALITY: int = 95

SHARPNESS_FACTOR: float = 2.0

CONTRAST_FACTOR: float = 1.8
