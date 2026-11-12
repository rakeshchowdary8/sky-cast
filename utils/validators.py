"""
utils/validators.py — Input validation functions.

All functions return (is_valid: bool, message: str).
An empty message means no error.
"""

import re


def validate_city_name(name: str) -> tuple[bool, str]:
    """
    Validate a city name before sending it to the geocoding API.

    Rules:
    - Must not be empty or whitespace-only.
    - Must be at least 2 characters long (after stripping).
    - Must not exceed 100 characters.
    - Must only contain letters, spaces, hyphens, apostrophes, and dots
      (to cover names like "St. John's", "Côte-d'Ivoire", "Ho Chi Minh City").

    Returns:
        (True, "") on valid input.
        (False, error_message) on invalid input.
    """
    if not name or not name.strip():
        return False, "Please enter a city name."

    name = name.strip()

    if len(name) < 2:
        return False, "City name must be at least 2 characters."

    if len(name) > 100:
        return False, "City name is too long (max 100 characters)."

    # Allow Unicode letters, spaces, hyphens, apostrophes, periods, commas
    if not re.match(r"^[\w\s\-'.,']+$", name, re.UNICODE):
        return False, "City name contains invalid characters."

    return True, ""


def validate_temperature_unit(unit: str) -> tuple[bool, str]:
    """Validate a temperature unit selection."""
    valid = {"Celsius", "Fahrenheit"}
    if unit not in valid:
        return False, f"Invalid temperature unit '{unit}'. Must be one of: {valid}."
    return True, ""


def validate_wind_unit(unit: str) -> tuple[bool, str]:
    """Validate a wind speed unit selection."""
    valid = {"km/h", "mph"}
    if unit not in valid:
        return False, f"Invalid wind unit '{unit}'. Must be one of: {valid}."
    return True, ""


def validate_theme(theme: str) -> tuple[bool, str]:
    """Validate a theme selection."""
    valid = {"dark", "light"}
    if theme.lower() not in valid:
        return False, f"Invalid theme '{theme}'. Must be 'dark' or 'light'."
    return True, ""
