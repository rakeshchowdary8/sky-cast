"""
components/weather_card.py — Premium info card widget with hover effects and accent colors.

Features:
- Modern card design with subtle borders
- Hover effects with accent border highlight
- Per-metric accent colors
- Smooth color transitions
- Compact variant for dense layouts
"""

import customtkinter as ctk
from config.settings import (
    FONT_BODY, FONT_LABEL, FONT_MEDIUM, FONT_LARGE, FONT_DISPLAY,
    PAD_MD, PAD_SM, PAD_XS, CARD_CORNER_RADIUS,
    METRIC_ACCENTS,
)


def _get_light_accent(accent_key: str) -> str:
    """Get the light/background version of an accent color."""
    light_key = f"{accent_key}_light"
    return METRIC_ACCENTS.get(light_key, METRIC_ACCENTS.get(accent_key, "#3b82f6"))


class WeatherCard(ctk.CTkFrame):
    """
    Premium weather info card with icon, label, value, and unit.

    Args:
        parent: Parent widget.
        title: Metric label (e.g., "Humidity").
        value: Main value to display (e.g., "65").
        unit: Unit suffix (e.g., "%").
        icon: Emoji or text icon (e.g., "💧").
        accent_key: Key from METRIC_ACCENTS for accent color.
        colors: Current theme color dict.
    """

    def __init__(self, parent, title: str, value: str, unit: str,
                 icon: str, accent_key: str, colors: dict, **kwargs):
        super().__init__(
            parent,
            fg_color=colors["card"],
            corner_radius=CARD_CORNER_RADIUS,
            border_width=1,
            border_color=colors["card_border"],
            **kwargs,
        )
        self.colors = colors
        self.accent_key = accent_key
        self.accent_color = METRIC_ACCENTS.get(accent_key, colors["accent"])
        self.accent_light = _get_light_accent(accent_key)
        self._build(title, value, unit, icon)

    def _build(self, title: str, value: str, unit: str, icon: str):
        self.pack_propagate(False)

        # Accent border at top (subtle indicator)
        self._accent_bar = ctk.CTkFrame(
            self,
            height=3,
            fg_color=self.accent_color,
            corner_radius=0,
        )
        self._accent_bar.pack(fill="x", padx=0, pady=0)
        self._accent_bar.lower()

        # Content
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=PAD_MD, pady=PAD_MD)

        # Top row: Icon and title
        top_row = ctk.CTkFrame(content, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, PAD_SM))

        # Icon with accent background
        icon_container = ctk.CTkFrame(
            top_row,
            width=44,
            height=44,
            fg_color=self.accent_light,
            corner_radius=10,
        )
        icon_container.pack(side="left")
        icon_container.pack_propagate(False)

        ctk.CTkLabel(
            icon_container,
            text=icon,
            font=("Segoe UI Emoji", 20),
            text_color=self.accent_color,
            fg_color="transparent",
        ).pack(expand=True)

        # Title
        ctk.CTkLabel(
            top_row,
            text=title,
            font=FONT_LABEL,
            text_color=self.colors["text_secondary"],
            fg_color="transparent",
        ).pack(side="left", padx=(PAD_SM, 0), anchor="center")

        # Value with unit
        value_frame = ctk.CTkFrame(content, fg_color="transparent")
        value_frame.pack(fill="x", pady=(PAD_XS, 0))

        self._value_label = ctk.CTkLabel(
            value_frame,
            text=value,
            font=FONT_DISPLAY,
            text_color=self.colors["text"],
            fg_color="transparent",
        )
        self._value_label.pack(side="left")

        if unit:
            self._unit_label = ctk.CTkLabel(
                value_frame,
                text=unit,
                font=FONT_BODY,
                text_color=self.colors["text_dim"],
                fg_color="transparent",
            )
            self._unit_label.pack(side="left", padx=(PAD_XS, 0), anchor="s", pady=(0, 4))

        # Hover effects
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        for child in self.winfo_children():
            child.bind("<Enter>", self._on_enter)
            child.bind("<Leave>", self._on_leave)
            for grandchild in child.winfo_children():
                grandchild.bind("<Enter>", self._on_enter)
                grandchild.bind("<Leave>", self._on_leave)

    def _on_enter(self, _event):
        self.configure(
            border_color=self.accent_color,
            fg_color=self.colors["card_hover"],
        )
        self._accent_bar.configure(fg_color=self.accent_color)

    def _on_leave(self, _event):
        self.configure(
            border_color=self.colors["card_border"],
            fg_color=self.colors["card"],
        )
        self._accent_bar.configure(fg_color=self.accent_color)

    def update_value(self, value: str, unit: str = None):
        """Update the displayed value and optionally unit."""
        self._value_label.configure(text=value)
        if unit is not None and hasattr(self, '_unit_label'):
            self._unit_label.configure(text=unit)

    def apply_colors(self, colors: dict):
        self.colors = colors
        self.accent_color = METRIC_ACCENTS.get(self.accent_key, colors["accent"])
        self.configure(
            fg_color=colors["card"],
            border_color=colors["card_border"],
        )
        self._accent_bar.configure(fg_color=self.accent_color)
        # Children will be updated when their parent updates


class WeatherCardCompact(ctk.CTkFrame):
    """
    Compact weather card for dense layouts (e.g., sidebar, small spaces).
    """

    def __init__(self, parent, title: str, value: str, unit: str,
                 icon: str, accent_key: str, colors: dict, **kwargs):
        super().__init__(
            parent,
            fg_color=colors["card"],
            corner_radius=12,
            border_width=1,
            border_color=colors["card_border"],
            **kwargs,
        )
        self.colors = colors
        self.accent_key = accent_key
        self.accent_color = METRIC_ACCENTS.get(accent_key, colors["accent"])
        self._build(title, value, unit, icon)

    def _build(self, title: str, value: str, unit: str, icon: str):
        self.pack_propagate(False)

        # Accent bar at top
        self._accent_bar = ctk.CTkFrame(
            self,
            height=2,
            fg_color=self.accent_color,
            corner_radius=0,
        )
        self._accent_bar.pack(fill="x")

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=PAD_SM, pady=PAD_SM)

        # Icon and title row
        top_row = ctk.CTkFrame(content, fg_color="transparent")
        top_row.pack(fill="x")

        icon_lbl = ctk.CTkLabel(
            top_row,
            text=icon,
            font=("Segoe UI Emoji", 16),
            text_color=self.accent_color,
        )
        icon_lbl.pack(side="left")

        ctk.CTkLabel(
            top_row,
            text=title,
            font=FONT_SMALL,
            text_color=self.colors["text_secondary"],
        ).pack(side="left", padx=(PAD_SM, 0))

        # Value row
        value_row = ctk.CTkFrame(content, fg_color="transparent")
        value_row.pack(fill="x", pady=(PAD_XS, 0))

        self._value_label = ctk.CTkLabel(
            value_row,
            text=value,
            font=FONT_MEDIUM,
            text_color=self.colors["text"],
        )
        self._value_label.pack(side="left")

        if unit:
            ctk.CTkLabel(
                value_row,
                text=unit,
                font=FONT_SMALL,
                text_color=self.colors["text_dim"],
            ).pack(side="left", padx=(PAD_XS, 0))

        # Hover
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        for child in self.winfo_children():
            child.bind("<Enter>", self._on_enter)
            child.bind("<Leave>", self._on_leave)

    def _on_enter(self, _event):
        self.configure(
            border_color=self.accent_color,
            fg_color=self.colors["card_hover"],
        )

    def _on_leave(self, _event):
        self.configure(
            border_color=self.colors["card_border"],
            fg_color=self.colors["card"],
        )

    def update_value(self, value: str):
        self._value_label.configure(text=value)

    def apply_colors(self, colors: dict):
        self.colors = colors
        self.accent_color = METRIC_ACCENTS.get(self.accent_key, colors["accent"])
        self.configure(
            fg_color=colors["card"],
            border_color=colors["card_border"],
        )
        self._accent_bar.configure(fg_color=self.accent_color)