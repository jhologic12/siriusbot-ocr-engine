"""
Request Context Tests
---------------------
Pruebas del contexto por petición.
"""

from utils.request_context import (
    generate_request_id,
    get_request_id,
    set_request_id,
    clear_request_id,
)


def test_generate_request_id():

    request_id = generate_request_id()

    assert isinstance(request_id, str)

    assert len(request_id) > 30


def test_get_request_id():

    generate_request_id()

    assert get_request_id() != ""


def test_set_request_id():

    set_request_id("ABC123")

    assert get_request_id() == "ABC123"


def test_clear_request_id():

    set_request_id("ABC123")

    clear_request_id()

    assert get_request_id() == ""
