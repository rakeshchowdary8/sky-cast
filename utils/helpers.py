"""
utils/helpers.py — Formatting and unit-conversion utilities.

All pure functions — no Tkinter, no database, no network calls.
"""

from datetime import datetime


# ---------------------------------------------------------------------------
# Temperature
# ---------------------------------------------------------------------------

def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return round((celsius * 9 / 5) + 32, 1)


def format_temperature(value: float, unit: str = "Celsius") -> str:
    """
    Return a formatted temperature string with unit symbol.

    Args:
        value: Temperature in Celsius.
        unit:  "Celsius" or "Fahrenheit".
    """
    if unit == "Fahrenheit":
        return f"{celsius_to_fahrenheit(value):.0f}°F"
    return f"{value:.0f}°C"


# ---------------------------------------------------------------------------
# Wind speed
# ---------------------------------------------------------------------------

def kmh_to_mph(kmh: float) -> float:
    """Convert km/h to mph."""
    return round(kmh * 0.621371, 1)


def format_wind_speed(kmh: float, unit: str = "km/h") -> str:
    """Return a formatted wind speed string."""
    if unit == "mph":
        return f"{kmh_to_mph(kmh):.0f} mph"
    return f"{kmh:.0f} km/h"


# ---------------------------------------------------------------------------
# Date / Time
# ---------------------------------------------------------------------------

def format_date(date_str: str) -> str:
    """
    Format a 'YYYY-MM-DD' string into a friendly display, e.g. 'Thu, Nov 12'.
    """
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%a, %b %d")
    except (ValueError, TypeError):
        return date_str


def format_hour(iso_str: str) -> str:
    """
    Format an ISO datetime string into 'HH:MM' (24h) or '3 PM' (12h).
    Returns the hour label for the hourly forecast strip.
    """
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%I %p").lstrip("0")  # e.g. "3 PM"
    except (ValueError, TypeError):
        return iso_str


def format_time(iso_str: str) -> str:
    """Format an ISO datetime string into 'HH:MM' for sunrise/sunset."""
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%H:%M")
    except (ValueError, TypeError):
        return iso_str


def format_datetime_full(iso_str: str) -> str:
    """Format an ISO datetime string for display in history records."""
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%Y-%m-%d  %H:%M:%S")
    except (ValueError, TypeError):
        return iso_str


def now_local_str() -> str:
    """Return the current local date and time as a formatted string."""
    return datetime.now().strftime("%A, %d %B %Y  •  %H:%M")


# ---------------------------------------------------------------------------
# Pressure / Visibility / Humidity
# ---------------------------------------------------------------------------

def format_pressure(hpa: float) -> str:
    """Format atmospheric pressure."""
    return f"{hpa:.0f} hPa"


def format_visibility(metres: float) -> str:
    """Format visibility — show km if ≥ 1000 m, else metres."""
    if metres >= 1000:
        return f"{metres / 1000:.1f} km"
    return f"{metres:.0f} m"


def format_humidity(pct: int) -> str:
    """Format relative humidity."""
    return f"{pct}%"


def format_uv_index(uv: float) -> str:
    """Format UV index with a risk label."""
    if uv <= 2:
        label = "Low"
    elif uv <= 5:
        label = "Moderate"
    elif uv <= 7:
        label = "High"
    elif uv <= 10:
        label = "Very High"
    else:
        label = "Extreme"
    return f"{uv:.0f} ({label})"


# ---------------------------------------------------------------------------
# Wind direction
# ---------------------------------------------------------------------------

def degrees_to_cardinal(degrees: int) -> str:
    """Convert wind direction in degrees to a cardinal/intercardinal label."""
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    idx = round(degrees / (360 / len(dirs))) % len(dirs)
    return dirs[idx]

