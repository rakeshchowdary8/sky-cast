"""
models/weather.py — Domain dataclasses for weather data.

These are plain Python dataclasses with no external dependencies.
They are populated by services/weather_service.py and consumed by UI views.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class HourlyForecast:
    """Weather forecast for a single hour."""
    time: str               # ISO 8601 string, e.g. "2024-01-15T14:00"
    temperature: float      # °C
    weather_code: int       # WMO code
    precip_probability: int # 0–100 %


@dataclass
class DailyForecast:
    """Weather forecast for a single day."""
    date: str               # "YYYY-MM-DD"
    temp_max: float         # °C
    temp_min: float         # °C
    weather_code: int       # WMO code
    sunrise: str            # ISO 8601 string
    sunset: str             # ISO 8601 string
    uv_index_max: float     # 0–11+
    precip_sum: float       # mm


@dataclass
class WeatherData:
    """
    Complete weather dataset for a single location.
    Returned by WeatherService.fetch_weather().
    """
    # Location
    city: str
    country: str
    latitude: float
    longitude: float

    # Current conditions
    temperature: float          # °C
    feels_like: float           # °C (apparent temperature)
    humidity: int               # %
    wind_speed: float           # km/h
    wind_direction: int         # degrees (0–360)
    pressure: float             # hPa
    visibility: float           # metres
    weather_code: int           # WMO code
    is_day: int                 # 1 = daytime, 0 = night-time

    # Forecasts
    hourly: list[HourlyForecast] = field(default_factory=list)
    daily: list[DailyForecast] = field(default_factory=list)

    # Convenience properties --------------------------------------------------

    @property
    def visibility_km(self) -> float:
        """Visibility in kilometres (API returns metres)."""
        return round(self.visibility / 1000, 1)

    @property
    def wind_direction_label(self) -> str:
        """Cardinal direction string from degrees, e.g. 'NW'."""
        dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        idx = round(self.wind_direction / 45) % 8
        return dirs[idx]

