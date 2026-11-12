"""
config/settings.py — Application-wide constants, colors, fonts, and paths.
All paths are resolved relative to this file's location, not os.getcwd().
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT_DIR = Path(__file__).parent.parent
DB_PATH = ROOT_DIR / "data" / "skyview.db"
ASSETS_DIR = ROOT_DIR / "assets"
ICONS_DIR = ASSETS_DIR / "icons"

# ---------------------------------------------------------------------------
# Application metadata
# ---------------------------------------------------------------------------
APP_NAME = "SkyCast"
APP_VERSION = "2.1.0"
WINDOW_TITLE = "SkyCast – Premium Weather Dashboard"
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 800
WINDOW_DEFAULT_WIDTH = 1440
WINDOW_DEFAULT_HEIGHT = 900

# ---------------------------------------------------------------------------
# API settings
# ---------------------------------------------------------------------------
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
API_TIMEOUT = 10

FORECAST_CURRENT_PARAMS = (
    "temperature_2m,apparent_temperature,relative_humidity_2m,"
    "wind_speed_10m,wind_direction_10m,surface_pressure,"
    "visibility,weather_code,is_day,cloud_cover"
)
FORECAST_HOURLY_PARAMS = "temperature_2m,weather_code,precipitation_probability,cloud_cover"
FORECAST_DAILY_PARAMS = (
    "temperature_2m_max,temperature_2m_min,weather_code,"
    "sunrise,sunset,uv_index_max,precipitation_sum,precipitation_probability_max"
)
FORECAST_DAYS = 7

# ---------------------------------------------------------------------------
# Default user preferences
# ---------------------------------------------------------------------------
DEFAULT_TEMP_UNIT = "Celsius"
DEFAULT_WIND_UNIT = "km/h"
DEFAULT_THEME = "dark"
DEFAULT_CITY = ""

# ---------------------------------------------------------------------------
# Layout constants
# ---------------------------------------------------------------------------
SIDEBAR_WIDTH_EXPANDED = 260
SIDEBAR_WIDTH_COLLAPSED = 72
HEADER_HEIGHT = 64

# ---------------------------------------------------------------------------
# shadcn-inspired Design Tokens
# ---------------------------------------------------------------------------

# Border Radius Scale
RADIUS_NONE = 0
RADIUS_SM = 4
RADIUS_MD = 8
RADIUS_LG = 12
RADIUS_XL = 16
RADIUS_2XL = 20
RADIUS_FULL = 9999

CARD_CORNER_RADIUS = RADIUS_XL
BUTTON_CORNER_RADIUS = RADIUS_MD
INPUT_CORNER_RADIUS = RADIUS_MD
BADGE_CORNER_RADIUS = RADIUS_FULL

# Spacing Scale (4px base)
SPACE_0 = 0
SPACE_1 = 4
SPACE_2 = 8
SPACE_3 = 12
SPACE_4 = 16
SPACE_5 = 20
SPACE_6 = 24
SPACE_8 = 32
SPACE_10 = 40
SPACE_12 = 48
SPACE_16 = 64

PAD_XS = SPACE_1
PAD_SM = SPACE_2
PAD_MD = SPACE_4
PAD_LG = SPACE_6
PAD_XL = SPACE_8
PAD_2XL = SPACE_12

# Typography Scale
FONT_FAMILY_PRIMARY = "Inter"
FONT_FAMILY_DISPLAY = "Poppins"
FONT_FAMILY_MONO = "JetBrains Mono"

FONT_SIZE_XS = 10
FONT_SIZE_SM = 12
FONT_SIZE_BASE = 13
FONT_SIZE_LG = 14
FONT_SIZE_XL = 16
FONT_SIZE_2XL = 18
FONT_SIZE_3XL = 22
FONT_SIZE_4XL = 28
FONT_SIZE_5XL = 36
FONT_SIZE_6XL = 48
FONT_SIZE_7XL = 60
FONT_SIZE_8XL = 72
FONT_SIZE_9XL = 96

FONT_WEIGHT_NORMAL = "normal"
FONT_WEIGHT_MEDIUM = "bold"
FONT_WEIGHT_SEMIBOLD = "bold"
FONT_WEIGHT_BOLD = "bold"

FONT_TINY   = (FONT_FAMILY_PRIMARY, FONT_SIZE_XS)
FONT_SMALL  = (FONT_FAMILY_PRIMARY, FONT_SIZE_SM)
FONT_BODY   = (FONT_FAMILY_PRIMARY, FONT_SIZE_BASE)
FONT_LABEL  = (FONT_FAMILY_PRIMARY, FONT_SIZE_SM, FONT_WEIGHT_MEDIUM)
FONT_MEDIUM = (FONT_FAMILY_PRIMARY, FONT_SIZE_LG, FONT_WEIGHT_MEDIUM)
FONT_LARGE  = (FONT_FAMILY_PRIMARY, FONT_SIZE_2XL, FONT_WEIGHT_SEMIBOLD)
FONT_TITLE  = (FONT_FAMILY_PRIMARY, FONT_SIZE_3XL, FONT_WEIGHT_BOLD)
FONT_DISPLAY = (FONT_FAMILY_DISPLAY, FONT_SIZE_4XL, FONT_WEIGHT_BOLD)
FONT_HERO   = (FONT_FAMILY_DISPLAY, FONT_SIZE_8XL, FONT_WEIGHT_BOLD)
FONT_HERO_SM = (FONT_FAMILY_DISPLAY, FONT_SIZE_6XL, FONT_WEIGHT_BOLD)

# Animation / Transition System
ANIM_INSTANT = 0
ANIM_FAST = 120
ANIM_NORMAL = 200
ANIM_SLOW = 300
ANIM_SLOWER = 500

EASING_LINEAR = "linear"
EASING_EASE_IN = "ease_in"
EASING_EASE_OUT = "ease_out"
EASING_EASE_IN_OUT = "ease_in_out"
EASING_SPRING = "spring"

# Shadow System (simulated via border colors in CTk)
SHADOW_SM = "shadow_sm"
SHADOW_MD = "shadow_md"
SHADOW_LG = "shadow_lg"
SHADOW_XL = "shadow_xl"

# Z-Index Scale
Z_INDEX_DROPDOWN = 100
Z_INDEX_STICKY = 200
Z_INDEX_MODAL = 300
Z_INDEX_POPOVER = 400
Z_INDEX_TOAST = 500

# ---------------------------------------------------------------------------
# Color Palette — Dark Theme (shadcn-inspired slate + brand)
# ---------------------------------------------------------------------------
DARK = {
    # Base backgrounds
    "bg":            "#030712",      # slate-950
    "bg_secondary":  "#0f172a",      # slate-900
    "bg_tertiary":   "#1e293b",      # slate-800

    # Surface / Card backgrounds
    "card":          "#0f172a",      # slate-900
    "card_hover":    "#1e293b",      # slate-800
    "card_border":   "#1e293b",      # slate-800
    "card_border_hover": "#334155",  # slate-700

    # Sidebar
    "sidebar":       "#030712",      # slate-950
    "sidebar_border": "#1e293b",     # slate-800

    # Brand / Accent (Blue primary)
    "primary":       "#3b82f6",      # blue-500
    "primary_hover": "#2563eb",      # blue-600
    "primary_light": "#1e3a5f",      # blue-900/30
    "primary_foreground": "#ffffff",

    # Secondary accent (Cyan)
    "secondary":     "#06b6d4",      # cyan-500
    "secondary_hover": "#0891b2",    # cyan-600
    "secondary_light": "#0e4d5e",    # cyan-900/30
    "secondary_foreground": "#ffffff",

    # Tertiary accent (Purple)
    "tertiary":      "#a855f7",      # purple-500
    "tertiary_hover": "#9333ea",     # purple-600
    "tertiary_light": "#4c1d95",     # purple-900/30

    # Semantic colors
    "success":       "#10b981",      # emerald-500
    "success_hover": "#059669",      # emerald-600
    "success_light": "#064e3b",      # emerald-900/30
    "success_foreground": "#ffffff",

    "warning":       "#f59e0b",      # amber-500
    "warning_hover": "#d97706",      # amber-600
    "warning_light": "#78350f",      # amber-900/30
    "warning_foreground": "#000000",

    "destructive":   "#ef4444",      # red-500
    "destructive_hover": "#dc2626",  # red-600
    "destructive_light": "#7f1d1d",  # red-900/30
    "destructive_foreground": "#ffffff",

    # Text
    "text":          "#f8fafc",      # slate-50
    "text_secondary": "#94a3b8",     # slate-400
    "text_muted":    "#64748b",      # slate-500
    "text_dim":      "#475569",      # slate-600
    "text_on_primary": "#ffffff",
    "text_on_destructive": "#ffffff",

    # Inputs
    "input_bg":      "#030712",      # slate-950
    "input_border":  "#1e293b",      # slate-800
    "input_border_hover": "#334155", # slate-700
    "input_focus":   "#3b82f6",      # blue-500
    "input_placeholder": "#475569",  # slate-600

    # Buttons
    "btn_primary_bg": "#3b82f6",
    "btn_primary_hover": "#2563eb",
    "btn_primary_text": "#ffffff",

    "btn_secondary_bg": "#1e293b",
    "btn_secondary_hover": "#334155",
    "btn_secondary_text": "#f8fafc",
    "btn_secondary_border": "#1e293b",

    "btn_outline_bg": "transparent",
    "btn_outline_hover": "#1e293b",
    "btn_outline_text": "#f8fafc",
    "btn_outline_border": "#334155",

    "btn_ghost_bg": "transparent",
    "btn_ghost_hover": "#1e293b",
    "btn_ghost_text": "#f8fafc",

    "btn_destructive_bg": "#ef4444",
    "btn_destructive_hover": "#dc2626",
    "btn_destructive_text": "#ffffff",

    # Badge / Tag
    "badge_bg": "#1e293b",
    "badge_text": "#94a3b8",
    "badge_hover_bg": "#334155",
    "badge_hover_text": "#f8fafc",

    # Charts
    "chart_bg": "#030712",
    "chart_grid": "#1e293b",
    "chart_line": "#60a5fa",
    "chart_line_secondary": "#22d3ee",
    "chart_fill": "#1e3a5f",
    "chart_fill_secondary": "#0e4d5e",
    "chart_text": "#94a3b8",

    # Scrollbar
    "scrollbar": "#1e293b",
    "scrollbar_hover": "#334155",
    "scrollbar_thumb": "#334155",

    # Divider
    "divider": "#1e293b",

    # Focus ring
    "focus_ring": "#3b82f6",
    "focus_ring_offset": "#030712",

    # Overlay / Modal
    "overlay_bg": "#000000",
    "overlay_opacity": 0.5,
}

# ---------------------------------------------------------------------------
# Color Palette — Light Theme (shadcn-inspired)
# ---------------------------------------------------------------------------
LIGHT = {
    # Base backgrounds
    "bg":            "#f8fafc",      # slate-50
    "bg_secondary":  "#f1f5f9",      # slate-100
    "bg_tertiary":   "#e2e8f0",      # slate-200

    # Surface / Card backgrounds
    "card":          "#ffffff",      # white
    "card_hover":    "#f8fafc",      # slate-50
    "card_border":   "#e2e8f0",      # slate-200
    "card_border_hover": "#cbd5e1",  # slate-300

    # Sidebar
    "sidebar":       "#ffffff",      # white
    "sidebar_border": "#e2e8f0",     # slate-200

    # Brand / Accent
    "primary":       "#2563eb",      # blue-600
    "primary_hover": "#1d4ed8",      # blue-700
    "primary_light": "#dbeafe",      # blue-100
    "primary_foreground": "#ffffff",

    "secondary":     "#0891b2",      # cyan-600
    "secondary_hover": "#0e7490",    # cyan-700
    "secondary_light": "#cffafe",    # cyan-100
    "secondary_foreground": "#ffffff",

    "tertiary":      "#9333ea",      # purple-600
    "tertiary_hover": "#7e22ce",     # purple-700
    "tertiary_light": "#f3e8ff",     # purple-100

    # Semantic colors
    "success":       "#059669",      # emerald-600
    "success_hover": "#047857",      # emerald-700
    "success_light": "#dcfce7",      # emerald-100
    "success_foreground": "#ffffff",

    "warning":       "#d97706",      # amber-600
    "warning_hover": "#b45309",      # amber-700
    "warning_light": "#fef3c7",      # amber-100
    "warning_foreground": "#000000",

    "destructive":   "#dc2626",      # red-600
    "destructive_hover": "#b91c1c",  # red-700
    "destructive_light": "#fef2f2",  # red-100
    "destructive_foreground": "#ffffff",

    # Text
    "text":          "#0f172a",      # slate-900
    "text_secondary": "#475569",     # slate-600
    "text_muted":    "#64748b",      # slate-500
    "text_dim":      "#94a3b8",      # slate-400
    "text_on_primary": "#ffffff",
    "text_on_destructive": "#ffffff",

    # Inputs
    "input_bg":      "#ffffff",
    "input_border":  "#e2e8f0",
    "input_border_hover": "#cbd5e1",
    "input_focus":   "#2563eb",
    "input_placeholder": "#94a3b8",

    # Buttons
    "btn_primary_bg": "#2563eb",
    "btn_primary_hover": "#1d4ed8",
    "btn_primary_text": "#ffffff",

    "btn_secondary_bg": "#f1f5f9",
    "btn_secondary_hover": "#e2e8f0",
    "btn_secondary_text": "#0f172a",
    "btn_secondary_border": "#e2e8f0",

    "btn_outline_bg": "transparent",
    "btn_outline_hover": "#f1f5f9",
    "btn_outline_text": "#0f172a",
    "btn_outline_border": "#cbd5e1",

    "btn_ghost_bg": "transparent",
    "btn_ghost_hover": "#f1f5f9",
    "btn_ghost_text": "#0f172a",

    "btn_destructive_bg": "#dc2626",
    "btn_destructive_hover": "#b91c1c",
    "btn_destructive_text": "#ffffff",

    # Badge / Tag
    "badge_bg": "#f1f5f9",
    "badge_text": "#475569",
    "badge_hover_bg": "#e2e8f0",
    "badge_hover_text": "#0f172a",

    # Charts
    "chart_bg": "#ffffff",
    "chart_grid": "#e2e8f0",
    "chart_line": "#2563eb",
    "chart_line_secondary": "#0891b2",
    "chart_fill": "#dbeafe",
    "chart_fill_secondary": "#cffafe",
    "chart_text": "#475569",

    # Scrollbar
    "scrollbar": "#e2e8f0",
    "scrollbar_hover": "#cbd5e1",
    "scrollbar_thumb": "#cbd5e1",

    # Divider
    "divider": "#e2e8f0",

    # Focus ring
    "focus_ring": "#2563eb",
    "focus_ring_offset": "#ffffff",

    # Overlay / Modal
    "overlay_bg": "#000000",
    "overlay_opacity": 0.3,
}

# ---------------------------------------------------------------------------
# Component Variants (shadcn-inspired)
# ---------------------------------------------------------------------------

BUTTON_VARIANTS = {
    "default": {
        "bg_key": "btn_primary_bg",
        "hover_key": "btn_primary_hover",
        "text_key": "btn_primary_text",
        "border_width": 0,
    },
    "secondary": {
        "bg_key": "btn_secondary_bg",
        "hover_key": "btn_secondary_hover",
        "text_key": "btn_secondary_text",
        "border_width": 1,
        "border_key": "btn_secondary_border",
    },
    "outline": {
        "bg_key": "btn_outline_bg",
        "hover_key": "btn_outline_hover",
        "text_key": "btn_outline_text",
        "border_width": 1,
        "border_key": "btn_outline_border",
    },
    "ghost": {
        "bg_key": "btn_ghost_bg",
        "hover_key": "btn_ghost_hover",
        "text_key": "btn_ghost_text",
        "border_width": 0,
    },
    "destructive": {
        "bg_key": "btn_destructive_bg",
        "hover_key": "btn_destructive_hover",
        "text_key": "btn_destructive_text",
        "border_width": 0,
    },
}

BUTTON_SIZES = {
    "sm": {"height": 32, "padding_x": 12, "font": FONT_SMALL, "radius": RADIUS_SM},
    "default": {"height": 40, "padding_x": 16, "font": FONT_LABEL, "radius": BUTTON_CORNER_RADIUS},
    "lg": {"height": 48, "padding_x": 24, "font": FONT_MEDIUM, "radius": RADIUS_LG},
    "xl": {"height": 56, "padding_x": 32, "font": FONT_LARGE, "radius": RADIUS_XL},
    "icon": {"height": 40, "width": 40, "padding_x": 0, "font": FONT_LABEL, "radius": BUTTON_CORNER_RADIUS},
}

INPUT_SIZES = {
    "sm": {"height": 32, "padding_x": 10, "font": FONT_SMALL, "radius": RADIUS_SM},
    "default": {"height": 44, "padding_x": 14, "font": FONT_BODY, "radius": INPUT_CORNER_RADIUS},
    "lg": {"height": 52, "padding_x": 16, "font": FONT_MEDIUM, "radius": RADIUS_LG},
}

# ---------------------------------------------------------------------------
# Weather metric accent color mapping (shadcn-inspired with light variants)
# ---------------------------------------------------------------------------
METRIC_ACCENTS = {
    "temperature": {"main": "#3b82f6", "light": "#1e3a5f", "text": "#60a5fa"},      # Blue
    "feels_like": {"main": "#22d3ee", "light": "#0e4d5e", "text": "#67e8f9"},       # Cyan
    "humidity": {"main": "#10b981", "light": "#064e3b", "text": "#34d399"},          # Emerald
    "wind": {"main": "#ef4444", "light": "#7f1d1d", "text": "#f87171"},              # Red
    "pressure": {"main": "#f59e0b", "light": "#78350f", "text": "#fbbf24"},          # Amber
    "visibility": {"main": "#06b6d4", "light": "#0e4d5e", "text": "#22d3ee"},         # Cyan
    "uv_index": {"main": "#f97316", "light": "#7c2d12", "text": "#fb923c"},          # Orange
    "cloud_cover": {"main": "#a855f7", "light": "#4c1d95", "text": "#c084fc"},       # Purple
    "precipitation": {"main": "#3b82f6", "light": "#1e3a5f", "text": "#60a5fa"},     # Blue
    "sunrise": {"main": "#f97316", "light": "#7c2d12", "text": "#fb923c"},           # Orange
    "sunset": {"main": "#ef4444", "light": "#7f1d1d", "text": "#f87171"},             # Red
}

# Status colors with light variants for badges
STATUS_COLORS = {
    "clear": {"main": "#f97316", "light": "#7c2d12", "text": "#fb923c", "icon": "☀️"},
    "clouds": {"main": "#64748b", "light": "#1e293b", "text": "#94a3b8", "icon": "☁️"},
    "rain": {"main": "#3b82f6", "light": "#1e3a5f", "text": "#60a5fa", "icon": "🌧️"},
    "drizzle": {"main": "#06b6d4", "light": "#0e4d5e", "text": "#22d3ee", "icon": "🌦️"},
    "thunderstorm": {"main": "#a855f7", "light": "#4c1d95", "text": "#c084fc", "icon": "⛈️"},
    "snow": {"main": "#f8fafc", "light": "#f1f5f9", "text": "#94a3b8", "icon": "❄️"},
    "mist": {"main": "#94a3b8", "light": "#334155", "text": "#cbd5e1", "icon": "🌫️"},
    "fog": {"main": "#94a3b8", "light": "#334155", "text": "#cbd5e1", "icon": "🌫️"},
}

# ---------------------------------------------------------------------------
# Icon mappings (using Unicode emoji as fallback)
# ---------------------------------------------------------------------------
WEATHER_ICONS = {
    0: "☀️",   # Clear sky
    1: "🌤️",  # Mainly clear
    2: "⛅",   # Partly cloudy
    3: "☁️",   # Overcast
    45: "🌫️", # Fog
    48: "🌫️", # Depositing rime fog
    51: "🌦️", # Light drizzle
    53: "🌦️", # Moderate drizzle
    55: "🌧️", # Dense drizzle
    56: "🌧️", # Light freezing drizzle
    57: "🌧️", # Dense freezing drizzle
    61: "🌧️", # Slight rain
    63: "🌧️", # Moderate rain
    65: "🌧️", # Heavy rain
    66: "🌧️", # Light freezing rain
    67: "🌧️", # Heavy freezing rain
    71: "🌨️", # Slight snow fall
    73: "🌨️", # Moderate snow fall
    75: "🌨️", # Heavy snow fall
    77: "🌨️", # Snow grains
    80: "🌦️", # Slight rain showers
    81: "🌧️", # Moderate rain showers
    82: "🌧️", # Violent rain showers
    85: "🌨️", # Slight snow showers
    86: "🌨️", # Heavy snow showers
    95: "⛈️",  # Thunderstorm
    96: "⛈️",  # Thunderstorm with slight hail
    99: "⛈️",  # Thunderstorm with heavy hail
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_colors(theme: str = "dark") -> dict:
    """Get color palette for theme."""
    return DARK if theme == "dark" else LIGHT


def get_button_config(variant: str = "default", size: str = "default", colors: dict = None) -> dict:
    """Get button configuration for variant and size."""
    variant_cfg = BUTTON_VARIANTS.get(variant, BUTTON_VARIANTS["default"])
    size_cfg = BUTTON_SIZES.get(size, BUTTON_SIZES["default"])

    cfg = {**size_cfg}
    if colors:
        cfg["fg_color"] = colors[variant_cfg["bg_key"]]
        cfg["hover_color"] = colors[variant_cfg["hover_key"]]
        cfg["text_color"] = colors[variant_cfg["text_key"]]
        if variant_cfg.get("border_width"):
            cfg["border_width"] = variant_cfg["border_width"]
            cfg["border_color"] = colors[variant_cfg["border_key"]]
    return cfg


def get_input_config(size: str = "default", colors: dict = None) -> dict:
    """Get input configuration for size."""
    size_cfg = INPUT_SIZES.get(size, INPUT_SIZES["default"])

    cfg = {**size_cfg}
    if colors:
        cfg["fg_color"] = colors["input_bg"]
        cfg["border_color"] = colors["input_border"]
        cfg["text_color"] = colors["text"]
        cfg["placeholder_text_color"] = colors["input_placeholder"]
    return cfg


def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB tuple to hex color."""
    return f"#{r:02x}{g:02x}{b:02x}"


def lerp_color(color1: str, color2: str, t: float) -> str:
    """Linear interpolation between two hex colors."""
    r1, g1, b1 = hex_to_rgb(color1)
    r2, g2, b2 = hex_to_rgb(color2)
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return rgb_to_hex(r, g, b)


def ease_out_cubic(t: float) -> float:
    """Cubic ease-out easing function."""
    return 1 - pow(1 - t, 3)


def ease_in_out_cubic(t: float) -> float:
    """Cubic ease-in-out easing function."""
    return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2


def ease_out_expo(t: float) -> float:
    """Exponential ease-out easing function."""
    return 1 - pow(2, -10 * t) if t != 1 else 1


# ---------------------------------------------------------------------------
# Animation Presets
# ---------------------------------------------------------------------------
ANIMATION_PRESETS = {
    "fade_in": {"duration": ANIM_NORMAL, "easing": EASING_EASE_OUT},
    "fade_out": {"duration": ANIM_FAST, "easing": EASING_EASE_IN},
    "slide_up": {"duration": ANIM_NORMAL, "easing": EASING_EASE_OUT},
    "slide_down": {"duration": ANIM_NORMAL, "easing": EASING_EASE_OUT},
    "slide_left": {"duration": ANIM_NORMAL, "easing": EASING_EASE_OUT},
    "slide_right": {"duration": ANIM_NORMAL, "easing": EASING_EASE_OUT},
    "scale_in": {"duration": ANIM_FAST, "easing": EASING_EASE_OUT},
    "scale_out": {"duration": ANIM_FAST, "easing": EASING_EASE_IN},
    "sidebar_toggle": {"duration": ANIM_SLOW, "easing": EASING_EASE_IN_OUT},
    "tooltip": {"duration": ANIM_FAST, "easing": EASING_EASE_OUT},
    "dropdown": {"duration": ANIM_FAST, "easing": EASING_EASE_OUT},
    "chart_draw": {"duration": ANIM_SLOWER, "easing": EASING_EASE_OUT},
}