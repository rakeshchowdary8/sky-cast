# SkyView – Changelog

All notable changes to this project are documented here.  
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added
- Initial project documentation system
- Project directory structure
- `AGENTS.md` AI agent instruction manual
- `project-docs/` directory with 6 documentation files
- `requirements.txt` with all required dependencies
- `.gitignore` configured for Python projects
- `README.md` initial skeleton

---

## [0.1.0] – 2026-11-12 — Architecture & Documentation Setup

### Added
- Defined complete application architecture (see `project-docs/ARCHITECTURE.md`)
- Defined 4-table SQLite schema: `favorite_cities`, `search_history`, `weather_history`, `user_settings`
- Documented all technical decisions (see `project-docs/DECISIONS.md`)
- Created project folder structure: `config/`, `database/`, `services/`, `models/`, `components/`, `views/`, `utils/`, `assets/icons/`, `data/`
- Established WMO weather code mapping strategy (emoji fallback, PNG-ready)
- Established threading strategy (`ThreadPoolExecutor` + `root.after()`)
- Established API strategy (Open-Meteo geocoding + forecast, no API key)

### Notes
- No application code written yet — this is the architecture phase
- Awaiting user approval before Phase 2 begins
