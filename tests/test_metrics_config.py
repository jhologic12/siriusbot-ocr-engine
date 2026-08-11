"""
Pruebas unitarias para la política
del endpoint de métricas.
"""

from config import get_metrics_config


def test_metrics_enabled_in_development():
    """Las métricas deben estar disponibles en desarrollo."""

    result = get_metrics_config("development")

    assert result["enabled"] is True


def test_metrics_enabled_in_test():
    """Las métricas deben estar disponibles en testing."""

    result = get_metrics_config("test")

    assert result["enabled"] is True


def test_metrics_disabled_in_production():
    """Las métricas deben estar deshabilitadas en producción."""

    result = get_metrics_config("production")

    assert result["enabled"] is False
