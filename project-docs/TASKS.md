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
- [ ] Create Python virtual environment (`venv`)
- [ ] Install all dependencies (`pip install -r requirements.txt`)
- [ ] Verify all imports work correctly
- [ ] Create all `__init__.py` files
- [ ] Create all source file stubs (placeholder files)
- [ ] Create `data/.gitkeep`
- [ ] Verify `main.py` launches without errors (skeleton)
- [ ] Initialize Git repository

---

## Database Development

- [ ] Implement `database/connection.py` — SQLite connection manager
- [ ] Implement `database/schema.py` — table creation SQL
- [ ] Implement `database/database.py` — all CRUD functions
- [ ] Test: database auto-creates `data/skyview.db` on first run
- [ ] Test: `favorite_cities` table CRUD
- [ ] Test: `search_history` table CRUD
- [ ] Test: `weather_history` table CRUD
- [ ] Test: `user_settings` table read/write
- [ ] Test: duplicate prevention for favorite cities
- [ ] Test: parameterized queries prevent SQL injection
- [ ] Test: proper connection closing

---

## API Integration

- [ ] Implement `services/geocoding.py` — city name to lat/lon
- [ ] Implement `services/weather_api.py` — Open-Meteo forecast API
- [ ] Implement `services/weather_service.py` — orchestrator for geocoding + weather
- [ ] Implement `models/weather.py` — WeatherData, HourlyForecast, DailyForecast dataclasses
- [ ] Map all Open-Meteo WMO weather codes to descriptions
- [ ] Test: valid city name geocoding
- [ ] Test: invalid city name returns clear error
- [ ] Test: forecast API returns current weather
- [ ] Test: forecast API returns 24h hourly data
- [ ] Test: forecast API returns 7-day daily data
- [ ] Test: network timeout handled gracefully
- [ ] Test: no internet connection handled gracefully
- [ ] Test: unexpected API response handled gracefully

---

## UI Development

- [ ] Implement `main.py` — application entry point, root window
- [ ] Implement `config/settings.py` — constants, colors, fonts, defaults
- [ ] Implement `components/sidebar.py` — navigation sidebar
- [ ] Implement `components/header.py` — app header with search
- [ ] Implement `components/search_bar.py` — search field and button
- [ ] Implement `components/weather_card.py` — info cards (humidity, wind, etc.)
- [ ] Implement `components/forecast_card.py` — hourly/daily forecast cards
- [ ] Implement `views/dashboard.py` — main dashboard view
- [ ] Implement `views/favorites.py` — favorite cities view
- [ ] Implement `views/history.py` — search history view
- [ ] Implement `views/settings.py` — settings view
- [ ] Implement weather history sub-view in `views/history.py` or separate file
- [ ] Implement `utils/helpers.py` — formatting utilities
- [ ] Implement `utils/weather_icons.py` — WMO code to icon/emoji mapping
- [ ] Implement `utils/validators.py` — input validation

---

## Feature Development

- [ ] Dashboard: city search flow (input → geocode → fetch → display)
- [ ] Dashboard: loading spinner during API requests
- [ ] Dashboard: current weather display (temp, condition, feels-like)
- [ ] Dashboard: weather info cards (humidity, wind, pressure, visibility, UV)
- [ ] Dashboard: hourly forecast strip (24h)
- [ ] Dashboard: 7-day forecast section
- [ ] Dashboard: Matplotlib temperature chart (embedded in Tkinter)
- [ ] Dashboard: refresh button
- [ ] Favorites: add current city to favorites
- [ ] Favorites: list all favorite cities
- [ ] Favorites: remove a favorite city
- [ ] Favorites: click to load weather for a favorite city
- [ ] Search History: auto-save every successful search
- [ ] Search History: display recent searches list
- [ ] Search History: click to reload a past search
- [ ] Search History: clear all history button
- [ ] Weather History: auto-save weather snapshot after each API call
- [ ] Weather History: display snapshots list
- [ ] Weather History: filter by city name
- [ ] Weather History: Matplotlib chart of historical temps
- [ ] Settings: dark/light theme toggle (apply globally)
- [ ] Settings: temperature unit toggle (°C / °F)
- [ ] Settings: wind speed unit toggle (km/h / mph)
- [ ] Settings: default city input (loaded on startup)
- [ ] Settings: persist all settings in SQLite
- [ ] Settings: load saved settings on startup
- [ ] Threading: all API calls on background thread
- [ ] Threading: GUI updates via `root.after(0, callback)`
- [ ] Threading: stale response handling

---

## Testing

- [ ] Application starts successfully
- [ ] Database auto-initializes
- [ ] Search valid city — weather displayed
- [ ] Search invalid city — error message displayed
- [ ] No internet connection — graceful error
- [ ] Add favorite city — appears in list
- [ ] Remove favorite city — removed from list
- [ ] Favorites persist after restart
- [ ] Search history stored after search
- [ ] Weather snapshots stored after search
- [ ] Theme preference persists after restart
- [ ] Unit preference persists after restart
- [ ] Default city loads on startup
- [ ] Application does not freeze during API request
- [ ] Mock API tests for offline scenarios

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
- [ ] Code docstrings in all modules
- [ ] Inline comments for complex logic

---

## Deployment

- [ ] Verify app runs from a fresh virtual environment
- [ ] Test on Windows
- [ ] Consider PyInstaller packaging (future)

