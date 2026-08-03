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



def test_register_request():

    register_request(
        "GET",
        "/"
    )


    data = get_telemetry()


    assert (
        data["requests_total"]
        == 1
    )



def test_register_success():

    register_success(
        2.5
    )


    data = get_telemetry()


    assert (
        data["requests_success"]
        == 1
    )


    assert (
        data["total_processing_time"]
        == 2.5
    )



def test_register_error():

    register_error(
        "INVALID_IMAGE"
    )


    data = get_telemetry()


    assert (
        data["requests_error"]
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
