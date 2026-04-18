"""
FEMA ETL pipeline.

Orchestrates extract, transform, and load operations.
"""

from conf.conf import get_logger
from db.postgres import create_database_if_not_exists, get_connection
from db.repositories import create_table_if_not_exists, insert_projects
from services.fema_service import get_processed_projects

# from typing import Any

logger = get_logger(__name__)


def run_pipeline() -> None:
    """
    Execute the full ETL pipeline.

    Steps:
        1. Ensure database exists
        2. Ensure table exists
        3. Extract data from API
        4. Transform data
        5. Load into database
    """
    logger.info("Starting pipeline")

    create_database_if_not_exists()
    create_table_if_not_exists()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT current_database();")
    result = cursor.fetchone()
    db_name = result[0] if result else "unknown"
    logger.info(f"Connected to DB: {db_name}")
    cursor.close()
    conn.close()

    for batch in get_processed_projects():
        insert_projects(batch)

    logger.info("Pipeline complete")
