# SkyView – Real-Time Weather Desktop Application

<p align="center">
  <strong>🌤️ A modern, professional weather desktop application built with Python</strong>
</p>

> **Status:** 🟡 In Development (Phase 1 — Architecture Complete)  
> **Platform:** Windows / Linux / macOS  
> **Python:** 3.10+

---

## Overview

**SkyView** is a native Python desktop weather application that displays real-time weather information for any city in the world. It features a modern dark-themed interface, live weather data from the Open-Meteo API (no API key required), SQLite-backed favorites and history, Matplotlib charts, and full unit/theme customization.

---

## Features

> ⚠️ Features listed below reflect the **planned design**. Implemented features will be verified and updated as development progresses.

### Planned Features
- 🔍 **City Search** — Search any city worldwide with geocoding
- 🌡️ **Current Weather** — Temperature, feels-like, humidity, wind, pressure, visibility, UV index
- ⏱️ **Hourly Forecast** — Next 24 hours
- 📅 **7-Day Forecast** — Daily max/min with conditions
- 📊 **Weather Charts** — Matplotlib temperature graphs
- ⭐ **Favorite Cities** — Save and quickly access favorite locations
- 🕒 **Search History** — Revisit previous searches
- 📂 **Weather History** — Browse recorded weather snapshots with historical charts
- ⚙️ **Settings** — Dark/light theme, °C/°F, km/h/mph, default city
- 💾 **Persistent Storage** — SQLite database for all user data
- 🧵 **Non-blocking UI** — Background threads for all API requests

---

## Screenshots

> 📷 Screenshots will be added after the UI is implemented.

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| GUI | Tkinter + CustomTkinter |
| Weather API | Open-Meteo (free, no key) |
| Geocoding | Open-Meteo Geocoding API |
| Database | SQLite (Python built-in `sqlite3`) |
| Charts | Matplotlib |
| HTTP | Requests |
| Images | Pillow (PIL) |
| Threading | `concurrent.futures.ThreadPoolExecutor` |

---

## Project Structure

```
SkyView/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── AGENTS.md                  # AI agent instruction manual
├── README.md
├── .gitignore
│
├── config/
│   └── settings.py            # App constants, colors, fonts, paths
│
├── database/
│   ├── connection.py          # SQLite connection manager
│   ├── schema.py              # Table creation SQL
│   └── database.py            # All CRUD functions
│
├── services/
│   ├── geocoding.py           # City name → lat/lon
│   ├── weather_api.py         # Open-Meteo forecast API client
│   └── weather_service.py     # Geocoding + weather orchestrator
│
├── models/
│   └── weather.py             # WeatherData, HourlyForecast, DailyForecast
│
├── components/
│   ├── sidebar.py             # Navigation sidebar
│   ├── header.py              # App header
│   ├── search_bar.py          # Search input widget
│   ├── weather_card.py        # Info card widget
│   └── forecast_card.py       # Forecast card widget
│
├── views/
│   ├── dashboard.py           # Main dashboard
│   ├── favorites.py           # Favorite cities
│   ├── history.py             # Search & weather history
│   └── settings.py            # App settings
│
├── utils/
│   ├── helpers.py             # Formatting utilities
│   ├── weather_icons.py       # WMO code → description + emoji
│   └── validators.py          # Input validation
│
├── assets/icons/              # Optional PNG weather icons
├── data/                      # SQLite database (auto-created)
└── project-docs/              # Developer documentation
```

---

## Installation

### Prerequisites
- Python 3.10 or higher
- pip

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/skyview-weather-app.git
cd skyview-weather-app
```

### 2. Create a Virtual Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python main.py
```

The SQLite database (`data/skyview.db`) is created automatically on first launch.

---

## API Information

SkyView uses **Open-Meteo** — a free, open-source weather API with no registration or API key required.

- **Website:** https://open-meteo.com/
- **Geocoding:** `https://geocoding-api.open-meteo.com/v1/search`
- **Forecast:** `https://api.open-meteo.com/v1/forecast`
- **Data:** Current weather, hourly (168h), daily (7 days)
- **Weather codes:** WMO standard codes

---

## Database Schema

| Table | Purpose |
|-------|---------|
| `favorite_cities` | User's saved city locations |
| `search_history` | Record of every successful city search |
| `weather_history` | Snapshots of weather at time of search |
| `user_settings` | Theme, units, default city preferences |

See `project-docs/ARCHITECTURE.md` for full schema details.

---

## Application Workflow

1. User enters a city name and presses Search
2. City name is validated locally
3. Geocoding API converts city → latitude/longitude (background thread)
4. Forecast API fetches weather data (background thread)
5. UI updates with current conditions, forecasts, and charts (main thread via `root.after()`)
6. Search is saved to `search_history`; weather snapshot saved to `weather_history`

---

## Error Handling

- **Invalid city name** — "City not found" message displayed
- **No internet** — "Connection error" message; app remains functional
- **API timeout** — Request cancelled after 10 seconds; error message shown
- **Database error** — Logged; app continues with degraded persistence
- **Unexpected API response** — Graceful fallback; no fabricated data displayed

---

## Testing

> Tests will be documented after the testing phase (Phase 10).

Planned test scenarios:
1. App starts successfully
2. Database auto-initializes
3. Valid city search
4. Invalid city search
5. No internet connection
6. Favorites CRUD
7. Settings persistence
8. UI responsiveness during API requests

---

## Future Improvements

- Weather alerts and severe weather warnings
- Multiple location dashboard
- Animated weather backgrounds
- Export weather data to CSV
- PyInstaller packaging for distribution
- Precipitation probability charts
- Wind direction compass widget
- Geolocation-based automatic city detection

---

## Contributing

This project follows the AI-agent-friendly development workflow documented in `AGENTS.md`.

1. Read `AGENTS.md` and `project-docs/PROJECT_STATUS.md` before contributing
2. Follow the existing architecture (see `project-docs/ARCHITECTURE.md`)
3. Update documentation files after every change
4. Use parameterized SQL queries; never hardcode secrets

---

## License

No license selected yet. All rights reserved until a license is chosen.
