"""
Database operations for FEMA project data.
"""

from typing import Any

from conf.conf import get_logger
from db.postgres import get_connection

logger = get_logger(__name__)


def create_schema_if_not_exists(schema: str = "bronze") -> None:
    """
    Create schema if it does not exist.

    Args:
        schema: Schema name (default: bronze)
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema};")

    conn.commit()
    cursor.close()
    conn.close()

    logger.info(f"Schema '{schema}' ready")


def create_table_if_not_exists(schema: str = "bronze") -> None:
    """
    Create FEMA projects table if it does not exist.
    """
    conn = get_connection()
    cursor = conn.cursor()
    if schema not in {"bronze", "silver", "gold"}:
        raise ValueError("Invalid schema")

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {schema}.fema_projects (
            id SERIAL PRIMARY KEY,
            disaster_number INTEGER,
            state TEXT,
            county TEXT,
            incident_type TEXT,
            declaration_date DATE,
            applicant_name TEXT,
            project_number TEXT,
            project_title TEXT,
            federal_share NUMERIC,
            total_obligated NUMERIC
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()

    logger.info(f"Table {schema}.fema_projects ready")


def insert_projects(projects: list[dict[str, Any]], schema: str = "bronze") -> None:
    """
    Insert FEMA project records into database.

    Args:
        projects (list): Transformed project records.
        schema: Target schema (default: bronze)
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO {schema}.fema_projects (
            disaster_number, state, county, incident_type,
            declaration_date, applicant_name, project_number,
            project_title, federal_share, total_obligated
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    data = [
        (
            p["disaster_number"],
            p["state"],
            p["county"],
            p["incident_type"],
            p["declaration_date"],
            p["applicant_name"],
            p["project_number"],
            p["project_title"],
            p["federal_share"],
            p["total_obligated"],
        )
        for p in projects
    ]

    cursor.executemany(query, data)
    inserted = cursor.rowcount

    conn.commit()
    cursor.close()
    conn.close()

    logger.info(f"Inserted {inserted} rows into {schema}.fema_projects")
