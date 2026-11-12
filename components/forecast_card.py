"""
components/forecast_card.py — Card widget for hourly or daily forecast display.
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
                 **kwargs):
        super().__init__(
            parent,
            fg_color=colors["card"],
            corner_radius=CARD_CORNER_RADIUS,
            **kwargs,
        )
        self.colors = colors

        ctk.CTkLabel(self, text=time_label, font=FONT_LABEL,
                     text_color=colors["text_dim"]).pack(pady=(PAD_SM, 2))
        ctk.CTkLabel(self, text=emoji, font=("Segoe UI Emoji", 18)).pack()
        ctk.CTkLabel(self, text=temperature, font=FONT_BODY,
                     text_color=colors["text"]).pack()
        if precip:
            ctk.CTkLabel(self, text=f"💧 {precip}%", font=FONT_LABEL,
                         text_color=colors["text_dim"]).pack(pady=(2, PAD_SM))
        else:
            ctk.CTkLabel(self, text="", font=FONT_LABEL).pack(pady=(2, PAD_SM))


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
            **kwargs,
        )
        self.colors = colors

        ctk.CTkLabel(self, text=date_label, font=FONT_LABEL,
                     text_color=colors["text_dim"]).pack(pady=(PAD_SM, 2))
        ctk.CTkLabel(self, text=emoji, font=("Segoe UI Emoji", 20)).pack()
        ctk.CTkLabel(self, text=temp_max, font=FONT_BODY,
                     text_color=colors["text"]).pack()
        ctk.CTkLabel(self, text=temp_min, font=FONT_LABEL,
                     text_color=colors["text_dim"]).pack(pady=(0, PAD_SM))
