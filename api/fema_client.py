"""
FEMA API client (extract layer).

Responsible for retrieving data from the FEMA API
using pagination.
"""

from collections.abc import Generator
from typing import Any

from conf.conf import get_logger
from conf.settings import API_TIMEOUT, FEMA_API_BASE, FEMA_ENDPOINT, FEMA_PAGE_LIMIT
from utils.http import get_request

logger = get_logger(__name__)


def fetch_all_projects(
    limit: int = FEMA_PAGE_LIMIT,
) -> Generator[list[dict[str, Any]], None, None]:
    """
    Fetch FEMA project data in paginated batches.

    Args:
        limit (int): Number of records per request.

    Yields:
        list: Batch of raw FEMA project records.
    """
    url = f"{FEMA_API_BASE}{FEMA_ENDPOINT}"
    offset = 0
    MAX_OFFSET = 200_000

    while True:
        params = {"limit": limit, "offset": offset}

        logger.info(f"Fetching: offset={offset}, limit={limit}")

        response = get_request(url, params=params, timeout=API_TIMEOUT)
        data = response.json().get("PublicAssistanceFundedProjectsDetails", [])

        if not data:
            break

        yield data

        if len(data) < limit:
            break

        if offset >= MAX_OFFSET:
            logger.warning("Max offset reached. Stopping pagination.")
            break

        offset += limit
