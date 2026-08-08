"""
Telemetry Tests
---------------
Pruebas del sistema de observabilidad.
"""


from utils.telemetry import (
    register_request,
    register_success,
    register_error,
    get_telemetry,
    reset_telemetry,
)



def setup_function():

    reset_telemetry()



def test_register_request(caplog):
    with caplog.at_level("INFO"):
        register_request(
            "GET",
            "/"
        )

    messages = [
        record.message
        for record in caplog.records
    ]

    assert "REQUEST GET /" in messages


def test_register_success():

    register_success()


    data = get_telemetry()


    assert (
        data["ocr_success"]
        == 1
    )


def test_register_error():

    register_error(
        "INVALID_IMAGE"
    )


    data = get_telemetry()


    assert (
        data["ocr_failed"]
        == 1
    )


    assert (
        data["INVALID_IMAGE"]
        == 1
    )



def test_reset_telemetry():

    register_request(
        "POST",
        "/ocr"
    )


    reset_telemetry()


    data = get_telemetry()


    assert (
        data["requests_total"]
        == 0
    )
