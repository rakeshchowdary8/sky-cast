"""
utils/weather_icons.py — WMO weather code → description + emoji mapping.

Reference: https://open-meteo.com/en/docs
Section: "WMO Weather interpretation codes (WW)"

Usage:
    from utils.weather_icons import get_weather_info
    desc, emoji = get_weather_info(code, is_day=1)
"""

# ---------------------------------------------------------------------------
# Full WMO code mapping: code → (description, day_emoji, night_emoji)
# ---------------------------------------------------------------------------
_WMO_MAP: dict[int, tuple[str, str, str]] = {
    0:  ("Clear Sky",              "☀️",  "🌙"),
    1:  ("Mainly Clear",           "🌤️", "🌙"),
    2:  ("Partly Cloudy",          "⛅",  "☁️"),
    3:  ("Overcast",               "☁️",  "☁️"),
    45: ("Foggy",                  "🌫️", "🌫️"),
    48: ("Icy Fog",                "🌫️", "🌫️"),
    51: ("Light Drizzle",          "🌦️", "🌧️"),
    53: ("Moderate Drizzle",       "🌦️", "🌧️"),
    55: ("Dense Drizzle",          "🌧️", "🌧️"),
    56: ("Light Freezing Drizzle", "🌧️", "🌧️"),
    57: ("Heavy Freezing Drizzle", "🌧️", "🌧️"),
    61: ("Slight Rain",            "🌧️", "🌧️"),
    63: ("Moderate Rain",          "🌧️", "🌧️"),
    65: ("Heavy Rain",             "🌧️", "🌧️"),
    66: ("Light Freezing Rain",    "🌨️", "🌨️"),
    67: ("Heavy Freezing Rain",    "🌨️", "🌨️"),
    71: ("Slight Snowfall",        "❄️",  "❄️"),
    73: ("Moderate Snowfall",      "❄️",  "❄️"),
    75: ("Heavy Snowfall",         "❄️",  "❄️"),
    77: ("Snow Grains",            "🌨️", "🌨️"),
    80: ("Slight Showers",         "🌦️", "🌧️"),
    81: ("Moderate Showers",       "🌧️", "🌧️"),
    82: ("Violent Showers",        "🌧️", "🌧️"),
    85: ("Slight Snow Showers",    "🌨️", "🌨️"),
    86: ("Heavy Snow Showers",     "🌨️", "🌨️"),
    95: ("Thunderstorm",           "⛈️",  "⛈️"),
    96: ("Thunderstorm w/ Hail",   "🌩️", "🌩️"),
    99: ("Thunderstorm w/ Hail",   "🌩️", "🌩️"),
}

_FALLBACK = ("Unknown",  "🌡️", "🌡️")


def get_weather_info(code: int, is_day: int = 1) -> tuple[str, str]:
    """
    Return (description, emoji) for a WMO weather code.

    Args:
        code:   WMO weather interpretation code from Open-Meteo.
        is_day: 1 for daytime, 0 for night-time (affects emoji choice).

    Returns:
        (description_string, emoji_string)
    """
    entry = _WMO_MAP.get(code, _FALLBACK)
    desc = entry[0]
    emoji = entry[1] if is_day else entry[2]
    return desc, emoji


def get_description(code: int) -> str:
    """Return only the text description for a WMO code."""
    return _WMO_MAP.get(code, _FALLBACK)[0]


def get_emoji(code: int, is_day: int = 1) -> str:
    """Return only the emoji for a WMO code."""
    entry = _WMO_MAP.get(code, _FALLBACK)
    return entry[1] if is_day else entry[2]


def get_all_codes() -> list[int]:
    """Return a sorted list of all supported WMO codes."""
    return sorted(_WMO_MAP.keys())
