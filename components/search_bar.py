"""
components/search_bar.py — Search input widget with button and status label.
"""

import customtkinter as ctk
from config.settings import FONT_BODY, FONT_SMALL, PAD_SM, BUTTON_CORNER_RADIUS


class SearchBar(ctk.CTkFrame):
    """
    A compact search field + button widget.

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
        # Search entry
        self._entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            width=260,
            height=38,
            font=FONT_BODY,
            fg_color=self.colors["input_bg"],
            text_color=self.colors["text"],
            border_color=self.colors["border"],
            corner_radius=BUTTON_CORNER_RADIUS,
        )
        self._entry.pack(side="left", padx=(0, PAD_SM))
        self._entry.bind("<Return>", self._on_return)

        # Search button
        self._btn = ctk.CTkButton(
            self,
            text="🔍 Search",
            width=100,
            height=38,
            font=FONT_BODY,
            fg_color=self.colors["button"],
            hover_color=self.colors["button_hover"],
            text_color="#ffffff",
            corner_radius=BUTTON_CORNER_RADIUS,
            command=self._submit,
        )
        self._btn.pack(side="left")

    def _on_return(self, _event):
        self._submit()

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
        self._entry.configure(
            fg_color=colors["input_bg"],
            text_color=colors["text"],
            border_color=colors["border"],
        )
        self._btn.configure(
            fg_color=colors["button"],
            hover_color=colors["button_hover"],
        )
