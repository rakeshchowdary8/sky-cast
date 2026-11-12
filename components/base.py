"""
components/base.py — Base UI components with shadcn-inspired design system.

Provides reusable styled components:
- Card, Button, Input, Badge, Separator, Avatar, Tooltip
- Consistent theming, hover states, focus rings, animations
"""

import customtkinter as ctk
from config.settings import (
    get_colors, get_button_config, get_input_config,
    CARD_CORNER_RADIUS, BUTTON_CORNER_RADIUS, INPUT_CORNER_RADIUS,
    BADGE_CORNER_RADIUS, RADIUS_SM, RADIUS_MD, RADIUS_LG, RADIUS_XL,
    FONT_BODY, FONT_LABEL, FONT_SMALL, FONT_MEDIUM, FONT_LARGE,
    SPACE_1, SPACE_2, SPACE_3, SPACE_4, SPACE_6, SPACE_8,
    ANIM_FAST, ANIM_NORMAL,
)
from utils.animations import (
    animate_color_transition, setup_hover_animation, setup_focus_ring,
    animate_button_press, pulse_animation,
)


# ---------------------------------------------------------------------------
# Card Component
# ---------------------------------------------------------------------------

class Card(ctk.CTkFrame):
    """
    shadcn-inspired Card component.

    Variants: default, outlined, elevated, ghost
    """

    def __init__(self, parent, variant: str = "default", padding: int = SPACE_6,
                 colors: dict = None, **kwargs):
        self.colors = colors or get_colors()
        self.variant = variant

        # Base configuration
        cfg = {
            "corner_radius": CARD_CORNER_RADIUS,
            "fg_color": self.colors["card"],
        }

        if variant == "outlined":
            cfg["border_width"] = 1
            cfg["border_color"] = self.colors["card_border"]
        elif variant == "elevated":
            cfg["border_width"] = 1
            cfg["border_color"] = self.colors["card_border"]
        elif variant == "ghost":
            cfg["fg_color"] = "transparent"
            cfg["border_width"] = 0

        super().__init__(parent, **cfg, **kwargs)

        # Inner content frame with padding
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=padding, pady=padding)

        # Setup hover animation for interactive cards
        if variant in ("default", "outlined", "elevated"):
            setup_hover_animation(
                self, self.colors,
                prop="fg_color",
                hover_color_key="card_hover",
                normal_color_key="card",
                duration=ANIM_FAST
            )

    def apply_colors(self, colors: dict):
        """Update colors for theme change."""
        self.colors = colors
        self.configure(fg_color=colors["card"])
        if self.variant == "outlined":
            self.configure(border_color=colors["card_border"])


class CardHeader(ctk.CTkFrame):
    """Card header with title and optional action."""

    def __init__(self, parent, title: str, description: str = None,
                 action_widget=None, colors: dict = None, **kwargs):
        self.colors = colors or get_colors()
        super().__init__(parent, fg_color="transparent", **kwargs)

        # Title area
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", side="left", expand=True)

        ctk.CTkLabel(
            title_frame, text=title,
            font=FONT_LARGE, text_color=self.colors["text"],
        ).pack(anchor="w")

        if description:
            ctk.CTkLabel(
                title_frame, text=description,
                font=FONT_SMALL, text_color=self.colors["text_muted"],
            ).pack(anchor="w", pady=(SPACE_1, 0))

        # Action widget on right
        if action_widget:
            action_widget.pack(side="right", padx=(SPACE_4, 0))


class CardContent(ctk.CTkFrame):
    """Card content area."""

    def __init__(self, parent, colors: dict = None, **kwargs):
        self.colors = colors or get_colors()
        super().__init__(parent, fg_color="transparent", **kwargs)


class CardFooter(ctk.CTkFrame):
    """Card footer with actions."""

    def __init__(self, parent, colors: dict = None, **kwargs):
        self.colors = colors or get_colors()
        super().__init__(parent, fg_color="transparent", **kwargs)
        # Add top border
        separator = ctk.CTkFrame(self, height=1, fg_color=self.colors["divider"])
        separator.pack(fill="x", pady=(0, SPACE_4))


# ---------------------------------------------------------------------------
# Button Component (shadcn variants)
# ---------------------------------------------------------------------------

class Button(ctk.CTkButton):
    """
    shadcn-inspired Button with variants and sizes.

    Variants: default, secondary, outline, ghost, destructive
    Sizes: sm, default, lg, xl, icon
    """

    def __init__(self, parent, variant: str = "default", size: str = "default",
                 colors: dict = None, loading: bool = False, **kwargs):
        self.colors = colors or get_colors()
        self.variant = variant
        self.size = size
        self.loading = loading
        self._original_text = kwargs.get("text", "")

        # Get configuration
        cfg = get_button_config(variant, size, self.colors)

        # Filter out non-CTkButton kwargs (padding_x, radius are for internal use)
        valid_kwargs = {k: v for k, v in cfg.items() if k not in ("padding_x", "radius")}

        # Merge with user kwargs (user kwargs take precedence)
        for key, value in valid_kwargs.items():
            if key not in kwargs:
                kwargs[key] = value

        # Ensure corner_radius is set
        if "corner_radius" not in kwargs:
            kwargs["corner_radius"] = cfg.get("radius", BUTTON_CORNER_RADIUS)

        super().__init__(parent, **kwargs)

        # Setup animations
        self._setup_animations()

        if loading:
            self.set_loading(True)

    def _setup_animations(self):
        """Setup hover, focus, and press animations."""
        # Hover animation
        if self.variant == "default":
            setup_hover_animation(
                self, self.colors,
                prop="fg_color",
                hover_color_key="btn_primary_hover",
                normal_color_key="btn_primary_bg",
                duration=ANIM_FAST
            )
        elif self.variant == "secondary":
            setup_hover_animation(
                self, self.colors,
                prop="fg_color",
                hover_color_key="btn_secondary_hover",
                normal_color_key="btn_secondary_bg",
                duration=ANIM_FAST
            )
        elif self.variant == "outline":
            setup_hover_animation(
                self, self.colors,
                prop="fg_color",
                hover_color_key="btn_outline_hover",
                normal_color_key="btn_outline_bg",
                duration=ANIM_FAST
            )
        elif self.variant == "ghost":
            setup_hover_animation(
                self, self.colors,
                prop="fg_color",
                hover_color_key="btn_ghost_hover",
                normal_color_key="btn_ghost_bg",
                duration=ANIM_FAST
            )
        elif self.variant == "destructive":
            setup_hover_animation(
                self, self.colors,
                prop="fg_color",
                hover_color_key="btn_destructive_hover",
                normal_color_key="btn_destructive_bg",
                duration=ANIM_FAST
            )

        # Press animation
        animate_button_press(self, self.colors)

        # Focus ring
        setup_focus_ring(self, self.colors)

    def set_loading(self, loading: bool):
        """Set loading state with spinner."""
        self.loading = loading
        if loading:
            self._original_text = self.cget("text")
            self.configure(text="⏳", state="disabled")
        else:
            self.configure(text=self._original_text, state="normal")

    def apply_colors(self, colors: dict):
        """Update colors for theme change."""
        self.colors = colors
        cfg = get_button_config(self.variant, self.size, colors)
        self.configure(
            fg_color=cfg["fg_color"],
            hover_color=cfg["hover_color"],
            text_color=cfg["text_color"],
        )
        if cfg.get("border_width"):
            self.configure(
                border_width=cfg["border_width"],
                border_color=cfg["border_color"]
            )
        self._setup_animations()


# ---------------------------------------------------------------------------
# Input Component
# ---------------------------------------------------------------------------

class Input(ctk.CTkEntry):
    """
    shadcn-inspired Input with label, error state, and focus ring.
    """

    def __init__(self, parent, label: str = None, placeholder: str = "",
                 size: str = "default", colors: dict = None, error: bool = False,
                 left_icon: str = None, right_icon: str = None, **kwargs):
        self.colors = colors or get_colors()
        self.size = size
        self.error = error
        self.left_icon = left_icon
        self.right_icon = right_icon

        # Container frame for label + input + error
        self.container = ctk.CTkFrame(parent, fg_color="transparent")
        self.container.pack(fill="x", **kwargs.pop("pack_kwargs", {}))

        # Label
        if label:
            self.label = ctk.CTkLabel(
                self.container, text=label,
                font=FONT_SMALL, text_color=self.colors["text_secondary"],
            )
            self.label.pack(anchor="w", pady=(0, SPACE_1))

        # Input wrapper (for icons)
        self.wrapper = ctk.CTkFrame(self.container, fg_color="transparent")
        self.wrapper.pack(fill="x")

        # Left icon
        if left_icon:
            self.icon_left = ctk.CTkLabel(
                self.wrapper, text=left_icon,
                font=("Segoe UI Emoji", 16), text_color=self.colors["text_muted"],
            )
            self.icon_left.pack(side="left", padx=(SPACE_3, 0))

        # Input configuration
        cfg = get_input_config(size, self.colors)

        # Merge with user kwargs
        for key, value in cfg.items():
            if key not in kwargs:
                kwargs[key] = value

        # Set placeholder
        kwargs["placeholder_text"] = placeholder
        kwargs["placeholder_text_color"] = self.colors["input_placeholder"]

        # Error state border
        if error:
            kwargs["border_color"] = self.colors["destructive"]

        super().__init__(self.wrapper, **kwargs)
        self.pack(side="left", fill="x", expand=True, padx=(SPACE_3, SPACE_3) if left_icon else (0, SPACE_3))

        # Right icon
        if right_icon:
            self.icon_right = ctk.CTkLabel(
                self.wrapper, text=right_icon,
                font=("Segoe UI Emoji", 16), text_color=self.colors["text_muted"],
            )
            self.icon_right.pack(side="right", padx=(0, SPACE_3))

        # Setup focus ring
        setup_focus_ring(self, self.colors)

        # Hover border
        def on_enter(_):
            if not self.error:
                animate_color_transition(self, "border_color",
                                          self.cget("border_color"),
                                          self.colors["input_border_hover"], ANIM_FAST)

        def on_leave(_):
            if not self.error:
                animate_color_transition(self, "border_color",
                                          self.cget("border_color"),
                                          self.colors["input_border"], ANIM_FAST)

        self.bind("<Enter>", on_enter)
        self.bind("<Leave>", on_leave)

        # Error message label (initially hidden)
        self.error_label = ctk.CTkLabel(
            self.container, text="",
            font=FONT_TINY, text_color=self.colors["destructive"],
        )

    def set_error(self, message: str = ""):
        """Set error state."""
        self.error = True
        self.configure(border_color=self.colors["destructive"])
        if message:
            self.error_label.configure(text=message)
            self.error_label.pack(anchor="w", pady=(SPACE_1, 0))

    def clear_error(self):
        """Clear error state."""
        self.error = False
        self.configure(border_color=self.colors["input_border"])
        self.error_label.pack_forget()

    def apply_colors(self, colors: dict):
        """Update colors for theme change."""
        self.colors = colors
        if self.label:
            self.label.configure(text_color=colors["text_secondary"])
        self.configure(
            fg_color=colors["input_bg"],
            border_color=colors["destructive"] if self.error else colors["input_border"],
            text_color=colors["text"],
            placeholder_text_color=colors["input_placeholder"],
        )
        if self.left_icon:
            self.icon_left.configure(text_color=colors["text_muted"])
        if self.right_icon:
            self.icon_right.configure(text_color=colors["text_muted"])
        self.error_label.configure(text_color=colors["destructive"])
        setup_focus_ring(self, colors)


# ---------------------------------------------------------------------------
# Badge Component
# ---------------------------------------------------------------------------

class Badge(ctk.CTkLabel):
    """
    shadcn-inspired Badge/Tag component.

    Variants: default, secondary, outline, destructive, success, warning
    """

    VARIANT_COLORS = {
        "default": ("badge_bg", "badge_text"),
        "secondary": ("btn_secondary_bg", "btn_secondary_text"),
        "outline": ("card", "text_secondary"),
        "destructive": ("destructive_light", "destructive"),
        "success": ("success_light", "success"),
        "warning": ("warning_light", "warning"),
    }

    def __init__(self, parent, text: str, variant: str = "default",
                 size: str = "default", colors: dict = None, **kwargs):
        self.colors = colors or get_colors()
        self.variant = variant

        # Size configuration
        size_configs = {
            "sm": {"font": FONT_TINY, "pad_x": SPACE_2, "pad_y": SPACE_1, "radius": RADIUS_SM},
            "default": {"font": FONT_SMALL, "pad_x": SPACE_2, "pad_y": SPACE_1, "radius": BADGE_CORNER_RADIUS},
            "lg": {"font": FONT_BODY, "pad_x": SPACE_3, "pad_y": SPACE_2, "radius": RADIUS_MD},
        }
        sc = size_configs.get(size, size_configs["default"])

        # Colors
        bg_key, text_key = self.VARIANT_COLORS.get(variant, self.VARIANT_COLORS["default"])

        cfg = {
            "text": text,
            "font": sc["font"],
            "text_color": self.colors[text_key],
            "fg_color": self.colors[bg_key],
            "corner_radius": sc["radius"],
            "padx": sc["pad_x"],
            "pady": sc["pad_y"],
        }
        cfg.update(kwargs)

        super().__init__(parent, **cfg)

    def apply_colors(self, colors: dict):
        """Update colors for theme change."""
        self.colors = colors
        bg_key, text_key = self.VARIANT_COLORS.get(self.variant, self.VARIANT_COLORS["default"])
        self.configure(
            text_color=colors[text_key],
            fg_color=colors[bg_key],
        )


# ---------------------------------------------------------------------------
# Separator Component
# ---------------------------------------------------------------------------

class Separator(ctk.CTkFrame):
    """shadcn-inspired Separator/Divider."""

    def __init__(self, parent, orientation: str = "horizontal", colors: dict = None, **kwargs):
        self.colors = colors or get_colors()
        self.orientation = orientation

        if orientation == "horizontal":
            cfg = {"height": 1, "fg_color": self.colors["divider"]}
        else:
            cfg = {"width": 1, "fg_color": self.colors["divider"]}

        cfg.update(kwargs)
        super().__init__(parent, **cfg)

    def apply_colors(self, colors: dict):
        self.colors = colors
        self.configure(fg_color=colors["divider"])


# ---------------------------------------------------------------------------
# Avatar Component
# ---------------------------------------------------------------------------

class Avatar(ctk.CTkFrame):
    """shadcn-inspired Avatar with fallback initials."""

    def __init__(self, parent, text: str = None, image_path: str = None,
                 size: str = "default", colors: dict = None, **kwargs):
        self.colors = colors or get_colors()

        size_configs = {
            "sm": 28, "default": 36, "lg": 44, "xl": 56, "2xl": 72,
        }
        diameter = size_configs.get(size, 36)

        cfg = {
            "width": diameter,
            "height": diameter,
            "corner_radius": diameter // 2,
            "fg_color": self.colors["primary"],
        }
        cfg.update(kwargs)

        super().__init__(parent, **cfg)
        self.pack_propagate(False)

        if image_path:
            # Image avatar (would need PIL to load)
            self.label = ctk.CTkLabel(self, text="", fg_color="transparent")
        else:
            # Text fallback (initials)
            initials = text[:2].upper() if text else "?"
            self.label = ctk.CTkLabel(
                self, text=initials,
                font=(FONT_FAMILY_PRIMARY, diameter // 3, "bold"),
                text_color=self.colors["primary_foreground"],
            )
        self.label.pack(expand=True)

    def apply_colors(self, colors: dict):
        self.colors = colors
        self.configure(fg_color=colors["primary"])
        self.label.configure(text_color=colors["primary_foreground"])


# ---------------------------------------------------------------------------
# Tooltip Component
# ---------------------------------------------------------------------------

class Tooltip:
    """Simple tooltip for widgets."""

    def __init__(self, widget, text: str, colors: dict = None, delay: int = 300):
        self.widget = widget
        self.text = text
        self.colors = colors or get_colors()
        self.delay = delay
        self.tooltip_window = None
        self.after_id = None

        widget.bind("<Enter>", self._on_enter)
        widget.bind("<Leave>", self._on_leave)
        widget.bind("<ButtonPress>", self._on_leave)

    def _on_enter(self, _):
        self.after_id = self.widget.after(self.delay, self._show)

    def _on_leave(self, _):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        self._hide()

    def _show(self):
        if self.tooltip_window:
            return

        x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
        y = self.widget.winfo_rooty() - 32

        self.tooltip_window = ctk.CTkToplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        self.tooltip_window.attributes("-topmost", True)

        label = ctk.CTkLabel(
            self.tooltip_window, text=self.text,
            font=FONT_SMALL, text_color=self.colors["text_on_primary"],
            fg_color=self.colors["primary"], corner_radius=RADIUS_MD,
            padx=SPACE_3, pady=SPACE_1,
        )
        label.pack()

    def _hide(self):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


# ---------------------------------------------------------------------------
# Skeleton Loader (for loading states)
# ---------------------------------------------------------------------------

class Skeleton(ctk.CTkFrame):
    """Skeleton loading placeholder with shimmer animation."""

    def __init__(self, parent, width: int = None, height: int = 20,
                 border_radius: int = RADIUS_MD, colors: dict = None, **kwargs):
        self.colors = colors or get_colors()

        cfg = {
            "fg_color": self.colors["card_border"],
            "corner_radius": border_radius,
        }
        if width:
            cfg["width"] = width
        if height:
            cfg["height"] = height

        cfg.update(kwargs)
        super().__init__(parent, **cfg)

        self._animating = False
        self._animation_id = None

    def start(self):
        """Start shimmer animation."""
        if self._animating:
            return
        self._animating = True
        self._shimmer_step(0)

    def stop(self):
        """Stop shimmer animation."""
        self._animating = False
        if self._animation_id:
            self.after_cancel(self._animation_id)
            self._animation_id = None

    def _shimmer_step(self, step: int):
        if not self._animating:
            return

        # Animate from card_border to card_hover and back
        steps = 30
        progress = (step % steps) / steps
        if progress > 0.5:
            progress = 1 - progress
        progress = progress * 2  # 0 to 1 to 0

        color = self._lerp_color(
            self.colors["card_border"],
            self.colors["card_hover"],
            progress
        )
        self.configure(fg_color=color)

        self._animation_id = self.after(50, lambda: self._shimmer_step(step + 1))

    def _lerp_color(self, c1: str, c2: str, t: float) -> str:
        r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
        r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        return f"#{r:02x}{g:02x}{b:02x}"


# ---------------------------------------------------------------------------
# Utility: Create shadcn-style component factory
# ---------------------------------------------------------------------------

def create_card(parent, **kwargs) -> Card:
    """Factory for Card."""
    return Card(parent, **kwargs)


def create_button(parent, **kwargs) -> Button:
    """Factory for Button."""
    return Button(parent, **kwargs)


def create_input(parent, **kwargs) -> Input:
    """Factory for Input."""
    return Input(parent, **kwargs)


def create_badge(parent, **kwargs) -> Badge:
    """Factory for Badge."""
    return Badge(parent, **kwargs)


def create_separator(parent, **kwargs) -> Separator:
    """Factory for Separator."""
    return Separator(parent, **kwargs)


def create_avatar(parent, **kwargs) -> Avatar:
    """Factory for Avatar."""
    return Avatar(parent, **kwargs)


def create_skeleton(parent, **kwargs) -> Skeleton:
    """Factory for Skeleton."""
    return Skeleton(parent, **kwargs)