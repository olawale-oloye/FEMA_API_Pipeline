"""
HTTP utility module.

Provides a reusable GET request function with retry
and exponential backoff handling.
"""

import time

import requests

from conf.conf import get_logger
from conf.settings import API_BACKOFF_FACTOR, API_MAX_RETRIES

logger = get_logger(__name__)


def get_request(
    url: str, params: dict[str, int] | None = None, timeout: float = 10.0
) -> requests.Response:
    """
    Perform an HTTP GET request with retry logic.

    Args:
        url (str): Target URL.
        params (dict, optional): Query parameters.
        timeout (int): Request timeout in seconds.

    Returns:
        requests.Response: Successful HTTP response.

    Raises:
        RuntimeError: If all retry attempts fail.
    """
    for attempt in range(API_MAX_RETRIES):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response

        except requests.RequestException as e:
            wait = API_BACKOFF_FACTOR * (2**attempt)
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(wait)

    raise RuntimeError("Max retries exceeded")
