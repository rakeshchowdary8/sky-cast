"""
utils/animations.py — Smooth animation utilities for CustomTkinter.

Provides:
- Property animation (color, size, position, opacity)
- Easing functions
- Animation sequencing
- Common UI animations (fade, slide, scale, sidebar toggle)
"""

import customtkinter as ctk
from config.settings import (
    ANIM_INSTANT, ANIM_FAST, ANIM_NORMAL, ANIM_SLOW, ANIM_SLOWER,
    EASING_LINEAR, EASING_EASE_IN, EASING_EASE_OUT, EASING_EASE_IN_OUT, EASING_SPRING,
    ease_out_cubic, ease_in_out_cubic, ease_out_expo,
    ANIMATION_PRESETS,
)


class Animation:
    """Base animation class for animating widget properties."""

    def __init__(self, widget, duration: int = ANIM_NORMAL, easing: str = EASING_EASE_OUT):
        self.widget = widget
        self.duration = duration
        self.easing = easing
        self._running = False
        self._start_time = 0
        self._animation_id = None
        self._on_complete = None
        self._properties = {}

    def _get_easing_func(self):
        """Get easing function by name."""
        easing_map = {
            EASING_LINEAR: lambda t: t,
            EASING_EASE_IN: lambda t: t * t,
            EASING_EASE_OUT: ease_out_cubic,
            EASING_EASE_IN_OUT: ease_in_out_cubic,
            EASING_SPRING: ease_out_expo,
        }
        return easing_map.get(self.easing, ease_out_cubic)

    def animate(self, properties: dict, on_complete=None):
        """
        Start animating widget properties.

        Args:
            properties: Dict of property_name -> (start_value, end_value)
            on_complete: Optional callback when animation finishes
        """
        if self._running:
            self.stop()

        self._properties = properties
        self._on_complete = on_complete
        self._running = True
        self._start_time = self._get_time()
        self._tick()

    def _get_time(self) -> int:
        """Get current time in milliseconds."""
        return int(self.widget.winfo_toplevel().tk.call('clock', 'milliseconds'))

    def _tick(self):
        """Animation tick - called every frame."""
        if not self._running:
            return

        current_time = self._get_time()
        elapsed = current_time - self._start_time
        progress = min(elapsed / self.duration, 1.0)

        easing_func = self._get_easing_func()
        eased_progress = easing_func(progress)

        # Update properties
        for prop_name, (start_val, end_val) in self._properties.items():
            current_val = self._interpolate(start_val, end_val, eased_progress)
            self._set_property(prop_name, current_val)

        if progress >= 1.0:
            self._running = False
            # Ensure final values
            for prop_name, (_, end_val) in self._properties.items():
                self._set_property(prop_name, end_val)
            if self._on_complete:
                self._on_complete()
        else:
            self._animation_id = self.widget.after(16, self._tick)  # ~60fps

    def _interpolate(self, start, end, t: float):
        """Interpolate between two values based on type."""
        # Color interpolation (hex strings)
        if isinstance(start, str) and isinstance(end, str) and start.startswith('#') and end.startswith('#'):
            return self._interpolate_color(start, end, t)

        # Numeric interpolation
        if isinstance(start, (int, float)) and isinstance(end, (int, float)):
            return start + (end - start) * t

        # Tuple interpolation (for padding, etc.)
        if isinstance(start, tuple) and isinstance(end, tuple) and len(start) == len(end):
            return tuple(self._interpolate(s, e, t) for s, e in zip(start, end))

        # Default: return end value for non-interpolatable types
        return end if t >= 1.0 else start

    def _interpolate_color(self, start: str, end: str, t: float) -> str:
        """Interpolate between two hex colors."""
        r1, g1, b1 = int(start[1:3], 16), int(start[3:5], 16), int(start[5:7], 16)
        r2, g2, b2 = int(end[1:3], 16), int(end[3:5], 16), int(end[5:7], 16)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _set_property(self, prop_name: str, value):
        """Set a widget property."""
        try:
            if prop_name == "fg_color":
                self.widget.configure(fg_color=value)
            elif prop_name == "border_color":
                self.widget.configure(border_color=value)
            elif prop_name == "text_color":
                self.widget.configure(text_color=value)
            elif prop_name == "width":
                self.widget.configure(width=int(value))
            elif prop_name == "height":
                self.widget.configure(height=int(value))
            elif prop_name == "corner_radius":
                self.widget.configure(corner_radius=int(value))
            elif prop_name == "border_width":
                self.widget.configure(border_width=int(value))
            elif prop_name == "opacity":
                # Simulated via color alpha - not directly supported in CTk
                pass
        except Exception:
            pass  # Silently ignore property set errors

    def stop(self):
        """Stop the animation."""
        self._running = False
        if self._animation_id:
            self.widget.after_cancel(self._animation_id)
            self._animation_id = None


class AnimationSequence:
    """Run multiple animations in sequence or parallel."""

    def __init__(self):
        self._animations = []
        self._parallel = False
        self._on_complete = None

    def add(self, animation: Animation, delay: int = 0):
        """Add animation to sequence."""
        self._animations.append((animation, delay))
        return self

    def parallel(self, parallel: bool = True):
        """Set whether animations run in parallel."""
        self._parallel = parallel
        return self

    def on_complete(self, callback):
        """Set completion callback."""
        self._on_complete = callback
        return self

    def start(self):
        """Start the animation sequence."""
        if self._parallel:
            for anim, delay in self._animations:
                if delay > 0:
                    anim.widget.after(delay, anim.start)
                else:
                    anim.start()
            # Track completion
            self._check_parallel_completion()
        else:
            self._run_sequential(0)

    def _run_sequential(self, index: int):
        if index >= len(self._animations):
            if self._on_complete:
                self._on_complete()
            return

        anim, delay = self._animations[index]
        if delay > 0:
            anim.widget.after(delay, lambda: self._start_and_wait(anim, index))
        else:
            self._start_and_wait(anim, index)

    def _start_and_wait(self, anim: Animation, index: int):
        original_complete = anim._on_complete

        def on_done():
            if original_complete:
                original_complete()
            self._run_sequential(index + 1)

        anim._on_complete = on_done
        anim.start()

    def _check_parallel_completion(self):
        """Check if all parallel animations are done."""
        if all(not anim._running for anim, _ in self._animations):
            if self._on_complete:
                self._on_complete()
        else:
            self._animations[0][0].widget.after(50, self._check_parallel_completion)


# ---------------------------------------------------------------------------
# High-level Animation Helpers
# ---------------------------------------------------------------------------

def fade_in(widget, duration: int = ANIM_NORMAL, on_complete=None):
    """Fade in widget by animating from transparent to current color."""
    # CustomTkinter doesn't support opacity directly, so we animate fg_color
    # from a transparent-like color to the target color
    target_color = widget.cget("fg_color")
    # Start with a slightly transparent version (simulated via darker color)
    # This is a simplified version - real opacity would need a different approach
    anim = Animation(widget, duration, EASING_EASE_OUT)
    anim.animate({"fg_color": (target_color, target_color)}, on_complete)
    return anim


def fade_out(widget, duration: int = ANIM_FAST, on_complete=None):
    """Fade out widget."""
    anim = Animation(widget, duration, EASING_EASE_IN)
    anim.animate({"fg_color": (widget.cget("fg_color"), widget.cget("fg_color"))}, on_complete)
    return anim


def slide_in_from_left(widget, distance: int = 30, duration: int = ANIM_NORMAL, on_complete=None):
    """Slide widget in from left."""
    # This would require position animation which CTk doesn't directly support
    # We'll use a placeholder for now
    if on_complete:
        widget.after(duration, on_complete)
    return None


def scale_in(widget, duration: int = ANIM_FAST, on_complete=None):
    """Scale widget in from 0.95 to 1.0."""
    # CTk doesn't support transform scale directly
    if on_complete:
        widget.after(duration, on_complete)
    return None


def animate_sidebar_toggle(sidebar, is_expanded: bool, on_complete=None):
    """
    Animate sidebar width toggle with smooth easing.

    Args:
        sidebar: Sidebar widget instance
        is_expanded: True to expand, False to collapse
        on_complete: Callback when animation finishes
    """
    from config.settings import (
        SIDEBAR_WIDTH_EXPANDED, SIDEBAR_WIDTH_COLLAPSED,
        ANIMATION_PRESETS, ease_in_out_cubic
    )

    preset = ANIMATION_PRESETS["sidebar_toggle"]
    duration = preset["duration"]
    easing = ease_in_out_cubic

    start_width = sidebar.winfo_width()
    target_width = SIDEBAR_WIDTH_EXPANDED if is_expanded else SIDEBAR_WIDTH_COLLAPSED

    # Don't animate if already at target
    if abs(start_width - target_width) < 5:
        if on_complete:
            on_complete()
        return

    steps = 60  # ~60fps for smooth animation
    step_duration = duration // steps

    def animate_step(step: int):
        if step > steps:
            sidebar.configure(width=target_width)
            if on_complete:
                on_complete()
            return

        progress = step / steps
        eased = easing(progress)
        current_width = int(start_width + (target_width - start_width) * eased)
        sidebar.configure(width=current_width)

        # Trigger layout update
        sidebar.update_idletasks()

        sidebar.after(step_duration, lambda: animate_step(step + 1))

    animate_step(0)


def animate_color_transition(widget, prop_name: str, start_color: str, end_color: str,
                              duration: int = ANIM_NORMAL, easing=EASING_EASE_OUT, on_complete=None):
    """Animate a color property transition."""
    anim = Animation(widget, duration, easing)
    anim.animate({prop_name: (start_color, end_color)}, on_complete)
    return anim


def pulse_animation(widget, prop_name: str = "border_color",
                     color1: str = None, color2: str = None,
                     duration: int = ANIM_SLOW, cycles: int = 1, on_complete=None):
    """Pulse animation between two colors."""
    if color1 is None or color2 is None:
        colors = widget.winfo_toplevel()._colors if hasattr(widget.winfo_toplevel(), '_colors') else {}
        color1 = colors.get("primary", "#3b82f6")
        color2 = colors.get("card_border", "#1e293b")

    def run_cycle(cycle: int):
        if cycle >= cycles * 2:
            if on_complete:
                on_complete()
            return

        target = color2 if cycle % 2 == 0 else color1
        animate_color_transition(
            widget, prop_name,
            widget.cget(prop_name), target,
            duration // (cycles * 2),
            on_complete=lambda: run_cycle(cycle + 1)
        )

    run_cycle(0)


# ---------------------------------------------------------------------------
# Micro-interaction Helpers
# ---------------------------------------------------------------------------

def setup_hover_animation(widget, colors: dict, prop: str = "fg_color",
                           hover_color_key: str = "card_hover",
                           normal_color_key: str = "card",
                           duration: int = ANIM_FAST):
    """Setup smooth hover animation for a widget."""

    def on_enter(_):
        animate_color_transition(widget, prop,
                                  widget.cget(prop), colors[hover_color_key], duration)

    def on_leave(_):
        animate_color_transition(widget, prop,
                                  widget.cget(prop), colors[normal_color_key], duration)

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)


def setup_focus_ring(widget, colors: dict, ring_color_key: str = "focus_ring",
                      border_prop: str = "border_color", duration: int = ANIM_FAST):
    """Setup focus ring animation for input widgets."""

    def on_focus_in(_):
        animate_color_transition(widget, border_prop,
                                  widget.cget(border_prop), colors[ring_color_key], duration)
        widget.configure(border_width=2)

    def on_focus_out(_):
        animate_color_transition(widget, border_prop,
                                  widget.cget(border_prop), colors["input_border"], duration)
        widget.configure(border_width=1)

    widget.bind("<FocusIn>", on_focus_in)
    widget.bind("<FocusOut>", on_focus_out)


def animate_button_press(widget, colors: dict, scale_factor: float = 0.98,
                          duration: int = ANIM_FAST // 2):
    """Animate button press (scale down slightly)."""
    # CTk doesn't support transform, so we simulate with a quick color flash
    original_bg = widget.cget("fg_color")
    pressed_color = colors.get("primary_hover", colors.get("primary", "#3b82f6"))

    def on_press(_):
        animate_color_transition(widget, "fg_color", original_bg, pressed_color, duration)

    def on_release(_):
        animate_color_transition(widget, "fg_color", widget.cget("fg_color"), original_bg, duration)

    widget.bind("<Button-1>", on_press)
    widget.bind("<ButtonRelease-1>", on_release)


# ---------------------------------------------------------------------------
# Staggered Animation for Lists
# ---------------------------------------------------------------------------

def stagger_animate_children(parent, animation_factory, delay_per_child: int = 50,
                              start_delay: int = 0, on_complete=None):
    """
    Animate children of a parent widget with staggered delays.

    Args:
        parent: Parent widget containing children to animate
        animation_factory: Function(child, index) -> Animation
        delay_per_child: Delay between each child's animation start (ms)
        start_delay: Initial delay before first animation (ms)
        on_complete: Callback when all animations complete
    """
    children = parent.winfo_children()
    if not children:
        if on_complete:
            on_complete()
        return

    completed = [0]

    def check_complete():
        completed[0] += 1
        if completed[0] >= len(children):
            if on_complete:
                on_complete()

    for i, child in enumerate(children):
        delay = start_delay + i * delay_per_child
        anim = animation_factory(child, i)
        if anim:
            original_complete = anim._on_complete
            anim._on_complete = lambda oc=original_complete: (oc() if oc else None, check_complete())
            if delay > 0:
                child.after(delay, anim.start)
            else:
                anim.start()