import importlib

import pytest

import config


def test_config_defaults():
    assert config.APP_ENV in {"development", "test", "production"}
    assert config.LOG_LEVEL in {
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    }
    assert config.OCR_TIMEOUT_SECONDS > 0
    assert config.MAX_FILE_SIZE_MB > 0


@pytest.mark.parametrize(
    "value",
    ["development", "test", "production"],
)
def test_valid_app_env(monkeypatch, value):
    monkeypatch.setenv("APP_ENV", value)

    importlib.reload(config)

    assert config.APP_ENV == value


@pytest.mark.parametrize(
    "value",
    ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
)
def test_valid_log_level(monkeypatch, value):
    monkeypatch.setenv("LOG_LEVEL", value)

    importlib.reload(config)

    assert config.LOG_LEVEL == value


def test_invalid_app_env(monkeypatch):
    monkeypatch.setenv("APP_ENV", "invalid")

    with pytest.raises(ValueError, match="APP_ENV"):
        importlib.reload(config)


def test_invalid_log_level(monkeypatch):
    monkeypatch.setenv("LOG_LEVEL", "INVALID")

    with pytest.raises(ValueError, match="LOG_LEVEL"):
        importlib.reload(config)


def test_invalid_ocr_timeout(monkeypatch):
    monkeypatch.setenv("OCR_TIMEOUT_SECONDS", "0")

    with pytest.raises(ValueError, match="OCR_TIMEOUT_SECONDS"):
        importlib.reload(config)


def test_invalid_max_file_size(monkeypatch):
    monkeypatch.setenv("MAX_FILE_SIZE_MB", "0")

    with pytest.raises(ValueError, match="MAX_FILE_SIZE_MB"):
        importlib.reload(config)
