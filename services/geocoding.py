"""
services/geocoding.py — City name → (latitude, longitude, country) via Open-Meteo.

API docs: https://open-meteo.com/en/docs/geocoding-api
"""

import logging
import requests
from config.settings import GEOCODING_URL, API_TIMEOUT

logger = logging.getLogger(__name__)


class GeocodingError(Exception):
    """Raised when geocoding fails for any reason."""


class CityNotFoundError(GeocodingError):
    """Raised when the city name returns no results."""


def geocode_city(city_name: str) -> dict:
    """
    Resolve a city name to geographic coordinates.

    Args:
        city_name: User-entered city name string.

    Returns:
        A dict with keys: 'city', 'country', 'latitude', 'longitude'.

    Raises:
        CityNotFoundError: If the city is not found in the geocoding API.
        GeocodingError:    For network errors, timeouts, or unexpected responses.
    """
    params = {
        "name": city_name.strip(),
        "count": 1,
        "language": "en",
        "format": "json",
    }

    try:
        response = requests.get(GEOCODING_URL, params=params, timeout=API_TIMEOUT)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.ConnectionError:
        raise GeocodingError(
            "No internet connection. Please check your network and try again."
        )
    except requests.exceptions.Timeout:
        raise GeocodingError(
            f"The geocoding request timed out after {API_TIMEOUT} seconds."
        )
    except requests.exceptions.HTTPError as e:
        raise GeocodingError(f"Geocoding API error: {e}")
    except Exception as e:
        raise GeocodingError(f"Unexpected geocoding error: {e}")

    results = data.get("results")
    if not results:
        raise CityNotFoundError(
            f"City '{city_name}' not found. Please check the spelling and try again."
        )

    result = results[0]
    try:
        return {
            "city": result["name"],
            "country": result.get("country", ""),
            "latitude": float(result["latitude"]),
            "longitude": float(result["longitude"]),
        }
    except (KeyError, ValueError, TypeError) as e:
        raise GeocodingError(f"Unexpected geocoding response format: {e}")
