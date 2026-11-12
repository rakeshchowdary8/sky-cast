"""
database/schema.py — DDL statements for all SkyView tables.

These are executed once at startup via initialize_database().
All CREATE TABLE statements use IF NOT EXISTS for idempotency.
"""

# ---------------------------------------------------------------------------
# Table: favorite_cities
# UNIQUE(latitude, longitude) prevents duplicate entries for the same location.
# ---------------------------------------------------------------------------
CREATE_FAVORITE_CITIES = """
CREATE TABLE IF NOT EXISTS favorite_cities (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name   TEXT    NOT NULL,
    country     TEXT,
    latitude    REAL    NOT NULL,
    longitude   REAL    NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(latitude, longitude)
);
"""

# ---------------------------------------------------------------------------
# Table: search_history
# Records every successful city search (duplicates allowed — it's a log).
# ---------------------------------------------------------------------------
CREATE_SEARCH_HISTORY = """
CREATE TABLE IF NOT EXISTS search_history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name   TEXT    NOT NULL,
    country     TEXT,
    latitude    REAL,
    longitude   REAL,
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# ---------------------------------------------------------------------------
# Table: weather_history
# Snapshot of weather conditions saved after each successful API fetch.
# ---------------------------------------------------------------------------
CREATE_WEATHER_HISTORY = """
CREATE TABLE IF NOT EXISTS weather_history (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name         TEXT    NOT NULL,
    temperature       REAL,
    feels_like        REAL,
    humidity          REAL,
    wind_speed        REAL,
    pressure          REAL,
    weather_condition TEXT,
    recorded_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# ---------------------------------------------------------------------------
# Table: user_settings
# Single-row table (id=1 always). INSERT OR REPLACE used for updates.
# ---------------------------------------------------------------------------
CREATE_USER_SETTINGS = """
CREATE TABLE IF NOT EXISTS user_settings (
    id               INTEGER PRIMARY KEY,
    temperature_unit TEXT    DEFAULT 'Celsius',
    wind_unit        TEXT    DEFAULT 'km/h',
    theme            TEXT    DEFAULT 'dark',
    default_city     TEXT    DEFAULT ''
);
"""

# ---------------------------------------------------------------------------
# Seed row for user_settings (id=1 must always exist)
# ---------------------------------------------------------------------------
SEED_USER_SETTINGS = """
INSERT OR IGNORE INTO user_settings (id, temperature_unit, wind_unit, theme, default_city)
VALUES (1, 'Celsius', 'km/h', 'dark', '');
"""

# Ordered list of all DDL statements to execute at startup
ALL_SCHEMA = [
    CREATE_FAVORITE_CITIES,
    CREATE_SEARCH_HISTORY,
    CREATE_WEATHER_HISTORY,
    CREATE_USER_SETTINGS,
    SEED_USER_SETTINGS,
]
