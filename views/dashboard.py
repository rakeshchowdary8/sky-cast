"""
views/dashboard.py — Premium SkyCast main dashboard view (shadcn-inspired).

Layout:
- Header: Location, date, search bar, refresh/favorite buttons
- Hero: Large temperature, condition, large weather illustration
- Detail Cards: 6 metric cards (humidity, wind, pressure, visibility, UV, cloud)
- Hourly Forecast: Horizontal scrollable strip with current hour highlight
- Daily Forecast: 5-day forecast cards
- Sunrise/Sunset & Atmospheric Conditions
- Weather Alerts (if any)
- Temperature Chart (24h) with gradient fill
"""

import customtkinter as ctk
from config.settings import (
    FONT_BODY, FONT_LABEL, FONT_MEDIUM, FONT_LARGE, FONT_TITLE,
    FONT_DISPLAY, FONT_HERO, FONT_HERO_SM, FONT_SMALL, FONT_TINY,
    SPACE_1, SPACE_2, SPACE_3, SPACE_4, SPACE_6, SPACE_8,
    CARD_CORNER_RADIUS, BUTTON_CORNER_RADIUS, INPUT_CORNER_RADIUS,
    BADGE_CORNER_RADIUS, RADIUS_MD, RADIUS_LG,
    METRIC_ACCENTS, STATUS_COLORS,
    ANIM_FAST, ANIM_NORMAL, ANIM_SLOW,
    ease_out_cubic,
)
from components.forecast_card import HourlyCard, DailyCard
from components.detail_card import DetailCard
from components.search_bar import SearchBar
from components.base import Card, Button, Badge, Separator
from utils.helpers import format_temperature, format_wind_speed, format_pressure, format_visibility
from utils.weather_icons import get_emoji as get_weather_emoji, get_description as get_weather_description
from utils.animations import (
    animate_color_transition, stagger_animate_children, ease_out_cubic,
    fade_in, slide_in_from_left, scale_in
)
import tkinter as tk
from datetime import datetime


class DashboardView(ctk.CTkFrame):
    """
    Premium main dashboard view with modern shadcn-inspired layout.

    Args:
        parent: Parent widget.
        colors: Current theme color dict.
        settings: Current settings dict.
        on_city_search: Callback(city_name: str) for search.
        on_refresh: Callback() for manual refresh.
        on_add_favorite: Callback() to add current city to favorites.
    """

    def __init__(self, parent, colors: dict, settings: dict,
                 on_city_search, on_refresh, on_add_favorite, on_toggle_theme=None, **kwargs):
        super().__init__(parent, fg_color=colors["bg"], corner_radius=0, **kwargs)
        self.colors = colors
        self.settings = settings
        self.on_city_search = on_city_search
        self.on_refresh = on_refresh
        self.on_add_favorite = on_add_favorite
        self.on_toggle_theme = on_toggle_theme

        # Weather data
        self._weather_data = None
        self._city_name = ""
        self._country = ""

        # UI components
        self._hourly_cards = []
        self._daily_cards = []
        self._detail_cards = {}
        self._chart_canvas = None
        self._search_bar = None

        self._build()

    def _build(self):
        # Main scrollable container
        self._scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=self.colors["scrollbar"],
            scrollbar_button_hover_color=self.colors["scrollbar_hover"],
        )
        self._scroll.pack(fill="both", expand=True)

        # Enable trackpad/mouse wheel scrolling on Windows (improved for trackpads)
        self._setup_scroll_bindings(self._scroll)

        # Content frame
        content = ctk.CTkFrame(self._scroll, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=SPACE_8, pady=SPACE_6)

        # ============================================================
        # HEADER SECTION
        # ============================================================
        self._build_header(content)

        # ============================================================
        # HERO SECTION - Current Weather
        # ============================================================
        self._build_hero(content)

        # ============================================================
        # DETAIL CARDS - 6 Metrics
        # ============================================================
        self._build_detail_cards(content)

        # ============================================================
        # HOURLY FORECAST
        # ============================================================
        self._build_hourly_section(content)

        # ============================================================
        # DAILY FORECAST (5-day)
        # ============================================================
        self._build_daily_section(content)

        # ============================================================
        # SUNRISE/SUNSET & ATMOSPHERIC
        # ============================================================
        self._build_sun_atmospheric(content)

        # ============================================================
        # WEATHER ALERTS
        # ============================================================
        self._build_alerts_section(content)

        # ============================================================
        # TEMPERATURE CHART (24h)
        # ============================================================
        self._build_chart_section(content)

        # Store section frames for animation
        self._section_frames = [
            self._hero_frame,
            self._detail_section,
            self._hourly_section,
            self._daily_section,
            self._sun_atmos_section,
            self._chart_section,
        ]

        # Initially show empty state
        self._show_empty_state()

    # -------------------------------------------------------------------------
    # Header
    # -------------------------------------------------------------------------
    def _build_header(self, parent):
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, SPACE_8))
        header.columnconfigure(1, weight=1)

        # Location and date (left)
        left = ctk.CTkFrame(header, fg_color="transparent")
        left.grid(row=0, column=0, sticky="w")

        self._location_label = ctk.CTkLabel(
            left,
            text="",
            font=FONT_DISPLAY,
            text_color=self.colors["text"],
        )
        self._location_label.pack(anchor="w")

        self._date_label = ctk.CTkLabel(
            left,
            text="",
            font=FONT_BODY,
            text_color=self.colors["text_secondary"],
        )
        self._date_label.pack(anchor="w", pady=(SPACE_1, 0))

        # Search bar (center) - using new SearchBar component
        self._search_bar = SearchBar(
            header,
            on_search=self.on_city_search,
            colors=self.colors,
            placeholder="Search city...",
        )
        self._search_bar.grid(row=0, column=1, sticky="ew", padx=SPACE_8)

        # Right side - theme toggle and favorite buttons using new Button component
        right = ctk.CTkFrame(header, fg_color="transparent")
        right.grid(row=0, column=2, sticky="e")

        # Theme toggle button in header (replaces sidebar theme toggle)
        theme_icon = "☀️" if self.settings.get("theme", "dark") == "dark" else "🌙"
        self._theme_btn = Button(
            right,
            text=theme_icon,
            variant="ghost",
            size="icon",
            colors=self.colors,
            command=self.on_toggle_theme,
        )
        self._theme_btn.pack(side="right", padx=(SPACE_2, 0))

        self._favorite_btn = Button(
            right,
            text="☆ Add to Favorites",
            variant="default",
            size="default",
            colors=self.colors,
            command=self._on_add_favorite,
        )
        self._favorite_btn.pack(side="right")

    # -------------------------------------------------------------------------
    # Hero Section
    # -------------------------------------------------------------------------
    def _build_hero(self, parent):
        # Use Card component for hero
        self._hero_frame = Card(
            parent,
            variant="default",
            padding=SPACE_8,
            colors=self.colors,
        )
        self._hero_frame.pack(fill="x", pady=(0, SPACE_8))

        # Content with padding
        hero_content = ctk.CTkFrame(self._hero_frame.content, fg_color="transparent")
        hero_content.pack(fill="both", expand=True)

        # Left: Temperature and condition
        left = ctk.CTkFrame(hero_content, fg_color="transparent")
        left.pack(side="left", fill="y", anchor="center")

        # Temperature
        self._temp_label = ctk.CTkLabel(
            left,
            text="--°",
            font=FONT_HERO,
            text_color=self.colors["text"],
        )
        self._temp_label.pack(anchor="w")

        # Condition
        self._condition_label = ctk.CTkLabel(
            left,
            text="",
            font=FONT_LARGE,
            text_color=self.colors["text_secondary"],
        )
        self._condition_label.pack(anchor="w", pady=(SPACE_2, 0))

        # Feels like / Min-Max
        self._feels_label = ctk.CTkLabel(
            left,
            text="",
            font=FONT_BODY,
            text_color=self.colors["text_dim"],
        )
        self._feels_label.pack(anchor="w", pady=(SPACE_2, 0))

        # Right: Large weather illustration
        right = ctk.CTkFrame(hero_content, fg_color="transparent")
        right.pack(side="right", fill="y", anchor="center", padx=(SPACE_8, 0))

        self._weather_icon_label = ctk.CTkLabel(
            right,
            text="☁️",
            font=("Segoe UI Emoji", 140),
        )
        self._weather_icon_label.pack(anchor="e")

    # -------------------------------------------------------------------------
    # Detail Cards (6 metrics)
    # -------------------------------------------------------------------------
    def _build_detail_cards(self, parent):
        # Section container - groups header + cards together
        self._detail_section = ctk.CTkFrame(parent, fg_color="transparent")
        self._detail_section.pack(fill="x", pady=(0, SPACE_8))

        # Section header
        header = ctk.CTkFrame(self._detail_section, fg_color="transparent")
        header.pack(fill="x", pady=(0, SPACE_4))

        ctk.CTkLabel(
            header,
            text="Weather Details",
            font=FONT_TITLE,
            text_color=self.colors["text"],
        ).pack(side="left")

        # Cards container - grid layout
        self._detail_container = ctk.CTkFrame(self._detail_section, fg_color="transparent")
        self._detail_container.pack(fill="x")

        # Configure 3 columns
        for i in range(3):
            self._detail_container.grid_columnconfigure(i, weight=1)

        # Create 6 detail cards using DetailCard component
        detail_configs = [
            (0, "Humidity", "--", "%", "💧", "humidity"),
            (1, "Wind", "--", "km/h", "💨", "wind"),
            (2, "Pressure", "--", "hPa", "📊", "pressure"),
            (3, "Visibility", "--", "km", "👁️", "visibility"),
            (4, "UV Index", "--", "", "☀️", "uv_index"),
            (5, "Cloud Cover", "--", "%", "☁️", "cloud_cover"),
        ]

        for idx, title, value, unit, icon, accent_key in detail_configs:
            row = idx // 3
            col = idx % 3

            card = DetailCard(
                self._detail_container,
                title=title,
                value=value,
                unit=unit,
                icon=icon,
                accent_key=accent_key,
                colors=self.colors,
            )
            card.grid(row=row, column=col, padx=SPACE_2, pady=SPACE_2, sticky="nsew")
            self._detail_cards[idx] = card

    # -------------------------------------------------------------------------
    # Hourly Forecast Section
    # -------------------------------------------------------------------------
    def _build_hourly_section(self, parent):
        # Section container - groups header + cards together
        self._hourly_section = ctk.CTkFrame(parent, fg_color="transparent")
        self._hourly_section.pack(fill="x", pady=(0, SPACE_8))

        # Section header
        header = ctk.CTkFrame(self._hourly_section, fg_color="transparent")
        header.pack(fill="x", pady=(0, SPACE_4))

        ctk.CTkLabel(
            header,
            text="Hourly Forecast",
            font=FONT_TITLE,
            text_color=self.colors["text"],
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text="Next 24 hours",
            font=FONT_SMALL,
            text_color=self.colors["text_dim"],
        ).pack(side="left", padx=(SPACE_3, 0), anchor="s")

        # Horizontal scrollable container
        self._hourly_scroll = ctk.CTkScrollableFrame(
            self._hourly_section,
            fg_color="transparent",
            orientation="horizontal",
            height=170,
            scrollbar_button_color=self.colors["scrollbar"],
            scrollbar_button_hover_color=self.colors["scrollbar_hover"],
        )
        self._hourly_scroll.pack(fill="x")

        # Enable trackpad/mouse wheel horizontal scrolling (improved)
        self._setup_scroll_bindings(self._hourly_scroll, horizontal=True)

        # Inner frame for cards
        self._hourly_inner = ctk.CTkFrame(self._hourly_scroll, fg_color="transparent")
        self._hourly_inner.pack(fill="both", expand=True)

    # -------------------------------------------------------------------------
    # Daily Forecast Section
    # -------------------------------------------------------------------------
    def _build_daily_section(self, parent):
        # Section container - groups header + cards together
        self._daily_section = ctk.CTkFrame(parent, fg_color="transparent")
        self._daily_section.pack(fill="x", pady=(0, SPACE_8))

        # Section header
        header = ctk.CTkFrame(self._daily_section, fg_color="transparent")
        header.pack(fill="x", pady=(0, SPACE_4))

        ctk.CTkLabel(
            header,
            text="5-Day Forecast",
            font=FONT_TITLE,
            text_color=self.colors["text"],
        ).pack(side="left")

        # Cards container (horizontal scroll)
        self._daily_scroll = ctk.CTkScrollableFrame(
            self._daily_section,
            fg_color="transparent",
            orientation="horizontal",
            height=210,
            scrollbar_button_color=self.colors["scrollbar"],
            scrollbar_button_hover_color=self.colors["scrollbar_hover"],
        )
        self._daily_scroll.pack(fill="x")

        # Enable trackpad/mouse wheel horizontal scrolling (improved)
        self._setup_scroll_bindings(self._daily_scroll, horizontal=True)

        self._daily_inner = ctk.CTkFrame(self._daily_scroll, fg_color="transparent")
        self._daily_inner.pack(fill="both", expand=True)

    # -------------------------------------------------------------------------
    # Sunrise/Sunset & Atmospheric
    # -------------------------------------------------------------------------
    def _build_sun_atmospheric(self, parent):
        # Section container - groups header + cards together
        self._sun_atmos_section = ctk.CTkFrame(parent, fg_color="transparent")
        self._sun_atmos_section.pack(fill="x", pady=(0, SPACE_8))

        # Section header
        header = ctk.CTkFrame(self._sun_atmos_section, fg_color="transparent")
        header.pack(fill="x", pady=(0, SPACE_4))

        ctk.CTkLabel(
            header,
            text="Sun & Atmosphere",
            font=FONT_TITLE,
            text_color=self.colors["text"],
        ).pack(side="left")

        # Container for two cards side by side using Card components
        self._sun_atmos_container = ctk.CTkFrame(self._sun_atmos_section, fg_color="transparent")
        self._sun_atmos_container.pack(fill="x")
        self._sun_atmos_container.grid_columnconfigure(0, weight=1)
        self._sun_atmos_container.grid_columnconfigure(1, weight=1)

        # Sunrise/Sunset Card
        self._sun_card = Card(
            self._sun_atmos_container,
            variant="default",
            padding=SPACE_6,
            colors=self.colors,
        )
        self._sun_card.grid(row=0, column=0, padx=(0, SPACE_2), sticky="nsew")

        sun_content = self._sun_card.content

        # Title with icon
        ctk.CTkLabel(
            sun_content,
            text="☀️  Sunrise / Sunset",
            font=FONT_MEDIUM,
            text_color=self.colors["text"],
        ).pack(anchor="w", pady=(0, SPACE_4))

        self._sunrise_label = ctk.CTkLabel(
            sun_content,
            text="Sunrise: --:--",
            font=FONT_BODY,
            text_color=self.colors["text_secondary"],
        )
        self._sunrise_label.pack(anchor="w", pady=SPACE_1)

        self._sunset_label = ctk.CTkLabel(
            sun_content,
            text="Sunset: --:--",
            font=FONT_BODY,
            text_color=self.colors["text_secondary"],
        )
        self._sunset_label.pack(anchor="w", pady=SPACE_1)

        self._daylight_label = ctk.CTkLabel(
            sun_content,
            text="Daylight: --h --m",
            font=FONT_SMALL,
            text_color=self.colors["text_dim"],
        )
        self._daylight_label.pack(anchor="w", pady=(SPACE_3, 0))

        # Atmospheric Card
        self._atmos_card = Card(
            self._sun_atmos_container,
            variant="default",
            padding=SPACE_6,
            colors=self.colors,
        )
        self._atmos_card.grid(row=0, column=1, padx=(SPACE_2, 0), sticky="nsew")

        atmos_content = self._atmos_card.content

        ctk.CTkLabel(
            atmos_content,
            text="🌫️  Atmospheric Conditions",
            font=FONT_MEDIUM,
            text_color=self.colors["text"],
        ).pack(anchor="w", pady=(0, SPACE_4))

        self._cloud_label = ctk.CTkLabel(
            atmos_content,
            text="Cloud Cover: --%",
            font=FONT_BODY,
            text_color=self.colors["text_secondary"],
        )
        self._cloud_label.pack(anchor="w", pady=SPACE_1)

        self._visibility_label = ctk.CTkLabel(
            atmos_content,
            text="Visibility: -- km",
            font=FONT_BODY,
            text_color=self.colors["text_secondary"],
        )
        self._visibility_label.pack(anchor="w", pady=SPACE_1)

        self._pressure_label = ctk.CTkLabel(
            atmos_content,
            text="Pressure: -- hPa",
            font=FONT_BODY,
            text_color=self.colors["text_secondary"],
        )
        self._pressure_label.pack(anchor="w", pady=SPACE_1)

    # -------------------------------------------------------------------------
    # Weather Alerts Section
    # -------------------------------------------------------------------------
    def _build_alerts_section(self, parent):
        self._alerts_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self._alerts_frame.pack(fill="x", pady=(0, SPACE_8))

        # Initially hidden
        self._alerts_frame.pack_forget()

        # Use Card with destructive variant colors for alerts
        self._alerts_card = Card(
            self._alerts_frame,
            variant="outlined",
            padding=SPACE_6,
            colors=self.colors,
        )
        # Override border color for alerts
        self._alerts_card.configure(
            border_color=self.colors["destructive"],
            fg_color=self.colors["destructive_light"],
        )
        self._alerts_card.pack(fill="x")

        alerts_content = self._alerts_card.content

        alert_header = ctk.CTkFrame(alerts_content, fg_color="transparent")
        alert_header.pack(fill="x", pady=(0, SPACE_2))

        ctk.CTkLabel(
            alert_header,
            text="⚠️  Weather Alert",
            font=FONT_MEDIUM,
            text_color=self.colors["destructive"],
        ).pack(side="left")

        self._alert_text = ctk.CTkLabel(
            alerts_content,
            text="",
            font=FONT_BODY,
            text_color=self.colors["text"],
            wraplength=800,
            justify="left",
        )
        self._alert_text.pack(anchor="w")

    # -------------------------------------------------------------------------
    # Chart Section
    # -------------------------------------------------------------------------
    def _build_chart_section(self, parent):
        # Section container - groups header + chart together
        self._chart_section = ctk.CTkFrame(parent, fg_color="transparent")
        self._chart_section.pack(fill="x", pady=(0, SPACE_8))

        # Section header
        header = ctk.CTkFrame(self._chart_section, fg_color="transparent")
        header.pack(fill="x", pady=(0, SPACE_4))

        ctk.CTkLabel(
            header,
            text="Temperature Trend (24h)",
            font=FONT_TITLE,
            text_color=self.colors["text"],
        ).pack(side="left")

        # Chart container using Card
        self._chart_frame = Card(
            self._chart_section,
            variant="default",
            padding=SPACE_4,
            colors=self.colors,
        )
        self._chart_frame.pack(fill="x")
        self._chart_frame.configure(height=300)
        self._chart_frame.pack_propagate(False)

        self._chart_placeholder = ctk.CTkLabel(
            self._chart_frame.content,
            text="📊  Temperature chart will appear here",
            font=FONT_MEDIUM,
            text_color=self.colors["text_dim"],
        )
        self._chart_placeholder.pack(expand=True)

    # -------------------------------------------------------------------------
    # Empty State
    # -------------------------------------------------------------------------
    def _show_empty_state(self):
        """Show empty state when no weather data loaded."""
        self._hero_frame.pack_forget()
        self._detail_section.pack_forget()
        self._hourly_section.pack_forget()
        self._daily_section.pack_forget()
        self._sun_atmos_section.pack_forget()
        self._chart_section.pack_forget()

        # Show empty state in hero area using Card
        self._empty_frame = Card(
            self._scroll,
            variant="default",
            padding=SPACE_8,
            colors=self.colors,
        )
        self._empty_frame.pack(fill="both", expand=True, padx=SPACE_8, pady=SPACE_8)

        empty_content = self._empty_frame.content

        ctk.CTkLabel(
            empty_content,
            text="🌤️",
            font=("Segoe UI Emoji", 80),
        ).pack(pady=(SPACE_8, SPACE_6))

        ctk.CTkLabel(
            empty_content,
            text="Welcome to SkyCast",
            font=FONT_DISPLAY,
            text_color=self.colors["text"],
        ).pack()

        ctk.CTkLabel(
            empty_content,
            text="Search for a city to see premium weather details",
            font=FONT_BODY,
            text_color=self.colors["text_secondary"],
        ).pack(pady=(SPACE_2, SPACE_6))

        Button(
            empty_content,
            text="Search City",
            variant="default",
            size="lg",
            colors=self.colors,
            command=lambda: self.on_city_search(""),
        ).pack()

    def _hide_empty_state(self):
        """Hide empty state and show weather content."""
        if hasattr(self, '_empty_frame'):
            self._empty_frame.destroy()

        # All sections were created in _build() - just repack them in order
        self._hero_frame.pack(fill="x", pady=(0, SPACE_8))
        self._detail_section.pack(fill="x", pady=(0, SPACE_8))
        self._hourly_section.pack(fill="x", pady=(0, SPACE_8))
        self._daily_section.pack(fill="x", pady=(0, SPACE_8))
        self._sun_atmos_section.pack(fill="x", pady=(0, SPACE_8))
        self._chart_section.pack(fill="x", pady=(0, SPACE_8))

        # Trigger staggered entrance animations for sections
        self._animate_sections_entrance()

    def _setup_scroll_bindings(self, scroll_frame, horizontal=False):
        """Setup improved mouse wheel/trackpad scrolling bindings for a CTkScrollableFrame.

        Handles both regular mouse wheel and trackpad two-finger scrolling on Windows.
        """
        def on_mousewheel(event):
            # Windows trackpad sends larger delta values, normalize to units
            # Standard mouse wheel delta is 120 per notch
            # Trackpad can send varying values, so we normalize
            delta = event.delta
            if delta == 0:
                return

            # Normalize delta: trackpad often sends values like 1000+ for fast scroll
            # We'll use a factor to make it feel natural
            units = -int(delta / 120)
            # Clamp to reasonable range for trackpad
            units = max(-5, min(5, units))

            if horizontal:
                scroll_frame._parent_canvas.xview_scroll(units, "units")
            else:
                scroll_frame._parent_canvas.yview_scroll(units, "units")
            return "break"  # Prevent event propagation

        def on_shift_mousewheel(event):
            # Shift+MouseWheel for horizontal scrolling
            delta = event.delta
            if delta == 0:
                return
            units = -int(delta / 120)
            units = max(-5, min(5, units))
            if horizontal:
                scroll_frame._parent_canvas.yview_scroll(units, "units")
            else:
                scroll_frame._parent_canvas.xview_scroll(units, "units")
            return "break"

        # Bind both regular and shift-modified wheel events
        scroll_frame.bind("<MouseWheel>", on_mousewheel)
        scroll_frame.bind("<Shift-MouseWheel>", on_shift_mousewheel)
        # Also bind to the inner canvas for better coverage
        if hasattr(scroll_frame, '_parent_canvas'):
            scroll_frame._parent_canvas.bind("<MouseWheel>", on_mousewheel)
            scroll_frame._parent_canvas.bind("<Shift-MouseWheel>", on_shift_mousewheel)

    def _animate_sections_entrance(self):
        """Animate dashboard sections with staggered entrance."""
        sections = [
            self._hero_frame,
            self._detail_section,
            self._hourly_section,
            self._daily_section,
            self._sun_atmos_section,
            self._chart_section,
        ]

        stagger_animate_children(
            self._scroll,
            lambda child, idx: None,  # Sections animate themselves via their own logic
            delay_per_child=60,
            start_delay=100,
        )

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------
    def display_weather(self, weather_data, city_name: str, country: str):
        """Display weather data in the dashboard."""
        self._weather_data = weather_data
        self._city_name = city_name
        self._country = country

        self._hide_empty_state()

        # Update header
        self._location_label.configure(text=f"{city_name}, {country}")
        self._date_label.configure(text=datetime.now().strftime("%A, %B %d, %Y"))

        # Update hero
        temp_unit = "°C" if self.settings.get("temperature_unit") == "Celsius" else "°F"
        temp = weather_data.current.temperature
        if self.settings.get("temperature_unit") == "Fahrenheit":
            temp = temp * 9/5 + 32
        self._temp_label.configure(text=f"{temp:.0f}{temp_unit}")

        condition = get_weather_description(weather_data.current.weather_code)
        icon = get_weather_emoji(weather_data.current.weather_code, weather_data.current.is_day)
        self._condition_label.configure(text=f"{icon}  {condition}")
        self._weather_icon_label.configure(text=icon)

        # Feels like / Min-Max
        feels = weather_data.current.feels_like
        if self.settings.get("temperature_unit") == "Fahrenheit":
            feels = feels * 9/5 + 32

        daily = weather_data.daily[0] if weather_data.daily else None
        if daily:
            high = daily.temp_max
            low = daily.temp_min
            if self.settings.get("temperature_unit") == "Fahrenheit":
                high = high * 9/5 + 32
                low = low * 9/5 + 32
            self._feels_label.configure(
                text=f"Feels like {feels:.0f}{temp_unit}  •  H {high:.0f}{temp_unit} / L {low:.0f}{temp_unit}"
            )
        else:
            self._feels_label.configure(text=f"Feels like {feels:.0f}{temp_unit}")

        # Update detail cards
        self._update_detail_cards(weather_data)

        # Update hourly forecast
        self._update_hourly_forecast(weather_data)

        # Update daily forecast
        self._update_daily_forecast(weather_data)

        # Update sun & atmospheric
        self._update_sun_atmospheric(weather_data)

        # Update chart
        self._update_chart(weather_data)

    def _update_detail_cards(self, weather_data):
        """Update the 6 detail cards with current weather data."""
        current = weather_data.current
        temp_unit = "°C" if self.settings.get("temperature_unit") == "Celsius" else "°F"
        wind_unit = self.settings.get("wind_unit", "km/h")

        # Card data: (index, title, value, unit, icon, accent_key)
        cards_data = [
            (0, "Humidity", f"{current.humidity:.0f}", "%", "💧", "humidity"),
            (1, "Wind", format_wind_speed(current.wind_speed, wind_unit), wind_unit, "💨", "wind"),
            (2, "Pressure", format_pressure(current.pressure), "hPa", "📊", "pressure"),
            (3, "Visibility", format_visibility(current.visibility), "km", "👁️", "visibility"),
            (4, "UV Index", f"{weather_data.daily[0].uv_index_max:.0f}" if weather_data.daily else "--", "", "☀️", "uv_index"),
            (5, "Cloud Cover", f"{current.cloud_cover:.0f}" if hasattr(current, 'cloud_cover') and current.cloud_cover is not None else "--", "%", "☁️", "cloud_cover"),
        ]

        for idx, title, value, unit, icon, accent_key in cards_data:
            if idx in self._detail_cards:
                card = self._detail_cards[idx]
                card.update_value(value, unit)
                # Update title and icon would need card recreation - simplified for now
                # In a full implementation, we'd store references to all labels

    def _update_hourly_forecast(self, weather_data):
        """Update hourly forecast cards with staggered animation."""
        # Clear existing
        for widget in self._hourly_inner.winfo_children():
            widget.destroy()
        self._hourly_cards = []

        if not weather_data.hourly:
            return

        # Show next 24 hours
        for i, hour in enumerate(weather_data.hourly[:24]):
            time_str = hour.time.strftime("%I %p").lstrip("0").lower()
            if i == 0:
                time_str = "Now"

            temp_unit = "°C" if self.settings.get("temperature_unit") == "Celsius" else "°F"
            temp = hour.temperature
            if self.settings.get("temperature_unit") == "Fahrenheit":
                temp = temp * 9/5 + 32

            icon = get_weather_emoji(hour.weather_code, hour.time.hour >= 6 and hour.time.hour < 18)
            is_current = (i == 0)

            card = HourlyCard(
                self._hourly_inner,
                time_str=time_str,
                temp=f"{temp:.0f}{temp_unit}",
                condition_icon=icon,
                precip_prob=hour.precip_probability,
                is_current=is_current,
                colors=self.colors,
            )
            card.pack(side="left", padx=(0, SPACE_2) if i < 23 else (0, 0))
            self._hourly_cards.append(card)

        # Stagger animate the cards
        stagger_animate_children(
            self._hourly_inner,
            lambda child, idx: None,  # Cards animate themselves
            delay_per_child=40,
            start_delay=50,
        )

    def _update_daily_forecast(self, weather_data):
        """Update daily forecast cards with staggered animation."""
        # Clear existing
        for widget in self._daily_inner.winfo_children():
            widget.destroy()
        self._daily_cards = []

        if not weather_data.daily:
            return

        for i, day in enumerate(weather_data.daily[:5]):
            date_obj = day.date
            day_str = date_obj.strftime("%a")
            date_str = date_obj.strftime("%b %d")
            is_today = (i == 0)
            if is_today:
                day_str = "Today"

            temp_unit = "°C" if self.settings.get("temperature_unit") == "Celsius" else "°F"
            high = day.temp_max
            low = day.temp_min
            if self.settings.get("temperature_unit") == "Fahrenheit":
                high = high * 9/5 + 32
                low = low * 9/5 + 32

            icon = get_weather_emoji(day.weather_code, True)

            card = DailyCard(
                self._daily_inner,
                day_str=day_str,
                date_str=date_str,
                high_temp=f"{high:.0f}{temp_unit}",
                low_temp=f"{low:.0f}{temp_unit}",
                condition_icon=icon,
                precip_prob=day.precipitation_probability_max or 0,
                uv_index=day.uv_index_max or 0,
                is_today=is_today,
                colors=self.colors,
            )
            card.pack(side="left", padx=(0, SPACE_2) if i < 4 else (0, 0))
            self._daily_cards.append(card)

        # Stagger animate the cards
        stagger_animate_children(
            self._daily_inner,
            lambda child, idx: None,
            delay_per_child=50,
            start_delay=50,
        )

    def _update_sun_atmospheric(self, weather_data):
        """Update sunrise/sunset and atmospheric conditions."""
        if not weather_data.daily:
            return

        today = weather_data.daily[0]

        # Sunrise/Sunset
        if today.sunrise and today.sunset:
            self._sunrise_label.configure(text=f"Sunrise: {today.sunrise.strftime('%I:%M %p').lstrip('0')}")
            self._sunset_label.configure(text=f"Sunset: {today.sunset.strftime('%I:%M %p').lstrip('0')}")

            # Daylight duration
            daylight_seconds = (today.sunset - today.sunrise).total_seconds()
            hours = int(daylight_seconds // 3600)
            minutes = int((daylight_seconds % 3600) // 60)
            self._daylight_label.configure(text=f"Daylight: {hours}h {minutes}m")

        # Atmospheric
        current = weather_data.current
        if hasattr(current, 'cloud_cover') and current.cloud_cover is not None:
            self._cloud_label.configure(text=f"Cloud Cover: {current.cloud_cover:.0f}%")
        self._visibility_label.configure(text=f"Visibility: {format_visibility(current.visibility)}")
        self._pressure_label.configure(text=f"Pressure: {format_pressure(current.pressure)}")

    def _update_chart(self, weather_data):
        """Update temperature chart with Matplotlib."""
        if not weather_data.hourly:
            return

        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            import numpy as np

            # Prepare data
            hours = weather_data.hourly[:24]
            times = [h.time.strftime("%H:%M") for h in hours]
            temps = [h.temperature for h in hours]
            if self.settings.get("temperature_unit") == "Fahrenheit":
                temps = [t * 9/5 + 32 for t in temps]

            # Create figure
            fig, ax = plt.subplots(figsize=(10, 3.5), facecolor=self.colors["chart_bg"])
            ax.set_facecolor(self.colors["chart_bg"])

            # Plot
            x = np.arange(len(times))
            ax.plot(x, temps, color=self.colors["chart_line"], linewidth=2.5, marker='o', markersize=4, markerfacecolor=self.colors["chart_line"])
            ax.fill_between(x, temps, alpha=0.15, color=self.colors["chart_fill"])

            # Styling
            ax.set_xticks(x[::2])
            ax.set_xticklabels([times[i] for i in range(0, len(times), 2)], color=self.colors["text_dim"], fontsize=9, fontfamily='Inter')
            ax.tick_params(axis='y', colors=self.colors["text_dim"], labelsize=9)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color(self.colors["chart_grid"])
            ax.spines['bottom'].set_color(self.colors["chart_grid"])
            ax.grid(True, alpha=0.15, color=self.colors["chart_grid"], linestyle='-', linewidth=0.5)
            ax.set_axisbelow(True)

            # Y label
            unit = "°F" if self.settings.get("temperature_unit") == "Fahrenheit" else "°C"
            ax.set_ylabel(f"Temperature ({unit})", color=self.colors["text_secondary"], fontsize=10, fontfamily='Inter', labelpad=10)

            plt.tight_layout(pad=1.5)

            # Remove placeholder
            self._chart_placeholder.pack_forget()

            # Remove old canvas
            if self._chart_canvas:
                self._chart_canvas.get_tk_widget().destroy()

            # Embed in Tkinter
            self._chart_canvas = FigureCanvasTkAgg(fig, master=self._chart_frame.content)
            self._chart_canvas.draw()
            self._chart_canvas.get_tk_widget().pack(fill="both", expand=True, padx=SPACE_4, pady=SPACE_4)

        except Exception as e:
            print(f"Chart error: {e}")
            self._chart_placeholder.configure(text="Chart unavailable")

    def show_loading(self):
        """Show loading state."""
        if self._search_bar:
            self._search_bar.set_enabled(False)
            self._search_bar.show_loading(True)

    def show_error(self, message: str):
        """Show error state."""
        if self._search_bar:
            self._search_bar.set_enabled(True)
            self._search_bar.show_loading(False)
        # Could show error in a toast or status area

    def _on_add_favorite(self):
        """Handle add to favorites click."""
        if self._city_name:
            self.on_add_favorite()

    def apply_colors(self, colors: dict):
        """Apply new theme colors."""
        self.colors = colors
        self.configure(fg_color=colors["bg"])
        self._scroll.configure(
            scrollbar_button_color=colors["scrollbar"],
            scrollbar_button_hover_color=colors["scrollbar_hover"],
        )
        # Update search bar
        if self._search_bar:
            self._search_bar.apply_colors(colors)

        # Update buttons (theme toggle and favorite)
        if self._theme_btn:
            self._theme_btn.apply_colors(colors)
            # Update theme icon
            theme_icon = "☀️" if self.settings.get("theme", "dark") == "dark" else "🌙"
            self._theme_btn.configure(text=theme_icon)
        self._favorite_btn.apply_colors(colors)

        # Update hero card
        self._hero_frame.apply_colors(colors)

        # Update detail cards
        for card in self._detail_cards.values():
            card.apply_colors(colors)

        # Update sun/atmos cards
        self._sun_card.apply_colors(colors)
        self._atmos_card.apply_colors(colors)

        # Update alerts card
        self._alerts_card.apply_colors(colors)
        self._alerts_card.configure(
            border_color=colors["destructive"],
            fg_color=colors["destructive_light"],
        )

        # Update chart card
        self._chart_frame.apply_colors(colors)

        # Update forecast cards
        for card in self._hourly_cards:
            card.apply_colors(colors)
        for card in self._daily_cards:
            card.apply_colors(colors)

        # Update text colors
        self._location_label.configure(text_color=colors["text"])
        self._date_label.configure(text_color=colors["text_secondary"])
        self._temp_label.configure(text_color=colors["text"])
        self._condition_label.configure(text_color=colors["text_secondary"])
        self._feels_label.configure(text_color=colors["text_dim"])
        self._sunrise_label.configure(text_color=colors["text_secondary"])
        self._sunset_label.configure(text_color=colors["text_secondary"])
        self._daylight_label.configure(text_color=colors["text_dim"])
        self._cloud_label.configure(text_color=colors["text_secondary"])
        self._visibility_label.configure(text_color=colors["text_secondary"])
        self._pressure_label.configure(text_color=colors["text_secondary"])
        self._alert_text.configure(text_color=colors["text"])
        self._chart_placeholder.configure(text_color=colors["text_dim"])