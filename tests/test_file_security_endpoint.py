from pathlib import Path

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_ocr_rejects_fake_extension():

    file_path = Path("tests/invoices/test_invoice.jpg")

    response = client.post(
        "/api/v1/ocr",
        files={
            "file": (
                "test_invoice.jpg",
                file_path.read_bytes(),
                "image/jpeg",
            )
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["success"] is False

    assert data["error"]["code"] == "FILE_SECURITY_ERROR"
