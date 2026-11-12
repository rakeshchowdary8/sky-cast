# SkyCast – Application Architecture

> **Last Updated:** 2026-11-12  
> **Version:** 2.0 (Premium UI Redesign)

---

## Overview

SkyCast (formerly SkyView) is a **premium native Python desktop weather application** using a layered, modular architecture. The design separates:

1. **Presentation Layer** — Tkinter/CustomTkinter UI (views, components)
2. **Service Layer** — Weather API and geocoding logic
3. **Data Layer** — SQLite database operations
4. **Model Layer** — Python dataclasses representing domain objects
5. **Utility Layer** — Shared helpers, validators, icon mapping
6. **Configuration** — App-wide constants and settings (premium design system)

---

## Project Folder Structure

```
SkyCast/
│
├── main.py                    # Entry point. Creates App, starts Tkinter mainloop.
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── AGENTS.md                  # AI agent instruction manual
├── .gitignore
│
├── config/
│   └── settings.py            # App constants: colors, fonts, default values, paths, design tokens
│
├── database/
│   ├── __init__.py
│   ├── connection.py          # SQLite connection factory / context manager
│   ├── schema.py              # CREATE TABLE SQL statements
│   └── database.py            # All CRUD functions (no SQL in UI files)
│
├── services/
│   ├── __init__.py
│   ├── geocoding.py           # Converts city name → latitude/longitude via Open-Meteo
│   ├── weather_api.py         # Calls Open-Meteo forecast API, parses JSON response
│   └── weather_service.py     # Orchestrates geocoding + weather fetch, returns models
│
├── models/
│   ├── __init__.py
│   └── weather.py             # Dataclasses: WeatherData, CurrentWeather, HourlyForecast, DailyForecast
│
├── components/
│   ├── __init__.py
│   ├── base.py                # shadcn-inspired base components (Card, Button, Input, Badge, Separator, Avatar, Tooltip, Skeleton)
│   ├── sidebar.py             # Left navigation sidebar (animated indicator, SkyCast branding, collapsible)
│   ├── search_bar.py          # Premium search input with autocomplete dropdown
│   ├── weather_card.py        # Premium info card (accent colors, hover effects)
│   ├── forecast_card.py       # Premium hourly/daily forecast card widgets
│   └── detail_card.py         # Premium 6-metric detail cards for dashboard
│
├── views/
│   ├── __init__.py
│   ├── dashboard.py           # Premium dashboard (hero, detail cards, hourly, daily, sun/atmos, chart)
│   ├── favorites.py           # Favorite cities view (modern cards)
│   ├── history.py             # Search history + weather history view (tabbed)
│   └── settings.py            # Settings view (modern segmented buttons)
│
├── utils/
│   ├── __init__.py
│   ├── animations.py          # Animation framework (Animation, AnimationSequence, easing, micro-interactions)
│   ├── helpers.py             # Format temp, wind, date/time, unit conversion
│   ├── weather_icons.py       # WMO weather code → description + emoji mapping
│   └── validators.py          # Input validation (city name, etc.)
│
├── assets/
│   └── icons/                 # PNG weather icons (optional, emoji fallback used)
│
├── data/
│   ├── .gitkeep               # Keeps directory in Git; skyview.db created at runtime
│   └── skyview.db             # Auto-created SQLite database (gitignored)
│
└── project-docs/
    ├── PROJECT_STATUS.md
    ├── TASKS.md
    ├── ARCHITECTURE.md        (this file)
    ├── DECISIONS.md
    ├── CHANGELOG.md
    └── DEVELOPMENT_LOG.md
```

---

## Application Execution Flow

```
main.py
  └── creates App instance (inherits CTk)
        ├── Loads config/settings.py (colors, fonts, DB path, design tokens)
        ├── Calls database.initialize_database() → creates data/skyview.db if absent
        ├── Loads user_settings from DB (theme, units, default city)
        ├── Applies theme via customtkinter.set_appearance_mode()
        ├── Creates Sidebar (left panel, 260px)
        ├── Creates content frame (right panel)
        ├── Creates all Views: Dashboard, Favorites, History, Settings
        │     (all views are CTkFrame children of content frame)
        ├── Shows Dashboard by default (or default city's weather)
        └── Starts Tkinter mainloop()
```

---

## View Switching Mechanism

```
Sidebar button click
  → App.show_view("dashboard" | "favorites" | "history" | "settings")
      → Hides all view frames (frame.pack_forget())
      → Shows selected view frame (frame.pack(...))
      → Calls view.on_show() to refresh data if needed
```

---

## Weather Search Flow

```
User types city + clicks Search (or selects autocomplete suggestion)
  → SearchBar triggers App.search_city(city_name)
      → Input validated (validators.py)
      → Loading indicator shown (search button → "⏳")
      → ThreadPoolExecutor submits weather_service.fetch_weather(city_name)
           → geocoding.py: GET geocoding API → returns (city, country, lat, lon)
           → weather_api.py: GET forecast API → returns raw JSON
           → Parses JSON into WeatherData dataclass (models/weather.py)
      → Thread completes → root.after(0, callback) fires on main thread
           → Loading indicator hidden
           → Dashboard updates all widgets with WeatherData
           → database.insert_search_history(city, country, lat, lon)
           → database.insert_weather_history(city, weather snapshot)
```

---

## API Integration Flow

### Geocoding (city → coordinates)
```
GET https://geocoding-api.open-meteo.com/v1/search
    ?name={city}
    &count=1
    &language=en
    &format=json

Response → results[0] → { name, country, latitude, longitude }
```

### Autocomplete Suggestions (partial city name → suggestions)
```
GET https://geocoding-api.open-meteo.com/v1/search
    ?name={partial}
    &count=8
    &language=en
    &format=json

Response → results[] → [{ city, country, admin1, latitude, longitude }]
```

### Forecast (coordinates → weather)
```
GET https://api.open-meteo.com/v1/forecast
    ?latitude={lat}
    &longitude={lon}
    &current=temperature_2m,apparent_temperature,relative_humidity_2m,
              wind_speed_10m,wind_direction_10m,surface_pressure,
              visibility,weather_code,is_day,cloud_cover
    &hourly=temperature_2m,weather_code,precipitation_probability,cloud_cover
    &daily=temperature_2m_max,temperature_2m_min,weather_code,
           sunrise,sunset,uv_index_max,precipitation_sum,precipitation_probability_max
    &wind_speed_unit=kmh
    &temperature_unit=celsius
    &timezone=auto
    &forecast_days=7
```

---

## Database Interaction Flow

```
database/connection.py
  └── get_connection() → returns sqlite3.Connection
        └── Used as context manager in database.py functions

database/schema.py
  └── CREATE TABLE IF NOT EXISTS statements for:
        - favorite_cities
        - search_history
        - weather_history
        - user_settings

database/database.py
  └── initialize_database()     → runs schema.py DDL
  └── insert_favorite_city()    → INSERT OR IGNORE (dedup by lat/lon)
  └── get_favorite_cities()     → SELECT all
  └── delete_favorite_city()    → DELETE by id
  └── insert_search_history()   → INSERT
  └── get_recent_searches()     → SELECT ORDER BY searched_at DESC LIMIT 50
  └── clear_search_history()    → DELETE all
  └── insert_weather_history()  → INSERT snapshot
  └── get_weather_history()     → SELECT with optional city filter
  └── get_settings()            → SELECT id=1 (single row)
  └── update_settings()         → INSERT OR REPLACE id=1
```

---

## Threading & Background Task Management

| Scenario | Approach |
|----------|----------|
| API call during city search | `ThreadPoolExecutor.submit()` |
| GUI update from worker thread | `root.after(0, lambda: callback(data))` |
| Stale request cancellation | Incrementing `_request_id`; discard if ID mismatch |
| Prevent duplicate requests | Disable Search button while request is in-flight |
| App shutdown cleanup | `executor.shutdown(wait=False)` on window close |

---

## Important Classes and Functions

### `App` (main.py)
- Root application class, inherits `customtkinter.CTk`
- Owns: sidebar, all views, executor, database reference
- Methods: `search_city()`, `show_view()`, `apply_settings()`, `on_close()`

### `WeatherData` (models/weather.py)
- Dataclass holding all current + forecast weather data
- Fields: `city`, `country`, `lat`, `lon`, `current: CurrentWeather`, `hourly: list[HourlyForecast]`, `daily: list[DailyForecast]`

### `CurrentWeather` (models/weather.py)
- Dataclass for current conditions
- Fields: `temperature`, `feels_like`, `humidity`, `wind_speed`, `wind_direction`, `pressure`, `visibility`, `weather_code`, `is_day`, `cloud_cover`

### `HourlyForecast` / `DailyForecast` (models/weather.py)
- Dataclasses with datetime objects for time fields
- Hourly: `time`, `temperature`, `weather_code`, `precip_probability`, `cloud_cover`
- Daily: `date`, `temp_max`, `temp_min`, `weather_code`, `sunrise`, `sunset`, `uv_index_max`, `precip_sum`, `precipitation_probability_max`

### `WeatherService` (services/weather_service.py)
- `fetch_weather(city_name: str) → WeatherData`
- Calls geocoding, then forecast API, constructs WeatherData
- Raises descriptive exceptions on failure

### `DatabaseManager` (database/database.py)
- Module-level functions (not a class) for all CRUD operations
- All use parameterized queries

---

## Module Relationships

```
main.py
  ├── config/settings.py
  ├── database/database.py ──► database/connection.py
  │                        ──► database/schema.py
  ├── services/weather_service.py ──► services/geocoding.py
  │                               ──► services/weather_api.py
  │                               ──► models/weather.py
  ├── components/ ──► config/settings.py
  ├── views/dashboard.py ──► components/*
  │                      ──► utils/*
  │                      ──► models/weather.py
  ├── views/favorites.py ──► database/database.py
  ├── views/history.py   ──► database/database.py
  │                      ──► matplotlib
  └── views/settings.py  ──► database/database.py
                          ──► config/settings.py
```

---

## Premium Design System (Phase 11)

### Color Palette — Dark Theme (SkyCast Premium)
| Role | Color | Usage |
|------|-------|-------|
| Background | `#0a0e17` | Main window background |
| Background Elevated | `#111827` | Elevated surfaces |
| Sidebar | `#0d121c` | Sidebar background |
| Card | `#141c2e` | Card backgrounds |
| Card Hover | `#1a2540` | Card hover state |
| Card Border | `#1e2a4a` | Card borders |
| Accent (Primary) | `#3b82f6` | Primary actions, links |
| Accent Hover | `#60a5fa` | Primary hover |
| Accent Soft | `#1e3a5f` | Selected/active backgrounds |
| Accent Cyan | `#06b6d4` | Visibility, info |
| Accent Purple | `#a855f7` | Cloud cover, UV |
| Accent Green | `#10b981` | Humidity, success |
| Accent Amber | `#f59e0b` | Pressure, warning |
| Accent Red | `#ef4444` | Wind, error |
| Accent Orange | `#f97316` | UV, sunrise |
| Text Primary | `#f8fafc` | Primary text |
| Text Secondary | `#94a3b8` | Secondary text |
| Text Dim | `#64748b` | Dimmed text |

### Color Palette — Light Theme
| Role | Color | Usage |
|------|-------|-------|
| Background | `#f8fafc` | Main window background |
| Background Elevated | `#ffffff` | Elevated surfaces |
| Sidebar | `#ffffff` | Sidebar background |
| Card | `#ffffff` | Card backgrounds |
| Card Hover | `#f1f5f9` | Card hover state |
| Card Border | `#e2e8f0` | Card borders |
| Accent (Primary) | `#2563eb` | Primary actions |
| Accent Hover | `#1d4ed8` | Primary hover |
| Accent Soft | `#dbeafe` | Selected/active backgrounds |
| ... | ... | (full palette in settings.py) |

### Typography
| Token | Font | Size | Weight | Usage |
|-------|------|------|--------|-------|
| FONT_TINY | Inter | 10 | Regular | Small labels |
| FONT_SMALL | Inter | 12 | Regular | Body small |
| FONT_BODY | Inter | 13 | Regular | Body text |
| FONT_LABEL | Inter | 11 | Bold | Labels |
| FONT_MEDIUM | Inter | 14 | Bold | Sub-headings |
| FONT_LARGE | Inter | 18 | Bold | Section headers |
| FONT_TITLE | Inter | 24 | Bold | Page titles |
| FONT_DISPLAY | Poppins | 20 | Bold | Display text |
| FONT_HERO | Poppins | 72 | Bold | Hero temperature |
| FONT_HERO_SM | Poppins | 48 | Bold | Medium hero |

### Spacing Scale
| Token | Value | Usage |
|-------|-------|-------|
| PAD_XS | 4px | Tight spacing |
| PAD_SM | 8px | Small gaps |
| PAD_MD | 16px | Medium gaps (standard) |
| PAD_LG | 24px | Large gaps |
| PAD_XL | 32px | Section spacing |
| PAD_2XL | 48px | Major section spacing |

### Border Radius
| Token | Value | Usage |
|-------|-------|-------|
| CARD_CORNER_RADIUS | 16px | Cards, panels |
| BUTTON_CORNER_RADIUS | 10px | Buttons, inputs |
| SIDEBAR_BUTTON_HEIGHT | 48px | Sidebar nav items |

### Animation Timings
| Token | Value | Usage |
|-------|-------|-------|
| ANIM_FAST | 150ms | Micro-interactions |
| ANIM_NORMAL | 250ms | Standard transitions |
| ANIM_SLOW | 350ms | Complex animations |

### Metric Accent Colors (with Light Variants)
| Metric | Accent | Light Variant |
|--------|--------|---------------|
| Temperature | `#3b82f6` | `#1e3a5f` |
| Humidity | `#10b981` | `#064e3b` |
| Wind | `#ef4444` | `#7f1d1d` |
| Pressure | `#f59e0b` | `#78350f` |
| Visibility | `#06b6d4` | `#0e4d5e` |
| UV Index | `#f97316` | `#7c2d12` |
| Cloud Cover | `#a855f7` | `#4c1d95` |

---

## shadcn-inspired Component System (Phase 13)

### Design Token System (`config/settings.py`)

Complete shadcn-inspired design tokens providing a unified visual language:

| Category | Tokens | Description |
|----------|--------|-------------|
| **Color Palettes** | `DARK`, `LIGHT` | Full semantic color dictionaries with 60+ keys |
| **Spacing** | `SPACE_1`–`SPACE_16` | 16-step scale (4px base unit) |
| **Border Radius** | `RADIUS_NONE`–`RADIUS_FULL` | 8-step scale (0px → 9999px) |
| **Typography** | `FONT_SIZE_XS`–`FONT_SIZE_9XL` | 12-step scale with Inter/Poppins families |
| **Animation** | `ANIM_INSTANT`–`ANIM_SLOWER` | 6 durations with easing presets |
| **Metric Accents** | `METRIC_ACCENTS` | Per-metric colors with main/light/text variants |
| **Status Colors** | `STATUS_COLORS` | Weather condition colors with light variants |
| **Weather Icons** | `WEATHER_ICONS` | WMO code → emoji mapping (43 codes) |

**Helper Functions:** `get_colors()`, `get_button_config()`, `get_input_config()`, `hex_to_rgb()`, `lerp_color()`, easing functions (`ease_out_cubic`, `ease_in_out_cubic`, `ease_out_expo`)

### Animation Framework (`utils/animations.py`)

| Class/Function | Purpose |
|----------------|---------|
| `Animation` | Base class for property interpolation (color, numeric, tuple) with easing |
| `AnimationSequence` | Run animations in parallel or sequence with delays |
| `fade_in` / `fade_out` | Opacity-like transitions via color interpolation |
| `slide_in_from_left` | Position animations |
| `scale_in` | Scale animations |
| `animate_sidebar_toggle` | Specialized sidebar width animation with cubic easing |
| `animate_color_transition` | Smooth color property transitions |
| `pulse_animation` | Pulsing between two colors |
| `setup_hover_animation` | Reusable hover enter/leave animations |
| `setup_focus_ring` | Focus ring animations for inputs |
| `animate_button_press` | Button press scale/color feedback |
| `stagger_animate_children` | Staggered animations for lists |

### Base Component Library (`components/base.py`)

| Component | Variants | Sizes | Key Features |
|-----------|----------|-------|--------------|
| `Card` | default, outlined, elevated, ghost | — | Hover animations, padding configurable |
| `Button` | default, secondary, outline, ghost, destructive | sm, default, lg, xl, icon | Hover/focus/press animations, loading state |
| `Input` | — | sm, default, lg | Label, error state, left/right icons, focus ring |
| `Badge` | default, secondary, outline, destructive, success, warning | sm, default, lg | Semantic color variants |
| `Separator` | horizontal, vertical | — | Divider lines |
| `Avatar` | — | sm, default, lg, xl, 2xl | Text fallback with initials |
| `Tooltip` | — | — | Hover tooltip with delay |
| `Skeleton` | — | — | Shimmer loading animation |

**Factory Functions:** `create_card()`, `create_button()`, `create_input()`, `create_badge()`, `create_separator()`, `create_avatar()`, `create_skeleton()`

### Component Migration Strategy

All existing custom components migrated to use base components:

| Original Component | New Base Component Usage |
|-------------------|-------------------------|
| Custom card frames | `Card` (default/outlined/elevated/ghost) |
| Custom CTkButton | `Button` (variants + sizes) |
| Custom CTkEntry | `Input` (with label, error, icons) |
| Custom status badges | `Badge` (6 variants) |
| Custom dividers | `Separator` |

### Staggered Entrance Animations

All list-based views use `stagger_animate_children` for polished entrances:

- **Sidebar nav items**: Slide from left with 60ms delay per item
- **Dashboard sections**: Sequential fade+slide with 60ms delay
- **Hourly/Daily forecast cards**: Fade+slide-up with 40-50ms delay
- **Favorites/History cards**: Fade+slide-up with 30-50ms delay

---

## WMO Weather Code Mapping (Key Groups)

| Code | Description | Emoji |
|------|-------------|-------|
| 0 | Clear sky | ☀️ |
| 1–3 | Partly cloudy | ⛅ |
| 45, 48 | Foggy | 🌫️ |
| 51–67 | Drizzle/Rain | 🌧️ |
| 71–77 | Snow | ❄️ |
| 80–82 | Showers | 🌦️ |
| 95 | Thunderstorm | ⛈️ |
| 96, 99 | Hail storm | 🌩️ |

Full mapping in `utils/weather_icons.py` (43 codes).