"""
Application configuration module.

This module loads environment variables and exposes configuration
settings for API access and PostgreSQL connection.

It should contain only configuration values and no execution logic.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

ENV_PATH = PROJECT_ROOT / ".env"
# Load .env
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
else:
    load_dotenv()

# -----------------------------
# API Configuration
# -----------------------------
API_TIMEOUT = float(os.getenv("API_TIMEOUT", "10"))
API_MAX_RETRIES = int(os.getenv("API_MAX_RETRIES", "3"))
API_BACKOFF_FACTOR = float(os.getenv("API_BACKOFF_FACTOR", "0.5"))

FEMA_API_BASE = os.getenv("FEMA_API_BASE", "https://www.fema.gov/api/open/v2")
FEMA_ENDPOINT = "/PublicAssistanceFundedProjectsDetails"
FEMA_PAGE_LIMIT = int(os.getenv("FEMA_PAGE_LIMIT", "1000"))

# -----------------------------
# Database Configuration
# -----------------------------
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = int(os.getenv("PG_PORT", "5432"))
PG_DB = os.getenv("PG_DB", "fema")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
