"""
Tests Request Security
----------------------
Validaciones de seguridad HTTP.
"""

import pytest

from fastapi import HTTPException
from starlette.requests import Request

from utils.request_security import validate_request

@pytest.mark.anyio
async def test_reject_non_multipart_request():

    scope = {
        "type": "http",
        "method": "POST",
        "headers": [
            (
                b"content-type",
                b"application/json"
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
                b"multipart/form-data"
            ),
            (
                b"content-length",
                b"999999999"
            )
        ],
    }


    request = Request(scope)


    with pytest.raises(HTTPException) as error:

        await validate_request(request)


    assert error.value.status_code == 413



@pytest.mark.anyio
async def test_accept_valid_request():

    scope = {
        "type": "http",
        "method": "POST",
        "headers": [
            (
                b"content-type",
                b"multipart/form-data"
            ),
            (
                b"content-length",
                b"1000"
            )
        ],
    }


    request = Request(scope)


    result = await validate_request(request)


    assert result is None