# SkyView – Task Tracker

> **Last Updated:** 2026-11-12  
> Legend: ✅ Completed | 🔄 In Progress | ⬜ Pending

---

## Project Setup

- [x] Define project requirements and architecture
- [x] Create project directory structure
- [x] Create `requirements.txt`
- [x] Create `.gitignore`
- [x] Create documentation system (`project-docs/`)
- [x] Create `AGENTS.md`
- [x] Initialize README.md skeleton
- [x] Create Python virtual environment (`venv`)
- [x] Install all dependencies (`pip install -r requirements.txt`)
- [x] Verify all imports work correctly
- [x] Create all `__init__.py` files
- [x] Create all source file stubs (placeholder files)
- [x] Create `data/.gitkeep`
- [x] Verify `main.py` launches without errors (skeleton)
- [x] Initialize Git repository

---

## Database Development

- [x] Implement `database/connection.py` — SQLite connection manager
- [x] Implement `database/schema.py` — table creation SQL
- [x] Implement `database/database.py` — all CRUD functions
- [x] Test: database auto-creates `data/skyview.db` on first run
- [x] Test: `favorite_cities` table CRUD
- [x] Test: `search_history` table CRUD
- [x] Test: `weather_history` table CRUD
- [x] Test: `user_settings` table read/write
- [x] Test: duplicate prevention for favorite cities
- [x] Test: parameterized queries prevent SQL injection
- [x] Test: proper connection closing

---

## API Integration

- [x] Implement `services/geocoding.py` — city name to lat/lon
- [x] Implement `services/weather_api.py` — Open-Meteo forecast API
- [x] Implement `services/weather_service.py` — orchestrator for geocoding + weather
- [x] Implement `models/weather.py` — WeatherData, HourlyForecast, DailyForecast dataclasses
- [x] Map all Open-Meteo WMO weather codes to descriptions
- [x] Test: valid city name geocoding
- [x] Test: invalid city name returns clear error
- [x] Test: forecast API returns current weather
- [x] Test: forecast API returns 24h hourly data
- [x] Test: forecast API returns 7-day daily data
- [x] Test: network timeout handled gracefully
- [x] Test: no internet connection handled gracefully
- [x] Test: unexpected API response handled gracefully

---

## UI Development

- [x] Implement `main.py` — application entry point, root window
- [x] Implement `config/settings.py` — constants, colors, fonts, defaults
- [x] Implement `components/sidebar.py` — navigation sidebar
- [x] Implement `components/header.py` — top header bar with logo, search, theme toggle
- [x] Implement `components/search_bar.py` — search field and button
- [x] Implement `components/weather_card.py` — info cards (humidity, wind, etc.)
- [x] Implement `components/forecast_card.py` — hourly/daily forecast cards
- [x] Implement `views/dashboard.py` — main dashboard view
- [x] Implement `views/favorites.py` — favorite cities view
- [x] Implement `views/history.py` — search history + weather history view
- [x] Implement `views/settings.py` — settings view
- [x] Implement weather history sub-view in `views/history.py` or separate file
- [x] Implement `utils/helpers.py` — formatting utilities
- [x] Implement `utils/weather_icons.py` — WMO code to icon/emoji mapping
- [x] Implement `utils/validators.py` — input validation

---

## Feature Development

- [x] Dashboard: city search flow (input → geocode → fetch → display)
- [x] Dashboard: loading spinner during API requests
- [x] Dashboard: current weather display (temp, condition, feels-like)
- [x] Dashboard: weather info cards (humidity, wind, pressure, visibility, UV)
- [x] Dashboard: hourly forecast strip (24h)
- [x] Dashboard: 7-day forecast section
- [x] Dashboard: Matplotlib temperature chart (embedded in Tkinter)
- [x] Dashboard: refresh button (via search)
- [x] Favorites: add current city to favorites
- [x] Favorites: list all favorite cities
- [x] Favorites: remove a favorite city
- [x] Favorites: click to load weather for a favorite city
- [x] Search History: auto-save every successful search
- [x] Search History: display recent searches list
- [x] Search History: click to reload a past search
- [x] Search History: clear all history button
- [x] Weather History: auto-save weather snapshot after each API call
- [x] Weather History: display snapshots list
- [x] Weather History: filter by city name
- [x] Weather History: Matplotlib chart of historical temps
- [x] Settings: dark/light theme toggle (apply globally)
- [x] Settings: temperature unit toggle (°C / °F)
- [x] Settings: wind speed unit toggle (km/h / mph)
- [x] Settings: default city input (loaded on startup)
- [x] Settings: persist all settings in SQLite
- [x] Settings: load saved settings on startup
- [x] Threading: all API calls on background thread
- [x] Threading: GUI updates via `root.after(0, callback)`
- [x] Threading: stale response handling

---

## Testing

- [x] Application starts successfully
- [x] Database auto-initializes
- [x] Search valid city — weather displayed
- [x] Search invalid city — error message displayed
- [x] No internet connection — graceful error
- [x] Add favorite city — appears in list
- [x] Remove favorite city — removed from list
- [x] Favorites persist after restart
- [x] Search history stored after search
- [x] Weather snapshots stored after search
- [x] Theme preference persists after restart
- [x] Unit preference persists after restart
- [x] Default city loads on startup
- [x] Application does not freeze during API request
- [x] Mock API tests for offline scenarios (verified via error handling)

---

## Bug Fixes

- [ ] (None yet — to be filled as bugs are discovered)

---

## Documentation

- [x] `project-docs/PROJECT_STATUS.md`
- [x] `project-docs/TASKS.md` (this file)
- [x] `project-docs/ARCHITECTURE.md`
- [x] `project-docs/DECISIONS.md`
- [x] `project-docs/CHANGELOG.md`
- [x] `project-docs/DEVELOPMENT_LOG.md`
- [x] `AGENTS.md`
- [x] `README.md` skeleton
- [ ] README.md final version (after app completion)
- [x] Code docstrings in all modules
- [x] Inline comments for complex logic

---

## Deployment

- [ ] Verify app runs from a fresh virtual environment
- [ ] Test on Windows
- [ ] Consider PyInstaller packaging (future)

---