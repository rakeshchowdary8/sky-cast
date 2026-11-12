# AGENTS.md — AI Agent Instruction Manual for SkyView

> **READ THIS FILE FIRST** before every development session.  
> This file is the permanent instruction manual for every AI coding agent working on this project.

---

## Project Identity

- **Project Name:** SkyView – Real-Time Weather Desktop Application
- **Language:** Python 3.15+
- **GUI:** CustomTkinter (Tkinter-based)
- **Database:** SQLite (`sqlite3` built-in)
- **Weather API:** Open-Meteo (no API key required)
- **Charts:** Matplotlib
- **HTTP:** Requests library
- **Images:** Pillow

---

## Before Every Development Session

Mandatory reading — in this order:

1. **This file** (`AGENTS.md`) — instruction rules
2. **`project-docs/PROJECT_STATUS.md`** — current state, completed features, next task
3. **`project-docs/TASKS.md`** — granular task checklist (what is done, what is pending)
4. **`project-docs/ARCHITECTURE.md`** — module structure, data flows, design patterns
5. **`project-docs/DECISIONS.md`** — why key decisions were made (read when relevant)
6. **Actual source code** — inspect files related to the requested task before modifying them

> ⚠️ Never trust documentation alone. Verify features exist by reading the source code.  
> ⚠️ Documentation may lag behind code. Always reconcile discrepancies.

---

## Project Structure Quick Reference

```
SkyView/
├── main.py                    # Entry point
├── config/settings.py         # Constants, paths, colors, fonts
├── database/
│   ├── connection.py          # SQLite connection management
│   ├── schema.py              # CREATE TABLE statements
│   └── database.py            # All CRUD functions
├── services/
│   ├── geocoding.py           # City → lat/lon
│   ├── weather_api.py         # Open-Meteo forecast API
│   └── weather_service.py     # Orchestrator
├── models/weather.py          # WeatherData, HourlyForecast, DailyForecast
├── components/                # Reusable UI widgets
├── views/                     # Full-page views (Dashboard, Favorites, History, Settings)
├── utils/                     # Helpers, icons, validators
├── assets/icons/              # Optional PNG weather icons
├── data/skyview.db            # Auto-created SQLite DB (gitignored)
└── project-docs/              # Documentation system
```

---

## During Development

### Architecture Rules
1. Follow the existing modular architecture strictly.
2. Never put SQL queries inside UI files (views or components).
3. Never put API calls inside UI files.
4. Never perform network requests on the Tkinter main thread.
5. Use `ThreadPoolExecutor` for all API calls.
6. Use `root.after(0, callback)` to update GUI from worker threads.
7. Database path: resolved from `config/settings.py` using `Path(__file__)`, not `os.getcwd()`.

### Code Quality Rules
8. Avoid unnecessary code rewrites — extend, don't replace.
9. Never duplicate existing functionality — reuse existing functions.
10. Do not remove working features without explicit user permission.
11. Write modular, maintainable code with meaningful names.
12. Add comments for non-obvious logic.
13. Use parameterized SQL queries always — no string formatting in SQL.
14. Do not hardcode credentials, paths, or secrets.

### Error Handling Rules
15. Handle network failures gracefully (show user-friendly message, don't crash).
16. Handle invalid city names (show "City not found" message).
17. Handle SQLite exceptions with try/except.
18. Validate user input before submitting to API or database.
19. Never display fabricated or cached-as-real weather data.

### Testing Rules
20. Test important functionality after implementing it.
21. Use mock API responses for offline/error scenario tests.
22. Verify database operations with actual SQLite queries.
23. Do not mark a task complete unless verified.

---

## After Every Completed Task

Automatically update these files — do not skip:

| File | What to Update |
|------|---------------|
| `project-docs/PROJECT_STATUS.md` | Current phase, completed features, next task, files modified |
| `project-docs/TASKS.md` | Mark completed tasks ✅, mark in-progress tasks 🔄 |
| `project-docs/ARCHITECTURE.md` | Update if structure or patterns changed |
| `project-docs/DECISIONS.md` | Add new decisions with full context |
| `project-docs/CHANGELOG.md` | Add entries under [Unreleased] with Added/Changed/Fixed/Removed |
| `project-docs/DEVELOPMENT_LOG.md` | Add new session entry at the top |
| `README.md` | Update if features, setup, or structure changed |

> ⚠️ Update documentation *after* verifying the code works, not before.  
> ⚠️ Never mark a feature as complete in documentation if the code is broken or missing.

---

## Before Ending Every Session

Prepare and save a handover summary in `project-docs/PROJECT_STATUS.md`:

- Current development phase
- Completed tasks this session
- Current incomplete task (if any)
- Pending tasks
- Known issues and bugs
- Files created / modified / deleted
- Tests performed and actual results
- **Exact next step** for the next AI agent

---

## API Reference

### Geocoding
```
GET https://geocoding-api.open-meteo.com/v1/search
    ?name={city_name}&count=1&language=en&format=json
```
Response: `results[0].name`, `results[0].country`, `results[0].latitude`, `results[0].longitude`

### Weather Forecast
```
GET https://api.open-meteo.com/v1/forecast
    ?latitude={lat}&longitude={lon}
    &current=temperature_2m,apparent_temperature,relative_humidity_2m,
              wind_speed_10m,wind_direction_10m,surface_pressure,
              visibility,weather_code,is_day
    &hourly=temperature_2m,weather_code,precipitation_probability
    &daily=temperature_2m_max,temperature_2m_min,weather_code,
           sunrise,sunset,uv_index_max,precipitation_sum
    &wind_speed_unit=kmh&temperature_unit=celsius
    &timezone=auto&forecast_days=7
```

---

## Database Schema Quick Reference

```sql
-- favorite_cities: user's saved locations
CREATE TABLE favorite_cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name TEXT NOT NULL,
    country TEXT,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(latitude, longitude)
);

-- search_history: every successful city search
CREATE TABLE search_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name TEXT NOT NULL,
    country TEXT,
    latitude REAL,
    longitude REAL,
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- weather_history: snapshot after each API call
CREATE TABLE weather_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name TEXT NOT NULL,
    temperature REAL,
    feels_like REAL,
    humidity REAL,
    wind_speed REAL,
    pressure REAL,
    weather_condition TEXT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- user_settings: single-row preferences table
CREATE TABLE user_settings (
    id INTEGER PRIMARY KEY,
    temperature_unit TEXT DEFAULT 'Celsius',
    wind_unit TEXT DEFAULT 'km/h',
    theme TEXT DEFAULT 'dark',
    default_city TEXT
);
```

---

## Common Patterns

### Safe GUI Update from Thread
```python
# In worker thread:
result = fetch_weather(city)
# Schedule GUI update on main thread:
self.root.after(0, lambda: self._update_weather_display(result))
```

### Parameterized SQL Query
```python
cursor.execute(
    "INSERT INTO favorite_cities (city_name, country, latitude, longitude) VALUES (?, ?, ?, ?)",
    (city_name, country, latitude, longitude)
)
```

### Database Path Resolution
```python
from pathlib import Path
DB_PATH = Path(__file__).parent.parent / "data" / "skyview.db"
```

---

## Git Conventions

- Commit messages: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:` prefixes
- Never commit `data/skyview.db` (gitignored)
- Never commit `.env` files or secrets
- Always commit documentation updates together with code changes

---

## Contacts & Resources

- Open-Meteo docs: https://open-meteo.com/
- CustomTkinter docs: https://customtkinter.tomschimansky.com/
- WMO weather codes: https://open-meteo.com/en/docs (see "WMO Weather interpretation codes")
- Project documentation: `project-docs/` directory
