"""
PostgreSQL connection and database setup module.
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extensions import connection as Connection

from conf.conf import get_logger
from conf.settings import PG_DB, PG_HOST, PG_PASSWORD, PG_PORT, PG_USER

logger = get_logger(__name__)


def get_server_connection() -> Connection:
    """
    Connect to default PostgreSQL database.

    Used for administrative tasks such as creating databases.

    Returns:
        connection: psycopg2 connection object.
    """
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname="postgres",
        user=PG_USER,
        password=PG_PASSWORD,
    )


def get_connection() -> Connection:
    """
    Connect to target application database.

    Returns:
        connection: psycopg2 connection object.
    """
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD,
    )


def create_database_if_not_exists() -> None:
    """
    Create the application database if it does not exist.
    """
    conn = get_server_connection()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (PG_DB,))
    exists = cursor.fetchone()

    if not exists:
        cursor.execute(f"CREATE DATABASE {PG_DB};")
        logger.info(f"Database {PG_DB} created")
    else:
        logger.info(f"Database {PG_DB} exists")

    cursor.close()
    conn.close()
