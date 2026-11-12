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
    Resolve a city name to geographic coordinates (first match only).

    Args:
        city_name: User-entered city name string.

    Returns:
        A dict with keys: 'city', 'country', 'latitude', 'longitude'.

    Raises:
        CityNotFoundError: If the city is not found in the geocoding API.
        GeocodingError:    For network errors, timeouts, or unexpected responses.
    """
    results = _fetch_geocoding_results(city_name.strip(), count=1)
    if not results:
        raise CityNotFoundError(
            f"City '{city_name}' not found. Please check the spelling and try again."
        )
    return _parse_geocoding_result(results[0])


def get_city_suggestions(query: str, max_results: int = 8) -> list[dict]:
    """
    Get city suggestions for autocomplete based on partial query.

    Args:
        query: Partial city name (minimum 2 characters).
        max_results: Maximum number of suggestions to return.

    Returns:
        List of dicts with keys: 'city', 'country', 'latitude', 'longitude', 'admin1'.
        Returns empty list on error or if query too short.
    """
    if not query or len(query.strip()) < 2:
        return []

    try:
        results = _fetch_geocoding_results(query.strip(), count=max_results)
        return [_parse_geocoding_result(r) for r in results]
    except Exception:
        # Silently fail for suggestions - don't disrupt typing
        logger.debug("Failed to fetch suggestions for: %s", query)
        return []


def _fetch_geocoding_results(city_name: str, count: int = 10) -> list:
    """Internal: fetch raw results from geocoding API."""
    params = {
        "name": city_name,
        "count": count,
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

    return data.get("results", [])


def _parse_geocoding_result(result: dict) -> dict:
    """Parse a single geocoding result into standardized dict."""
    try:
        return {
            "city": result["name"],
            "country": result.get("country", ""),
            "admin1": result.get("admin1", ""),  # State/province
            "latitude": float(result["latitude"]),
            "longitude": float(result["longitude"]),
        }
    except (KeyError, ValueError, TypeError) as e:
        raise GeocodingError(f"Unexpected geocoding response format: {e}")

