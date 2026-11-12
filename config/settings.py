"""
config/settings.py — Application-wide constants, colors, fonts, and paths.
All paths are resolved relative to this file's location, not os.getcwd().
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
# Root of the SkyView project (parent of config/)
ROOT_DIR = Path(__file__).parent.parent

# SQLite database location
DB_PATH = ROOT_DIR / "data" / "skyview.db"

# Assets
ASSETS_DIR = ROOT_DIR / "assets"
ICONS_DIR = ASSETS_DIR / "icons"

# ---------------------------------------------------------------------------
# Application metadata
# ---------------------------------------------------------------------------
APP_NAME = "SkyView"
APP_VERSION = "1.0.0"
WINDOW_TITLE = "SkyView – Real-Time Weather"
WINDOW_MIN_WIDTH = 1100
WINDOW_MIN_HEIGHT = 700
WINDOW_DEFAULT_WIDTH = 1280
WINDOW_DEFAULT_HEIGHT = 800

# ---------------------------------------------------------------------------
# API settings
# ---------------------------------------------------------------------------
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
API_TIMEOUT = 10  # seconds

# Default forecast parameters
FORECAST_CURRENT_PARAMS = (
    "temperature_2m,apparent_temperature,relative_humidity_2m,"
    "wind_speed_10m,wind_direction_10m,surface_pressure,"
    "visibility,weather_code,is_day"
)
FORECAST_HOURLY_PARAMS = "temperature_2m,weather_code,precipitation_probability"
FORECAST_DAILY_PARAMS = (
    "temperature_2m_max,temperature_2m_min,weather_code,"
    "sunrise,sunset,uv_index_max,precipitation_sum"
)
FORECAST_DAYS = 7

# ---------------------------------------------------------------------------
# Default user preferences (used when DB has no saved settings)
# ---------------------------------------------------------------------------
DEFAULT_TEMP_UNIT = "Celsius"       # or "Fahrenheit"
DEFAULT_WIND_UNIT = "km/h"          # or "mph"
DEFAULT_THEME = "dark"              # or "light"
DEFAULT_CITY = ""                   # empty = no default city

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
SIDEBAR_WIDTH = 200

# ---------------------------------------------------------------------------
# Color palette — Dark theme
# ---------------------------------------------------------------------------
DARK = {
    "bg":           "#1a1a2e",
    "sidebar":      "#16213e",
    "card":         "#0f3460",
    "card_hover":   "#1a4a80",
    "accent":       "#e94560",
    "accent_hover": "#ff6b81",
    "text":         "#ffffff",
    "text_dim":     "#a0a0b0",
    "success":      "#00d4aa",
    "warning":      "#f5a623",
    "border":       "#2a2a4a",
    "input_bg":     "#0f3460",
    "button":       "#e94560",
    "button_hover": "#ff6b81",
    "chart_bg":     "#0f3460",
    "chart_line":   "#e94560",
    "chart_fill":   "#e9456040",
}

# ---------------------------------------------------------------------------
# Color palette — Light theme
# ---------------------------------------------------------------------------
LIGHT = {
    "bg":           "#f0f4f8",
    "sidebar":      "#ffffff",
    "card":         "#ffffff",
    "card_hover":   "#e8f0fe",
    "accent":       "#2563eb",
    "accent_hover": "#1d4ed8",
    "text":         "#1a202c",
    "text_dim":     "#718096",
    "success":      "#10b981",
    "warning":      "#f59e0b",
    "border":       "#e2e8f0",
    "input_bg":     "#ffffff",
    "button":       "#2563eb",
    "button_hover": "#1d4ed8",
    "chart_bg":     "#ffffff",
    "chart_line":   "#2563eb",
    "chart_fill":   "#2563eb40",
}

# ---------------------------------------------------------------------------
# Fonts (CustomTkinter uses tuples: (family, size, weight))
# ---------------------------------------------------------------------------
FONT_FAMILY = "Segoe UI"  # Falls back gracefully on non-Windows

FONT_TINY   = (FONT_FAMILY, 10)
FONT_SMALL  = (FONT_FAMILY, 12)
FONT_BODY   = (FONT_FAMILY, 13)
FONT_LABEL  = (FONT_FAMILY, 11)
FONT_MEDIUM = (FONT_FAMILY, 14, "bold")
FONT_LARGE  = (FONT_FAMILY, 18, "bold")
FONT_TITLE  = (FONT_FAMILY, 24, "bold")
FONT_HERO   = (FONT_FAMILY, 56, "bold")  # Big temperature display

# ---------------------------------------------------------------------------
# Spacing / padding constants
# ---------------------------------------------------------------------------
PAD_XS = 4
PAD_SM = 8
PAD_MD = 16
PAD_LG = 24
PAD_XL = 32

CARD_CORNER_RADIUS = 12
BUTTON_CORNER_RADIUS = 8
SIDEBAR_BUTTON_HEIGHT = 44

