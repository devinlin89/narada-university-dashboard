# config/logger.py

import logging

from config.config import settings


def configure_logging() -> None:
    # Configure project-wide logging

    logging.basicConfig(
        level=settings.logging.level,
        format=settings.logging.format,
        datefmt=settings.logging.date_format,
    )

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)