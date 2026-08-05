"""
Constantes globales del OCR Engine
"""


# ==========================
# Seguridad entrada imagen
# ==========================

MAX_UPLOAD_SIZE_MB = 10

MAX_UPLOAD_SIZE_BYTES = (
    MAX_UPLOAD_SIZE_MB * 1024 * 1024
)


# ==========================
# Seguridad MIME
# ==========================

ALLOWED_IMAGE_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


# ==========================
# Seguridad extensión
# ==========================

ALLOWED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}