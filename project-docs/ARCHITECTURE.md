# SkyView – Application Architecture

> **Last Updated:** 2026-11-12  
> **Version:** 1.0 (Initial Design)

---

## Overview

SkyView is a **native Python desktop application** using a layered, modular architecture. The design separates:

1. **Presentation Layer** — Tkinter/CustomTkinter UI (views, components)
2. **Service Layer** — Weather API and geocoding logic
3. **Data Layer** — SQLite database operations
4. **Model Layer** — Python dataclasses representing domain objects
5. **Utility Layer** — Shared helpers, validators, icon mapping
6. **Configuration** — App-wide constants and settings

---

## Project Folder Structure

```
SkyView/
│
├── main.py                    # Entry point. Creates App, starts Tkinter mainloop.
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── AGENTS.md                  # AI agent instruction manual
├── .gitignore
│
├── config/
│   └── settings.py            # App constants: colors, fonts, default values, paths
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
│   └── weather.py             # Dataclasses: WeatherData, HourlyForecast, DailyForecast
│
├── components/
│   ├── __init__.py
│   ├── sidebar.py             # Left navigation sidebar (CTkFrame with buttons)
│   ├── header.py              # Top header bar with logo, search, theme toggle
│   ├── search_bar.py          # Search input + button widget
│   ├── weather_card.py        # Reusable info card (humidity, wind, pressure, etc.)
│   └── forecast_card.py       # Reusable hourly/daily forecast card widget
│
├── views/
│   ├── __init__.py
│   ├── dashboard.py           # Main dashboard view (weather display + charts)
│   ├── favorites.py           # Favorite cities view
│   ├── history.py             # Search history + weather history view
│   └── settings.py            # Settings view (theme, units, default city)
│
├── utils/
│   ├── __init__.py
│   ├── helpers.py             # Format temp, wind, date/time, unit conversion
│   ├── weather_icons.py       # WMO weather code → description + emoji/icon mapping
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
        ├── Loads config/settings.py (colors, fonts, DB path)
        ├── Calls database.initialize_database() → creates data/skyview.db if absent
        ├── Loads user_settings from DB (theme, units, default city)
        ├── Applies theme via customtkinter.set_appearance_mode()
        ├── Creates Sidebar (left panel)
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
User types city + clicks Search
  → header/search_bar.py triggers App.search_city(city_name)
      → Input validated (validators.py)
      → Loading indicator shown
      → ThreadPoolExecutor submits weather_service.fetch_weather(city_name)
           → geocoding.py: GET geocoding API → returns (lat, lon, country)
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

### Forecast (coordinates → weather)
```
GET https://api.open-meteo.com/v1/forecast
    ?latitude={lat}
    &longitude={lon}
    &current=temperature_2m,apparent_temperature,relative_humidity_2m,
              wind_speed_10m,wind_direction_10m,surface_pressure,
              visibility,weather_code,is_day
    &hourly=temperature_2m,weather_code,precipitation_probability
    &daily=temperature_2m_max,temperature_2m_min,weather_code,
           sunrise,sunset,uv_index_max,precipitation_sum
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
- Methods: `search_city()`, `show_view()`, `apply_theme()`, `on_close()`

### `WeatherData` (models/weather.py)
- Dataclass holding all current + forecast weather data
- Fields: `city`, `country`, `lat`, `lon`, `temperature`, `feels_like`, `humidity`, `wind_speed`, `wind_direction`, `pressure`, `visibility`, `weather_code`, `is_day`, `hourly: list[HourlyForecast]`, `daily: list[DailyForecast]`

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

## Color Palette & Theme

### Dark Theme (default)
| Role | Color |
|------|-------|
| Background | `#1a1a2e` |
| Sidebar | `#16213e` |
| Card background | `#0f3460` |
| Accent / Primary | `#e94560` |
| Text primary | `#ffffff` |
| Text secondary | `#a0a0b0` |
| Success | `#00d4aa` |
| Warning | `#f5a623` |

### Light Theme
| Role | Color |
|------|-------|
| Background | `#f0f4f8` |
| Sidebar | `#ffffff` |
| Card background | `#ffffff` |
| Accent / Primary | `#2563eb` |
| Text primary | `#1a202c` |
| Text secondary | `#718096` |

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

Full mapping in `utils/weather_icons.py`.

