"""
logger.py – Logger configuration for the Marginal Tax Calculator API

Provides a utility to configure and retrieve named loggers across the application
with a consistent format and severity levels.

@module     logger
@logging    INFO, DEBUG, WARNING, ERROR, CRITICAL
@usage      from app.utils.logger import get_logger
"""

import logging

def get_logger(name: str = "marginal tax calculator api") -> logging.Logger:
    """
    Returns a logger instance with standardized formatting and handler setup.

    Args:
        name (str): Name of the logger. Typically the module name or app name.

    Returns:
        logging.Logger: Configured logger object

    Notes:
        - Logger will not duplicate handlers if called multiple times.
        - Logs are output to the console (stdout) using StreamHandler.
        - Format includes timestamp, log level, and message.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger