"""
Tests
-----
Logger centralizado del OCR Engine.
"""

import logging

from utils.logger import get_logger



def test_logger_returns_instance():

    logger = get_logger()

    assert isinstance(
        logger,
        logging.Logger
    )



def test_logger_name():

    logger = get_logger(
        "test"
    )

    assert logger.name == "test"



def test_logger_level():

    logger = get_logger()

    assert logger.level == logging.INFO



def test_logger_has_handler():

    logger = get_logger()

    assert len(
        logger.handlers
    ) > 0
