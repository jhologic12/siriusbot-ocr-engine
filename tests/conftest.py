"""Configuración compartida para las pruebas."""

import pytest

from utils.rate_limiter import rate_limiter


@pytest.fixture(autouse=True)
def isolate_rate_limiter():
    """Evita que el estado del limitador se comparta entre pruebas."""
    rate_limiter.reset()
    yield
    rate_limiter.reset()
