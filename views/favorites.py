"""
views/favorites.py — Premium favorite cities management view (shadcn-inspired).

Features:
- Clean card-based list with hover animations
- View and remove actions
- Empty state with call-to-action
- Staggered entrance animations
"""

import customtkinter as ctk
from config.settings import (
    FONT_TITLE, FONT_MEDIUM, FONT_BODY, FONT_SMALL, FONT_LABEL, FONT_TINY,
    SPACE_1, SPACE_2, SPACE_3, SPACE_4, SPACE_6, SPACE_8,
    CARD_CORNER_RADIUS, BUTTON_CORNER_RADIUS, RADIUS_MD,
    STATUS_COLORS,
    ANIM_FAST,
)
from components.base import Card, Button, Badge
from utils.animations import stagger_animate_children, animate_color_transition, ease_out_cubic
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
        self._favorite_cards = []
        self._build()

    def _build(self):
        # Header with icon
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=SPACE_8, pady=(SPACE_6, SPACE_3))

        ctk.CTkLabel(
            header, text="⭐  Favorite Cities",
            font=FONT_TITLE, text_color=self.colors["text"],
        ).pack(side="left")

        ctk.CTkLabel(
            header, text="Your saved locations",
            font=FONT_SMALL, text_color=self.colors["text_dim"],
        ).pack(side="left", padx=(SPACE_3, 0))

        # Scrollable list
        self._list_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent", corner_radius=0
        )
        self._list_frame.pack(fill="both", expand=True, padx=SPACE_8, pady=SPACE_2)

        self._refresh_list()

    def _refresh_list(self):
        """Clear and re-populate the favorites list from the database."""
        for widget in self._list_frame.winfo_children():
            widget.destroy()

        self._favorite_cards = []
        favorites = database.get_favorite_cities()

        if not favorites:
            self._build_empty_state()
            return

        for fav in favorites:
            self._build_favorite_card(fav)

        # Stagger animate the cards
        stagger_animate_children(
            self._list_frame,
            lambda child, idx: None,  # Cards animate themselves
            delay_per_child=50,
            start_delay=50,
        )

    def _build_empty_state(self):
        """Show empty state illustration using Card component."""
        empty_frame = Card(
            self._list_frame,
            variant="default",
            padding=SPACE_8,
            colors=self.colors,
        )
        empty_frame.pack(fill="x", pady=SPACE_8 * 2)

        empty_content = empty_frame.content

        ctk.CTkLabel(
            empty_content, text="🌍",
            font=("Segoe UI Emoji", 48),
        ).pack(pady=(SPACE_6, SPACE_4))

        ctk.CTkLabel(
            empty_content, text="No favorites yet",
            font=FONT_MEDIUM, text_color=self.colors["text"],
        ).pack()

        ctk.CTkLabel(
            empty_content,
            text="Search for a city and click 'Add to Favorites'\nto save it for quick access.",
            font=FONT_BODY, text_color=self.colors["text_dim"],
            justify="center",
        ).pack(pady=(SPACE_2, SPACE_6))

    def _build_favorite_card(self, fav: dict):
        """Build a modern card for a favorite city using Card component."""
        card = Card(
            self._list_frame,
            variant="default",
            padding=SPACE_4,
            colors=self.colors,
        )
        card.pack(fill="x", pady=SPACE_1)
        card.configure(cursor="hand2")

        # Store default colors for hover
        card._default_fg = self.colors["card"]
        card._default_border = self.colors["card_border"]
        card._hover_fg = self.colors["card_hover"]
        card._hover_border = self.colors["primary"]

        # Hover effect with smooth animation
        def on_enter(_):
            animate_color_transition(card, "fg_color",
                                      card.cget("fg_color"), self.colors["card_hover"], ANIM_FAST)
            animate_color_transition(card, "border_color",
                                      card.cget("border_color"), self.colors["primary"], ANIM_FAST)

        def on_leave(_):
            animate_color_transition(card, "fg_color",
                                      card.cget("fg_color"), self.colors["card"], ANIM_FAST)
            animate_color_transition(card, "border_color",
                                      card.cget("border_color"), self.colors["card_border"], ANIM_FAST)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        # Main content
        content = card.content

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

        # Right: Action buttons using Button component
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(side="right", padx=SPACE_2)

        view_btn = Button(
            btn_frame, text="🌤️  View",
            variant="default",
            size="sm",
            colors=self.colors,
            command=lambda f=fav: self._load_favorite(f),
        )
        view_btn.pack(side="left", padx=SPACE_1)

        # Bind hover to card too
        view_btn.bind("<Enter>", on_enter)
        view_btn.bind("<Leave>", on_leave)

        remove_btn = Button(
            btn_frame, text="🗑️  Remove",
            variant="ghost",
            size="sm",
            colors=self.colors,
            command=lambda f=fav: self._remove_favorite(f),
        )
        # Override colors for destructive action
        remove_btn.configure(
            text_color=self.colors["destructive"],
            hover_color=self.colors["destructive_light"],
        )
        remove_btn.pack(side="left")
        remove_btn.bind("<Enter>", on_enter)
        remove_btn.bind("<Leave>", on_leave)

        self._favorite_cards.append(card)

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