"""
views/favorites.py — Modern favorite cities management view.
"""

import customtkinter as ctk
from config.settings import (
    FONT_TITLE, FONT_MEDIUM, FONT_BODY, FONT_SMALL,
    PAD_LG, PAD_MD, PAD_SM, CARD_CORNER_RADIUS,
)
from database import database


class FavoritesView(ctk.CTkFrame):
    """
    Displays the list of favorite cities with modern card-based UI.

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
        # Header with icon
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=PAD_LG, pady=(PAD_LG, PAD_SM))

        ctk.CTkLabel(
            header, text="⭐  Favorite Cities",
            font=FONT_TITLE, text_color=self.colors["text"],
        ).pack(side="left")

        ctk.CTkLabel(
            header, text="Your saved locations",
            font=FONT_SMALL, text_color=self.colors["text_dim"],
        ).pack(side="left", padx=(PAD_MD, 0))

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
            self._build_empty_state()
            return

        for fav in favorites:
            self._build_favorite_card(fav)

    def _build_empty_state(self):
        """Show empty state illustration."""
        empty_frame = ctk.CTkFrame(
            self._list_frame, fg_color=self.colors["card"],
            corner_radius=CARD_CORNER_RADIUS, border_width=1,
            border_color=self.colors["border"],
        )
        empty_frame.pack(fill="x", pady=PAD_LG * 2)

        ctk.CTkLabel(
            empty_frame, text="🌍",
            font=("Segoe UI Emoji", 48),
        ).pack(pady=(PAD_LG * 2, PAD_MD))

        ctk.CTkLabel(
            empty_frame, text="No favorites yet",
            font=FONT_MEDIUM, text_color=self.colors["text"],
        ).pack()

        ctk.CTkLabel(
            empty_frame,
            text="Search for a city and click 'Add to Favorites'\nto save it for quick access.",
            font=FONT_BODY, text_color=self.colors["text_dim"],
            justify="center",
        ).pack(pady=(PAD_SM, PAD_LG * 2))

    def _build_favorite_card(self, fav: dict):
        """Build a modern card for a favorite city."""
        card = ctk.CTkFrame(
            self._list_frame,
            fg_color=self.colors["card"],
            corner_radius=CARD_CORNER_RADIUS,
            border_width=1,
            border_color=self.colors["border"],
        )
        card.pack(fill="x", pady=PAD_SM // 2)

        # Hover effect
        default_fg = self.colors["card"]
        hover_fg = self.colors["card_hover"]
        default_border = self.colors["border"]
        hover_border = self.colors["accent"]

        def on_enter(_):
            card.configure(fg_color=hover_fg, border_color=hover_border)
        def on_leave(_):
            card.configure(fg_color=default_fg, border_color=default_border)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        # Main content
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=PAD_MD, pady=PAD_MD)

        # Left: City info
        info = ctk.CTkFrame(content, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True)

        city_text = f"{fav['city_name']}, {fav['country']}" if fav.get("country") else fav["city_name"]
        ctk.CTkLabel(
            info, text=f"📍  {city_text}",
            font=FONT_MEDIUM, text_color=self.colors["text"], anchor="w",
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"Lat: {fav['latitude']:.3f}   Lon: {fav['longitude']:.3f}   •   Added: {fav['created_at'][:10]}",
            font=FONT_SMALL, text_color=self.colors["text_dim"],
        ).pack(anchor="w")

        # Right: Action buttons
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(side="right", padx=PAD_SM)

        view_btn = ctk.CTkButton(
            btn_frame, text="🌤️  View",
            font=FONT_SMALL,
            width=90, height=34,
            fg_color=self.colors["accent"],
            hover_color=self.colors.get("accent_hover", self.colors["accent"]),
            text_color="#ffffff",
            corner_radius=8,
            command=lambda f=fav: self._load_favorite(f),
        )
        view_btn.pack(side="left", padx=PAD_SM // 2)

        # Bind hover to card too
        view_btn.bind("<Enter>", on_enter)
        view_btn.bind("<Leave>", on_leave)

        remove_btn = ctk.CTkButton(
            btn_frame, text="🗑️  Remove",
            font=FONT_SMALL,
            width=100, height=34,
            fg_color="transparent",
            hover_color="#c0392b",
            text_color=self.colors["warning"],
            border_width=1,
            border_color=self.colors["warning"],
            corner_radius=8,
            command=lambda f=fav: self._remove_favorite(f),
        )
        remove_btn.pack(side="left")
        remove_btn.bind("<Enter>", on_enter)
        remove_btn.bind("<Leave>", on_leave)

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