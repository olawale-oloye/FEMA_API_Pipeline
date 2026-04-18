"""
Logging configuration module.

Provides centralized logging setup and logger retrieval
for consistent logging across the application.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"


def setup_logging() -> None:
    """
    Configure global logging.

    Logs are written to both console and a rotating file.
    """
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=3)
    console_handler = logging.StreamHandler()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)-8s - [%(filename)-20s:%(lineno)4d] - %(funcName)-30s - %(message)-50s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[file_handler, console_handler],
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Retrieve a logger instance.

    Args:
        name (str): Module name.

    Returns:
        logging.Logger: Configured logger.
    """
    return logging.getLogger(name)
