from config import (
    APP_ENV,
    OCR_TIMEOUT_SECONDS,
    MAX_FILE_SIZE_MB,
)


def test_config_defaults():

    assert APP_ENV is not None
    assert OCR_TIMEOUT_SECONDS > 0
    assert MAX_FILE_SIZE_MB > 0
