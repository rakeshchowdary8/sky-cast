# SkyView – Technical Decisions Log

> **Last Updated:** 2026-11-12

---

## Decision 001 — GUI Framework: CustomTkinter over PyQt5/wxPython

**Date:** 2026-11-12  
**Problem:** Choose a GUI framework for the desktop weather application.  
**Chosen Approach:** `customtkinter` on top of Python's built-in `tkinter`.  
**Reason:**
- CustomTkinter provides modern-looking, rounded widgets without system-native widget constraints
- Tkinter is built into Python — zero install risk, no licensing concerns
- CustomTkinter is actively maintained and has first-class dark/light theme support
- Significantly simpler than PyQt5 (no Qt Designer, no signals/slots complexity)
- Lightweight compared to Electron-based or web-based alternatives

**Alternatives Considered:**
- PyQt5 — powerful but heavier, GPL licensing complications for distribution
- wxPython — native look but complex cross-platform theming
- Dear PyGui — game-loop-oriented, overkill for this use case
- Tkinter alone — available but visually dated without CustomTkinter

**Trade-offs:** CustomTkinter has a smaller community than PyQt5; some advanced widgets must be built manually.

---

## Decision 002 — Weather API: Open-Meteo (Free, No API Key)

**Date:** 2026-11-12  
**Problem:** Choose a weather API that works without user registration.  
**Chosen Approach:** Open-Meteo forecast API + Open-Meteo Geocoding API.  
**Reason:**
- Completely free for non-commercial use
- No API key required — zero setup friction for end users
- Provides current weather, hourly forecasts, 7-day daily forecasts
- Provides WMO standard weather codes (well-documented)
- Provides UV index, sunrise/sunset, precipitation probability
- JSON response — easy to parse
- High reliability and global coverage

**Alternatives Considered:**
- OpenWeatherMap — requires API key, free tier has limitations
- WeatherAPI.com — requires API key
- Weatherstack — paid for real-time data
- NOAA — US-only, complex parsing

**Trade-offs:** Open-Meteo's geocoding may have fewer city aliases than OpenWeatherMap; rare city names may not resolve.

---

## Decision 003 — Database: SQLite via Built-in `sqlite3`

**Date:** 2026-11-12  
**Problem:** Choose a local data persistence solution.  
**Chosen Approach:** Python's built-in `sqlite3` module with a local `data/skyview.db` file.  
**Reason:**
- No external dependencies required
- File-based — no server process, perfect for desktop apps
- Sufficient for the data volumes of a weather app (favorites, history, settings)
- Python's `sqlite3` supports parameterized queries natively

**Alternatives Considered:**
- PostgreSQL — server-based, excessive for a desktop app
- MySQL — same issue
- SQLAlchemy ORM — adds abstraction complexity; overkill for a small schema
- TinyDB (JSON file) — no SQL, weaker querying

**Trade-offs:** SQLite is not suitable for concurrent multi-user write workloads; acceptable here as the app is single-user.

---

## Decision 004 — Threading: `ThreadPoolExecutor` with `root.after()` for GUI Updates

**Date:** 2026-11-12  
**Problem:** Prevent Tkinter GUI from freezing during HTTP requests.  
**Chosen Approach:** Submit API calls to `concurrent.futures.ThreadPoolExecutor`; use `root.after(0, callback)` to marshal results back to the main thread.  
**Reason:**
- Tkinter is not thread-safe — GUI widgets must only be updated from the main thread
- `ThreadPoolExecutor` provides a managed thread pool with graceful shutdown
- `root.after(0, fn)` schedules a function to run on the next Tkinter event loop iteration — the correct pattern for thread-to-GUI communication
- Simpler and more Pythonic than `queue.Queue` polling loops

**Alternatives Considered:**
- `threading.Thread` directly — works but `ThreadPoolExecutor` provides better lifecycle management
- `asyncio` with `tkinter` — complex integration; Tkinter has no native async event loop
- `queue.Queue` with polling `root.after(100, check_queue)` — works but adds unnecessary complexity

**Trade-offs:** Worker threads must never touch GUI widgets directly; discipline required in service layer code.

---

## Decision 005 — WMO Weather Codes Over Custom Codes

**Date:** 2026-11-12  
**Problem:** How to map numeric weather codes to human-readable descriptions and icons.  
**Chosen Approach:** Use the WMO (World Meteorological Organization) standard codes as returned by Open-Meteo, mapped to descriptions and emoji in `utils/weather_icons.py`.  
**Reason:**
- Open-Meteo uses standard WMO codes — no proprietary translation layer needed
- Emoji provide universal icon fallback without requiring PNG asset files
- PNG icons in `assets/icons/` can be added later without changing business logic

**Trade-offs:** Emoji rendering varies slightly across operating systems; PNG icons provide more visual consistency.

---

## Decision 006 — Database Path: Relative to Project Root, Not CWD

**Date:** 2026-11-12  
**Problem:** How to reliably locate `data/skyview.db` regardless of where the app is launched from.  
**Chosen Approach:** Compute the database path in `config/settings.py` using `Path(__file__).parent.parent / "data" / "skyview.db"`, which is relative to the `config/` file's location, not `os.getcwd()`.  
**Reason:**
- `os.getcwd()` changes if the user launches the app from a different directory
- `Path(__file__)` always resolves to the script's own location, which is stable
- This pattern is idiomatic Python for bundled applications

**Trade-offs:** None significant.

---

## Decision 007 — View Switching: Frame Show/Hide over Notebook Widget

**Date:** 2026-11-12  
**Problem:** How to implement sidebar navigation between multiple views.  
**Chosen Approach:** Each view is a `CTkFrame`; navigation switches visibility using `pack()`/`pack_forget()` and calls `on_show()` on the activated view.  
**Reason:**
- `CTkTabview` and `ttk.Notebook` impose fixed tab-at-top layouts, incompatible with a sidebar design
- Manual frame switching gives full control over layout and transition behavior
- Each view can implement `on_show()` to refresh its data lazily

**Alternatives Considered:**
- `ttk.Notebook` — tab-based, not sidebar-compatible
- `CTkTabview` — same issue
- Destroying and recreating frames — wastes resources and loses widget state

**Trade-offs:** Requires explicit show/hide management; all views are always in memory.

