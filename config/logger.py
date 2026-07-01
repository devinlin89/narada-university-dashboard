# config/logger.py

import logging

LOG_LEVEL = logging.INFO

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%H:%M:%S"

def configure_logging() -> None:
    # Configure project-wide logging

    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)