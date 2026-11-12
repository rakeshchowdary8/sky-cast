"""
components/sidebar.py — Premium collapsible sidebar with smooth animations (shadcn-inspired).

Features:
- Smooth width animation (expanded ↔ collapsed) with cubic easing
- Animated indicator for active nav item
- Toggle button with chevron animation
- Shadcn-inspired visual design with proper tokens
- Full theme consistency
- Staggered entrance animations
"""

import customtkinter as ctk
from config.settings import (
    SIDEBAR_WIDTH_EXPANDED, SIDEBAR_WIDTH_COLLAPSED,
    SPACE_1, SPACE_2, SPACE_3, SPACE_4, SPACE_6, SPACE_8,
    FONT_TINY, FONT_LABEL, FONT_DISPLAY, FONT_TITLE,
    CARD_CORNER_RADIUS, RADIUS_MD,
    ANIM_NORMAL, ANIM_FAST, ANIM_SLOW,
    EASING_EASE_OUT, EASING_EASE_IN_OUT,
    ease_out_cubic, ease_in_out_cubic,
    get_colors,
)
from utils.animations import animate_color_transition, animate_sidebar_toggle


class Sidebar(ctk.CTkFrame):
    """
    Premium collapsible navigation sidebar with smooth animations.

    Args:
        parent: Parent widget.
        on_navigate: Callback(view_name: str) called on button click.
        colors: Current theme color dict.
        on_toggle: Optional callback(is_expanded: bool) when sidebar toggles.
    """

    NAV_ITEMS = [
        ("dashboard",  "🏠", "Dashboard"),
        ("favorites",  "⭐", "Favorites"),
        ("history",    "🕒", "Search History"),
        ("whistory",   "📊", "Weather History"),
        ("settings",   "⚙️", "Settings"),
    ]

    def __init__(self, parent, on_navigate, colors: dict, on_toggle=None, **kwargs):
        super().__init__(
            parent,
            width=SIDEBAR_WIDTH_EXPANDED,
            corner_radius=0,
            fg_color=colors["sidebar"],
            **kwargs,
        )
        self.on_navigate = on_navigate
        self.on_toggle = on_toggle
        self.colors = colors
        self._buttons: dict[str, ctk.CTkFrame] = {}
        self._icon_labels: dict[str, ctk.CTkLabel] = {}
        self._text_labels: dict[str, ctk.CTkLabel] = {}
        self._btn_frames: dict[str, ctk.CTkFrame] = {}
        self._active_view = "dashboard"
        self._indicator = None
        self._is_expanded = True
        self._animating = False
        self._logo_text_widgets = []

        # Staggered animation state
        self._nav_items_animated = False

        self._build()
        self._animate_entrance()

    def _build(self):
        self.pack_propagate(False)

        # --- Header with logo + toggle button ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=SPACE_4, pady=(SPACE_8, SPACE_4))

        # Logo icon
        self._logo_icon = ctk.CTkLabel(
            header_frame,
            text="☁️",
            font=("Segoe UI Emoji", 28),
            fg_color="transparent",
            cursor="hand2",
        )
        self._logo_icon.pack(side="left", padx=(SPACE_3, 0))
        self._logo_text_widgets.append(self._logo_icon)

        # App name (hidden when collapsed)
        name_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        name_frame.pack(side="left", fill="x", expand=True, padx=(SPACE_3, 0))

        self._logo_sky = ctk.CTkLabel(
            name_frame,
            text="Sky",
            font=FONT_TITLE,
            text_color=self.colors["text"],
        )
        self._logo_sky.pack(side="left")
        self._logo_text_widgets.append(self._logo_sky)

        self._logo_cast = ctk.CTkLabel(
            name_frame,
            text="Cast",
            font=FONT_TITLE,
            text_color=self.colors["primary"],
        )
        self._logo_cast.pack(side="left")
        self._logo_text_widgets.append(self._logo_cast)

        self._logo_tagline = ctk.CTkLabel(
            name_frame,
            text="Premium Weather",
            font=FONT_TINY,
            text_color=self.colors["text_muted"],
        )
        self._logo_tagline.pack(side="left", padx=(SPACE_1, 0), anchor="s")
        self._logo_text_widgets.append(self._logo_tagline)

        # Toggle button (chevron) - shadcn ghost variant
        self._toggle_btn = ctk.CTkButton(
            header_frame,
            text="◀",
            width=36,
            height=36,
            font=("Segoe UI Emoji", 16),
            fg_color="transparent",
            text_color=self.colors["text_muted"],
            hover_color=self.colors["card_hover"],
            corner_radius=RADIUS_MD,
            command=self._toggle_sidebar,
        )
        self._toggle_btn.pack(side="right", padx=(0, SPACE_2))

        # Setup hover animation for toggle button
        self._setup_toggle_hover()

        # Divider
        divider = ctk.CTkFrame(self, height=1, fg_color=self.colors["divider"])
        divider.pack(fill="x", padx=SPACE_4, pady=SPACE_4)

        # --- Navigation buttons ---
        self._nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._nav_frame.pack(fill="x", padx=SPACE_2, pady=SPACE_2)

        for view_name, icon, label in self.NAV_ITEMS:
            self._create_nav_item(view_name, icon, label)

        # Create active indicator (animated bar on left)
        self._indicator = ctk.CTkFrame(
            self._nav_frame,
            width=3,
            height=44,
            fg_color=self.colors["primary"],
            corner_radius=2,
        )

        # Version label at bottom (hidden when collapsed)
        version_frame = ctk.CTkFrame(self, fg_color="transparent")
        version_frame.pack(side="bottom", fill="x", padx=SPACE_4, pady=SPACE_8)
        self._version_frame = version_frame

        self._version_label = ctk.CTkLabel(
            version_frame,
            text=f"v{APP_VERSION}" if 'APP_VERSION' in globals() else "v2.1.0",
            font=FONT_TINY,
            text_color=self.colors["text_muted"],
        )
        self._version_label.pack(side="left")

        # Theme toggle button at bottom
        self._theme_btn = ctk.CTkButton(
            version_frame,
            text="🌙",
            width=36,
            height=36,
            font=("Segoe UI Emoji", 16),
            fg_color="transparent",
            text_color=self.colors["text_muted"],
            hover_color=self.colors["card_hover"],
            corner_radius=RADIUS_MD,
            command=self._toggle_theme,
        )
        self._theme_btn.pack(side="right")
        self._setup_theme_btn_hover()

        # Activate default (without animation initially)
        self._set_active("dashboard", animate=False)

    def _create_nav_item(self, view_name: str, icon: str, label: str):
        """Create a navigation item with icon and label."""
        btn_frame = ctk.CTkFrame(self._nav_frame, fg_color="transparent", height=44)
        btn_frame.pack(fill="x", pady=SPACE_1)
        btn_frame.pack_propagate(False)
        self._btn_frames[view_name] = btn_frame

        # Icon label (always visible)
        icon_lbl = ctk.CTkLabel(
            btn_frame,
            text=icon,
            font=("Segoe UI Emoji", 20),
            text_color=self.colors["text_muted"],
            fg_color="transparent",
            width=44,
        )
        icon_lbl.pack(side="left", padx=(SPACE_4, SPACE_3))
        self._icon_labels[view_name] = icon_lbl

        # Text label (hidden when collapsed)
        text_lbl = ctk.CTkLabel(
            btn_frame,
            text=label,
            font=FONT_LABEL,
            text_color=self.colors["text_muted"],
            fg_color="transparent",
            cursor="hand2",
        )
        text_lbl.pack(side="left", fill="x", expand=True, anchor="w")
        self._text_labels[view_name] = text_lbl

        # Click handler on entire row
        for w in (btn_frame, icon_lbl, text_lbl):
            w.bind("<Button-1>", lambda e, v=view_name: self._on_click(v))
            w.configure(cursor="hand2")

        # Hover animation for the whole row
        def on_enter(_):
            if view_name != self._active_view:
                animate_color_transition(btn_frame, "fg_color",
                                          "transparent", self.colors["card_hover"], ANIM_FAST)
                animate_color_transition(icon_lbl, "text_color",
                                          icon_lbl.cget("text_color"), self.colors["text"], ANIM_FAST)
                animate_color_transition(text_lbl, "text_color",
                                          text_lbl.cget("text_color"), self.colors["text"], ANIM_FAST)

        def on_leave(_):
            if view_name != self._active_view:
                animate_color_transition(btn_frame, "fg_color",
                                          btn_frame.cget("fg_color"), "transparent", ANIM_FAST)
                animate_color_transition(icon_lbl, "text_color",
                                          icon_lbl.cget("text_color"), self.colors["text_muted"], ANIM_FAST)
                animate_color_transition(text_lbl, "text_color",
                                          text_lbl.cget("text_color"), self.colors["text_muted"], ANIM_FAST)

        btn_frame.bind("<Enter>", on_enter)
        btn_frame.bind("<Leave>", on_leave)

    def _setup_toggle_hover(self):
        """Setup hover animation for toggle button."""
        def on_enter(_):
            animate_color_transition(self._toggle_btn, "fg_color",
                                      "transparent", self.colors["card_hover"], ANIM_FAST)
            animate_color_transition(self._toggle_btn, "text_color",
                                      self._toggle_btn.cget("text_color"), self.colors["text"], ANIM_FAST)

        def on_leave(_):
            animate_color_transition(self._toggle_btn, "fg_color",
                                      self._toggle_btn.cget("fg_color"), "transparent", ANIM_FAST)
            animate_color_transition(self._toggle_btn, "text_color",
                                      self._toggle_btn.cget("text_color"), self.colors["text_muted"], ANIM_FAST)

        self._toggle_btn.bind("<Enter>", on_enter)
        self._toggle_btn.bind("<Leave>", on_leave)

    def _setup_theme_btn_hover(self):
        """Setup hover animation for theme toggle button."""
        def on_enter(_):
            animate_color_transition(self._theme_btn, "fg_color",
                                      "transparent", self.colors["card_hover"], ANIM_FAST)
            animate_color_transition(self._theme_btn, "text_color",
                                      self._theme_btn.cget("text_color"), self.colors["text"], ANIM_FAST)

        def on_leave(_):
            animate_color_transition(self._theme_btn, "fg_color",
                                      self._theme_btn.cget("fg_color"), "transparent", ANIM_FAST)
            animate_color_transition(self._theme_btn, "text_color",
                                      self._theme_btn.cget("text_color"), self.colors["text_muted"], ANIM_FAST)

        self._theme_btn.bind("<Enter>", on_enter)
        self._theme_btn.bind("<Leave>", on_leave)

    def _animate_entrance(self):
        """Staggered entrance animation for nav items."""
        if self._nav_items_animated:
            return
        self._nav_items_animated = True

        def animate_item(view_name: str, delay: int):
            btn_frame = self._btn_frames.get(view_name)
            if not btn_frame:
                return

            # Start off-screen
            btn_frame.place_configure(x=-30)

            def step_anim(step=0, total=10):
                if step > total:
                    btn_frame.place_configure(x=0)
                    btn_frame.pack(fill="x", pady=SPACE_1)
                    btn_frame.place_forget()
                    return

                progress = step / total
                eased = ease_out_cubic(progress)
                x = int(-30 * (1 - eased))
                btn_frame.place_configure(x=x)
                self.after(16, lambda: step_anim(step + 1))

            self.after(delay, lambda: (btn_frame.place(x=-30, y=btn_frame.winfo_y(), relwidth=1), step_anim()))

        for i, (view_name, _, _) in enumerate(self.NAV_ITEMS):
            animate_item(view_name, i * 60)

    def _on_click(self, view_name: str):
        self._set_active(view_name)
        self.on_navigate(view_name)

    def _set_active(self, view_name: str, animate=True):
        """Highlight the active nav button with smooth indicator animation."""
        # Reset previous
        if self._active_view in self._icon_labels:
            self._icon_labels[self._active_view].configure(text_color=self.colors["text_muted"])
        if self._active_view in self._text_labels:
            self._text_labels[self._active_view].configure(text_color=self.colors["text_muted"])
        if self._active_view in self._btn_frames:
            self._btn_frames[self._active_view].configure(fg_color="transparent")

        # Activate new
        self._active_view = view_name
        if view_name in self._icon_labels:
            self._icon_labels[view_name].configure(text_color=self.colors["primary"])
        if view_name in self._text_labels:
            self._text_labels[view_name].configure(text_color=self.colors["primary"])
        if view_name in self._btn_frames:
            self._btn_frames[view_name].configure(fg_color=self.colors["primary_light"])

        # Move indicator to active button
        if animate:
            self._animate_indicator(view_name)
        else:
            btn_frame = self._btn_frames.get(view_name)
            if btn_frame:
                target_y = btn_frame.winfo_y() + 3
                self._indicator.place(x=0, y=target_y)
                self._indicator.lift()

    def _animate_indicator(self, view_name: str):
        """Animate indicator to target button position with easing."""
        btn_frame = self._btn_frames.get(view_name)
        if not btn_frame:
            return

        target_y = btn_frame.winfo_y() + 3

        def animate_step(current_y, target_y, step=0):
            total_steps = 12
            if step >= total_steps:
                self._indicator.place(x=0, y=target_y)
                return

            progress = step / total_steps
            eased = ease_out_cubic(progress)
            current_y = current_y + (target_y - current_y) * eased

            self._indicator.place(x=0, y=int(current_y))
            self.after(ANIM_NORMAL // total_steps, lambda: animate_step(current_y, target_y, step + 1))

        current_y = self._indicator.winfo_y() if self._indicator.winfo_ismapped() else target_y
        animate_step(current_y, target_y)
        self._indicator.lift()

    def _toggle_sidebar(self):
        """Toggle sidebar expanded/collapsed state with smooth animation."""
        if self._animating:
            return

        self._animating = True
        self._is_expanded = not self._is_expanded

        target_width = SIDEBAR_WIDTH_EXPANDED if self._is_expanded else SIDEBAR_WIDTH_COLLAPSED

        # Update toggle button icon with animation
        new_icon = "▶" if self._is_expanded else "◀"
        self._animate_toggle_icon(new_icon)

        # Use the animation utility
        animate_sidebar_toggle(self, self._is_expanded, self._on_animation_complete)

    def _animate_toggle_icon(self, new_icon: str):
        """Animate toggle button icon change."""
        # Quick scale animation simulation
        self._toggle_btn.configure(text=new_icon)

    def _on_animation_complete(self):
        """Called when sidebar width animation completes."""
        self._animating = False
        self._update_collapsed_state(instant=True)
        if self.on_toggle:
            self.on_toggle(self._is_expanded)

    def _update_collapsed_state(self, instant=False):
        """Update visibility of text elements based on collapsed state."""
        show_text = self._is_expanded

        for view_name in self._text_labels:
            if show_text:
                self._text_labels[view_name].pack(side="left", fill="x", expand=True, anchor="w")
            else:
                self._text_labels[view_name].pack_forget()

        # Logo text
        for w in self._logo_text_widgets[1:]:  # Skip icon
            if show_text:
                w.pack(side="left")
            else:
                w.pack_forget()

        # Version label
        if show_text:
            self._version_label.pack(side="left")
        else:
            self._version_label.pack_forget()

        # Adjust button frames for icon-only mode
        if not self._is_expanded:
            # Center the icon in collapsed mode
            for view_name in self._btn_frames:
                self._icon_labels[view_name].pack_configure(padx=(SPACE_6, SPACE_6))
        else:
            for view_name in self._btn_frames:
                self._icon_labels[view_name].pack_configure(padx=(SPACE_4, SPACE_3))

    def _toggle_theme(self):
        """Toggle theme - delegate to main app."""
        # This will be connected via the main app
        if hasattr(self, '_theme_callback'):
            self._theme_callback()

    def set_theme_callback(self, callback):
        """Set theme toggle callback."""
        self._theme_callback = callback

    def apply_colors(self, colors: dict):
        """Re-apply colors after a theme change."""
        self.colors = colors
        self.configure(fg_color=colors["sidebar"])
        self._indicator.configure(fg_color=colors["primary"])

        # Logo
        self._logo_sky.configure(text_color=colors["text"])
        self._logo_cast.configure(text_color=colors["primary"])
        self._logo_tagline.configure(text_color=colors["text_muted"])
        self._logo_icon.configure(text_color=colors["text"])

        # Toggle button
        self._toggle_btn.configure(
            text_color=colors["text_muted"],
            hover_color=colors["card_hover"],
        )
        self._theme_btn.configure(
            text_color=colors["text_muted"],
            hover_color=colors["card_hover"],
        )

        # Version
        self._version_label.configure(text_color=colors["text_muted"])

        # Nav items
        self._set_active(self._active_view, animate=False)
        for name in self._icon_labels:
            is_active = (name == self._active_view)
            self._icon_labels[name].configure(
                text_color=colors["primary"] if is_active else colors["text_muted"],
            )
            if name in self._text_labels:
                self._text_labels[name].configure(
                    text_color=colors["primary"] if is_active else colors["text_muted"],
                )
            if name in self._btn_frames:
                self._btn_frames[name].configure(
                    fg_color=colors["primary_light"] if is_active else "transparent",
                )

        # Re-setup hover animations with new colors
        self._setup_toggle_hover()
        self._setup_theme_btn_hover()

    # Public API
    def is_expanded(self) -> bool:
        return self._is_expanded

    def toggle(self):
        """Public method to toggle sidebar programmatically."""
        self._toggle_sidebar()

    def expand(self):
        if not self._is_expanded:
            self._toggle_sidebar()

    def collapse(self):
        if self._is_expanded:
            self._toggle_sidebar()