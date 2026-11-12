"""
components/forecast_card.py — Modern forecast cards with hover effects.
"""

import customtkinter as ctk
from config.settings import (
    CARD_CORNER_RADIUS, PAD_SM, PAD_MD,
    FONT_SMALL, FONT_BODY, FONT_LABEL,
)


class HourlyCard(ctk.CTkFrame):
    """Single-hour forecast card for the horizontal hourly strip."""

    def __init__(self, parent, colors: dict,
                 time_label: str = "", emoji: str = "",
                 temperature: str = "", precip: str = "",
                 is_day: bool = True, **kwargs):
        super().__init__(
            parent,
            fg_color=colors["card"],
            corner_radius=CARD_CORNER_RADIUS,
            border_width=1,
            border_color=colors["border"],
            **kwargs,
        )
        self.colors = colors
        self._default_fg = colors["card"]
        self._hover_fg = colors["card_hover"]

        self._build(time_label, emoji, temperature, precip)
        self._bind_hover()

    def _build(self, time_label: str, emoji: str, temperature: str, precip: str):
        # Time
        self._time_label = ctk.CTkLabel(
            self, text=time_label, font=FONT_LABEL,
            text_color=self.colors["text_dim"],
        )
        self._time_label.pack(pady=(PAD_SM, 2))

        # Weather emoji
        self._emoji_label = ctk.CTkLabel(
            self, text=emoji, font=("Segoe UI Emoji", 24),
        )
        self._emoji_label.pack()

        # Temperature
        self._temp_label = ctk.CTkLabel(
            self, text=temperature, font=FONT_BODY,
            text_color=self.colors["text"],
        )
        self._temp_label.pack()

        # Precipitation probability
        precip_text = f"💧 {precip}%" if precip else ""
        self._precip_label = ctk.CTkLabel(
            self, text=precip_text, font=FONT_LABEL,
            text_color=self.colors["accent"] if precip else self.colors["text_dim"],
        )
        self._precip_label.pack(pady=(2, PAD_SM))

    def _bind_hover(self):
        self.bind("<Enter>", lambda _: self._set_hover(True))
        self.bind("<Leave>", lambda _: self._set_hover(False))
        for child in self.winfo_children():
            child.bind("<Enter>", lambda _: self._set_hover(True))
            child.bind("<Leave>", lambda _: self._set_hover(False))

    def _set_hover(self, hover: bool):
        self.configure(
            fg_color=self._hover_fg if hover else self._default_fg,
            border_color=self.colors["accent"] if hover else self.colors["border"],
        )

    def update_data(self, time_label: str, emoji: str, temperature: str, precip: str):
        self._time_label.configure(text=time_label)
        self._emoji_label.configure(text=emoji)
        self._temp_label.configure(text=temperature)
        precip_text = f"💧 {precip}%" if precip else ""
        self._precip_label.configure(
            text=precip_text,
            text_color=self.colors["accent"] if precip else self.colors["text_dim"],
        )

    def apply_colors(self, colors: dict):
        self.colors = colors
        self._default_fg = colors["card"]
        self._hover_fg = colors["card_hover"]
        self._set_hover(False)
        self._time_label.configure(text_color=colors["text_dim"])
        self._temp_label.configure(text_color=colors["text"])
        self._precip_label.configure(text_color=colors["accent"])


class DailyCard(ctk.CTkFrame):
    """Single-day forecast card for the 7-day forecast row."""

    def __init__(self, parent, colors: dict,
                 date_label: str = "", emoji: str = "",
                 temp_max: str = "", temp_min: str = "",
                 **kwargs):
        super().__init__(
            parent,
            fg_color=colors["card"],
            corner_radius=CARD_CORNER_RADIUS,
            border_width=1,
            border_color=colors["border"],
            **kwargs,
        )
        self.colors = colors
        self._default_fg = colors["card"]
        self._hover_fg = colors["card_hover"]

        self._build(date_label, emoji, temp_max, temp_min)
        self._bind_hover()

    def _build(self, date_label: str, emoji: str, temp_max: str, temp_min: str):
        # Date
        self._date_label = ctk.CTkLabel(
            self, text=date_label, font=FONT_LABEL,
            text_color=self.colors["text_dim"],
        )
        self._date_label.pack(pady=(PAD_SM, 2))

        # Weather emoji
        self._emoji_label = ctk.CTkLabel(
            self, text=emoji, font=("Segoe UI Emoji", 26),
        )
        self._emoji_label.pack()

        # Max temp
        self._max_label = ctk.CTkLabel(
            self, text=temp_max, font=FONT_BODY,
            text_color=self.colors["text"],
        )
        self._max_label.pack()

        # Min temp
        self._min_label = ctk.CTkLabel(
            self, text=temp_min, font=FONT_LABEL,
            text_color=self.colors["text_dim"],
        )
        self._min_label.pack(pady=(0, PAD_SM))

    def _bind_hover(self):
        self.bind("<Enter>", lambda _: self._set_hover(True))
        self.bind("<Leave>", lambda _: self._set_hover(False))
        for child in self.winfo_children():
            child.bind("<Enter>", lambda _: self._set_hover(True))
            child.bind("<Leave>", lambda _: self._set_hover(False))

    def _set_hover(self, hover: bool):
        self.configure(
            fg_color=self._hover_fg if hover else self._default_fg,
            border_color=self.colors["accent"] if hover else self.colors["border"],
        )

    def update_data(self, date_label: str, emoji: str, temp_max: str, temp_min: str):
        self._date_label.configure(text=date_label)
        self._emoji_label.configure(text=emoji)
        self._max_label.configure(text=temp_max)
        self._min_label.configure(text=temp_min)

    def apply_colors(self, colors: dict):
        self.colors = colors
        self._default_fg = colors["card"]
        self._hover_fg = colors["card_hover"]
        self._set_hover(False)
        self._date_label.configure(text_color=colors["text_dim"])
        self._max_label.configure(text_color=colors["text"])
        self._min_label.configure(text_color=colors["text_dim"])