"""
Pruebas unitarias para la política
de documentación de la API.
"""

from config import get_api_docs_config


def test_api_docs_enabled_in_development():
    """La documentación debe estar disponible en desarrollo."""

    result = get_api_docs_config("development")

    assert result["docs_url"] == "/docs"
    assert result["redoc_url"] == "/redoc"
    assert result["openapi_url"] == "/openapi.json"


def test_api_docs_enabled_in_test():
    """La documentación debe estar disponible en testing."""

    result = get_api_docs_config("test")

    assert result["docs_url"] == "/docs"
    assert result["redoc_url"] == "/redoc"
    assert result["openapi_url"] == "/openapi.json"


def test_api_docs_disabled_in_production():
    """La documentación debe estar deshabilitada en producción."""

    result = get_api_docs_config("production")

    assert result["docs_url"] is None
    assert result["redoc_url"] is None
    assert result["openapi_url"] is None
