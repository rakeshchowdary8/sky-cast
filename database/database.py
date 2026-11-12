"""
database/database.py — All CRUD functions for SkyView.

Rules:
- No SQL queries anywhere else in the codebase.
- All queries use parameterized placeholders (?) — never string formatting.
- All functions use get_connection() context manager.
- Exceptions are caught, logged, and re-raised or handled gracefully.
"""

import logging
from typing import Optional
from database.connection import get_connection
from database.schema import ALL_SCHEMA

logger = logging.getLogger(__name__)


# ===========================================================================
# Database Initialization
# ===========================================================================

def initialize_database() -> None:
    """
    Create all tables and seed default settings.
    Safe to call on every startup — uses CREATE TABLE IF NOT EXISTS.
    """
    try:
        with get_connection() as conn:
            for statement in ALL_SCHEMA:
                conn.execute(statement)
            conn.commit()
        logger.info("Database initialized successfully at startup.")
    except Exception as e:
        logger.critical("Failed to initialize database: %s", e)
        raise


# ===========================================================================
# Favorite Cities
# ===========================================================================

def insert_favorite_city(city_name: str, country: str,
                          latitude: float, longitude: float) -> bool:
    """
    Add a city to favorites.

    Returns True if inserted, False if already exists (UNIQUE constraint).
    """
    try:
        with get_connection() as conn:
            conn.execute(
                """INSERT OR IGNORE INTO favorite_cities
                   (city_name, country, latitude, longitude)
                   VALUES (?, ?, ?, ?)""",
                (city_name, country, latitude, longitude)
            )
            conn.commit()
            # rowcount 0 means the UNIQUE constraint fired (duplicate)
            changes = conn.execute("SELECT changes()").fetchone()[0]
            return changes > 0
    except Exception as e:
        logger.error("insert_favorite_city failed: %s", e)
        return False


def get_favorite_cities() -> list[dict]:
    """Return all favorite cities, ordered by most recently added."""
    try:
        with get_connection() as conn:
            rows = conn.execute(
                """SELECT id, city_name, country, latitude, longitude, created_at
                   FROM favorite_cities
                   ORDER BY created_at DESC"""
            ).fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        logger.error("get_favorite_cities failed: %s", e)
        return []


def delete_favorite_city(city_id: int) -> bool:
    """Delete a favorite city by its primary key id."""
    try:
        with get_connection() as conn:
            conn.execute(
                "DELETE FROM favorite_cities WHERE id = ?",
                (city_id,)
            )
            conn.commit()
            return True
    except Exception as e:
        logger.error("delete_favorite_city(%d) failed: %s", city_id, e)
        return False


def is_favorite_city(latitude: float, longitude: float) -> bool:
    """Check if a location (by lat/lon) is already in favorites."""
    try:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT id FROM favorite_cities WHERE latitude=? AND longitude=?",
                (latitude, longitude)
            ).fetchone()
            return row is not None
    except Exception as e:
        logger.error("is_favorite_city failed: %s", e)
        return False


# ===========================================================================
# Search History
# ===========================================================================

def insert_search_history(city_name: str, country: str,
                           latitude: float, longitude: float) -> None:
    """Record a successful city search."""
    try:
        with get_connection() as conn:
            conn.execute(
                """INSERT INTO search_history
                   (city_name, country, latitude, longitude)
                   VALUES (?, ?, ?, ?)""",
                (city_name, country, latitude, longitude)
            )
            conn.commit()
    except Exception as e:
        logger.error("insert_search_history failed: %s", e)


def get_recent_searches(limit: int = 50) -> list[dict]:
    """Return most recent searches, newest first."""
    try:
        with get_connection() as conn:
            rows = conn.execute(
                """SELECT id, city_name, country, latitude, longitude, searched_at
                   FROM search_history
                   ORDER BY searched_at DESC
                   LIMIT ?""",
                (limit,)
            ).fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        logger.error("get_recent_searches failed: %s", e)
        return []


def clear_search_history() -> bool:
    """Delete all search history records."""
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM search_history")
            conn.commit()
            return True
    except Exception as e:
        logger.error("clear_search_history failed: %s", e)
        return False


# ===========================================================================
# Weather History
# ===========================================================================

def insert_weather_history(city_name: str, temperature: float,
                            feels_like: float, humidity: float,
                            wind_speed: float, pressure: float,
                            weather_condition: str) -> None:
    """Save a weather snapshot after a successful API fetch."""
    try:
        with get_connection() as conn:
            conn.execute(
                """INSERT INTO weather_history
                   (city_name, temperature, feels_like, humidity,
                    wind_speed, pressure, weather_condition)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (city_name, temperature, feels_like, humidity,
                 wind_speed, pressure, weather_condition)
            )
            conn.commit()
    except Exception as e:
        logger.error("insert_weather_history failed: %s", e)


def get_weather_history(city_filter: Optional[str] = None,
                         limit: int = 100) -> list[dict]:
    """
    Return weather history records, newest first.

    Args:
        city_filter: If provided, return only records for that city name
                     (case-insensitive partial match).
        limit: Maximum rows to return.
    """
    try:
        with get_connection() as conn:
            if city_filter:
                rows = conn.execute(
                    """SELECT id, city_name, temperature, feels_like, humidity,
                              wind_speed, pressure, weather_condition, recorded_at
                       FROM weather_history
                       WHERE LOWER(city_name) LIKE LOWER(?)
                       ORDER BY recorded_at DESC
                       LIMIT ?""",
                    (f"%{city_filter}%", limit)
                ).fetchall()
            else:
                rows = conn.execute(
                    """SELECT id, city_name, temperature, feels_like, humidity,
                              wind_speed, pressure, weather_condition, recorded_at
                       FROM weather_history
                       ORDER BY recorded_at DESC
                       LIMIT ?""",
                    (limit,)
                ).fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        logger.error("get_weather_history failed: %s", e)
        return []


def get_distinct_history_cities() -> list[str]:
    """Return a sorted list of distinct city names in weather history."""
    try:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT DISTINCT city_name FROM weather_history ORDER BY city_name"
            ).fetchall()
            return [row["city_name"] for row in rows]
    except Exception as e:
        logger.error("get_distinct_history_cities failed: %s", e)
        return []


# ===========================================================================
# User Settings
# ===========================================================================

def get_settings() -> dict:
    """
    Retrieve user preferences (always returns a dict, even on error).
    Falls back to defaults if the row is missing.
    """
    defaults = {
        "id": 1,
        "temperature_unit": "Celsius",
        "wind_unit": "km/h",
        "theme": "dark",
        "default_city": "",
    }
    try:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM user_settings WHERE id = 1"
            ).fetchone()
            if row:
                return dict(row)
            return defaults
    except Exception as e:
        logger.error("get_settings failed: %s", e)
        return defaults


def update_settings(temperature_unit: str, wind_unit: str,
                    theme: str, default_city: str) -> bool:
    """
    Persist user preferences. Uses INSERT OR REPLACE to upsert id=1.
    """
    try:
        with get_connection() as conn:
            conn.execute(
                """INSERT OR REPLACE INTO user_settings
                   (id, temperature_unit, wind_unit, theme, default_city)
                   VALUES (1, ?, ?, ?, ?)""",
                (temperature_unit, wind_unit, theme, default_city)
            )
            conn.commit()
            return True
    except Exception as e:
        logger.error("update_settings failed: %s", e)
        return False

