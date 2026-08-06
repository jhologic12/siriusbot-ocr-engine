"""
Tests OCR Timeout Protection
----------------------------
Valida protección contra procesos OCR
que exceden el tiempo permitido.
"""

from unittest.mock import patch

import pytest

from PIL import Image

from services.ocr import extract_text

from utils.exceptions import OCRTimeoutException


def test_ocr_timeout_exception():
    """
    Simula que Tesseract supera
    el tiempo máximo permitido.
    """

    image = Image.new(
        "RGB",
        (1000, 1000),
    )

    with patch("services.ocr.pytesseract.image_to_string") as mock_ocr:

        mock_ocr.side_effect = TimeoutError()

        with pytest.raises(OCRTimeoutException):

            extract_text(image)
