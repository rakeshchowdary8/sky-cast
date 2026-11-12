"""
components/forecast_card.py — Premium forecast card widgets (shadcn-inspired).

Modern card widgets for hourly and daily forecasts with:
- Clean typography hierarchy
- Smooth hover/tap interactions with elevation
- Current hour/today highlight with animated badges
- Precipitation and UV indicators with semantic colors
- Theme-aware styling with proper tokens
- Staggered entrance animations
"""

import customtkinter as ctk
from config.settings import (
    FONT_TINY, FONT_BODY, FONT_LABEL, FONT_MEDIUM, FONT_SMALL,
    SPACE_1, SPACE_2, SPACE_3, SPACE_4, SPACE_6,
    CARD_CORNER_RADIUS, RADIUS_SM, RADIUS_MD, BADGE_CORNER_RADIUS,
    ANIM_FAST, ANIM_NORMAL,
    METRIC_ACCENTS, STATUS_COLORS,
    ease_out_cubic,
)
from utils.animations import animate_color_transition, stagger_animate_children


class HourlyCard(ctk.CTkFrame):
    """
    Premium hourly forecast card (shadcn-inspired).

    Args:
        parent: Parent widget.
        time_str: Time string (e.g., "2 PM", "Now").
        temp: Temperature string (e.g., "22°").
        condition_icon: Weather emoji (e.g., "☀️").
        precip_prob: Precipitation probability (0-100).
        is_current: Whether this is the current hour.
        colors: Current theme color dict.
    """

    def __init__(self, parent, time_str: str, temp: str, condition_icon: str,
                 precip_prob: int, is_current: bool, colors: dict, **kwargs):
        self.colors = colors
        self.is_current = is_current
        self._animating_hover = False

        # Determine border and accent for current hour
        accent_color = colors["primary"] if is_current else None
        border_color = colors["primary"] if is_current else colors["card_border"]
        border_width = 2 if is_current else 1

        super().__init__(
            parent,
            fg_color=colors["card"],
            corner_radius=CARD_CORNER_RADIUS,
            border_width=border_width,
            border_color=border_color,
            **kwargs,
        )
        self.default_border = border_color
        self._build(time_str, temp, condition_icon, precip_prob, is_current)
        self._animate_entrance()

    def _build(self, time_str: str, temp: str, condition_icon: str,
               precip_prob: int, is_current: bool):
        self.pack_propagate(False)
        self.configure(width=88, height=150, cursor="hand2")

        # Content with padding
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=SPACE_3, pady=SPACE_3)

        # Time label with accent color for current hour
        time_color = self.colors["primary"] if is_current else self.colors["text"]
        time_font = FONT_LABEL if is_current else FONT_SMALL

        self._time_label = ctk.CTkLabel(
            content,
            text=time_str,
            font=time_font,
            text_color=time_color,
        )
        self._time_label.pack(pady=(0, SPACE_1))

        # "Now" badge for current hour - animated
        if is_current:
            self._now_badge = ctk.CTkFrame(
                content,
                fg_color=self.colors["primary"],
                corner_radius=BADGE_CORNER_RADIUS,
            )
            self._now_badge.pack(pady=(0, SPACE_2))
            ctk.CTkLabel(
                self._now_badge,
                text="NOW",
                font=("Inter", 8, "bold"),
                text_color=self.colors["primary_foreground"],
            ).pack(padx=8, pady=SPACE_1)
        else:
            self._now_badge = None

        # Weather icon - larger for better visibility
        self._icon_label = ctk.CTkLabel(
            content,
            text=condition_icon,
            font=("Segoe UI Emoji", 32),
        )
        self._icon_label.pack(pady=SPACE_2)

        # Temperature - prominent
        self._temp_label = ctk.CTkLabel(
            content,
            text=temp,
            font=FONT_MEDIUM,
            text_color=self.colors["text"],
        )
        self._temp_label.pack(pady=(0, SPACE_1))

        # Precipitation probability with semantic color
        self._precip_frame = None
        self._precip_label = None
        if precip_prob > 0:
            self._precip_frame = ctk.CTkFrame(content, fg_color="transparent")
            self._precip_frame.pack()
            ctk.CTkLabel(
                self._precip_frame,
                text="💧",
                font=("Segoe UI Emoji", 10),
            ).pack(side="left")
            self._precip_label = ctk.CTkLabel(
                self._precip_frame,
                text=f"{precip_prob}%",
                font=FONT_TINY,
                text_color=self.colors["secondary"],
            )
            self._precip_label.pack(side="left", padx=(SPACE_1, 0))

        # Bind hover events with smooth animations
        self._bind_hover_events()

    def _animate_entrance(self):
        """Animate card entrance with fade + slide up."""
        # Start slightly below and transparent
        self.place_configure(y=10)
        original_fg = self.cget("fg_color")

        def step_anim(step=0, total=12):
            if step > total:
                self.place_configure(y=0)
                return

            progress = step / total
            eased = ease_out_cubic(progress)
            y = int(10 * (1 - eased))
            self.place_configure(y=y)
            self.after(16, lambda: step_anim(step + 1))

        step_anim()

    def _bind_hover_events(self):
        """Bind hover events with smooth color transitions."""
        def on_enter(_):
            if self._animating_hover or self.is_current:
                return
            self._animating_hover = True
            animate_color_transition(self, "border_color",
                                      self.cget("border_color"), self.colors["primary"], ANIM_FAST)
            animate_color_transition(self, "fg_color",
                                      self.cget("fg_color"), self.colors["card_hover"], ANIM_FAST)
            self._animating_hover = False

        def on_leave(_):
            if self._animating_hover or self.is_current:
                return
            self._animating_hover = True
            animate_color_transition(self, "border_color",
                                      self.cget("border_color"), self.default_border, ANIM_FAST)
            animate_color_transition(self, "fg_color",
                                      self.cget("fg_color"), self.colors["card"], ANIM_FAST)
            self._animating_hover = False

        self.bind("<Enter>", on_enter)
        self.bind("<Leave>", on_leave)

        # Propagate to children
        for child in self.winfo_children():
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)
            for grandchild in child.winfo_children():
                grandchild.bind("<Enter>", on_enter)
                grandchild.bind("<Leave>", on_leave)

    def update_data(self, time_str: str, temp: str, condition_icon: str,
                    precip_prob: int, is_current: bool):
        """Update card data with smooth transitions."""
        self.is_current = is_current

        # Time label
        time_color = self.colors["primary"] if is_current else self.colors["text"]
        time_font = FONT_LABEL if is_current else FONT_SMALL
        self._time_label.configure(text=time_str, font=time_font, text_color=time_color)

        # Now badge
        if is_current and not self._now_badge:
            self._now_badge = ctk.CTkFrame(
                self._time_label.master,
                fg_color=self.colors["primary"],
                corner_radius=BADGE_CORNER_RADIUS,
            )
            self._now_badge.pack(pady=(0, SPACE_2), before=self._icon_label)
            ctk.CTkLabel(
                self._now_badge,
                text="NOW",
                font=("Inter", 8, "bold"),
                text_color=self.colors["primary_foreground"],
            ).pack(padx=8, pady=SPACE_1)
        elif not is_current and self._now_badge:
            self._now_badge.destroy()
            self._now_badge = None

        # Icon and temp
        self._icon_label.configure(text=condition_icon)
        self._temp_label.configure(text=temp)

        # Precipitation
        if self._precip_frame:
            if precip_prob > 0:
                self._precip_label.configure(text=f"{precip_prob}%")
                self._precip_label.pack(side="left", padx=(SPACE_1, 0))
                self._precip_frame.pack()
            else:
                self._precip_frame.pack_forget()
        elif precip_prob > 0:
            self._precip_frame = ctk.CTkFrame(self._temp_label.master, fg_color="transparent")
            self._precip_frame.pack()
            ctk.CTkLabel(self._precip_frame, text="💧", font=("Segoe UI Emoji", 10)).pack(side="left")
            self._precip_label = ctk.CTkLabel(self._precip_frame, text=f"{precip_prob}%",
                                               font=FONT_TINY, text_color=self.colors["secondary"])
            self._precip_label.pack(side="left", padx=(SPACE_1, 0))

        # Border update
        new_border = self.colors["primary"] if is_current else self.colors["card_border"]
        new_width = 2 if is_current else 1
        animate_color_transition(self, "border_color",
                                  self.cget("border_color"), new_border, ANIM_FAST)
        self.configure(border_width=new_width)
        self.default_border = new_border

    def apply_colors(self, colors: dict):
        self.colors = colors
        self.configure(
            fg_color=colors["card"],
            border_color=colors["primary"] if self.is_current else colors["card_border"],
        )
        self.default_border = colors["primary"] if self.is_current else colors["card_border"]
        # Children would need individual updates - simplified


class DailyCard(ctk.CTkFrame):
    """
    Premium daily forecast card (shadcn-inspired).

    Args:
        parent: Parent widget.
        day_str: Day string (e.g., "Mon", "Today").
        date_str: Date string (e.g., "Dec 12").
        high_temp: High temperature (e.g., "25°").
        low_temp: Low temperature (e.g., "14°").
        condition_icon: Weather emoji (e.g., "☀️").
        precip_prob: Max precipitation probability (0-100).
        uv_index: UV index max.
        is_today: Whether this is today.
        colors: Current theme color dict.
    """

    def __init__(self, parent, day_str: str, date_str: str,
                 high_temp: str, low_temp: str, condition_icon: str,
                 precip_prob: int, uv_index: float, is_today: bool,
                 colors: dict, **kwargs):
        self.colors = colors
        self.is_today = is_today
        self._animating_hover = False

        accent_color = colors["primary"] if is_today else None
        border_color = colors["primary"] if is_today else colors["card_border"]
        border_width = 2 if is_today else 1

        super().__init__(
            parent,
            fg_color=colors["card"],
            corner_radius=CARD_CORNER_RADIUS,
            border_width=border_width,
            border_color=border_color,
            **kwargs,
        )
        self.default_border = border_color
        self._build(day_str, date_str, high_temp, low_temp,
                    condition_icon, precip_prob, uv_index, is_today)
        self._animate_entrance()

    def _build(self, day_str: str, date_str: str,
               high_temp: str, low_temp: str, condition_icon: str,
               precip_prob: int, uv_index: float, is_today: bool):
        self.pack_propagate(False)
        self.configure(width=170, height=190, cursor="hand2")

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=SPACE_4, pady=SPACE_4)

        # Day and date row
        day_frame = ctk.CTkFrame(content, fg_color="transparent")
        day_frame.pack(fill="x", pady=(0, SPACE_2))

        day_color = self.colors["primary"] if is_today else self.colors["text"]
        day_font = FONT_LABEL if is_today else FONT_BODY

        self._day_label = ctk.CTkLabel(
            day_frame,
            text=day_str,
            font=day_font,
            text_color=day_color,
        )
        self._day_label.pack(side="left")

        self._date_label = ctk.CTkLabel(
            day_frame,
            text=date_str,
            font=FONT_SMALL,
            text_color=self.colors["text_muted"],
        )
        self._date_label.pack(side="left", padx=(SPACE_2, 0))

        # Today badge
        if is_today:
            self._today_badge = ctk.CTkFrame(
                day_frame,
                fg_color=self.colors["primary"],
                corner_radius=BADGE_CORNER_RADIUS,
            )
            self._today_badge.pack(side="right")
            ctk.CTkLabel(
                self._today_badge,
                text="TODAY",
                font=("Inter", 8, "bold"),
                text_color=self.colors["primary_foreground"],
            ).pack(padx=8, pady=SPACE_1)
        else:
            self._today_badge = None

        # Weather icon - prominent
        self._icon_label = ctk.CTkLabel(
            content,
            text=condition_icon,
            font=("Segoe UI Emoji", 40),
        )
        self._icon_label.pack(pady=SPACE_3)

        # Temperature range - high/low
        temp_frame = ctk.CTkFrame(content, fg_color="transparent")
        temp_frame.pack(fill="x", pady=SPACE_2)

        self._high_label = ctk.CTkLabel(
            temp_frame,
            text=high_temp,
            font=FONT_MEDIUM,
            text_color=self.colors["text"],
        )
        self._high_label.pack(side="left")

        self._low_label = ctk.CTkLabel(
            temp_frame,
            text=low_temp,
            font=FONT_MEDIUM,
            text_color=self.colors["text_secondary"],
        )
        self._low_label.pack(side="right")

        # Details row: precip + UV
        details_frame = ctk.CTkFrame(content, fg_color="transparent")
        details_frame.pack(fill="x", pady=(SPACE_2, 0))

        # Precipitation
        self._precip_frame = None
        self._precip_label = None
        if precip_prob > 0:
            self._precip_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
            self._precip_frame.pack(side="left")
            ctk.CTkLabel(
                self._precip_frame,
                text="💧",
                font=("Segoe UI Emoji", 11),
            ).pack(side="left")
            self._precip_label = ctk.CTkLabel(
                self._precip_frame,
                text=f"{precip_prob}%",
                font=FONT_SMALL,
                text_color=self.colors["secondary"],
            )
            self._precip_label.pack(side="left", padx=(SPACE_1, 0))

        # UV Index with semantic color based on level
        uv_color = self._get_uv_color(uv_index)
        self._uv_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        self._uv_frame.pack(side="right")
        ctk.CTkLabel(
            self._uv_frame,
            text="☀️",
            font=("Segoe UI Emoji", 11),
        ).pack(side="left")
        self._uv_label = ctk.CTkLabel(
            self._uv_frame,
            text=f"UV {int(uv_index)}" if uv_index > 0 else "UV --",
            font=FONT_SMALL,
            text_color=uv_color,
        )
        self._uv_label.pack(side="left", padx=(SPACE_1, 0))

        # Bind hover events
        self._bind_hover_events()

    def _get_uv_color(self, uv_index: float) -> str:
        """Get semantic color for UV index."""
        if uv_index >= 8:
            return self.colors["destructive"]
        elif uv_index >= 6:
            return self.colors["warning"]
        elif uv_index >= 3:
            return self.colors["tertiary"]
        else:
            return self.colors["text_dim"]

    def _animate_entrance(self):
        """Animate card entrance with fade + slide up."""
        self.place_configure(y=10)

        def step_anim(step=0, total=12):
            if step > total:
                self.place_configure(y=0)
                return

            progress = step / total
            eased = ease_out_cubic(progress)
            y = int(10 * (1 - eased))
            self.place_configure(y=y)
            self.after(16, lambda: step_anim(step + 1))

        step_anim()

    def _bind_hover_events(self):
        """Bind hover events with smooth color transitions."""
        def on_enter(_):
            if self._animating_hover or self.is_today:
                return
            self._animating_hover = True
            animate_color_transition(self, "border_color",
                                      self.cget("border_color"), self.colors["primary"], ANIM_FAST)
            animate_color_transition(self, "fg_color",
                                      self.cget("fg_color"), self.colors["card_hover"], ANIM_FAST)
            self._animating_hover = False

        def on_leave(_):
            if self._animating_hover or self.is_today:
                return
            self._animating_hover = True
            animate_color_transition(self, "border_color",
                                      self.cget("border_color"), self.default_border, ANIM_FAST)
            animate_color_transition(self, "fg_color",
                                      self.cget("fg_color"), self.colors["card"], ANIM_FAST)
            self._animating_hover = False

        self.bind("<Enter>", on_enter)
        self.bind("<Leave>", on_leave)

        for child in self.winfo_children():
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)
            for grandchild in child.winfo_children():
                grandchild.bind("<Enter>", on_enter)
                grandchild.bind("<Leave>", on_leave)

    def update_data(self, day_str: str, date_str: str,
                    high_temp: str, low_temp: str, condition_icon: str,
                    precip_prob: int, uv_index: float, is_today: bool):
        """Update card data with smooth transitions."""
        self.is_today = is_today

        day_color = self.colors["primary"] if is_today else self.colors["text"]
        day_font = FONT_LABEL if is_today else FONT_BODY

        self._day_label.configure(text=day_str, font=day_font, text_color=day_color)
        self._date_label.configure(text=date_str)
        self._icon_label.configure(text=condition_icon)
        self._high_label.configure(text=high_temp)
        self._low_label.configure(text=low_temp)

        # Precipitation
        if self._precip_frame:
            if precip_prob > 0:
                self._precip_label.configure(text=f"{precip_prob}%")
                self._precip_label.pack(side="left", padx=(SPACE_1, 0))
                self._precip_frame.pack(side="left")
            else:
                self._precip_frame.pack_forget()
        elif precip_prob > 0:
            self._precip_frame = ctk.CTkFrame(self._uv_frame.master, fg_color="transparent")
            self._precip_frame.pack(side="left")
            ctk.CTkLabel(self._precip_frame, text="💧", font=("Segoe UI Emoji", 11)).pack(side="left")
            self._precip_label = ctk.CTkLabel(self._precip_frame, text=f"{precip_prob}%",
                                               font=FONT_SMALL, text_color=self.colors["secondary"])
            self._precip_label.pack(side="left", padx=(SPACE_1, 0))

        # UV Index
        uv_color = self._get_uv_color(uv_index)
        self._uv_label.configure(
            text=f"UV {int(uv_index)}" if uv_index > 0 else "UV --",
            text_color=uv_color,
        )

        # Today badge
        if is_today and not self._today_badge:
            self._today_badge = ctk.CTkFrame(
                self._day_label.master,
                fg_color=self.colors["primary"],
                corner_radius=BADGE_CORNER_RADIUS,
            )
            self._today_badge.pack(side="right")
            ctk.CTkLabel(
                self._today_badge,
                text="TODAY",
                font=("Inter", 8, "bold"),
                text_color=self.colors["primary_foreground"],
            ).pack(padx=8, pady=SPACE_1)
        elif not is_today and self._today_badge:
            self._today_badge.destroy()
            self._today_badge = None

        # Border update
        new_border = self.colors["primary"] if is_today else self.colors["card_border"]
        new_width = 2 if is_today else 1
        animate_color_transition(self, "border_color",
                                  self.cget("border_color"), new_border, ANIM_FAST)
        self.configure(border_width=new_width)
        self.default_border = new_border

    def apply_colors(self, colors: dict):
        self.colors = colors
        self.configure(
            fg_color=colors["card"],
            border_color=colors["primary"] if self.is_today else colors["card_border"],
        )
        self.default_border = colors["primary"] if self.is_today else colors["card_border"]


def stagger_animate_forecast_cards(parent, card_type="hourly"):
    """Animate forecast cards with staggered entrance."""
    stagger_animate_children(
        parent,
        lambda child, idx: None,  # Cards animate themselves
        delay_per_child=40,
        start_delay=100,
    )