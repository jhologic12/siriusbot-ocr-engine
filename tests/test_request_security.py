"""
Tests Request Security
----------------------
Validaciones de seguridad HTTP.
"""

import pytest

from fastapi import HTTPException
from starlette.requests import Request

from config import MAX_FILE_SIZE
from utils.request_security import validate_request


@pytest.mark.anyio
async def test_reject_non_multipart_request():
    scope = {
        "type": "http",
        "method": "POST",
        "headers": [
            (
                b"content-type",
                b"application/json",
            )
        ],
    }

    request = Request(scope)

    with pytest.raises(HTTPException) as error:
        await validate_request(request)

    assert error.value.status_code == 415


@pytest.mark.anyio
async def test_reject_large_request():
    scope = {
        "type": "http",
        "method": "POST",
        "headers": [
            (
                b"content-type",
                b"multipart/form-data; boundary=test",
            ),
            (
                b"content-length",
                str(MAX_FILE_SIZE + 1).encode(),
            ),
        ],
    }

    request = Request(scope)

    with pytest.raises(HTTPException) as error:
        await validate_request(request)

    assert error.value.status_code == 413


@pytest.mark.anyio
async def test_accept_request_at_maximum_size():
    scope = {
        "type": "http",
        "method": "POST",
        "headers": [
            (
                b"content-type",
                b"multipart/form-data; boundary=test",
            ),
            (
                b"content-length",
                str(MAX_FILE_SIZE).encode(),
            ),
        ],
    }

    request = Request(scope)

    result = await validate_request(request)

    assert result is None


@pytest.mark.anyio
async def test_accept_request_without_content_length():
    scope = {
        "type": "http",
        "method": "POST",
        "headers": [
            (
                b"content-type",
                b"multipart/form-data; boundary=test",
            )
        ],
    }

    request = Request(scope)

    result = await validate_request(request)

    assert result is None
