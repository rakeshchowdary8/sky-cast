"""
components/search_bar.py — Simple search input (shadcn-inspired).

Features:
- Simple search entry with search button
- No autocomplete suggestions
- No loading states
- Clean styling with theme support
"""

import customtkinter as ctk
from config.settings import (
    FONT_BODY, FONT_SMALL, FONT_LABEL,
    SPACE_1, SPACE_2, SPACE_3, SPACE_4,
    CARD_CORNER_RADIUS, BUTTON_CORNER_RADIUS, INPUT_CORNER_RADIUS,
    ANIM_FAST, ANIM_NORMAL,
    get_colors,
)
from components.base import Button


class SearchBar(ctk.CTkFrame):
    """
    Simple search field with search button.

    Args:
        parent:      Parent widget.
        on_search:   Callback(city_name: str) triggered on submit.
        colors:      Current theme color dict.
        placeholder: Placeholder text in the entry field.
    """

    def __init__(self, parent, on_search, colors: dict,
                 placeholder: str = "Search city...", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.on_search = on_search
        self.colors = colors

        self._build(placeholder)

    def _build(self, placeholder: str):
        # Main container - using Card-like styling
        self._container = ctk.CTkFrame(
            self,
            fg_color=self.colors["card"],
            corner_radius=CARD_CORNER_RADIUS,
            border_width=1,
            border_color=self.colors["card_border"],
        )
        self._container.pack(fill="x", expand=True)

        # Inner frame for entry and button
        inner = ctk.CTkFrame(self._container, fg_color="transparent")
        inner.pack(fill="x", padx=SPACE_2, pady=SPACE_2)

        # Search icon
        self._search_icon = ctk.CTkLabel(
            inner,
            text="🔍",
            font=("Segoe UI Emoji", 18),
            text_color=self.colors["text_muted"],
            fg_color="transparent",
        )
        self._search_icon.pack(side="left", padx=(SPACE_4, SPACE_2))

        # Main search entry
        self._entry = ctk.CTkEntry(
            inner,
            placeholder_text=placeholder,
            width=380,
            height=48,
            font=FONT_BODY,
            fg_color=self.colors["input_bg"],
            text_color=self.colors["text"],
            border_color=self.colors["input_border"],
            border_width=1,
            corner_radius=INPUT_CORNER_RADIUS,
            placeholder_text_color=self.colors["input_placeholder"],
        )
        self._entry.pack(side="left", padx=(0, SPACE_2), fill="x", expand=True)

        # Bind events
        self._entry.bind("<Return>", self._on_return)
        self._entry.bind("<FocusIn>", self._on_focus_in)
        self._entry.bind("<FocusOut>", self._on_focus_out)

        # Search button using base Button component
        self._btn = Button(
            inner,
            text="Search",
            width=110,
            height=48,
            variant="default",
            size="default",
            colors=self.colors,
            command=self._submit,
        )
        self._btn.pack(side="left")

        # Setup container hover/focus animations
        self._setup_container_animations()

    def _setup_container_animations(self):
        """Setup hover and focus animations for the container."""
        def on_enter(_):
            animate_color_transition(
                self._container, "border_color",
                self._container.cget("border_color"),
                self.colors["primary"], ANIM_FAST
            )

        def on_leave(_):
            animate_color_transition(
                self._container, "border_color",
                self._container.cget("border_color"),
                self.colors["card_border"], ANIM_FAST
            )

        self._container.bind("<Enter>", on_enter)
        self._container.bind("<Leave>", on_leave)

    # -------------------------------------------------------------------------
    # Event handlers
    # -------------------------------------------------------------------------

    def _on_focus_in(self, _event):
        """Focus in - show focus ring."""
        animate_color_transition(
            self._container, "border_color",
            self._container.cget("border_color"),
            self.colors["input_focus"], ANIM_FAST
        )
        self._container.configure(border_width=2)

    def _on_return(self, _event):
        self._submit()

    def _on_focus_out(self, _event):
        animate_color_transition(
            self._container, "border_color",
            self._container.cget("border_color"),
            self.colors["card_border"], ANIM_FAST
        )
        self._container.configure(border_width=1)

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def _submit(self):
        city = self._entry.get().strip()
        if city:
            self.on_search(city)

    def set_enabled(self, enabled: bool):
        """Enable or disable the search controls (during API call)."""
        state = "normal" if enabled else "disabled"
        self._entry.configure(state=state)
        self._btn.configure(state=state)

    def clear(self):
        """Clear the search entry field."""
        self._entry.delete(0, "end")

    def set_text(self, text: str):
        """Set the entry text (e.g. when loading a favorite city)."""
        self._entry.delete(0, "end")
        self._entry.insert(0, text)

    def apply_colors(self, colors: dict):
        self.colors = colors
        self._container.configure(
            fg_color=colors["card"],
            border_color=colors["card_border"],
        )
        self._search_icon.configure(text_color=colors["text_muted"])
        self._entry.configure(
            fg_color=colors["input_bg"],
            text_color=colors["text"],
            border_color=colors["input_border"],
            placeholder_text_color=colors["input_placeholder"],
        )
        self._btn.apply_colors(colors)


# Import animate_color_transition for the animations
from utils.animations import animate_color_transition, ease_out_cubic