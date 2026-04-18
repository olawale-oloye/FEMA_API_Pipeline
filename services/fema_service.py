"""
Business logic layer for FEMA data.

Coordinates extraction and transformation steps.
"""

from collections.abc import Generator
from typing import Any

from api.fema_client import fetch_all_projects
from conf.conf import get_logger
from services.fema_transform import transform_projects

logger = get_logger(__name__)


def get_processed_projects() -> Generator[list[dict[str, Any]], None, None]:
    """
    Fetch and transform FEMA project data.

    Yields:
        list: Batch of processed project records.
    """
    for batch in fetch_all_projects():
        transformed = transform_projects(batch)

        logger.info(f"Processed batch size: {len(transformed)}")

        yield transformed
