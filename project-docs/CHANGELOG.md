# SkyCast – Changelog

All notable changes to this project are documented here.  
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased] — SkyCast Phase 15: Simplified Search & Clean Sidebar

### Changed
- **Removed Search Autocomplete**: Search bar no longer shows autocomplete suggestions dropdown
- **Removed Loading State on Search Button**: Search button no longer shows loading spinner during API calls
- **Removed Sidebar Active Indicator**: Blue vertical line indicator removed from sidebar navigation items
- **Simplified SearchBar Component**: Clean search input with search button only

### Added
- **Error Toast Notification**: "City not found" and other errors now display as a toast notification at the top of the dashboard with dismiss button and auto-hide after 5 seconds

---

## [Unreleased] — SkyCast Phase 14: Light Mode Only & Search Dropdown Z-Index Fix

### Added — Phase 11: Premium UI Redesign (SkyCast)
- **Premium Dark Theme**: Deep navy/charcoal backgrounds (#0a0e17), soft blue/cyan/purple accents (#3b82f6, #06b6d4, #a855f7)
- **Premium Typography**: Inter (UI) + Poppins (display/hero) font families
- **Design Token System**: Spacing scale (PAD_XS→PAD_2XL), border radius tokens, animation timings, metric accent colors with light variants
- **Hero Dashboard Section**: 72pt temperature display, 120pt weather emoji, feels-like + min/max row
- **6 Premium Detail Cards**: Humidity (green), Wind (red), Pressure (amber), Visibility (cyan), UV Index (orange), Cloud Cover (purple) — each with accent icon container, hover border highlight
- **Horizontal Hourly Forecast**: 24-hour scrollable strip, current hour highlighted with "NOW" badge
- **5-Day Daily Forecast**: Horizontal scrollable cards, "Today" badge, high/low temps, precip probability, UV index
- **Sunrise/Sunset Card**: Sunrise/sunset times with daylight duration calculation
- **Atmospheric Conditions Card**: Cloud cover, visibility, pressure
- **Weather Alerts Section**: Styled alert banner (ready for API integration)
- **Temperature Trend Chart**: 24-hour Matplotlib chart with gradient fill, theme-aware colors
- **Beautiful Empty State**: SkyCast branding onboarding screen with call-to-action
- **Comprehensive Hover Effects**: All interactive cards/buttons have smooth transitions with accent borders
- **Responsive Scrollable Layout**: Dashboard uses CTkScrollableFrame with proper spacing

### Added — Search & Navigation
- **Premium Search Bar**: Integrated search icon, autocomplete dropdown, debounced API (200ms), keyboard nav (↑/↓/Enter/Esc), loading states, focus ring animations
- **Animated Sidebar**: Active indicator with smooth animation, SkyCast split branding (Sky + Cast), version badge
- **Search Autocomplete**: Real-time city suggestions, shows city/state/country, click-to-select

### Added — Infrastructure
- **New Component**: `components/detail_card.py` — Premium metric cards
- **New Model Structure**: `CurrentWeather` dataclass, datetime objects, cloud_cover field
- **Enhanced API Parsing**: cloud_cover, sunrise/sunset as datetime, precipitation_probability_max

### Modernized (2026-11-12) — Phase 10 Polish
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
- **App Renamed**: SkyView → SkyCast (v2.0.0)
- **Window Title**: "SkyView – Real-Time Weather" → "SkyCast – Premium Weather Dashboard"
- **Default Window Size**: 1280×800 → 1440×900
- **Sidebar Width**: 200px → 260px
- **Search Integration**: Moved from header to dashboard for premium layout
- **Color Palette**: Complete overhaul with design tokens
- **Font System**: Segoe UI → Inter + Poppins
- **Weather Data Model**: Restructured with CurrentWeather, datetime objects
- **Documentation**: All docs updated for SkyCast branding

### Fixed
- Database path resolution using Path(__file__) not os.getcwd()
- Thread-safe GUI updates from background workers
- Duplicate favorite city prevention via UNIQUE constraint
- Sidebar indicator width/height constructor issue
- Color alpha values in CTkFrame fg_color (use valid 6-digit hex)
- Missing FONT_TINY import in forecast_card.py
- Missing PAD_XS import in sidebar.py
- WeatherData model attribute access (temperature → current.temperature)
- HourlyForecast attribute (precipitation_probability → precip_probability)
- All "border" color key references updated to "card_border"
- Matplotlib font warnings (Inter/Poppins fallback gracefully)
- **Trackpad scrolling on Windows** — Added mouse wheel bindings to all CTkScrollableFrame instances (main, hourly, daily)
- **Empty state transition** — Simplified `_hide_empty_state()` to reliably repack weather content sections
- **SearchBar integration** — Added SearchBar to dashboard header with autocomplete dropdown, keyboard navigation, loading states; fixed broken `_search_bar` references in main.py; fixed missing `CARD_CORNER_RADIUS` import in search_bar.py

### Added — Phase 12: shadcn-inspired UI Polish & Collapsible Sidebar
- **Detail Cards Redesigned** (`components/detail_card.py`): shadcn-inspired cards with icon containers, clear label/value/unit hierarchy, smooth hover elevation, full theme consistency
- **Collapsible Sidebar** (`components/sidebar.py`): Smooth width animation (260px ↔ 72px), chevron toggle button, icon-only mode, animated active indicator, logo/text hide/show
- **Settings View Redesigned** (`views/settings.py`): Modern card-based sections, proper segmented buttons with theme-aware colors, larger touch targets, better visual hierarchy
- **Theme Consistency Fix**: All components now use proper color keys (`card`, `card_border`, `input_bg`, `card_hover`, `text`, `text_secondary`, `text_dim`, `accent`, `accent_soft`, `success`, `warning`, `button_text`) — no more mixed dark/light elements
- **Sidebar Toggle Callback**: Main app receives `on_toggle` callback for layout adjustments

### Changed
- **DetailCard API**: Added `update_title()`, `update_icon()`, improved `apply_colors()` for full theme refresh
- **Sidebar API**: Added `toggle()`, `expand()`, `collapse()`, `is_expanded()` public methods
- **Settings Segmented Buttons**: Now use `input_bg` for unselected state, proper `fg_color`, consistent corner radius

### Fixed
- **Theme mixing in UI** — All components now consistently apply theme colors; no more dark components in light mode or vice versa
- **Detail cards not displaying well** — Redesigned with better visual hierarchy, larger icons, clearer value/unit separation
- **Sidebar toggle animation** — Smooth 300ms cubic easing with proper text/icon visibility transitions

---

## [2.1.0] – 2026-11-12 — shadcn-inspired Component System & Full View Migration (Phase 13)

### Added — Design System Foundation
- **Complete Design Token System** (`config/settings.py`): DARK/LIGHT color palettes following shadcn conventions, 16-step spacing scale (SPACE_1-16), 8-step border radius scale (RADIUS_NONE-FULL), 12-step typography scale (FONT_SIZE_XS-9XL), animation presets, METRIC_ACCENTS with light variants, STATUS_COLORS, WEATHER_ICONS, helper functions (get_colors, get_button_config, get_input_config, hex_to_rgb, lerp_color, easing functions)
- **Animation Framework** (`utils/animations.py`): Animation class with property interpolation (color, size, position), easing functions (cubic, expo), AnimationSequence for parallel/sequential execution, high-level helpers (fade_in, slide_in, scale_in, animate_sidebar_toggle, animate_color_transition, pulse_animation), micro-interaction helpers (setup_hover_animation, setup_focus_ring, animate_button_press), stagger_animate_children for lists
- **Base Component Library** (`components/base.py`): Card (default, outlined, elevated, ghost), Button (default, secondary, outline, ghost, destructive; sizes sm, default, lg, xl, icon), Input (label, error state, left/right icons, focus ring), Badge (default, secondary, outline, destructive, success, warning; sizes sm, default, lg), Separator, Avatar, Tooltip, Skeleton (shimmer animation), factory functions

### Added — Component Migration
- **SearchBar** (`components/search_bar.py`): Complete rewrite using base Input/Button, smooth dropdown entrance animation (fade+slide), keyboard navigation with animated selection (↑/↓/Enter/Escape), loading states via Button.set_loading(), hover/focus animations on container, apply_colors() for theme switching
- **Sidebar** (`components/sidebar.py`): Staggered entrance animations for nav items (slide from left), smooth width animation with cubic easing (260px ↔ 72px), animated active indicator (ease-out-cubic), hover animations on nav items, theme toggle button, chevron toggle with icon animation, progress-based text/icon visibility during collapse, apply_colors() with hover re-setup
- **Forecast Cards** (`components/forecast_card.py`): HourlyCard and DailyCard with entrance animations (fade+slide-up), smooth hover transitions via animate_color_transition, NOW/TODAY badges with accent colors, semantic UV index colors (green/yellow/orange/red), precipitation indicators, apply_colors()

### Added — View Migration
- **Dashboard** (`views/dashboard.py`): Complete migration to Card/Button/Badge components, Card-based hero/detail/sun-atmos/chart sections, integrated SearchBar, staggered entrance animations for all sections, proper apply_colors() with theme switching
- **Favorites** (`views/favorites.py`): Card component for list items, Button component for actions, staggered entrance animations for cards, proper theme consistency
- **History** (`views/history.py`): Card component for list items, Button component for tabs/actions, staggered animations, proper theme consistency
- **Settings** (`views/settings.py`): Card component for sections, Button component for save, Card-based sections with dividers, focus ring animation on entry field, proper theme consistency

### Changed
- **DetailCard** (`components/detail_card.py`): Fixed METRIC_ACCENTS dict access (use .main/.light keys), apply_colors() for new palette
- **Main.py**: Updated for new DashboardView, Sidebar with theme callback

### Fixed
- **Button component invalid kwargs** — Filtered out `padding_x` and `radius` from CTkButton constructor
- **apply_colors() bug** — Fixed color resolution logic (get_button_config already returns resolved colors)
- **CTkSegmentedButton bind issue** — Removed unsupported bind calls for hover animations
- **METRIC_ACCENTS access** — Fixed to access dict values properly (.main, .light, .text)
- **SearchBar dropdown width/height** — Fixed CTkFrame place() requiring dimensions in constructor
- **SearchBar animation guard** — Added winfo_exists() check before animating to prevent AttributeError
- **Section heading grouping** — Wrapped all dashboard section headers with their content containers for visual grouping (Detail Cards, Hourly Forecast, Daily Forecast, Sun & Atmosphere, Chart) — headings now visually belong to their sections

---

## [1.0.0] – 2026-11-12 — SkyView Complete Implementation

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