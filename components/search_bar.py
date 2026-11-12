"""
components/search_bar.py — Modern search input with autocomplete suggestions.

Features:
- Real-time city suggestions as you type (debounced)
- Dropdown list with city, country, state info
- Keyboard navigation (Up/Down/Enter/Escape)
- Click to select suggestion
- Modern styling with theme support
"""

import customtkinter as ctk
from config.settings import (
    FONT_BODY, FONT_SMALL, PAD_SM, BUTTON_CORNER_RADIUS,
    PAD_XS, PAD_MD,
)
from services.geocoding import get_city_suggestions
from concurrent.futures import ThreadPoolExecutor
import threading


class SearchBar(ctk.CTkFrame):
    """
    Modern search field with autocomplete dropdown and search button.

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
        self._executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="suggest")
        self._suggestion_timer = None
        self._suggestions_frame = None
        self._suggestion_buttons = []
        self._selected_index = -1
        self._last_query = ""
        self._debounce_ms = 200  # ms to wait before fetching suggestions

        self._build(placeholder)

    def _build(self, placeholder: str):
        # Main search entry with modern styling
        self._entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            width=300,
            height=44,
            font=FONT_BODY,
            fg_color=self.colors["input_bg"],
            text_color=self.colors["text"],
            border_color=self.colors["border"],
            corner_radius=BUTTON_CORNER_RADIUS,
        )
        self._entry.pack(side="left", padx=(0, PAD_SM), fill="x", expand=True)
        self._entry.bind("<Return>", self._on_return)
        self._entry.bind("<KeyRelease>", self._on_key_release)
        self._entry.bind("<FocusOut>", self._on_focus_out)
        self._entry.bind("<Down>", self._on_down_key)
        self._entry.bind("<Up>", self._on_up_key)
        self._entry.bind("<Escape>", lambda _: self._hide_suggestions())

        # Search button with icon
        self._btn = ctk.CTkButton(
            self,
            text="🔍  Search",
            width=120,
            height=44,
            font=FONT_BODY,
            fg_color=self.colors["button"],
            hover_color=self.colors["button_hover"],
            text_color="#ffffff",
            corner_radius=BUTTON_CORNER_RADIUS,
            command=self._submit,
        )
        self._btn.pack(side="left")

        # Loading indicator (hidden by default)
        self._loading_label = ctk.CTkLabel(
            self, text="", font=("Segoe UI Emoji", 14), text_color=self.colors["text_dim"]
        )

    # -------------------------------------------------------------------------
    # Event handlers
    # -------------------------------------------------------------------------

    def _on_return(self, _event):
        self._hide_suggestions()
        self._submit()

    def _on_key_release(self, event):
        """Handle key release for autocomplete suggestions."""
        # Ignore navigation keys
        if event.keysym in ("Up", "Down", "Left", "Right", "Return", "Escape", "Tab"):
            return

        query = self._entry.get().strip()

        # Cancel previous timer
        if self._suggestion_timer:
            self.after_cancel(self._suggestion_timer)

        # Debounce: wait before fetching
        if len(query) >= 2 and query != self._last_query:
            self._suggestion_timer = self.after(
                self._debounce_ms, lambda: self._fetch_suggestions(query)
            )
        elif len(query) < 2:
            self._hide_suggestions()

    def _on_focus_out(self, _event):
        """Hide suggestions when focus leaves (with small delay for click)."""
        self.after(150, self._hide_suggestions)

    def _on_down_key(self, _event):
        """Navigate down in suggestions."""
        if self._suggestions_frame and self._suggestions_frame.winfo_viewable():
            self._select_suggestion(self._selected_index + 1)
        return "break"  # Prevent cursor movement

    def _on_up_key(self, _event):
        """Navigate up in suggestions."""
        if self._suggestions_frame and self._suggestions_frame.winfo_viewable():
            self._select_suggestion(self._selected_index - 1)
        return "break"

    def _fetch_suggestions(self, query: str):
        """Fetch city suggestions in background thread."""
        self._last_query = query
        self._show_loading(True)
        self._executor.submit(self._bg_get_suggestions, query)

    def _bg_get_suggestions(self, query: str):
        """Background thread: fetch suggestions."""
        try:
            suggestions = get_city_suggestions(query, max_results=8)
            self.after(0, lambda: self._show_suggestions(suggestions))
        except Exception:
            self.after(0, self._hide_suggestions)
        finally:
            self.after(0, lambda: self._show_loading(False))

    # -------------------------------------------------------------------------
    # Suggestion dropdown UI
    # -------------------------------------------------------------------------

    def _show_suggestions(self, suggestions: list[dict]):
        """Display suggestions dropdown."""
        self._hide_suggestions()

        if not suggestions:
            return

        # Create dropdown frame
        self._suggestions_frame = ctk.CTkFrame(
            self,
            fg_color=self.colors["card"],
            corner_radius=8,
            border_width=1,
            border_color=self.colors["border"],
        )
        # Position below entry
        self._suggestions_frame.place(
            x=0, y=48, width=300, height=min(len(suggestions) * 44 + 8, 300)
        )
        self._suggestions_frame.lift()

        # Add suggestion items
        self._suggestion_buttons = []
        self._selected_index = -1

        for idx, sugg in enumerate(suggestions):
            btn = self._create_suggestion_button(self._suggestions_frame, sugg, idx)
            btn.pack(fill="x", padx=4, pady=2)
            self._suggestion_buttons.append(btn)

    def _create_suggestion_button(self, parent, suggestion: dict, index: int) -> ctk.CTkButton:
        """Create a styled suggestion button."""
        city = suggestion["city"]
        country = suggestion.get("country", "")
        admin1 = suggestion.get("admin1", "")

        # Build display text
        parts = [city]
        if admin1 and admin1 != city:
            parts.append(admin1)
        if country:
            parts.append(country)
        display_text = "  •  ".join(parts)

        btn = ctk.CTkButton(
            parent,
            text=display_text,
            font=FONT_SMALL,
            height=38,
            anchor="w",
            fg_color="transparent",
            text_color=self.colors["text"],
            hover_color=self.colors["card_hover"],
            corner_radius=6,
            command=lambda i=index: self._select_and_search(i),
        )
        return btn

    def _select_suggestion(self, index: int):
        """Highlight selected suggestion (keyboard navigation)."""
        if not self._suggestion_buttons:
            return

        # Clamp index
        index = max(0, min(index, len(self._suggestion_buttons) - 1))

        # Update previous selection
        if 0 <= self._selected_index < len(self._suggestion_buttons):
            self._suggestion_buttons[self._selected_index].configure(
                fg_color="transparent",
                text_color=self.colors["text"],
            )

        # Update new selection
        self._selected_index = index
        self._suggestion_buttons[index].configure(
            fg_color=self.colors["accent"],
            text_color="#ffffff",
        )
        # Scroll into view if needed
        self._suggestion_buttons[index].focus_set()

    def _select_and_search(self, index: int):
        """User clicked a suggestion - fill entry and search."""
        if 0 <= index < len(self._suggestion_buttons):
            btn = self._suggestion_buttons[index]
            text = btn.cget("text")
            # Extract city name (first part before "  •  ")
            city = text.split("  •  ")[0].strip()
            self._entry.delete(0, "end")
            self._entry.insert(0, city)
            self._hide_suggestions()
            self._submit()

    def _hide_suggestions(self):
        """Hide the suggestions dropdown."""
        if self._suggestions_frame:
            self._suggestions_frame.destroy()
            self._suggestions_frame = None
            self._suggestion_buttons = []
            self._selected_index = -1

    def _show_loading(self, show: bool):
        """Show/hide loading indicator in button."""
        if show:
            self._btn.configure(text="⏳", state="disabled", width=44)
        else:
            self._btn.configure(text="🔍  Search", state="normal", width=120)

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def _submit(self):
        city = self._entry.get().strip()
        if city:
            self._hide_suggestions()
            self.on_search(city)

    def set_enabled(self, enabled: bool):
        """Enable or disable the search controls (during API call)."""
        state = "normal" if enabled else "disabled"
        self._entry.configure(state=state)
        self._btn.configure(state=state)

    def clear(self):
        """Clear the search entry field."""
        self._entry.delete(0, "end")
        self._hide_suggestions()

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
        if self._suggestions_frame:
            self._suggestions_frame.configure(
                fg_color=colors["card"],
                border_color=colors["border"],
            )
            for btn in self._suggestion_buttons:
                btn.configure(
                    text_color=colors["text"],
                    hover_color=colors["card_hover"],
                )
                # Re-apply selection highlight
                if btn.cget("fg_color") == self.colors.get("accent", "#e94560"):
                    btn.configure(fg_color=colors["accent"], text_color="#ffffff")