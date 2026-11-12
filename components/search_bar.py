"""
components/search_bar.py — Premium search input with autocomplete suggestions (shadcn-inspired).

Features:
- Real-time city suggestions as you type (debounced)
- Dropdown list with city, country, state info
- Keyboard navigation (Up/Down/Enter/Escape)
- Click to select suggestion
- Modern styling with theme support
- Integrated search icon
- Loading states
- Smooth animations
"""

import customtkinter as ctk
from config.settings import (
    FONT_BODY, FONT_SMALL, FONT_LABEL,
    SPACE_1, SPACE_2, SPACE_3, SPACE_4,
    CARD_CORNER_RADIUS, BUTTON_CORNER_RADIUS, INPUT_CORNER_RADIUS,
    ANIM_FAST, ANIM_NORMAL,
    get_colors,
)
from components.base import Input, Button
from services.geocoding import get_city_suggestions
from concurrent.futures import ThreadPoolExecutor
from utils.animations import animate_color_transition, ease_out_cubic


class SearchBar(ctk.CTkFrame):
    """
    Premium search field with autocomplete dropdown and search button.

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
        self._debounce_ms = 200
        self._is_searching = False
        self._dropdown_visible = False

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

        # Main search entry using base Input component (but embedded)
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
        self._entry.bind("<KeyRelease>", self._on_key_release)
        self._entry.bind("<FocusOut>", self._on_focus_out)
        self._entry.bind("<Down>", self._on_down_key)
        self._entry.bind("<Up>", self._on_up_key)
        self._entry.bind("<Escape>", lambda _: self._hide_suggestions())
        self._entry.bind("<FocusIn>", self._on_focus_in)
        self._entry.bind("<Tab>", self._on_tab_key)

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
            if not self._is_searching and not self._dropdown_visible:
                animate_color_transition(
                    self._container, "border_color",
                    self._container.cget("border_color"),
                    self.colors["primary"], ANIM_FAST
                )

        def on_leave(_):
            if not self._is_searching and not self._dropdown_visible:
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
        """Focus in - show focus ring and potentially show suggestions."""
        animate_color_transition(
            self._container, "border_color",
            self._container.cget("border_color"),
            self.colors["input_focus"], ANIM_FAST
        )
        self._container.configure(border_width=2)

        # Show suggestions if there's a query
        query = self._entry.get().strip()
        if len(query) >= 2 and not self._dropdown_visible:
            self._fetch_suggestions(query)

    def _on_return(self, _event):
        self._hide_suggestions()
        self._submit()

    def _on_tab_key(self, _event):
        """Handle Tab key - select first suggestion if available."""
        if self._dropdown_visible and self._suggestion_buttons:
            self._select_and_search(0)
            return "break"

    def _on_key_release(self, event):
        """Handle key release for autocomplete suggestions."""
        # Ignore navigation keys
        if event.keysym in ("Up", "Down", "Left", "Right", "Return", "Escape", "Tab", "Shift_L", "Shift_R"):
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
        animate_color_transition(
            self._container, "border_color",
            self._container.cget("border_color"),
            self.colors["card_border"], ANIM_FAST
        )
        self._container.configure(border_width=1)

    def _on_down_key(self, _event):
        """Navigate down in suggestions."""
        if self._dropdown_visible and self._suggestion_buttons:
            self._select_suggestion(self._selected_index + 1)
        return "break"

    def _on_up_key(self, _event):
        """Navigate up in suggestions."""
        if self._dropdown_visible and self._suggestion_buttons:
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
        """Display suggestions dropdown with animation."""
        self._hide_suggestions()

        if not suggestions:
            self._dropdown_visible = False
            return

        self._dropdown_visible = True

        # Create dropdown frame with elevated styling
        self._suggestions_frame = ctk.CTkFrame(
            self,
            fg_color=self.colors["card"],
            corner_radius=12,
            border_width=1,
            border_color=self.colors["card_border"],
        )

        # Position below entry container
        self._suggestions_frame.place(
            x=0, y=64, width=520, height=min(len(suggestions) * 52 + 8, 320)
        )
        self._suggestions_frame.lift()

        # Animate dropdown entrance
        self._animate_dropdown_entrance()

        # Add suggestion items
        self._suggestion_buttons = []
        self._selected_index = -1

        for idx, sugg in enumerate(suggestions):
            btn = self._create_suggestion_button(self._suggestions_frame, sugg, idx)
            btn.pack(fill="x", padx=4, pady=2)
            self._suggestion_buttons.append(btn)

        # Auto-select first item
        if self._suggestion_buttons:
            self._select_suggestion(0)

    def _animate_dropdown_entrance(self):
        """Animate dropdown entrance (fade + slide)."""
        # Simple fade-in by temporarily adjusting position
        original_y = 64
        start_y = original_y - 10

        self._suggestions_frame.place_configure(y=start_y)

        def animate_step(step: int, total: int = 10):
            if step > total:
                self._suggestions_frame.place_configure(y=original_y)
                return

            progress = step / total
            eased = ease_out_cubic(progress)
            current_y = int(start_y + (original_y - start_y) * eased)
            self._suggestions_frame.place_configure(y=current_y)
            self.after(16, lambda: animate_step(step + 1))

        animate_step(0)

    def _create_suggestion_button(self, parent, suggestion: dict, index: int) -> ctk.CTkButton:
        """Create a styled suggestion button with shadcn-inspired design."""
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
            height=48,
            anchor="w",
            fg_color="transparent",
            text_color=self.colors["text"],
            hover_color=self.colors["card_hover"],
            corner_radius=8,
            command=lambda i=index: self._select_and_search(i),
        )

        # Add hover animation
        def on_enter(_):
            animate_color_transition(btn, "fg_color",
                                      btn.cget("fg_color"), self.colors["card_hover"], ANIM_FAST)
            animate_color_transition(btn, "text_color",
                                      btn.cget("text_color"), self.colors["primary"], ANIM_FAST)

        def on_leave(_):
            if index != self._selected_index:
                animate_color_transition(btn, "fg_color",
                                          btn.cget("fg_color"), "transparent", ANIM_FAST)
                animate_color_transition(btn, "text_color",
                                          btn.cget("text_color"), self.colors["text"], ANIM_FAST)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def _select_suggestion(self, index: int):
        """Highlight selected suggestion (keyboard navigation)."""
        if not self._suggestion_buttons:
            return

        # Clamp index
        index = max(0, min(index, len(self._suggestion_buttons) - 1))

        # Update previous selection
        if 0 <= self._selected_index < len(self._suggestion_buttons):
            prev_btn = self._suggestion_buttons[self._selected_index]
            animate_color_transition(prev_btn, "fg_color",
                                      prev_btn.cget("fg_color"), "transparent", ANIM_FAST)
            animate_color_transition(prev_btn, "text_color",
                                      prev_btn.cget("text_color"), self.colors["text"], ANIM_FAST)

        # Update new selection
        self._selected_index = index
        curr_btn = self._suggestion_buttons[index]
        animate_color_transition(curr_btn, "fg_color",
                                  curr_btn.cget("fg_color"), self.colors["primary_light"], ANIM_FAST)
        animate_color_transition(curr_btn, "text_color",
                                  curr_btn.cget("text_color"), self.colors["primary"], ANIM_FAST)

        # Scroll into view if needed
        curr_btn.focus_set()

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
            self._dropdown_visible = False

    def _show_loading(self, show: bool):
        """Show/hide loading indicator in button."""
        self._is_searching = show
        if show:
            self._btn.set_loading(True)
            animate_color_transition(
                self._container, "border_color",
                self._container.cget("border_color"),
                self.colors["primary"], ANIM_FAST
            )
        else:
            self._btn.set_loading(False)
            if not self._dropdown_visible:
                animate_color_transition(
                    self._container, "border_color",
                    self._container.cget("border_color"),
                    self.colors["card_border"], ANIM_FAST
                )

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

        if self._suggestions_frame:
            self._suggestions_frame.configure(
                fg_color=colors["card"],
                border_color=colors["card_border"],
            )
            for btn in self._suggestion_buttons:
                btn.configure(
                    text_color=colors["text"],
                    hover_color=colors["card_hover"],
                )
                # Re-apply selection highlight
                if btn.cget("fg_color") != "transparent":
                    btn.configure(fg_color=colors["primary_light"], text_color=colors["primary"])