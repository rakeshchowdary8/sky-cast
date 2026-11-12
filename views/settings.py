"""
views/settings.py — Modern application settings view.
Allows changing theme, temperature unit, wind unit, and default city.
All changes are saved to SQLite and applied immediately.
"""

import customtkinter as ctk
from config.settings import (
    FONT_TITLE, FONT_MEDIUM, FONT_BODY, FONT_SMALL,
    PAD_LG, PAD_MD, PAD_SM, PAD_XS, CARD_CORNER_RADIUS,
)
from database import database


class SettingsView(ctk.CTkFrame):
    """
    Settings view — theme, units, and default city preferences.

    Args:
        parent:  Parent widget.
        app:     App instance (for apply_theme callback).
        colors:  Current theme color dict.
        settings: Current settings dict from database.
    """

    def __init__(self, parent, app, colors: dict, settings: dict, **kwargs):
        super().__init__(parent, fg_color=colors["bg"], corner_radius=0, **kwargs)
        self.app = app
        self.colors = colors
        self._settings = settings.copy()
        self._build()

    def _build(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=PAD_LG, pady=PAD_LG)

        # Header
        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, PAD_LG))

        ctk.CTkLabel(
            header, text="⚙️  Settings",
            font=FONT_TITLE, text_color=self.colors["text"],
        ).pack(side="left")

        ctk.CTkLabel(
            header, text="Customize your SkyView experience",
            font=FONT_SMALL, text_color=self.colors["text_dim"],
        ).pack(side="left", padx=(PAD_MD, 0))

        # --- Theme ---
        self._build_section(scroll, "🎨  Appearance", [
            self._build_theme_row,
        ])

        # --- Units ---
        self._build_section(scroll, "📏  Units", [
            self._build_temp_unit_row,
            self._build_wind_unit_row,
        ])

        # --- Default City ---
        self._build_section(scroll, "🏙️  Default City", [
            self._build_default_city_row,
        ])

        # Save button
        self._save_btn = ctk.CTkButton(
            scroll, text="💾  Save Settings",
            font=FONT_MEDIUM,
            height=44,
            fg_color=self.colors["accent"],
            hover_color=self.colors.get("accent_hover", self.colors["accent"]),
            text_color="#ffffff",
            corner_radius=10,
            command=self._save_settings,
        )
        self._save_btn.pack(fill="x", pady=(PAD_LG, 0))

        # Status label
        self._status_label = ctk.CTkLabel(
            scroll, text="",
            font=FONT_SMALL, text_color=self.colors["success"],
        )
        self._status_label.pack(pady=PAD_SM)

    def _build_section(self, parent, title: str, row_builders: list):
        """Build a modern settings section card."""
        card = ctk.CTkFrame(
            parent, fg_color=self.colors["card"],
            corner_radius=CARD_CORNER_RADIUS,
            border_width=1,
            border_color=self.colors["border"],
        )
        card.pack(fill="x", pady=(0, PAD_MD))

        # Section header
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=PAD_MD, pady=(PAD_MD, PAD_SM))

        ctk.CTkLabel(
            header, text=title,
            font=FONT_MEDIUM, text_color=self.colors["text"],
        ).pack(side="left")

        # Divider
        ctk.CTkFrame(card, height=1, fg_color=self.colors["border"]).pack(
            fill="x", padx=PAD_MD
        )

        # Content area
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=PAD_MD, pady=(PAD_SM, PAD_MD))

        for builder in row_builders:
            builder(content)

    # -----------------------------------------------------------------------
    # Row builders
    # -----------------------------------------------------------------------

    def _build_theme_row(self, parent):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=PAD_SM)

        ctk.CTkLabel(
            row, text="Theme:",
            font=FONT_BODY, text_color=self.colors["text"],
        ).pack(side="left", padx=(0, PAD_MD))

        self._theme_var = ctk.StringVar(value=self._settings.get("theme", "dark").capitalize())
        theme_seg = ctk.CTkSegmentedButton(
            row,
            values=["☀️  Light", "🌙  Dark"],
            variable=self._theme_var,
            font=FONT_SMALL,
            height=36,
            selected_color=self.colors["accent"],
            selected_hover_color=self.colors.get("accent_hover", self.colors["accent"]),
            unselected_color=self.colors["border"],
            unselected_hover_color=self.colors["card_hover"],
            text_color=self.colors["text"],
            corner_radius=8,
        )
        theme_seg.pack(side="left")
        # Map display values to internal values
        self._theme_display_map = {"☀️  Light": "light", "🌙  Dark": "dark"}

    def _build_temp_unit_row(self, parent):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=PAD_SM)

        ctk.CTkLabel(
            row, text="Temperature:",
            font=FONT_BODY, text_color=self.colors["text"],
        ).pack(side="left", padx=(0, PAD_MD))

        self._temp_var = ctk.StringVar(value=self._settings.get("temperature_unit", "Celsius"))
        ctk.CTkSegmentedButton(
            row,
            values=["°C  Celsius", "°F  Fahrenheit"],
            variable=self._temp_var,
            font=FONT_SMALL,
            height=36,
            selected_color=self.colors["accent"],
            selected_hover_color=self.colors.get("accent_hover", self.colors["accent"]),
            unselected_color=self.colors["border"],
            unselected_hover_color=self.colors["card_hover"],
            text_color=self.colors["text"],
            corner_radius=8,
        ).pack(side="left")

    def _build_wind_unit_row(self, parent):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=PAD_SM)

        ctk.CTkLabel(
            row, text="Wind Speed:",
            font=FONT_BODY, text_color=self.colors["text"],
        ).pack(side="left", padx=(0, PAD_MD))

        self._wind_var = ctk.StringVar(value=self._settings.get("wind_unit", "km/h"))
        ctk.CTkSegmentedButton(
            row,
            values=["km/h", "mph"],
            variable=self._wind_var,
            font=FONT_SMALL,
            height=36,
            selected_color=self.colors["accent"],
            selected_hover_color=self.colors.get("accent_hover", self.colors["accent"]),
            unselected_color=self.colors["border"],
            unselected_hover_color=self.colors["card_hover"],
            text_color=self.colors["text"],
            corner_radius=8,
        ).pack(side="left")

    def _build_default_city_row(self, parent):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=PAD_SM)

        ctk.CTkLabel(
            row, text="Default City:",
            font=FONT_BODY, text_color=self.colors["text"],
        ).pack(side="left", padx=(0, PAD_MD))

        self._default_city_entry = ctk.CTkEntry(
            row,
            placeholder_text="Enter city name (e.g., New York, London, Tokyo)...",
            width=280, height=38,
            font=FONT_BODY,
            fg_color=self.colors["input_bg"],
            text_color=self.colors["text"],
            border_color=self.colors["border"],
            corner_radius=8,
        )
        default_city = self._settings.get("default_city", "")
        if default_city:
            self._default_city_entry.insert(0, default_city)
        self._default_city_entry.pack(side="left")

        # Helper text
        ctk.CTkLabel(
            parent, text="This city will be loaded automatically on startup.",
            font=FONT_SMALL, text_color=self.colors["text_dim"],
        ).pack(anchor="w", pady=(PAD_XS, 0))

    # -----------------------------------------------------------------------
    # Save
    # -----------------------------------------------------------------------

    def _save_settings(self):
        # Get values from UI (map theme display to internal)
        theme_display = self._theme_var.get()
        theme = self._theme_display_map.get(theme_display, theme_display.lower())
        temp_unit = self._temp_var.get()
        # Extract unit from display (e.g., "°C  Celsius" -> "Celsius")
        if "Celsius" in temp_unit:
            temp_unit = "Celsius"
        elif "Fahrenheit" in temp_unit:
            temp_unit = "Fahrenheit"
        wind_unit = self._wind_var.get()
        default_city = self._default_city_entry.get().strip()

        # Persist to DB
        success = database.update_settings(
            temperature_unit=temp_unit,
            wind_unit=wind_unit,
            theme=theme,
            default_city=default_city,
        )

        if success:
            self._status_label.configure(
                text="✅  Settings saved successfully!",
                text_color=self.colors["success"],
            )
            # Apply changes immediately in the app
            self.app.apply_settings(theme=theme, temp_unit=temp_unit, wind_unit=wind_unit)
        else:
            self._status_label.configure(
                text="❌  Failed to save settings.",
                text_color=self.colors["warning"],
            )

        # Clear status after 3 seconds
        self.after(3000, lambda: self._status_label.configure(text=""))

    # -----------------------------------------------------------------------
    # Public interface
    # -----------------------------------------------------------------------

    def on_show(self):
        """Refresh settings from DB when view is activated."""
        self._settings = database.get_settings()
        # Sync UI controls
        theme = self._settings.get("theme", "dark")
        self._theme_var.set("🌙  Dark" if theme == "dark" else "☀️  Light")
        self._temp_var.set("°C  Celsius" if self._settings.get("temperature_unit") == "Celsius" else "°F  Fahrenheit")
        self._wind_var.set(self._settings.get("wind_unit", "km/h"))
        city = self._settings.get("default_city", "")
        self._default_city_entry.delete(0, "end")
        if city:
            self._default_city_entry.insert(0, city)
        self._status_label.configure(text="")

    def apply_colors(self, colors: dict):
        self.colors = colors
        self.configure(fg_color=colors["bg"])
        # Rebuild to apply new colors
        for w in self.winfo_children():
            w.destroy()
        self._build()