"""
Logger Configuration
--------------------
Configuración centralizada de logs JSON
para SiriusBot OCR Engine.
"""

import logging
import sys

from pythonjsonlogger.json import JsonFormatter


def get_logger(
    name: str = "siriusbot-ocr",
) -> logging.Logger:
    """
    Retorna un logger configurado con salida JSON.
    """

    logger = logging.getLogger(name)

    # Evita duplicar handlers
    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stdout)

    formatter = JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    logger.setLevel(logging.INFO)

    return logger
