"""
components/sidebar.py — Modern navigation sidebar with smooth transitions.
"""

import customtkinter as ctk
from config.settings import (
    SIDEBAR_WIDTH, SIDEBAR_BUTTON_HEIGHT, PAD_MD, PAD_SM, PAD_LG,
    FONT_LARGE, FONT_BODY, FONT_SMALL,
)


class Sidebar(ctk.CTkFrame):
    """
    Modern vertical navigation sidebar with animated active state.

    Args:
        parent: Parent widget.
        on_navigate: Callback(view_name: str) called on button click.
        colors: Current theme color dict.
    """

    NAV_ITEMS = [
        ("dashboard",  "🏠  Dashboard"),
        ("favorites",  "⭐  Favorites"),
        ("history",    "🕒  Search History"),
        ("whistory",   "📊  Weather History"),
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
        self._indicator = None

        self._build()

    def _build(self):
        self.pack_propagate(False)  # Keep fixed width

        # --- Logo / App name ---
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(fill="x", padx=PAD_MD, pady=(PAD_LG, PAD_MD))

        # Animated sun/cloud icon
        self._logo_icon = ctk.CTkLabel(
            logo_frame,
            text="🌤️",
            font=("Segoe UI Emoji", 36),
            fg_color="transparent",
        )
        self._logo_icon.pack()

        ctk.CTkLabel(
            logo_frame,
            text="SkyView",
            font=FONT_LARGE,
            text_color=self.colors["text"],
        ).pack()

        ctk.CTkLabel(
            logo_frame,
            text="Weather",
            font=FONT_SMALL,
            text_color=self.colors["text_dim"],
        ).pack()

        # Divider with gradient-like effect
        divider = ctk.CTkFrame(self, height=1, fg_color=self.colors["border"])
        divider.pack(fill="x", padx=PAD_MD, pady=PAD_MD)

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
                corner_radius=10,
                command=lambda v=view_name: self._on_click(v),
            )
            btn.pack(fill="x", pady=3)
            self._buttons[view_name] = btn

        # Create active indicator (colored bar on left)
        self._indicator = ctk.CTkFrame(
            nav_frame,
            width=4,
            height=SIDEBAR_BUTTON_HEIGHT - 8,
            fg_color=self.colors["accent"],
            corner_radius=2,
        )

        # Activate default
        self._set_active("dashboard")

    def _on_click(self, view_name: str):
        self._set_active(view_name)
        self.on_navigate(view_name)

    def _set_active(self, view_name: str):
        """Highlight the active nav button with smooth indicator animation."""
        # Reset previous
        if self._active_view in self._buttons:
            self._buttons[self._active_view].configure(
                fg_color="transparent",
                text_color=self.colors["text_dim"],
            )

        # Activate new
        self._active_view = view_name
        if view_name in self._buttons:
            btn = self._buttons[view_name]
            btn.configure(
                fg_color=self.colors["card"],
                text_color=self.colors["accent"],
            )

            # Move indicator to active button
            self._indicator.place_forget()
            self._indicator.place(
                x=0, y=btn.winfo_y() + 4,
            )
            self._indicator.lift()

    def apply_colors(self, colors: dict):
        """Re-apply colors after a theme change."""
        self.colors = colors
        self.configure(fg_color=colors["sidebar"])
        self._indicator.configure(fg_color=colors["accent"])
        self._logo_icon.configure(text_color=colors["text"])
        self._set_active(self._active_view)
        for name, btn in self._buttons.items():
            if name != self._active_view:
                btn.configure(
                    text_color=colors["text_dim"],
                    hover_color=colors["card"],
                )
            else:
                btn.configure(
                    fg_color=colors["card"],
                    text_color=colors["accent"],
                )