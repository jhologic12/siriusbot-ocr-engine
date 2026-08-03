"""
Request Context
---------------
Gestiona el contexto de cada petición HTTP.
Permite almacenar un Request ID único por solicitud.
"""

from contextvars import ContextVar
from uuid import uuid4


# Contexto aislado por petición
_request_id: ContextVar[str] = ContextVar(
    "request_id",
    default=""
)


def generate_request_id() -> str:
    """
    Genera un nuevo Request ID y lo almacena
    en el contexto actual.
    """

    request_id = str(uuid4())

    _request_id.set(request_id)

    return request_id


def get_request_id() -> str:
    """
    Obtiene el Request ID actual.
    """

    return _request_id.get()


def set_request_id(
    request_id: str,
) -> None:
    """
    Permite establecer manualmente
    un Request ID.
    """

    _request_id.set(request_id)


def clear_request_id() -> None:
    """
    Limpia el contexto.
    """

    _request_id.set("")
