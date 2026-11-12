"""
components/weather_card.py — Reusable info card for a single weather metric.
"""

import customtkinter as ctk
from config.settings import (
    CARD_CORNER_RADIUS, PAD_MD, PAD_SM,
    FONT_SMALL, FONT_MEDIUM, FONT_BODY,
)


class WeatherCard(ctk.CTkFrame):
    """
    A compact card showing a label, icon, and value for one weather metric.

    Usage:
        card = WeatherCard(parent, colors, icon="💧", label="Humidity", value="72%")
    """

    def __init__(self, parent, colors: dict,
                 icon: str = "", label: str = "", value: str = "",
                 **kwargs):
        super().__init__(
            parent,
            fg_color=colors["card"],
            corner_radius=CARD_CORNER_RADIUS,
            **kwargs,
        )
        self.colors = colors

        self._icon_label = ctk.CTkLabel(
            self, text=icon,
            font=("Segoe UI Emoji", 22),
            fg_color="transparent",
        )
        self._icon_label.pack(pady=(PAD_MD, PAD_SM // 2))

        self._value_label = ctk.CTkLabel(
            self, text=value,
            font=FONT_MEDIUM,
            text_color=colors["text"],
            fg_color="transparent",
        )
        self._value_label.pack()

        self._name_label = ctk.CTkLabel(
            self, text=label,
            font=FONT_SMALL,
            text_color=colors["text_dim"],
            fg_color="transparent",
        )
        self._name_label.pack(pady=(2, PAD_MD))

    def update_value(self, value: str):
        """Update the displayed value."""
        self._value_label.configure(text=value)

    def update_icon(self, icon: str):
        """Update the icon."""
        self._icon_label.configure(text=icon)

    def apply_colors(self, colors: dict):
        self.colors = colors
        self.configure(fg_color=colors["card"])
        self._value_label.configure(text_color=colors["text"])
        self._name_label.configure(text_color=colors["text_dim"])
