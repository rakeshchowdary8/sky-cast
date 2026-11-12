"""
components/detail_card.py — Premium weather detail metric cards (shadcn-inspired).

Modern card widgets for displaying weather metrics with:
- Beautiful icon containers with accent gradients
- Clear typography hierarchy (label → value → unit)
- Smooth hover/tap interactions
- Full theme consistency (dark/light)
- Accessible color contrast
"""

import customtkinter as ctk
from config.settings import (
    FONT_BODY, FONT_LABEL, FONT_MEDIUM, FONT_DISPLAY, FONT_TITLE,
    PAD_MD, PAD_SM, PAD_XS, PAD_LG, CARD_CORNER_RADIUS,
    METRIC_ACCENTS,
)


def _get_light_accent(accent_key: str) -> str:
    """Get the light/background version of an accent color for current theme."""
    light_key = f"{accent_key}_light"
    return METRIC_ACCENTS.get(light_key, METRIC_ACCENTS.get(accent_key, "#3b82f6"))


class DetailCard(ctk.CTkFrame):
    """
    Premium weather detail card for a single metric (shadcn-inspired design).

    Features:
    - Icon container with accent-colored background
    - Clear label/value/unit hierarchy
    - Subtle top accent bar
    - Smooth hover elevation effect
    - Full dark/light theme support

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
        accent_dict = METRIC_ACCENTS.get(accent_key, {"main": colors["primary"], "light": colors["primary_light"], "text": colors["primary"]})
        self.accent_color = accent_dict["main"]
        self.accent_light = accent_dict["light"]
        self._value = value
        self._unit = unit
        self._title = title
        self._icon = icon
        self._build()

    def _build(self):
        self.pack_propagate(False)
        self.configure(cursor="hand2")

        # Subtle top accent bar (3px)
        self._accent_bar = ctk.CTkFrame(
            self,
            height=3,
            fg_color=self.accent_color,
            corner_radius=CARD_CORNER_RADIUS,
        )
        self._accent_bar.pack(fill="x", padx=0, pady=0)
        self._accent_bar.lower()

        # Main content with generous padding
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=PAD_LG, pady=PAD_LG)

        # --- Top: Icon container + Label ---
        top_row = ctk.CTkFrame(content, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, PAD_MD))

        # Icon container with accent background (circular-ish)
        self._icon_container = ctk.CTkFrame(
            top_row,
            width=52,
            height=52,
            fg_color=self.accent_light,
            corner_radius=14,
        )
        self._icon_container.pack(side="left")
        self._icon_container.pack_propagate(False)

        self._icon_label = ctk.CTkLabel(
            self._icon_container,
            text=self._icon,
            font=("Segoe UI Emoji", 24),
            text_color=self.accent_color,
            fg_color="transparent",
        )
        self._icon_label.pack(expand=True)

        # Metric label
        self._title_label = ctk.CTkLabel(
            top_row,
            text=self._title,
            font=FONT_LABEL,
            text_color=self.colors["text_secondary"],
            fg_color="transparent",
        )
        self._title_label.pack(side="left", padx=(PAD_MD, 0), anchor="s", pady=(0, 4))

        # --- Bottom: Large value + unit ---
        value_row = ctk.CTkFrame(content, fg_color="transparent")
        value_row.pack(fill="x")

        self._value_label = ctk.CTkLabel(
            value_row,
            text=self._value,
            font=FONT_DISPLAY,
            text_color=self.colors["text"],
            fg_color="transparent",
        )
        self._value_label.pack(side="left", anchor="s")

        if self._unit:
            self._unit_label = ctk.CTkLabel(
                value_row,
                text=self._unit,
                font=FONT_MEDIUM,
                text_color=self.colors["text_dim"],
                fg_color="transparent",
            )
            self._unit_label.pack(side="left", padx=(PAD_SM, 0), anchor="s", pady=(0, 6))

        # Bind hover/tap events
        self._bind_events()

    def _bind_events(self):
        """Bind hover and click events to card and all children."""
        widgets = [self, self._accent_bar]
        for w in self.winfo_children():
            widgets.append(w)
            for c in w.winfo_children():
                widgets.append(c)

        for w in widgets:
            w.bind("<Enter>", self._on_enter)
            w.bind("<Leave>", self._on_leave)

    def _on_enter(self, _event):
        """Hover: elevate card, highlight border, brighten accent bar."""
        self.configure(
            border_color=self.accent_color,
            fg_color=self.colors["card_hover"],
        )
        self._accent_bar.configure(fg_color=self.accent_color)

    def _on_leave(self, _event):
        """Leave: restore default state."""
        self.configure(
            border_color=self.colors["card_border"],
            fg_color=self.colors["card"],
        )
        self._accent_bar.configure(fg_color=self.accent_color)

    def update_value(self, value: str, unit: str = None):
        """Update the displayed value and optionally unit."""
        self._value = value
        self._value_label.configure(text=value)
        if unit is not None:
            self._unit = unit
            if hasattr(self, '_unit_label'):
                self._unit_label.configure(text=unit)

    def update_title(self, title: str):
        """Update the metric title."""
        self._title = title
        self._title_label.configure(text=title)

    def update_icon(self, icon: str):
        """Update the icon."""
        self._icon = icon
        self._icon_label.configure(text=icon)

    def apply_colors(self, colors: dict):
        """Apply new theme colors - full refresh for consistency."""
        self.colors = colors
        self.accent_color = METRIC_ACCENTS.get(self.accent_key, colors["accent"])
        self.accent_light = _get_light_accent(self.accent_key)

        self.configure(
            fg_color=colors["card"],
            border_color=colors["card_border"],
        )
        self._accent_bar.configure(fg_color=self.accent_color)
        self._icon_container.configure(fg_color=self.accent_light)
        self._icon_label.configure(text_color=self.accent_color)
        self._title_label.configure(text_color=colors["text_secondary"])
        self._value_label.configure(text_color=colors["text"])
        if hasattr(self, '_unit_label'):
            self._unit_label.configure(text_color=colors["text_dim"])


class DetailCardCompact(ctk.CTkFrame):
    """
    Compact version of detail card for tight spaces (sidebar, small windows).
    Maintains same visual language but condensed.
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
        accent_dict = METRIC_ACCENTS.get(accent_key, {"main": colors["primary"], "light": colors["primary_light"], "text": colors["primary"]})
        self.accent_color = accent_dict["main"]
        self.accent_light = accent_dict["light"]
        self._value = value
        self._unit = unit
        self._title = title
        self._icon = icon
        self._build()

    def _build(self):
        self.pack_propagate(False)
        self.configure(cursor="hand2")

        # Top accent bar (2px)
        self._accent_bar = ctk.CTkFrame(
            self,
            height=2,
            fg_color=self.accent_color,
            corner_radius=12,
        )
        self._accent_bar.pack(fill="x")

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=PAD_MD, pady=PAD_MD)

        # Single row: icon, title, value+unit
        row = ctk.CTkFrame(content, fg_color="transparent")
        row.pack(fill="x")

        # Small icon container
        icon_container = ctk.CTkFrame(
            row,
            width=36,
            height=36,
            fg_color=self.accent_light,
            corner_radius=10,
        )
        icon_container.pack(side="left")
        icon_container.pack_propagate(False)

        ctk.CTkLabel(
            icon_container,
            text=self._icon,
            font=("Segoe UI Emoji", 16),
            text_color=self.accent_color,
        ).pack(expand=True)

        # Title
        self._title_label = ctk.CTkLabel(
            row,
            text=self._title,
            font=FONT_SMALL,
            text_color=self.colors["text_secondary"],
        )
        self._title_label.pack(side="left", padx=(PAD_SM, 0), anchor="center")

        # Value + unit
        value_frame = ctk.CTkFrame(row, fg_color="transparent")
        value_frame.pack(side="right")

        self._value_label = ctk.CTkLabel(
            value_frame,
            text=self._value,
            font=FONT_MEDIUM,
            text_color=self.colors["text"],
        )
        self._value_label.pack(side="left", anchor="e")

        if self._unit:
            self._unit_label = ctk.CTkLabel(
                value_frame,
                text=self._unit,
                font=FONT_SMALL,
                text_color=self.colors["text_dim"],
            )
            self._unit_label.pack(side="left", padx=(PAD_XS, 0), anchor="e")

        # Hover events
        self._bind_events()

    def _bind_events(self):
        widgets = [self, self._accent_bar]
        for w in self.winfo_children():
            widgets.append(w)
            for c in w.winfo_children():
                widgets.append(c)

        for w in widgets:
            w.bind("<Enter>", self._on_enter)
            w.bind("<Leave>", self._on_leave)

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
        self._value = value
        self._value_label.configure(text=value)

    def apply_colors(self, colors: dict):
        self.colors = colors
        self.accent_color = METRIC_ACCENTS.get(self.accent_key, colors["accent"])
        self.accent_light = _get_light_accent(self.accent_key)

        self.configure(
            fg_color=colors["card"],
            border_color=colors["card_border"],
        )
        self._accent_bar.configure(fg_color=self.accent_color)
        self._title_label.configure(text_color=colors["text_secondary"])
        self._value_label.configure(text_color=colors["text"])
        if hasattr(self, '_unit_label'):
            self._unit_label.configure(text_color=colors["text_dim"])