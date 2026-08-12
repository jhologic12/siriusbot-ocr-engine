"""
Pruebas unitarias de los health checks.
"""

from utils.health import (
    check_ocr_language,
    check_readiness,
    check_tesseract,
    is_ready,
)


def test_check_tesseract():
    """
    Verifica que Tesseract esté disponible.
    """

    assert check_tesseract() is True


def test_check_ocr_language():
    """
    Verifica que el idioma OCR configurado esté disponible.
    """

    assert check_ocr_language() is True


def test_check_readiness():
    """
    Verifica que las dependencias necesarias estén listas.
    """

    checks = check_readiness()

    assert checks["tesseract"] == "ready"
    assert checks["ocr_language"] == "ready"


def test_is_ready_when_all_checks_are_ready():
    """
    Verifica que el servicio se considere listo
    cuando todas las dependencias están disponibles.
    """

    checks = {
        "tesseract": "ready",
        "ocr_language": "ready",
    }

    assert is_ready(checks) is True


def test_is_not_ready_when_a_check_fails():
    """
    Verifica que el servicio no esté listo cuando
    alguna dependencia no está disponible.
    """

    checks = {
        "tesseract": "ready",
        "ocr_language": "unavailable",
    }

    assert is_ready(checks) is False


def test_check_tesseract_when_unavailable(monkeypatch):
    """
    Verifica que el health check detecte
    cuando Tesseract no está disponible.
    """

    def raise_error():
        raise RuntimeError("Tesseract unavailable")

    monkeypatch.setattr(
        "utils.health.pytesseract.get_tesseract_version",
        raise_error,
    )

    assert check_tesseract() is False


def test_check_ocr_language_when_unavailable(monkeypatch):
    """
    Verifica que el health check detecte
    cuando el idioma OCR no está disponible.
    """

    monkeypatch.setattr(
        "utils.health.pytesseract.get_languages",
        lambda config="": ["eng", "osd"],
    )

    assert check_ocr_language() is False
