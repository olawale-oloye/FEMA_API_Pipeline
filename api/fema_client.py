"""
FEMA API client (extract layer).

Responsible for retrieving data from the FEMA API
using pagination.
"""

from conf.settings import FEMA_API_BASE, FEMA_ENDPOINT, FEMA_PAGE_LIMIT, API_TIMEOUT
from utils.http import get_request
from conf.conf import get_logger

logger = get_logger(__name__)


def fetch_all_projects(limit: int = FEMA_PAGE_LIMIT):
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
