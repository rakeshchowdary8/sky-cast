"""
views/favorites.py — Favorite cities management view.
"""

import customtkinter as ctk
from config.settings import (
    FONT_TITLE, FONT_MEDIUM, FONT_BODY, FONT_SMALL,
    PAD_LG, PAD_MD, PAD_SM, CARD_CORNER_RADIUS,
)
from database import database


class FavoritesView(ctk.CTkFrame):
    """
    Displays the list of favorite cities and allows adding/removing them.

    Args:
        parent:        Parent widget.
        app:           App instance (for search callback).
        colors:        Current theme color dict.
    """

    def __init__(self, parent, app, colors: dict, **kwargs):
        super().__init__(parent, fg_color=colors["bg"], corner_radius=0, **kwargs)
        self.app = app
        self.colors = colors
        self._build()

    def _build(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=PAD_LG, pady=(PAD_LG, PAD_SM))

        ctk.CTkLabel(
            header, text="⭐ Favorite Cities",
            font=FONT_TITLE, text_color=self.colors["text"],
        ).pack(side="left")

        # Scrollable list
        self._list_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent", corner_radius=0
        )
        self._list_frame.pack(fill="both", expand=True, padx=PAD_LG, pady=PAD_SM)

        self._refresh_list()

    def _refresh_list(self):
        """Clear and re-populate the favorites list from the database."""
        for widget in self._list_frame.winfo_children():
            widget.destroy()

        favorites = database.get_favorite_cities()

        if not favorites:
            ctk.CTkLabel(
                self._list_frame,
                text="No favorite cities yet.\nSearch for a city and click 'Add to Favorites'.",
                font=FONT_BODY,
                text_color=self.colors["text_dim"],
                justify="center",
            ).pack(pady=PAD_LG * 3)
            return

        for fav in favorites:
            self._build_favorite_row(fav)

    def _build_favorite_row(self, fav: dict):
        """Build one row for a favorite city."""
        row = ctk.CTkFrame(
            self._list_frame,
            fg_color=self.colors["card"],
            corner_radius=CARD_CORNER_RADIUS,
        )
        row.pack(fill="x", pady=PAD_SM // 2)

        # City info (clickable area)
        info = ctk.CTkFrame(row, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True, padx=PAD_MD, pady=PAD_MD)

        city_text = f"{fav['city_name']}, {fav['country']}" if fav.get("country") else fav["city_name"]
        ctk.CTkLabel(
            info, text=f"📍 {city_text}",
            font=FONT_MEDIUM, text_color=self.colors["text"],
            anchor="w",
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"Lat: {fav['latitude']:.3f}  Lon: {fav['longitude']:.3f}  •  Added: {fav['created_at'][:10]}",
            font=FONT_SMALL, text_color=self.colors["text_dim"],
        ).pack(anchor="w")

        # Buttons
        btn_frame = ctk.CTkFrame(row, fg_color="transparent")
        btn_frame.pack(side="right", padx=PAD_MD)

        ctk.CTkButton(
            btn_frame, text="🌤️ View",
            font=FONT_SMALL,
            width=80, height=30,
            fg_color=self.colors["accent"],
            hover_color=self.colors.get("accent_hover", self.colors["accent"]),
            text_color="#ffffff",
            corner_radius=6,
            command=lambda f=fav: self._load_favorite(f),
        ).pack(side="left", padx=PAD_SM // 2)

        ctk.CTkButton(
            btn_frame, text="🗑️ Remove",
            font=FONT_SMALL,
            width=90, height=30,
            fg_color="#c0392b",
            hover_color="#922b21",
            text_color="#ffffff",
            corner_radius=6,
            command=lambda f=fav: self._remove_favorite(f),
        ).pack(side="left")

    def _load_favorite(self, fav: dict):
        """Load weather for a favorite city."""
        self.app.search_city(fav["city_name"])
        self.app.show_view("dashboard")

    def _remove_favorite(self, fav: dict):
        """Remove a favorite city from the database and refresh list."""
        database.delete_favorite_city(fav["id"])
        self._refresh_list()

    def on_show(self):
        """Refresh the list whenever this view is activated."""
        self._refresh_list()

    def apply_colors(self, colors: dict):
        self.colors = colors
        self.configure(fg_color=colors["bg"])
        self._refresh_list()
