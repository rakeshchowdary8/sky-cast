"""
database/connection.py — SQLite connection factory.

Provides a context manager for safe, auto-closing database connections.
All database operations should use get_connection() as a context manager.
"""

import sqlite3
import logging
from contextlib import contextmanager
from config.settings import DB_PATH

logger = logging.getLogger(__name__)


@contextmanager
def get_connection():
    """
    Context manager that yields an open SQLite connection and closes it on exit.

    Usage:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ...")

    Raises:
        sqlite3.Error — re-raised after logging.
    """
    conn = None
    try:
        # Ensure the data directory exists
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row  # Rows accessible by column name
        conn.execute("PRAGMA journal_mode=WAL")  # Better concurrent performance
        conn.execute("PRAGMA foreign_keys=ON")
        yield conn
    except sqlite3.Error as e:
        logger.error("Database connection error: %s", e)
        raise
    finally:
        if conn:
            conn.close()

