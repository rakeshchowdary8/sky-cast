"""
main.py — SkyView application entry point.

Creates the App window, initializes the database, loads settings,
builds the sidebar and all views, then starts the Tkinter event loop.

Architecture:
  App (CTk root)
    ├── Sidebar (left column)
    └── Content frame (right column)
          ├── DashboardView
          ├── FavoritesView
          ├── HistoryView
          └── SettingsView

Threading pattern:
  API calls → ThreadPoolExecutor.submit()
  GUI updates → root.after(0, callback)   ← always on main thread
"""

import logging
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import customtkinter as ctk

# ---------------------------------------------------------------------------
# Ensure the project root is on sys.path so all imports work when running
# `python main.py` directly (not as a package).
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ---------------------------------------------------------------------------
# Project imports
# ---------------------------------------------------------------------------
from config import settings as S
from database import database
from services.weather_service import fetch_weather, WeatherServiceError
from utils.validators import validate_city_name
from components.sidebar import Sidebar
from components.search_bar import SearchBar
from views.dashboard import DashboardView
from views.favorites import FavoritesView
from views.history import HistoryView
from views.settings import SettingsView

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ===========================================================================
# App — Root CustomTkinter window
# ===========================================================================

class App(ctk.CTk):
    """
    SkyView main application window.

    Responsibilities:
    - Initialise the database on startup.
    - Load user settings and apply theme.
    - Build sidebar + content area.
    - Route navigation between views.
    - Manage the background thread pool.
    - Coordinate weather search flow.
    """

    def __init__(self):
        super().__init__()

        # --- Database init ---
        database.initialize_database()
        logger.info("Database initialised.")

        # --- Load user settings ---
        self._db_settings = database.get_settings()
        self._theme = self._db_settings.get("theme", "dark")
        self._temp_unit = self._db_settings.get("temperature_unit", "Celsius")
        self._wind_unit = self._db_settings.get("wind_unit", "km/h")
        self._default_city = self._db_settings.get("default_city", "")

        # --- Apply theme ---
        ctk.set_appearance_mode(self._theme)
        ctk.set_default_color_theme("blue")
        self._colors = S.DARK if self._theme == "dark" else S.LIGHT

        # --- Window config ---
        self.title(S.WINDOW_TITLE)
        self.geometry(f"{S.WINDOW_DEFAULT_WIDTH}x{S.WINDOW_DEFAULT_HEIGHT}")
        self.minsize(S.WINDOW_MIN_WIDTH, S.WINDOW_MIN_HEIGHT)
        self.configure(fg_color=self._colors["bg"])

        # --- Thread pool ---
        self._executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="skyview")
        self._request_id = 0  # Incremented on each search; used to discard stale results

        # --- Build UI ---
        self._build_layout()

        # --- Keyboard shortcut: Ctrl+Q to quit ---
        self.bind("<Control-q>", lambda _: self.on_close())
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # --- Load default city if configured ---
        if self._default_city:
            self.after(300, lambda: self.search_city(self._default_city))

        logger.info("SkyView started.")

    # -----------------------------------------------------------------------
    # Layout
    # -----------------------------------------------------------------------

    def _build_layout(self):
        """Construct the two-column layout: sidebar | content."""
        # Main container
        self._main = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self._main.pack(fill="both", expand=True)
        self._main.columnconfigure(1, weight=1)
        self._main.rowconfigure(0, weight=1)

        # --- Sidebar ---
        self._sidebar = Sidebar(
            self._main,
            on_navigate=self.show_view,
            colors=self._colors,
        )
        self._sidebar.grid(row=0, column=0, sticky="nsew")

        # --- Right panel: header + content ---
        right_panel = ctk.CTkFrame(self._main, fg_color="transparent", corner_radius=0)
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.rowconfigure(1, weight=1)
        right_panel.columnconfigure(0, weight=1)

        # Header strip with search bar
        self._build_header(right_panel)

        # Content frame that holds all swappable views
        self._content = ctk.CTkFrame(right_panel, fg_color="transparent", corner_radius=0)
        self._content.grid(row=1, column=0, sticky="nsew")
        self._content.rowconfigure(0, weight=1)
        self._content.columnconfigure(0, weight=1)

        # Instantiate all views (all hidden except dashboard)
        self._dashboard = DashboardView(
            self._content, app=self,
            colors=self._colors,
            temp_unit=self._temp_unit,
            wind_unit=self._wind_unit,
        )
        self._favorites = FavoritesView(self._content, app=self, colors=self._colors)
        self._history = HistoryView(
            self._content, app=self,
            colors=self._colors,
            temp_unit=self._temp_unit,
        )
        self._settings_view = SettingsView(
            self._content, app=self,
            colors=self._colors,
            settings=self._db_settings,
        )

        self._views = {
            "dashboard": self._dashboard,
            "favorites": self._favorites,
            "history":   self._history,
            "whistory":  self._history,   # sidebar alias
            "settings":  self._settings_view,
        }

        self.show_view("dashboard")

    def _build_header(self, parent):
        """Top bar with logo text, search bar, and theme toggle."""
        header = ctk.CTkFrame(
            parent,
            height=64,
            fg_color=self._colors["sidebar"],
            corner_radius=0,
        )
        header.grid(row=0, column=0, sticky="ew")
        header.pack_propagate(False)

        inner = ctk.CTkFrame(header, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=S.PAD_MD)

        # App name
        ctk.CTkLabel(
            inner, text=f"🌤️  {S.APP_NAME}",
            font=S.FONT_LARGE,
            text_color=self._colors["text"],
        ).pack(side="left", padx=(0, S.PAD_LG))

        # Search bar
        self._search_bar = SearchBar(
            inner,
            on_search=self.search_city,
            colors=self._colors,
        )
        self._search_bar.pack(side="left", padx=(0, S.PAD_MD))

        # Theme toggle button
        self._theme_btn = ctk.CTkButton(
            inner,
            text="☀️ Light" if self._theme == "dark" else "🌙 Dark",
            width=90, height=36,
            font=S.FONT_SMALL,
            fg_color=self._colors["card"],
            hover_color=self._colors["card_hover"],
            text_color=self._colors["text"],
            corner_radius=S.BUTTON_CORNER_RADIUS,
            command=self._toggle_theme,
        )
        self._theme_btn.pack(side="right")

    # -----------------------------------------------------------------------
    # View navigation
    # -----------------------------------------------------------------------

    def show_view(self, view_name: str):
        """Show the requested view and hide all others."""
        for name, view in self._views.items():
            view.pack_forget()

        # Resolve alias
        target = self._views.get(view_name)
        if target:
            target.pack(fill="both", expand=True)
            if hasattr(target, "on_show"):
                target.on_show()

        logger.debug("Switched to view: %s", view_name)

    # -----------------------------------------------------------------------
    # Weather search flow
    # -----------------------------------------------------------------------

    def search_city(self, city_name: str):
        """
        Validate input, then dispatch a background API fetch.
        Called from SearchBar or any view that triggers a city search.
        """
        is_valid, error_msg = validate_city_name(city_name)
        if not is_valid:
            self._dashboard.show_error(error_msg)
            self.show_view("dashboard")
            return

        # Increment request ID — any older in-flight request will be ignored
        self._request_id += 1
        my_id = self._request_id

        # Show loading state
        self._dashboard.show_loading()
        self.show_view("dashboard")
        self._search_bar.set_enabled(False)

        # Submit background task
        self._executor.submit(self._bg_fetch_weather, city_name, my_id)

    def _bg_fetch_weather(self, city_name: str, request_id: int):
        """
        Background thread: fetch weather, then schedule GUI update.
        NEVER touches Tkinter widgets directly.
        """
        try:
            data = fetch_weather(city_name)
            self.after(0, lambda: self._on_weather_success(data, request_id))
        except WeatherServiceError as e:
            self.after(0, lambda: self._on_weather_error(str(e), request_id))
        except Exception as e:
            logger.exception("Unexpected error in background fetch")
            self.after(0, lambda: self._on_weather_error(
                "An unexpected error occurred. Please try again.", request_id
            ))

    def _on_weather_success(self, data, request_id: int):
        """Main-thread callback: render weather data if request is still current."""
        if request_id != self._request_id:
            return  # Stale response — discard

        self._search_bar.set_enabled(True)
        self._dashboard.display_weather(data)

        # Persist to database
        database.insert_search_history(
            data.city, data.country, data.latitude, data.longitude
        )
        from utils.weather_icons import get_description
        database.insert_weather_history(
            city_name=data.city,
            temperature=data.temperature,
            feels_like=data.feels_like,
            humidity=data.humidity,
            wind_speed=data.wind_speed,
            pressure=data.pressure,
            weather_condition=get_description(data.weather_code),
        )
        logger.info("Weather displayed for %s", data.city)

    def _on_weather_error(self, message: str, request_id: int):
        """Main-thread callback: show error if request is still current."""
        if request_id != self._request_id:
            return

        self._search_bar.set_enabled(True)
        self._dashboard.show_error(message)
        logger.warning("Weather fetch error: %s", message)

    # -----------------------------------------------------------------------
    # Favorites
    # -----------------------------------------------------------------------

    def add_to_favorites(self, data):
        """Add currently displayed city to favorites."""
        from database import database as db
        inserted = db.insert_favorite_city(
            data.city, data.country, data.latitude, data.longitude
        )
        if inserted:
            logger.info("Added '%s' to favorites.", data.city)
        else:
            logger.info("'%s' is already in favorites.", data.city)

    # -----------------------------------------------------------------------
    # Settings application
    # -----------------------------------------------------------------------

    def apply_settings(self, theme: str, temp_unit: str, wind_unit: str):
        """
        Apply theme and unit changes immediately across all views.
        Called by SettingsView after saving.
        """
        theme_changed = theme != self._theme
        self._theme = theme
        self._temp_unit = temp_unit
        self._wind_unit = wind_unit
        self._colors = S.DARK if theme == "dark" else S.LIGHT

        if theme_changed:
            ctk.set_appearance_mode(theme)
            theme_btn_text = "☀️ Light" if theme == "dark" else "🌙 Dark"
            self._theme_btn.configure(text=theme_btn_text)
            self._apply_colors_all()

        # Update units in relevant views
        self._dashboard.update_units(temp_unit, wind_unit)
        self._history.update_units(temp_unit)

    def _toggle_theme(self):
        """Toggle between dark and light themes."""
        new_theme = "light" if self._theme == "dark" else "dark"
        self.apply_settings(new_theme, self._temp_unit, self._wind_unit)
        database.update_settings(
            temperature_unit=self._temp_unit,
            wind_unit=self._wind_unit,
            theme=new_theme,
            default_city=self._default_city,
        )

    def _apply_colors_all(self):
        """Propagate new color palette to all widgets."""
        colors = self._colors
        self.configure(fg_color=colors["bg"])
        self._sidebar.apply_colors(colors)
        self._search_bar.apply_colors(colors)
        self._dashboard.apply_colors(colors)
        self._favorites.apply_colors(colors)
        self._history.apply_colors(colors)
        self._settings_view.apply_colors(colors)

    # -----------------------------------------------------------------------
    # Cleanup
    # -----------------------------------------------------------------------

    def on_close(self):
        """Gracefully shutdown threads and close the window."""
        logger.info("Shutting down SkyView.")
        self._executor.shutdown(wait=False, cancel_futures=True)
        self.destroy()


# ===========================================================================
# Entry point
# ===========================================================================

if __name__ == "__main__":
    app = App()
    app.mainloop()
