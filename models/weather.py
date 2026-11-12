"""
models/weather.py — Domain dataclasses for weather data.

These are plain Python dataclasses with no external dependencies.
They are populated by services/weather_service.py and consumed by UI views.
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class HourlyForecast:
    """Weather forecast for a single hour."""
    time: datetime               # datetime object
    temperature: float           # °C
    weather_code: int            # WMO code
    precip_probability: int      # 0–100 %
    cloud_cover: Optional[int] = None  # %


@dataclass
class DailyForecast:
    """Weather forecast for a single day."""
    date: datetime               # datetime object
    temp_max: float              # °C
    temp_min: float              # °C
    weather_code: int            # WMO code
    sunrise: datetime            # datetime object
    sunset: datetime             # datetime object
    uv_index_max: float          # 0–11+
    precip_sum: float            # mm
    precipitation_probability_max: Optional[int] = None  # 0–100 %


@dataclass
class CurrentWeather:
    """Current weather conditions."""
    temperature: float           # °C
    feels_like: float            # °C (apparent temperature)
    humidity: int                # %
    wind_speed: float            # km/h
    wind_direction: int          # degrees (0–360)
    pressure: float              # hPa
    visibility: float            # metres
    weather_code: int            # WMO code
    is_day: int                  # 1 = daytime, 0 = night-time
    cloud_cover: Optional[int] = None  # %


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
    current: CurrentWeather = field(default_factory=lambda: CurrentWeather(
        temperature=0, feels_like=0, humidity=0, wind_speed=0,
        wind_direction=0, pressure=0, visibility=0, weather_code=0,
        is_day=1, cloud_cover=None
    ))

    # Forecasts
    hourly: list[HourlyForecast] = field(default_factory=list)
    daily: list[DailyForecast] = field(default_factory=list)

    # Convenience properties --------------------------------------------------

    @property
    def visibility_km(self) -> float:
        """Visibility in kilometres (API returns metres)."""
        return round(self.current.visibility / 1000, 1)

    @property
    def wind_direction_label(self) -> str:
        """Cardinal direction string from degrees, e.g. 'NW'."""
        dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        idx = round(self.current.wind_direction / 45) % 8
        return dirs[idx]