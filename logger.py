"""
Logger Configuration
--------------------
Configuración centralizada de logs
para SiriusBot OCR Engine.
"""

import logging
import sys


LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)


def get_logger(
    name: str = "siriusbot-ocr",
) -> logging.Logger:
    """
    Retorna un logger configurado.

    Args:
        name:
            Nombre del logger.

    Returns:
        logging.Logger
    """

    logger = logging.getLogger(name)


    # Evitar handlers duplicados
    if logger.handlers:
        return logger


    handler = logging.StreamHandler(
        sys.stdout
    )


    formatter = logging.Formatter(
        LOG_FORMAT
    )


    handler.setFormatter(
        formatter
    )


    logger.addHandler(
        handler
    )


    logger.setLevel(
        logging.INFO
    )


    return logger
