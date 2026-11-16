# SkyCast – Real-Time Weather Desktop Application

<p align="center">
  <strong>🌤️ A modern, professional weather desktop application built with Python</strong>
</p>

> **Status:** 🟢 **Complete & Working** — All Core Features Implemented + Modernized UI  
> **Platform:** Windows / Linux / macOS  
> **Python:** 3.10+

---

## Overview

**SkyCast** is a native Python desktop weather application that displays real-time weather information for any city in the world. It features a modern dark-themed interface, live weather data from the Open-Meteo API (no API key required), SQLite-backed favorites and history, Matplotlib charts, and full unit/theme customization.

---

## Features

✅ **All features implemented and verified working**

### 🔍 Smart City Search with Autocomplete
- Real-time city suggestions as you type (debounced 200ms)
- Keyboard navigation (↑/↓/Enter/Escape)
- Shows city, state/province, country
- Powered by Open-Meteo Geocoding API

### 🌡️ Current Weather
- Temperature, feels-like, humidity, wind, pressure, visibility, UV index
- Weather condition with emoji (☀️🌧️❄️⛈️ etc.)
- Sunrise/sunset times
- Large hero temperature display

### ⏱️ Hourly Forecast (24h)
- Horizontal scrollable strip
- Time, temperature, precipitation probability, condition emoji
- Hover effects on each card

### 📅 7-Day Forecast
- Daily max/min temperatures
- Condition emoji per day
- "Today" label for current day
- Hover effects on each card

### 📊 Weather Charts
- **Dashboard:** Temperature trend for next 24 hours (Matplotlib)
- **History:** Historical temperature trend with gradient fill
- Theme-aware colors (dark/light)
- Smooth rendering embedded in Tkinter

### ⭐ Favorite Cities
- Save current city to favorites (one-click from dashboard)
- Modern card-based list with hover states
- Click to load weather instantly
- Remove with confirmation
- Empty state illustration

### 🕒 Search History
- Automatic logging of every successful search
- Click to re-search any past city
- Clear all history button
- Modern card layout with timestamps

### 📂 Weather History
- Automatic weather snapshots after each API call
- Filter by city dropdown
- Historical temperature trend chart
- Detailed metric display (temp, humidity, wind, condition)

### ⚙️ Settings
- **Theme:** Dark/Light with instant preview
- **Temperature:** °C / °F with unit symbols
- **Wind Speed:** km/h / mph
- **Default City:** Auto-load on startup
- All settings persist in SQLite across restarts

### 💾 Persistent Storage
- SQLite database for all user data (survives restarts)
- 4 tables: favorites, search_history, weather_history, user_settings
- WAL mode for better performance

### 🧵 Non-blocking UI
- Background threads for all API requests via `ThreadPoolExecutor`
- Thread-safe GUI updates via `root.after()`
- Request token system discards stale responses
- Loading indicators during fetch

### 🎨 Modern UI/UX
- CustomTkinter with rounded cards, smooth theme switching
- Hover effects on all interactive elements
- Per-metric accent colors (humidity=green, wind=red, pressure=amber, etc.)
- Animated sidebar active indicator
- Empty state illustrations
- Theme-aware styling throughout

---

## Screenshots

> 📷 The application is fully functional. Run `python main.py` to see it in action!

---

## Technology Stack

| Component | Technology |
|---|---|
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

```text
SkyCast/
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
│   ├── geocoding.py           # City name → lat/lon + suggestions
│   ├── weather_api.py         # Open-Meteo forecast API client
│   └── weather_service.py     # Geocoding + weather orchestrator
│
├── models/
│   └── weather.py             # WeatherData, HourlyForecast, DailyForecast
│
├── components/
│   ├── sidebar.py             # Navigation sidebar (animated indicator)
│   ├── search_bar.py          # Search input with autocomplete
│   ├── weather_card.py        # Info card widget (hover, accent colors)
│   └── forecast_card.py       # Forecast card widget (hover effects)
│
├── views/
│   ├── dashboard.py           # Main dashboard
│   ├── favorites.py           # Favorite cities (modern cards)
│   ├── history.py             # Search & weather history (tabs)
│   └── settings.py            # App settings (modern design)
│
├── utils/
│   ├── helpers.py             # Formatting utilities
│   ├── weather_icons.py       # WMO code → description + emoji
│   └── validators.py          # Input validation
│
├── assets/icons/              # Optional PNG weather icons
├── data/                      # SQLite database (auto-created, gitignored)
└── project-docs/              # Developer documentation
```

---

## Installation

### Prerequisites

- Python 3.10 or higher
- pip
- Git (to clone the repository)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/skycast-weather-app.git
cd skycast-weather-app
```

Replace `yourusername` with your actual GitHub username.

### 2. Create a Virtual Environment

A virtual environment keeps project dependencies isolated from other Python projects.

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

Install all required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

Check that Python and pip are available:

```bash
python --version
pip --version
```

---

## How to Run the Application

After completing the installation steps, follow these instructions to launch SkyCast.

### Windows

1. Open Command Prompt or PowerShell.
2. Navigate to the project directory:

```cmd
cd skycast-weather-app
```

3. Activate the virtual environment:

```cmd
venv\Scripts\activate
```

4. Start the application:

```cmd
python main.py
```

### Linux / macOS

1. Open the terminal.
2. Navigate to the project directory:

```bash
cd skycast-weather-app
```

3. Activate the virtual environment:

```bash
source venv/bin/activate
```

4. Start the application:

```bash
python3 main.py
```

### Using VS Code

You can also run SkyCast directly through Visual Studio Code:

1. Open the SkyCast project folder in VS Code.
2. Open the integrated terminal using **Ctrl + `**.
3. Activate the virtual environment.
4. Run the following command:

```bash
python main.py
```

### First Launch

- The application window will open automatically.
- The SQLite database (`data/skycast.db`) will be created automatically if it does not exist.
- The application loads the configured default city, if available.
- An active internet connection is required to retrieve weather information.

**Note:** Keep the virtual environment activated whenever you run the application from the terminal. Close the desktop window to exit SkyCast.

---

## API Information

SkyCast uses **Open-Meteo**, a free and open-source weather API that does not require registration or an API key.

- **Website:** https://open-meteo.com/
- **Geocoding API:** `https://geocoding-api.open-meteo.com/v1/search`
- **Forecast API:** `https://api.open-meteo.com/v1/forecast`
- **Data:** Current weather, hourly (168h), daily (7 days)
- **Weather Codes:** WMO standard codes

---

## Database Schema

SkyCast uses SQLite for persistent local storage. The database is automatically initialized when the application starts.

| Table | Purpose |
|---|---|
| `favorite_cities` | User's saved city locations (unique by lat/lon) |
| `search_history` | Record of every successful city search |
| `weather_history` | Snapshots of weather at time of search |
| `user_settings` | Theme, units, default city preferences (single row, id=1) |

See `project-docs/ARCHITECTURE.md` for full schema details.

---

## Application Workflow

1. User enters a city name and presses Search (or Enter).
2. City name is validated locally (minimum 2 characters, valid characters).
3. **Autocomplete:** Suggestions appear as the user types, with a debounce mechanism.
4. Geocoding API converts the city name into latitude and longitude in a background thread.
5. Forecast API fetches current, hourly, and daily weather data in a background thread.
6. UI updates with current conditions, forecasts, and charts on the main thread using `root.after()`.
7. Successful searches are saved to `search_history`, and weather snapshots are stored in `weather_history`.

---

## Error Handling

- **Invalid city name:** "City not found" message displayed with a suggestion.
- **No internet:** "Connection error" message; app remains functional.
- **API timeout:** Request times out after 10 seconds; error message shown.
- **Database error:** Error logged; app continues with degraded persistence.
- **Unexpected API response:** Graceful fallback; no fabricated data displayed.
- **Stale requests:** Request token system discards out-of-order responses.

---

## Testing

All core functionality has been verified:

1. ✅ App starts successfully.
2. ✅ Database auto-initializes with all 4 tables.
3. ✅ Valid city search (tested: New York, Berlin, Kāvali, London, Tokyo).
4. ✅ **Search autocomplete** (type "New" → Newark, New York, New Delhi...).
5. ✅ **Keyboard navigation** in suggestions (↑/↓/Enter/Escape).
6. ✅ Invalid city search shows a clear error.
7. ✅ No internet connection handled gracefully.
8. ✅ Favorites CRUD (add, list, remove, click-to-load).
9. ✅ Settings persistence across restarts (theme, units, default city).
10. ✅ UI remains responsive during API requests (background threading).
11. ✅ Search history stored and displayed.
12. ✅ Weather history stored, filtered, and charted.
13. ✅ Theme toggle (dark/light) applies immediately.
14. ✅ Unit conversion (Celsius/Fahrenheit, km/h/mph) applies immediately.
15. ✅ **Hover effects** on cards, buttons, and sidebar items.
16. ✅ **Modern charts** with gradient fills and clean axes.

---

## Future Improvements

Potential enhancements for future versions:

- Weather alerts and severe weather warnings.
- Multiple location dashboard.
- Animated weather backgrounds.
- Export weather data to CSV.
- PyInstaller packaging for distribution.
- Precipitation probability charts.
- Wind direction compass widget.
- Geolocation-based automatic city detection.

---

## Contributing

This project follows the AI-agent-friendly development workflow documented in `AGENTS.md`.

1. Read `AGENTS.md` and `project-docs/PROJECT_STATUS.md` before contributing.
2. Follow the existing architecture (see `project-docs/ARCHITECTURE.md`).
3. Update documentation files after every change.
4. Use parameterized SQL queries; never hardcode secrets.

---

## License

No license selected yet. All rights reserved until a license is chosen.
