"""
views/settings.py — Premium application settings view (shadcn-inspired).

Allows changing theme, temperature unit, wind unit, and default city.
All changes are saved to SQLite and applied immediately.

Features:
- Clean card-based sections with Card component
- Segmented buttons with proper theme colors
- Real-time preview of changes
- Full dark/light theme consistency
- Smooth animations
"""

import customtkinter as ctk
from config.settings import (
    FONT_TITLE, FONT_MEDIUM, FONT_BODY, FONT_SMALL, FONT_LABEL, FONT_TINY,
    SPACE_1, SPACE_2, SPACE_3, SPACE_4, SPACE_6, SPACE_8,
    CARD_CORNER_RADIUS, BUTTON_CORNER_RADIUS, RADIUS_MD,
    STATUS_COLORS,
    ANIM_FAST,
)
from components.base import Card, Button
from utils.animations import animate_color_transition, ease_out_cubic
from database import database


class SettingsView(ctk.CTkFrame):
    """
    Settings view — theme, units, and default city preferences.

    Features:
    - Clean card-based sections
    - Segmented buttons with proper theme colors
    - Real-time preview of changes
    - Full dark/light theme consistency

    Args:
        parent:  Parent widget.
        app:     App instance (for apply_settings callback).
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
        scroll.pack(fill="both", expand=True, padx=SPACE_8, pady=SPACE_6)

        # Header
        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, SPACE_8))

        ctk.CTkLabel(
            header, text="⚙️  Settings",
            font=FONT_TITLE, text_color=self.colors["text"],
        ).pack(side="left")

        ctk.CTkLabel(
            header, text="Customize your SkyCast experience",
            font=FONT_SMALL, text_color=self.colors["text_dim"],
        ).pack(side="left", padx=(SPACE_3, 0))

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

        # Save button using Button component
        self._save_btn = Button(
            scroll, text="💾  Save Settings",
            variant="default",
            size="lg",
            colors=self.colors,
            command=self._save_settings,
        )
        self._save_btn.pack(fill="x", pady=(SPACE_8, 0))

        # Status label
        self._status_label = ctk.CTkLabel(
            scroll, text="",
            font=FONT_SMALL, text_color=self.colors["success"],
        )
        self._status_label.pack(pady=SPACE_2)

    def _build_section(self, parent, title: str, row_builders: list):
        """Build a modern settings section card using Card component."""
        card = Card(
            parent, variant="default",
            padding=SPACE_6,
            colors=self.colors,
        )
        card.pack(fill="x", pady=(0, SPACE_6))

        # Section header
        header = ctk.CTkFrame(card.content, fg_color="transparent")
        header.pack(fill="x", pady=(0, SPACE_4))

        ctk.CTkLabel(
            header, text=title,
            font=FONT_MEDIUM, text_color=self.colors["text"],
        ).pack(side="left")

        # Divider
        ctk.CTkFrame(card.content, height=1, fg_color=self.colors["card_border"]).pack(
            fill="x", pady=(0, SPACE_4)
        )

        # Content area
        for builder in row_builders:
            builder(card.content)

    # -----------------------------------------------------------------------
    # Row builders
    # -----------------------------------------------------------------------

    def _build_theme_row(self, parent):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=SPACE_2)

        ctk.CTkLabel(
            row, text="Theme:",
            font=FONT_BODY, text_color=self.colors["text"],
        ).pack(side="left", padx=(0, SPACE_3))

        theme = self._settings.get("theme", "dark")
        self._theme_var = ctk.StringVar(value="🌙  Dark" if theme == "dark" else "☀️  Light")

        theme_seg = ctk.CTkSegmentedButton(
            row,
            values=["☀️  Light", "🌙  Dark"],
            variable=self._theme_var,
            font=FONT_SMALL,
            height=44,
            selected_color=self.colors["primary"],
            selected_hover_color=self.colors["primary_hover"],
            unselected_color=self.colors["input_bg"],
            unselected_hover_color=self.colors["card_hover"],
            text_color=self.colors["text"],
            fg_color=self.colors["input_bg"],
            corner_radius=RADIUS_MD,
        )
        theme_seg.pack(side="left")
        # Map display values to internal values
        self._theme_display_map = {"☀️  Light": "light", "🌙  Dark": "dark"}

    def _build_temp_unit_row(self, parent):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=SPACE_2)

        ctk.CTkLabel(
            row, text="Temperature:",
            font=FONT_BODY, text_color=self.colors["text"],
        ).pack(side="left", padx=(0, SPACE_3))

        temp_unit = self._settings.get("temperature_unit", "Celsius")
        self._temp_var = ctk.StringVar(value="°C  Celsius" if temp_unit == "Celsius" else "°F  Fahrenheit")

        temp_seg = ctk.CTkSegmentedButton(
            row,
            values=["°C  Celsius", "°F  Fahrenheit"],
            variable=self._temp_var,
            font=FONT_SMALL,
            height=44,
            selected_color=self.colors["primary"],
            selected_hover_color=self.colors["primary_hover"],
            unselected_color=self.colors["input_bg"],
            unselected_hover_color=self.colors["card_hover"],
            text_color=self.colors["text"],
            fg_color=self.colors["input_bg"],
            corner_radius=RADIUS_MD,
        )
        temp_seg.pack(side="left")

    def _build_wind_unit_row(self, parent):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=SPACE_2)

        ctk.CTkLabel(
            row, text="Wind Speed:",
            font=FONT_BODY, text_color=self.colors["text"],
        ).pack(side="left", padx=(0, SPACE_3))

        self._wind_var = ctk.StringVar(value=self._settings.get("wind_unit", "km/h"))
        wind_seg = ctk.CTkSegmentedButton(
            row,
            values=["km/h", "mph"],
            variable=self._wind_var,
            font=FONT_SMALL,
            height=44,
            selected_color=self.colors["primary"],
            selected_hover_color=self.colors["primary_hover"],
            unselected_color=self.colors["input_bg"],
            unselected_hover_color=self.colors["card_hover"],
            text_color=self.colors["text"],
            fg_color=self.colors["input_bg"],
            corner_radius=RADIUS_MD,
        )
        wind_seg.pack(side="left")

    def _build_default_city_row(self, parent):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=SPACE_2)

        ctk.CTkLabel(
            row, text="Default City:",
            font=FONT_BODY, text_color=self.colors["text"],
        ).pack(side="left", padx=(0, SPACE_3))

        self._default_city_entry = ctk.CTkEntry(
            row,
            placeholder_text="Enter city name (e.g., New York, London, Tokyo)...",
            width=360, height=44,
            font=FONT_BODY,
            fg_color=self.colors["input_bg"],
            text_color=self.colors["text"],
            border_color=self.colors["card_border"],
            corner_radius=RADIUS_MD,
        )
        default_city = self._settings.get("default_city", "")
        if default_city:
            self._default_city_entry.insert(0, default_city)
        self._default_city_entry.pack(side="left")

        # Add focus ring animation
        def on_focus_in(_):
            animate_color_transition(self._default_city_entry, "border_color",
                                      self._default_city_entry.cget("border_color"), self.colors["focus_ring"], ANIM_FAST)
            self._default_city_entry.configure(border_width=2)

        def on_focus_out(_):
            animate_color_transition(self._default_city_entry, "border_color",
                                      self._default_city_entry.cget("border_color"), self.colors["card_border"], ANIM_FAST)
            self._default_city_entry.configure(border_width=1)

        self._default_city_entry.bind("<FocusIn>", on_focus_in)
        self._default_city_entry.bind("<FocusOut>", on_focus_out)

        # Helper text
        ctk.CTkLabel(
            parent, text="This city will be loaded automatically on startup.",
            font=FONT_SMALL, text_color=self.colors["text_dim"],
        ).pack(anchor="w", pady=(SPACE_1, 0))

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