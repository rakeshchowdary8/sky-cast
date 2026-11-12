"""
components/sidebar.py — Left navigation sidebar.
"""

import customtkinter as ctk
from config.settings import (
    SIDEBAR_WIDTH, SIDEBAR_BUTTON_HEIGHT, PAD_MD, PAD_SM,
    FONT_LARGE, FONT_BODY, FONT_SMALL,
)


class Sidebar(ctk.CTkFrame):
    """
    Vertical navigation sidebar with app logo and nav buttons.

    Args:
        parent: Parent widget.
        on_navigate: Callback(view_name: str) called on button click.
        colors: Current theme color dict.
    """

    NAV_ITEMS = [
        ("dashboard",  "🌤️  Dashboard"),
        ("favorites",  "⭐  Favorites"),
        ("history",    "🕒  Search History"),
        ("whistory",   "📋  Weather History"),
        ("settings",   "⚙️  Settings"),
    ]

    def __init__(self, parent, on_navigate, colors: dict, **kwargs):
        super().__init__(
            parent,
            width=SIDEBAR_WIDTH,
            corner_radius=0,
            fg_color=colors["sidebar"],
            **kwargs,
        )
        self.on_navigate = on_navigate
        self.colors = colors
        self._buttons: dict[str, ctk.CTkButton] = {}
        self._active_view = "dashboard"

        self._build()

    def _build(self):
        self.pack_propagate(False)  # Keep fixed width

        # --- Logo / App name ---
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(fill="x", padx=PAD_MD, pady=(PAD_MD * 2, PAD_MD))

        ctk.CTkLabel(
            logo_frame,
            text="🌤️",
            font=("Segoe UI Emoji", 32),
            fg_color="transparent",
        ).pack()

        ctk.CTkLabel(
            logo_frame,
            text="SkyView",
            font=FONT_LARGE,
            text_color=self.colors["text"],
        ).pack()

        ctk.CTkLabel(
            logo_frame,
            text="Weather App",
            font=FONT_SMALL,
            text_color=self.colors["text_dim"],
        ).pack()

        # Divider
        ctk.CTkFrame(self, height=1, fg_color=self.colors["border"]).pack(
            fill="x", padx=PAD_MD, pady=PAD_MD
        )

        # --- Navigation buttons ---
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(fill="x", padx=PAD_SM, pady=PAD_SM)

        for view_name, label in self.NAV_ITEMS:
            btn = ctk.CTkButton(
                nav_frame,
                text=label,
                height=SIDEBAR_BUTTON_HEIGHT,
                anchor="w",
                font=FONT_BODY,
                fg_color="transparent",
                text_color=self.colors["text_dim"],
                hover_color=self.colors["card"],
                corner_radius=8,
                command=lambda v=view_name: self._on_click(v),
            )
            btn.pack(fill="x", pady=2)
            self._buttons[view_name] = btn

        # Activate default
        self._set_active("dashboard")

    def _on_click(self, view_name: str):
        self._set_active(view_name)
        self.on_navigate(view_name)

    def _set_active(self, view_name: str):
        """Highlight the active nav button."""
        # Reset previous
        if self._active_view in self._buttons:
            self._buttons[self._active_view].configure(
                fg_color="transparent",
                text_color=self.colors["text_dim"],
            )
        # Activate new
        self._active_view = view_name
        if view_name in self._buttons:
            self._buttons[view_name].configure(
                fg_color=self.colors["accent"],
                text_color="#ffffff",
            )

    def apply_colors(self, colors: dict):
        """Re-apply colors after a theme change."""
        self.colors = colors
        self.configure(fg_color=colors["sidebar"])
        self._set_active(self._active_view)
        for name, btn in self._buttons.items():
            if name != self._active_view:
                btn.configure(
                    text_color=colors["text_dim"],
                    hover_color=colors["card"],
                )
