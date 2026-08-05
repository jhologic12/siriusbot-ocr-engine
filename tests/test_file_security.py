"""
Tests File Security Service
"""

from pathlib import Path


from services.file_security import (
    validate_file_security,
)


INVOICE_PATH = Path(
    "tests/invoices/test_invoice.jpg"
)


FAKE_PATH = Path(
    "tests/invoices/fake.txt"
)



def test_reject_fake_text_file():

    file_bytes = FAKE_PATH.read_bytes()


    valid, errors = validate_file_security(
        "fake.txt",
        file_bytes,
    )


    assert valid is False
    assert len(errors) > 0



def test_detect_extension_mismatch():

    file_bytes = INVOICE_PATH.read_bytes()


    valid, errors = validate_file_security(
        "test_invoice.jpg",
        file_bytes,
    )


    assert valid is False

    assert any(
        "Extensión no coincide" in error
        for error in errors
    )