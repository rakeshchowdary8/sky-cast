# SkyView – Changelog

All notable changes to this project are documented here.  
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added
- Full application implementation (Phases 2-9 complete)
- SQLite database with 4 tables: favorite_cities, search_history, weather_history, user_settings
- Open-Meteo geocoding API integration with error handling
- Open-Meteo forecast API integration with full JSON parsing
- Weather service orchestrator coordinating geocoding + forecast
- Weather data models: WeatherData, HourlyForecast, DailyForecast
- CustomTkinter main window with sidebar navigation
- Dashboard view: current weather, info cards, hourly/daily forecasts, Matplotlib chart
- Favorites view: add, list, remove, click-to-load favorite cities
- History view: search history tab + weather history tab with filtering and chart
- Settings view: theme toggle, temperature/wind units, default city
- Dark/Light theme support with immediate application
- Unit conversion: Celsius/Fahrenheit, km/h/mph
- Thread-safe API calls via ThreadPoolExecutor + root.after()
- Request token system for stale response handling
- Loading indicators and comprehensive error handling
- WMO weather code to description/emoji mapping (43 codes)
- Input validation for city names and settings

### Modernized (2026-11-12)
- **Search Autocomplete**: Real-time city suggestions as you type (debounced, keyboard navigable)
- **Modern UI Components**: Hover effects, smooth transitions, card-based layouts
- **Enhanced Sidebar**: Animated active indicator, improved visual hierarchy
- **Weather Cards**: Per-metric accent colors, hover animations, border highlights
- **Forecast Cards**: Hover effects with accent borders, better visual feedback
- **Favorites View**: Modern card design with hover states, empty state illustration
- **History View**: Tabbed interface with modern cards, empty states, improved charts
- **Settings View**: Redesigned with icons, better segmented buttons, helper text
- **Theme-Aware Styling**: All components properly respond to theme changes

### Changed
- Updated all documentation to reflect completed implementation
- SearchBar now uses `get_city_suggestions()` for autocomplete
- Geocoding service exposes `get_city_suggestions()` for partial matching
- WeatherCard accepts `accent_color` for per-metric theming

### Fixed
- Database path resolution using Path(__file__) not os.getcwd()
- Thread-safe GUI updates from background workers
- Duplicate favorite city prevention via UNIQUE constraint
- Sidebar indicator width/height constructor issue

---

## [0.1.0] – 2026-11-12 — Architecture & Documentation Setup

### Added
- Initial project documentation system
- Project directory structure
- `AGENTS.md` AI agent instruction manual
- `project-docs/` directory with 6 documentation files
- `requirements.txt` with all required dependencies
- `.gitignore` configured for Python projects
- `README.md` initial skeleton

---

## [0.0.0] – 2026-11-12 — Architecture & Documentation Setup

### Added
- Defined complete application architecture (see `project-docs/ARCHITECTURE.md`)
- Defined 4-table SQLite schema: `favorite_cities`, `search_history`, `weather_history`, `user_settings`
- Documented all technical decisions (see `project-docs/DECISIONS.md`)
- Created project folder structure: `config/`, `database/`, `services/`, `models/`, `components/`, `views/`, `utils/`, `assets/icons/`, `data/`
- Established WMO weather code mapping strategy (emoji fallback, PNG-ready)
- Established threading strategy (`ThreadPoolExecutor` + `root.after()`)
- Established API strategy (Open-Meteo geocoding + forecast, no API key)
- Established UI layout (sidebar + header + main content + cards + charts)
- Designed color palette for dark and light themes

### Notes
- No application code written yet — this is the architecture phase
- Awaiting user approval before Phase 2 begins