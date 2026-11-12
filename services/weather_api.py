"""
services/weather_api.py — Open-Meteo forecast API client.

Fetches and parses weather data into WeatherData / HourlyForecast / DailyForecast.
API docs: https://open-meteo.com/en/docs
"""

import logging
import requests
from datetime import datetime
from config.settings import (
    FORECAST_URL, API_TIMEOUT,
    FORECAST_CURRENT_PARAMS, FORECAST_HOURLY_PARAMS,
    FORECAST_DAILY_PARAMS, FORECAST_DAYS,
)
from models.weather import WeatherData, HourlyForecast, DailyForecast, CurrentWeather

logger = logging.getLogger(__name__)


class WeatherAPIError(Exception):
    """Raised when the weather API call fails."""


def fetch_weather_data(city: str, country: str,
                        latitude: float, longitude: float) -> WeatherData:
    """
    Fetch forecast data for given coordinates and return a WeatherData object.

    Args:
        city:      Resolved city name from geocoding.
        country:   Country name.
        latitude:  Decimal latitude.
        longitude: Decimal longitude.

    Returns:
        Populated WeatherData dataclass.

    Raises:
        WeatherAPIError: On network errors, timeouts, or bad responses.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": FORECAST_CURRENT_PARAMS,
        "hourly": FORECAST_HOURLY_PARAMS,
        "daily": FORECAST_DAILY_PARAMS,
        "wind_speed_unit": "kmh",
        "temperature_unit": "celsius",
        "timezone": "auto",
        "forecast_days": FORECAST_DAYS,
    }

    try:
        response = requests.get(FORECAST_URL, params=params, timeout=API_TIMEOUT)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.ConnectionError:
        raise WeatherAPIError(
            "No internet connection. Please check your network and try again."
        )
    except requests.exceptions.Timeout:
        raise WeatherAPIError(
            f"The weather request timed out after {API_TIMEOUT} seconds."
        )
    except requests.exceptions.HTTPError as e:
        raise WeatherAPIError(f"Weather API HTTP error: {e}")
    except Exception as e:
        raise WeatherAPIError(f"Unexpected weather API error: {e}")

    return _parse_response(data, city, country, latitude, longitude)


def _parse_response(data: dict, city: str, country: str,
                    latitude: float, longitude: float) -> WeatherData:
    """Parse the raw Open-Meteo JSON into a WeatherData dataclass."""
    try:
        cur = data["current"]

        # --- Current conditions ---
        current = CurrentWeather(
            temperature=float(cur.get("temperature_2m", 0)),
            feels_like=float(cur.get("apparent_temperature", 0)),
            humidity=int(cur.get("relative_humidity_2m", 0)),
            wind_speed=float(cur.get("wind_speed_10m", 0)),
            wind_direction=int(cur.get("wind_direction_10m", 0)),
            pressure=float(cur.get("surface_pressure", 0)),
            visibility=float(cur.get("visibility", 0)),
            weather_code=int(cur.get("weather_code", 0)),
            is_day=int(cur.get("is_day", 1)),
            cloud_cover=cur.get("cloud_cover"),
        )

        weather = WeatherData(
            city=city,
            country=country,
            latitude=latitude,
            longitude=longitude,
            current=current,
            hourly=[],
            daily=[],
        )

        # --- Hourly forecast (next 24+ entries) ---
        hourly = data.get("hourly", {})
        times = hourly.get("time", [])
        temps = hourly.get("temperature_2m", [])
        codes = hourly.get("weather_code", [])
        precips = hourly.get("precipitation_probability", [])
        cloud_covers = hourly.get("cloud_cover", [])

        for i in range(min(48, len(times))):  # Get 48 hours for better coverage
            weather.hourly.append(HourlyForecast(
                time=datetime.fromisoformat(times[i].replace('Z', '+00:00')) if 'T' in times[i] else datetime.fromisoformat(times[i] + 'T00:00'),
                temperature=float(temps[i]) if i < len(temps) else 0.0,
                weather_code=int(codes[i]) if i < len(codes) else 0,
                precip_probability=int(precips[i]) if i < len(precips) else 0,
                cloud_cover=int(cloud_covers[i]) if i < len(cloud_covers) else None,
            ))

        # --- Daily forecast ---
        daily = data.get("daily", {})
        dates = daily.get("time", [])
        max_temps = daily.get("temperature_2m_max", [])
        min_temps = daily.get("temperature_2m_min", [])
        daily_codes = daily.get("weather_code", [])
        sunrises = daily.get("sunrise", [])
        sunsets = daily.get("sunset", [])
        uv_indices = daily.get("uv_index_max", [])
        precip_sums = daily.get("precipitation_sum", [])
        precip_probs = daily.get("precipitation_probability_max", [])

        for i in range(len(dates)):
            # Parse sunrise/sunset times
            sunrise_dt = None
            sunset_dt = None
            if i < len(sunrises) and sunrises[i]:
                try:
                    sunrise_dt = datetime.fromisoformat(sunrises[i].replace('Z', '+00:00'))
                except:
                    pass
            if i < len(sunsets) and sunsets[i]:
                try:
                    sunset_dt = datetime.fromisoformat(sunsets[i].replace('Z', '+00:00'))
                except:
                    pass

            weather.daily.append(DailyForecast(
                date=datetime.fromisoformat(dates[i] + 'T00:00'),
                temp_max=float(max_temps[i]) if i < len(max_temps) else 0.0,
                temp_min=float(min_temps[i]) if i < len(min_temps) else 0.0,
                weather_code=int(daily_codes[i]) if i < len(daily_codes) else 0,
                sunrise=sunrise_dt,
                sunset=sunset_dt,
                uv_index_max=float(uv_indices[i]) if i < len(uv_indices) else 0.0,
                precip_sum=float(precip_sums[i]) if i < len(precip_sums) else 0.0,
                precipitation_probability_max=int(precip_probs[i]) if i < len(precip_probs) else None,
            ))

        return weather

    except (KeyError, TypeError, ValueError) as e:
        raise WeatherAPIError(f"Failed to parse weather API response: {e}")