"""
components/weather_card.py — Modern weather metric card with animations.

Features:
- Icon, value, label layout
- Hover effects
- Theme-aware colors
- Smooth color transitions
"""

import customtkinter as ctk
from config.settings import (
    CARD_CORNER_RADIUS, PAD_MD, PAD_SM,
    FONT_SMALL, FONT_MEDIUM, FONT_BODY,
)


class WeatherCard(ctk.CTkFrame):
    """
    A modern card showing a label, icon, and value for one weather metric.

    Usage:
        card = WeatherCard(parent, colors, icon="💧", label="Humidity", value="72%")
    """

    def __init__(self, parent, colors: dict,
                 icon: str = "", label: str = "", value: str = "",
                 accent_color: str = None, **kwargs):
        super().__init__(
            parent,
            fg_color=colors["card"],
            corner_radius=CARD_CORNER_RADIUS,
            border_width=1,
            border_color=colors["border"],
            **kwargs,
        )
        self.colors = colors
        self.accent_color = accent_color or colors["accent"]
        self._hovered = False

        self._build(icon, label, value)
        self._bind_events()

    def _build(self, icon: str, label: str, value: str):
        # Icon
        self._icon_label = ctk.CTkLabel(
            self, text=icon,
            font=("Segoe UI Emoji", 26),
            fg_color="transparent",
        )
        self._icon_label.pack(pady=(PAD_MD, PAD_SM // 2))

        # Value (large)
        self._value_label = ctk.CTkLabel(
            self, text=value,
            font=FONT_MEDIUM,
            text_color=self.colors["text"],
            fg_color="transparent",
        )
        self._value_label.pack()

        # Label (small, dimmed)
        self._name_label = ctk.CTkLabel(
            self, text=label,
            font=FONT_SMALL,
            text_color=self.colors["text_dim"],
            fg_color="transparent",
        )
        self._name_label.pack(pady=(2, PAD_MD))

    def _bind_events(self):
        """Add hover effects."""
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        for child in (self._icon_label, self._value_label, self._name_label):
            child.bind("<Enter>", self._on_enter)
            child.bind("<Leave>", self._on_leave)

    def _on_enter(self, _event):
        if not self._hovered:
            self._hovered = True
            self.configure(
                fg_color=self.colors["card_hover"],
                border_color=self.accent_color,
            )

    def _on_leave(self, _event):
        if self._hovered:
            self._hovered = False
            self.configure(
                fg_color=self.colors["card"],
                border_color=self.colors["border"],
            )

    def update_value(self, value: str):
        """Update the displayed value."""
        self._value_label.configure(text=value)

    def update_icon(self, icon: str):
        """Update the icon."""
        self._icon_label.configure(text=icon)

    def apply_colors(self, colors: dict):
        self.colors = colors
        self.accent_color = colors["accent"]
        if self._hovered:
            self.configure(
                fg_color=colors["card_hover"],
                border_color=colors["accent"],
            )
        else:
            self.configure(
                fg_color=colors["card"],
                border_color=colors["border"],
            )
        self._value_label.configure(text_color=colors["text"])
        self._name_label.configure(text_color=colors["text_dim"])


class WeatherCardCompact(ctk.CTkFrame):
    """
    Compact horizontal weather card for tighter layouts.
    """

    def __init__(self, parent, colors: dict,
                 icon: str = "", label: str = "", value: str = "", **kwargs):
        super().__init__(
            parent,
            fg_color=colors["card"],
            corner_radius=8,
            border_width=1,
            border_color=colors["border"],
            **kwargs,
        )
        self.colors = colors

        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=PAD_MD, pady=PAD_SM)

        ctk.CTkLabel(
            inner, text=icon,
            font=("Segoe UI Emoji", 18),
        ).pack(side="left", padx=(0, PAD_SM))

        text_frame = ctk.CTkFrame(inner, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)

        self._value_label = ctk.CTkLabel(
            text_frame, text=value,
            font=FONT_BODY, text_color=colors["text"], anchor="w",
        )
        self._value_label.pack(anchor="w")

        self._name_label = ctk.CTkLabel(
            text_frame, text=label,
            font=FONT_SMALL, text_color=colors["text_dim"], anchor="w",
        )
        self._name_label.pack(anchor="w")

    def update_value(self, value: str):
        self._value_label.configure(text=value)

    def apply_colors(self, colors: dict):
        self.colors = colors
        self.configure(fg_color=colors["card"], border_color=colors["border"])
        self._value_label.configure(text_color=colors["text"])
        self._name_label.configure(text_color=colors["text_dim"])