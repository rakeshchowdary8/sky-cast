"""
views/dashboard.py — Main dashboard view.

Shows current weather, info cards, hourly/daily forecasts, and Matplotlib chart.
All data display is driven by WeatherData objects passed from App.
"""

import customtkinter as ctk
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for embedding in Tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker

from config.settings import (
    FONT_HERO, FONT_TITLE, FONT_LARGE, FONT_MEDIUM, FONT_BODY,
    FONT_SMALL, FONT_LABEL, PAD_MD, PAD_SM, PAD_LG, PAD_XL,
    CARD_CORNER_RADIUS,
)
from components.weather_card import WeatherCard
from components.forecast_card import HourlyCard, DailyCard
from models.weather import WeatherData
from utils.weather_icons import get_weather_info, get_emoji
from utils.helpers import (
    format_temperature, format_wind_speed, format_pressure,
    format_visibility, format_humidity, format_uv_index,
    format_hour, format_date, format_time, now_local_str,
    degrees_to_cardinal,
)


class DashboardView(ctk.CTkFrame):
    """
    Dashboard view — the main screen shown after a weather search.

    Args:
        parent:        Parent widget (the content frame in App).
        app:           Reference to the App instance (for callbacks).
        colors:        Current theme color dict.
        temp_unit:     'Celsius' or 'Fahrenheit'.
        wind_unit:     'km/h' or 'mph'.
    """

    def __init__(self, parent, app, colors: dict,
                 temp_unit: str = "Celsius", wind_unit: str = "km/h", **kwargs):
        super().__init__(parent, fg_color=colors["bg"], corner_radius=0, **kwargs)
        self.app = app
        self.colors = colors
        self.temp_unit = temp_unit
        self.wind_unit = wind_unit
        self._current_data: WeatherData | None = None
        self._chart_canvas = None
        self._chart_fig = None

        self._build_layout()

    # -----------------------------------------------------------------------
    # Layout construction
    # -----------------------------------------------------------------------

    def _build_layout(self):
        """Build the scrollable dashboard layout."""
        # Outer scrollable container
        self._scroll = ctk.CTkScrollableFrame(
            self, fg_color=self.colors["bg"], corner_radius=0
        )
        self._scroll.pack(fill="both", expand=True, padx=0, pady=0)

        self._build_welcome_banner()

    def _build_welcome_banner(self):
        """Welcome placeholder shown before first search."""
        self._welcome = ctk.CTkFrame(
            self._scroll, fg_color=self.colors["card"],
            corner_radius=CARD_CORNER_RADIUS
        )
        self._welcome.pack(fill="x", padx=PAD_LG, pady=PAD_XL)

        ctk.CTkLabel(
            self._welcome, text="🌤️",
            font=("Segoe UI Emoji", 64),
        ).pack(pady=(PAD_XL, PAD_SM))

        ctk.CTkLabel(
            self._welcome, text="Welcome to SkyView",
            font=FONT_TITLE,
            text_color=self.colors["text"],
        ).pack()

        ctk.CTkLabel(
            self._welcome,
            text="Search for a city above to see real-time weather.",
            font=FONT_BODY,
            text_color=self.colors["text_dim"],
        ).pack(pady=(PAD_SM, PAD_XL))

    # -----------------------------------------------------------------------
    # Public interface — called by App
    # -----------------------------------------------------------------------

    def show_loading(self):
        """Show a loading indicator and disable interactivity."""
        self._clear_weather_widgets()
        if hasattr(self, "_welcome"):
            self._welcome.destroy()

        self._loading_frame = ctk.CTkFrame(
            self._scroll, fg_color=self.colors["card"],
            corner_radius=CARD_CORNER_RADIUS
        )
        self._loading_frame.pack(fill="x", padx=PAD_LG, pady=PAD_XL)

        ctk.CTkLabel(
            self._loading_frame,
            text="⏳  Fetching weather data...",
            font=FONT_LARGE,
            text_color=self.colors["text"],
        ).pack(pady=PAD_XL)

    def show_error(self, message: str):
        """Display an error message."""
        self._clear_weather_widgets()

        self._error_frame = ctk.CTkFrame(
            self._scroll, fg_color=self.colors["card"],
            corner_radius=CARD_CORNER_RADIUS
        )
        self._error_frame.pack(fill="x", padx=PAD_LG, pady=PAD_XL)

        ctk.CTkLabel(
            self._error_frame, text="⚠️",
            font=("Segoe UI Emoji", 48),
        ).pack(pady=(PAD_XL, PAD_SM))

        ctk.CTkLabel(
            self._error_frame, text=message,
            font=FONT_BODY,
            text_color=self.colors["warning"],
            wraplength=600,
        ).pack(pady=(0, PAD_XL))

    def display_weather(self, data: WeatherData):
        """Render all weather sections from a WeatherData object."""
        self._current_data = data
        self._clear_weather_widgets()

        self._build_current_section(data)
        self._build_info_cards(data)
        self._build_hourly_forecast(data)
        self._build_daily_forecast(data)
        self._build_chart(data)

    def on_show(self):
        """Called when this view is navigated to."""
        pass  # Nothing to refresh — data already set

    # -----------------------------------------------------------------------
    # Section builders
    # -----------------------------------------------------------------------

    def _build_current_section(self, data: WeatherData):
        """City name, date/time, temperature, condition."""
        frame = ctk.CTkFrame(
            self._scroll, fg_color=self.colors["card"],
            corner_radius=CARD_CORNER_RADIUS
        )
        frame.pack(fill="x", padx=PAD_LG, pady=(PAD_LG, PAD_SM))
        self._weather_widgets.append(frame)

        # Top row: city + favorite button
        top_row = ctk.CTkFrame(frame, fg_color="transparent")
        top_row.pack(fill="x", padx=PAD_LG, pady=(PAD_LG, 0))

        city_text = f"{data.city}, {data.country}" if data.country else data.city
        ctk.CTkLabel(
            top_row, text=city_text,
            font=FONT_TITLE, text_color=self.colors["text"],
        ).pack(side="left")

        ctk.CTkButton(
            top_row, text="⭐ Add to Favorites",
            font=FONT_SMALL,
            fg_color=self.colors["accent"],
            hover_color=self.colors.get("accent_hover", self.colors["accent"]),
            text_color="#ffffff",
            width=160, height=32,
            corner_radius=8,
            command=lambda: self.app.add_to_favorites(data),
        ).pack(side="right")

        # Date and time
        ctk.CTkLabel(
            frame, text=now_local_str(),
            font=FONT_SMALL, text_color=self.colors["text_dim"],
        ).pack(anchor="w", padx=PAD_LG, pady=(PAD_SM // 2, 0))

        # Main weather display row
        main_row = ctk.CTkFrame(frame, fg_color="transparent")
        main_row.pack(fill="x", padx=PAD_LG, pady=PAD_SM)

        # Temperature
        temp_str = format_temperature(data.temperature, self.temp_unit)
        ctk.CTkLabel(
            main_row, text=temp_str,
            font=FONT_HERO, text_color=self.colors["text"],
        ).pack(side="left")

        # Condition details
        desc, emoji = get_weather_info(data.weather_code, data.is_day)
        detail_col = ctk.CTkFrame(main_row, fg_color="transparent")
        detail_col.pack(side="left", padx=PAD_XL)

        ctk.CTkLabel(
            detail_col, text=emoji,
            font=("Segoe UI Emoji", 52),
        ).pack(anchor="w")

        ctk.CTkLabel(
            detail_col, text=desc,
            font=FONT_LARGE, text_color=self.colors["text"],
        ).pack(anchor="w")

        feels = format_temperature(data.feels_like, self.temp_unit)
        ctk.CTkLabel(
            detail_col,
            text=f"Feels like {feels}",
            font=FONT_BODY, text_color=self.colors["text_dim"],
        ).pack(anchor="w")

        # Sunrise / sunset if daily data available
        if data.daily:
            today = data.daily[0]
            sun_text = (
                f"🌅 Sunrise {format_time(today.sunrise)}    "
                f"🌇 Sunset {format_time(today.sunset)}"
            )
            ctk.CTkLabel(
                frame, text=sun_text,
                font=FONT_SMALL, text_color=self.colors["text_dim"],
            ).pack(anchor="w", padx=PAD_LG, pady=(0, PAD_LG))

    def _build_info_cards(self, data: WeatherData):
        """Row of weather metric cards."""
        frame = ctk.CTkFrame(self._scroll, fg_color="transparent")
        frame.pack(fill="x", padx=PAD_LG, pady=PAD_SM)
        self._weather_widgets.append(frame)

        # Determine UV index (from daily[0] if available)
        uv_val = data.daily[0].uv_index_max if data.daily else 0.0

        metrics = [
            ("💧", "Humidity",    format_humidity(data.humidity), self.colors["success"]),
            ("💨", "Wind",        f"{format_wind_speed(data.wind_speed, self.wind_unit)} {degrees_to_cardinal(data.wind_direction)}", self.colors["accent"]),
            ("🌡️", "Pressure",   format_pressure(data.pressure), self.colors["warning"]),
            ("👁️", "Visibility", format_visibility(data.visibility), self.colors["accent"]),
            ("☀️", "UV Index",   format_uv_index(uv_val), self.colors["warning"]),
        ]

        for col_idx, (icon, label, value, accent) in enumerate(metrics):
            card = WeatherCard(
                frame, self.colors, icon=icon, label=label, value=value, accent_color=accent
            )
            card.grid(row=0, column=col_idx, padx=PAD_SM, pady=0, sticky="nsew")
            frame.columnconfigure(col_idx, weight=1)

    def _build_hourly_forecast(self, data: WeatherData):
        """Horizontal strip of hourly forecast cards."""
        if not data.hourly:
            return

        section = ctk.CTkFrame(self._scroll, fg_color="transparent")
        section.pack(fill="x", padx=PAD_LG, pady=(PAD_SM, 0))
        self._weather_widgets.append(section)

        ctk.CTkLabel(
            section, text="Hourly Forecast",
            font=FONT_MEDIUM, text_color=self.colors["text"],
        ).pack(anchor="w", pady=(0, PAD_SM))

        scroll_row = ctk.CTkScrollableFrame(
            section, fg_color="transparent",
            orientation="horizontal", height=120,
        )
        scroll_row.pack(fill="x")

        for hour in data.hourly:
            emoji = get_emoji(hour.weather_code, 1)
            temp = format_temperature(hour.temperature, self.temp_unit)
            HourlyCard(
                scroll_row, self.colors,
                time_label=format_hour(hour.time),
                emoji=emoji,
                temperature=temp,
                precip=str(hour.precip_probability),
            ).pack(side="left", padx=PAD_SM // 2)

    def _build_daily_forecast(self, data: WeatherData):
        """Row of daily forecast cards."""
        if not data.daily:
            return

        section = ctk.CTkFrame(self._scroll, fg_color="transparent")
        section.pack(fill="x", padx=PAD_LG, pady=(PAD_SM, 0))
        self._weather_widgets.append(section)

        ctk.CTkLabel(
            section, text="7-Day Forecast",
            font=FONT_MEDIUM, text_color=self.colors["text"],
        ).pack(anchor="w", pady=(0, PAD_SM))

        cards_row = ctk.CTkFrame(section, fg_color="transparent")
        cards_row.pack(fill="x")

        for i, day in enumerate(data.daily):
            emoji = get_emoji(day.weather_code, 1)
            date_lbl = "Today" if i == 0 else format_date(day.date)
            DailyCard(
                cards_row, self.colors,
                date_label=date_lbl,
                emoji=emoji,
                temp_max=format_temperature(day.temp_max, self.temp_unit),
                temp_min=format_temperature(day.temp_min, self.temp_unit),
            ).grid(row=0, column=i, padx=PAD_SM // 2, sticky="nsew")
            cards_row.columnconfigure(i, weight=1)

    def _build_chart(self, data: WeatherData):
        """Embed a Matplotlib temperature chart."""
        if not data.hourly:
            return

        section = ctk.CTkFrame(self._scroll, fg_color="transparent")
        section.pack(fill="x", padx=PAD_LG, pady=(PAD_SM, PAD_LG))
        self._weather_widgets.append(section)

        ctk.CTkLabel(
            section, text="Temperature Today",
            font=FONT_MEDIUM, text_color=self.colors["text"],
        ).pack(anchor="w", pady=(0, PAD_SM))

        chart_frame = ctk.CTkFrame(
            section, fg_color=self.colors["chart_bg"],
            corner_radius=CARD_CORNER_RADIUS,
        )
        chart_frame.pack(fill="x")

        # Collect chart data
        hours = [format_hour(h.time) for h in data.hourly]
        temps = [h.temperature for h in data.hourly]

        bg = self.colors["chart_bg"]
        line_color = self.colors["chart_line"]
        text_color = self.colors["text"]
        text_dim = self.colors["text_dim"]

        # Create figure
        fig, ax = plt.subplots(figsize=(10, 2.8))
        fig.patch.set_facecolor(bg)
        ax.set_facecolor(bg)

        # Plot line + fill
        ax.plot(hours, temps, color=line_color, linewidth=2, zorder=3)
        ax.fill_between(hours, temps,
                         min(temps) - 2,
                         alpha=0.25, color=line_color)

        # Style
        ax.set_xlabel("Hour", color=text_dim, fontsize=8)
        ax.set_ylabel("°C", color=text_dim, fontsize=8)
        ax.tick_params(colors=text_dim, labelsize=7)
        for spine in ax.spines.values():
            spine.set_edgecolor(self.colors.get("border", "#444"))
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=12))

        plt.xticks(rotation=45, ha="right")
        plt.tight_layout(pad=0.5)

        # Embed in Tkinter
        if self._chart_canvas:
            self._chart_canvas.get_tk_widget().destroy()
        self._chart_canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        self._chart_canvas.draw()
        self._chart_canvas.get_tk_widget().pack(fill="x", padx=PAD_SM, pady=PAD_SM)
        self._chart_fig = fig
        plt.close(fig)

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    def _clear_weather_widgets(self):
        """Remove all previously built weather sections."""
        if not hasattr(self, "_weather_widgets"):
            self._weather_widgets = []
        for widget in self._weather_widgets:
            widget.destroy()
        self._weather_widgets = []
        # Also destroy loading/error frames if present
        for attr in ("_loading_frame", "_error_frame", "_welcome"):
            if hasattr(self, attr):
                try:
                    getattr(self, attr).destroy()
                except Exception:
                    pass

    def apply_colors(self, colors: dict):
        """Re-apply theme colors."""
        self.colors = colors
        self.configure(fg_color=colors["bg"])
        self._scroll.configure(fg_color=colors["bg"])
        if self._current_data:
            self.display_weather(self._current_data)

    def update_units(self, temp_unit: str, wind_unit: str):
        """Re-render with new unit preferences."""
        self.temp_unit = temp_unit
        self.wind_unit = wind_unit
        if self._current_data:
            self.display_weather(self._current_data)

