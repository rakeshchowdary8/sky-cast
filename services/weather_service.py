"""
services/weather_service.py — Orchestrator for geocoding + weather API.

This is the single entry point that UI code calls to fetch weather data.
It coordinates geocoding and forecast API calls and returns a WeatherData object.
"""

import logging
from services.geocoding import geocode_city, GeocodingError, CityNotFoundError
from services.weather_api import fetch_weather_data, WeatherAPIError
from models.weather import WeatherData

logger = logging.getLogger(__name__)


class WeatherServiceError(Exception):
    """General error from WeatherService — suitable to display to the user."""


def fetch_weather(city_name: str) -> WeatherData:
    """
    Fetch weather for a city name. Full pipeline: geocode → forecast.

    This function is intended to be called from a background thread.
    It is SAFE to call from worker threads (no Tkinter interaction).

    Args:
        city_name: Raw user input, e.g. "London" or "New York".

    Returns:
        A fully populated WeatherData object.

    Raises:
        WeatherServiceError: With a user-friendly message on any failure.
    """
    logger.info("Fetching weather for city: %s", city_name)

    # Step 1: Geocode city name → coordinates
    try:
        geo = geocode_city(city_name)
    except CityNotFoundError as e:
        raise WeatherServiceError(str(e))
    except GeocodingError as e:
        raise WeatherServiceError(str(e))

    logger.info("Geocoded '%s' → lat=%.4f, lon=%.4f, country=%s",
                geo["city"], geo["latitude"], geo["longitude"], geo["country"])

    # Step 2: Fetch weather forecast
    try:
        weather = fetch_weather_data(
            city=geo["city"],
            country=geo["country"],
            latitude=geo["latitude"],
            longitude=geo["longitude"],
        )
    except WeatherAPIError as e:
        raise WeatherServiceError(str(e))

    logger.info("Weather fetched: %s, %.1f°C, code=%d",
                weather.city, weather.temperature, weather.weather_code)

    return weather
