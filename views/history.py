"""
views/history.py — Premium search history and weather history view with tabs (shadcn-inspired).

Features:
- Modern tab bar with animated transitions
- Search history cards with actions
- Weather history cards with chart
- Empty states with illustrations
- Full theme consistency
"""

import customtkinter as ctk
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from config.settings import (
    FONT_TITLE, FONT_MEDIUM, FONT_BODY, FONT_SMALL, FONT_LABEL, FONT_TINY,
    SPACE_1, SPACE_2, SPACE_3, SPACE_4, SPACE_6, SPACE_8,
    CARD_CORNER_RADIUS, BUTTON_CORNER_RADIUS, RADIUS_MD,
    STATUS_COLORS,
    ANIM_FAST, ANIM_NORMAL,
)
from components.base import Card, Button, Badge
from utils.animations import stagger_animate_children, animate_color_transition, ease_out_cubic
from database import database
from utils.helpers import format_datetime_full, format_temperature


class HistoryView(ctk.CTkFrame):
    """
    Modern tabbed view combining Search History and Weather History (shadcn-inspired).
    """

    def __init__(self, parent, app, colors: dict,
                 temp_unit: str = "Celsius", **kwargs):
        super().__init__(parent, fg_color=colors["bg"], corner_radius=0, **kwargs)
        self.app = app
        self.colors = colors
        self.temp_unit = temp_unit
        self._chart_canvas = None
        self._search_cards = []
        self._weather_cards = []
        self._build()

    def _build(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=SPACE_8, pady=(SPACE_6, SPACE_3))

        ctk.CTkLabel(
            header, text="🕒  History",
            font=FONT_TITLE, text_color=self.colors["text"],
        ).pack(side="left")

        ctk.CTkLabel(
            header, text="Your search and weather records",
            font=FONT_SMALL, text_color=self.colors["text_dim"],
        ).pack(side="left", padx=(SPACE_3, 0))

        # Modern tab bar
        self._tab_bar = ctk.CTkFrame(self, fg_color="transparent")
        self._tab_bar.pack(fill="x", padx=SPACE_8, pady=(0, SPACE_3))

        self._tab_search_btn = self._create_tab_button(
            self._tab_bar, "🔍  Search History", "search", active=True
        )
        self._tab_search_btn.pack(side="left", padx=(0, SPACE_2))

        self._tab_weather_btn = self._create_tab_button(
            self._tab_bar, "📊  Weather History", "weather", active=False
        )
        self._tab_weather_btn.pack(side="left")

        # Content area
        self._content = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self._content.pack(fill="both", expand=True)

        self._active_tab = "search"
        self._build_search_tab()

    def _create_tab_button(self, parent, text: str, tab_id: str, active: bool) -> Button:
        """Create a styled tab button using Button component."""
        if active:
            variant = "default"
        else:
            variant = "ghost"

        btn = Button(
            parent, text=text,
            variant=variant,
            size="default",
            colors=self.colors,
            command=lambda: self._switch_tab(tab_id),
        )
        return btn

    # -----------------------------------------------------------------------
    # Tab management
    # -----------------------------------------------------------------------

    def _switch_tab(self, tab: str):
        self._active_tab = tab
        for w in self._content.winfo_children():
            w.destroy()

        if tab == "search":
            self._tab_search_btn.configure(variant="default")
            self._tab_weather_btn.configure(variant="ghost")
            self._build_search_tab()
        else:
            self._tab_weather_btn.configure(variant="default")
            self._tab_search_btn.configure(variant="ghost")
            self._build_weather_tab()

    # -----------------------------------------------------------------------
    # Search History Tab
    # -----------------------------------------------------------------------

    def _build_search_tab(self):
        # Toolbar
        toolbar = ctk.CTkFrame(self._content, fg_color="transparent")
        toolbar.pack(fill="x", padx=SPACE_8, pady=(0, SPACE_2))

        ctk.CTkLabel(
            toolbar, text="Recent Searches",
            font=FONT_MEDIUM, text_color=self.colors["text"],
        ).pack(side="left")

        clear_btn = Button(
            toolbar, text="🗑️  Clear All",
            variant="ghost",
            size="sm",
            colors=self.colors,
            command=self._clear_search_history,
        )
        # Override for destructive action
        clear_btn.configure(
            text_color=self.colors["destructive"],
            hover_color=self.colors["destructive_light"],
        )
        clear_btn.pack(side="right")

        # Search list with cards
        self._search_list = ctk.CTkScrollableFrame(
            self._content, fg_color="transparent", corner_radius=0,
            scrollbar_button_color=self.colors["scrollbar"],
            scrollbar_button_hover_color=self.colors["scrollbar_hover"],
        )
        self._search_list.pack(fill="both", expand=True, padx=SPACE_8, pady=0)

        # Enable trackpad/mouse wheel scrolling
        self._setup_scroll_bindings(self._search_list)

        self._populate_search_list()

    def _populate_search_list(self):
        for w in self._search_list.winfo_children():
            w.destroy()

        self._search_cards = []
        records = database.get_recent_searches(limit=50)
        if not records:
            self._build_empty_state(self._search_list, "🔍", "No search history yet",
                                    "Search for cities to see them here.")
            return

        for rec in records:
            self._build_search_card(rec)

        # Stagger animate the cards
        stagger_animate_children(
            self._search_list,
            lambda child, idx: None,
            delay_per_child=40,
            start_delay=50,
        )

    def _build_search_card(self, rec: dict):
        """Build a modern card for a search history entry using Card component."""
        card = Card(
            self._search_list,
            variant="default",
            padding=SPACE_4,
            colors=self.colors,
        )
        card.pack(fill="x", pady=SPACE_1)
        card.configure(cursor="hand2")

        # Store default colors for hover
        card._default_fg = self.colors["card"]
        card._default_border = self.colors["card_border"]
        card._hovering = False

        # Hover effect with smooth animation and flicker guard
        def on_enter(_):
            if card._hovering:
                return
            card._hovering = True
            animate_color_transition(card, "fg_color",
                                      card.cget("fg_color"), self.colors["card_hover"], ANIM_FAST)
            animate_color_transition(card, "border_color",
                                      card.cget("border_color"), self.colors["primary"], ANIM_FAST)

        def on_leave(_):
            if not card._hovering:
                return
            card._hovering = False
            animate_color_transition(card, "fg_color",
                                      card.cget("fg_color"), self.colors["card"], ANIM_FAST)
            animate_color_transition(card, "border_color",
                                      card.cget("border_color"), self.colors["card_border"], ANIM_FAST)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        content = card.content

        # Left: City info
        info = ctk.CTkFrame(content, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True)

        city_text = f"{rec['city_name']}, {rec['country']}" if rec.get("country") else rec["city_name"]
        ctk.CTkLabel(
            info, text=f"📍  {city_text}",
            font=FONT_BODY, text_color=self.colors["text"], anchor="w",
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=format_datetime_full(rec["searched_at"]),
            font=FONT_LABEL, text_color=self.colors["text_dim"],
        ).pack(anchor="w")

        # Right: Action button using Button component
        search_btn = Button(
            content, text="🔍  Search Again",
            variant="default",
            size="sm",
            colors=self.colors,
            command=lambda r=rec: self._re_search(r),
        )
        search_btn.pack(side="right", padx=SPACE_2)

        self._search_cards.append(card)

    def _build_empty_state(self, parent, icon: str, title: str, message: str):
        """Show empty state illustration using Card component."""
        empty_frame = Card(
            parent, variant="default",
            padding=SPACE_8,
            colors=self.colors,
        )
        empty_frame.pack(fill="x", pady=SPACE_8 * 2)

        empty_content = empty_frame.content

        ctk.CTkLabel(
            empty_content, text=icon,
            font=("Segoe UI Emoji", 48),
        ).pack(pady=(SPACE_6, SPACE_4))

        ctk.CTkLabel(
            empty_content, text=title,
            font=FONT_MEDIUM, text_color=self.colors["text"],
        ).pack()

        ctk.CTkLabel(
            empty_content, text=message,
            font=FONT_BODY, text_color=self.colors["text_dim"],
            justify="center",
        ).pack(pady=(SPACE_2, SPACE_6))

    def _clear_search_history(self):
        database.clear_search_history()
        self._populate_search_list()

    def _re_search(self, rec: dict):
        self.app.search_city(rec["city_name"])
        self.app.show_view("dashboard")

    # -----------------------------------------------------------------------
    # Weather History Tab
    # -----------------------------------------------------------------------

    def _build_weather_tab(self):
        # Filter bar
        filter_bar = ctk.CTkFrame(self._content, fg_color="transparent")
        filter_bar.pack(fill="x", padx=SPACE_8, pady=(0, SPACE_2))

        ctk.CTkLabel(
            filter_bar, text="Filter by city:",
            font=FONT_SMALL, text_color=self.colors["text_dim"],
        ).pack(side="left", padx=(0, SPACE_2))

        cities = ["All"] + database.get_distinct_history_cities()
        self._city_filter_var = ctk.StringVar(value="All")

        # Use CTkOptionMenu (no base component for this yet)
        city_menu = ctk.CTkOptionMenu(
            filter_bar,
            values=cities,
            variable=self._city_filter_var,
            font=FONT_BODY,
            fg_color=self.colors["card"],
            button_color=self.colors["primary"],
            button_hover_color=self.colors["primary_hover"],
            text_color=self.colors["text"],
            dropdown_fg_color=self.colors["card"],
            dropdown_hover_color=self.colors["card_hover"],
            dropdown_text_color=self.colors["text"],
            corner_radius=RADIUS_MD,
            command=lambda _: self._refresh_weather_history(),
        )
        city_menu.pack(side="left")

        # Records list
        self._weather_list = ctk.CTkScrollableFrame(
            self._content, fg_color="transparent", height=250,
            scrollbar_button_color=self.colors["scrollbar"],
            scrollbar_button_hover_color=self.colors["scrollbar_hover"],
        )
        self._weather_list.pack(fill="x", padx=SPACE_8, pady=(0, SPACE_2))

        # Enable trackpad/mouse wheel scrolling
        self._setup_scroll_bindings(self._weather_list)

        # Chart section
        self._chart_section = ctk.CTkFrame(self._content, fg_color="transparent")
        self._chart_section.pack(fill="both", expand=True, padx=SPACE_8, pady=(0, SPACE_6))

        chart_header = ctk.CTkFrame(self._chart_section, fg_color="transparent")
        chart_header.pack(fill="x", pady=(0, SPACE_2))

        ctk.CTkLabel(
            chart_header,
            text="Historical Temperature Trend",
            font=FONT_MEDIUM, text_color=self.colors["text"],
        ).pack(side="left")

        # Chart placeholder using Card
        self._chart_placeholder = Card(
            self._chart_section,
            variant="default",
            padding=SPACE_4,
            colors=self.colors,
        )
        self._chart_placeholder.pack(fill="both", expand=True)

        self._refresh_weather_history()

    def _refresh_weather_history(self):
        for w in self._weather_list.winfo_children():
            w.destroy()

        self._weather_cards = []

        city_filter = self._city_filter_var.get()
        records = database.get_weather_history(
            city_filter=None if city_filter == "All" else city_filter,
            limit=100,
        )

        if not records:
            self._build_empty_state(self._weather_list, "📊", "No weather history yet",
                                    "Weather snapshots appear here after searching.")
        else:
            for rec in records:
                self._build_weather_card(rec)

            # Stagger animate the cards
            stagger_animate_children(
                self._weather_list,
                lambda child, idx: None,
                delay_per_child=30,
                start_delay=50,
            )

        self._build_weather_chart(records)

    def _build_weather_card(self, rec: dict):
        """Build a modern card for a weather history entry using Card component."""
        card = Card(
            self._weather_list,
            variant="default",
            padding=SPACE_4,
            colors=self.colors,
        )
        card.pack(fill="x", pady=SPACE_1)
        card.configure(cursor="hand2")

        # Store default colors for hover
        card._default_fg = self.colors["card"]
        card._default_border = self.colors["card_border"]
        card._hovering = False

        # Hover effect with smooth animation and flicker guard
        def on_enter(_):
            if card._hovering:
                return
            card._hovering = True
            animate_color_transition(card, "fg_color",
                                      card.cget("fg_color"), self.colors["card_hover"], ANIM_FAST)
            animate_color_transition(card, "border_color",
                                      card.cget("border_color"), self.colors["primary"], ANIM_FAST)

        def on_leave(_):
            if not card._hovering:
                return
            card._hovering = False
            animate_color_transition(card, "fg_color",
                                      card.cget("fg_color"), self.colors["card"], ANIM_FAST)
            animate_color_transition(card, "border_color",
                                      card.cget("border_color"), self.colors["card_border"], ANIM_FAST)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        info = ctk.CTkFrame(card.content, fg_color="transparent")
        info.pack(fill="x")

        temp_str = format_temperature(rec["temperature"], self.temp_unit)
        ctk.CTkLabel(
            info,
            text=f"📍  {rec['city_name']}     🌡️  {temp_str}     💧  {rec['humidity']:.0f}%     💨  {rec['wind_speed']:.0f} km/h",
            font=FONT_BODY, text_color=self.colors["text"], anchor="w",
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"{rec['weather_condition']}     •     {format_datetime_full(rec['recorded_at'])}",
            font=FONT_LABEL, text_color=self.colors["text_dim"],
        ).pack(anchor="w")

        self._weather_cards.append(card)

    def _build_weather_chart(self, records: list[dict]):
        """Plot historical temperature trend."""
        for w in self._chart_placeholder.content.winfo_children():
            w.destroy()

        if len(records) < 2:
            ctk.CTkLabel(
                self._chart_placeholder.content,
                text="📈\nNot enough data to draw a chart yet.\nSearch for more cities to see trends.",
                font=FONT_BODY, text_color=self.colors["text_dim"],
                justify="center",
            ).pack(pady=SPACE_8 * 2, expand=True)
            return

        # Reverse so oldest is on the left
        records_asc = list(reversed(records))
        dates = [r["recorded_at"][:16] for r in records_asc]
        temps = [r["temperature"] for r in records_asc]

        bg = self.colors["chart_bg"]
        line_color = self.colors["chart_line"]
        text_dim = self.colors["text_dim"]

        fig, ax = plt.subplots(figsize=(9, 2.5))
        fig.patch.set_facecolor(bg)
        ax.set_facecolor(bg)

        # Gradient fill
        ax.plot(range(len(temps)), temps, color=line_color, linewidth=2.5, marker="o", markersize=5,
                markerfacecolor=line_color, markeredgecolor=bg, markeredgewidth=2, zorder=3)
        ax.fill_between(range(len(temps)), temps, min(temps) - 1, alpha=0.15, color=line_color)

        ax.set_ylabel("°C", color=text_dim, fontsize=9)
        ax.tick_params(colors=text_dim, labelsize=8)
        ax.set_xticks(range(len(dates)))
        ax.set_xticklabels(dates, rotation=45, ha="right", fontsize=7)
        for spine in ax.spines.values():
            spine.set_edgecolor(self.colors.get("card_border", "#444"))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout(pad=0.5)

        if self._chart_canvas:
            self._chart_canvas.get_tk_widget().destroy()
        self._chart_canvas = FigureCanvasTkAgg(fig, master=self._chart_placeholder.content)
        self._chart_canvas.draw()
        self._chart_canvas.get_tk_widget().pack(fill="both", expand=True, padx=SPACE_2, pady=SPACE_2)
        plt.close(fig)

    # -----------------------------------------------------------------------
    # Public interface
    # -----------------------------------------------------------------------

    def on_show(self):
        self._switch_tab(self._active_tab)

    def _setup_scroll_bindings(self, scroll_frame, horizontal=False):
        """Setup improved mouse wheel/trackpad scrolling bindings for a CTkScrollableFrame."""
        def on_mousewheel(event):
            delta = event.delta
            if delta == 0:
                return
            units = -int(delta / 120)
            units = max(-5, min(5, units))
            if horizontal:
                scroll_frame._parent_canvas.xview_scroll(units, "units")
            else:
                scroll_frame._parent_canvas.yview_scroll(units, "units")
            return "break"

        def on_shift_mousewheel(event):
            delta = event.delta
            if delta == 0:
                return
            units = -int(delta / 120)
            units = max(-5, min(5, units))
            if horizontal:
                scroll_frame._parent_canvas.yview_scroll(units, "units")
            else:
                scroll_frame._parent_canvas.xview_scroll(units, "units")
            return "break"

        scroll_frame.bind("<MouseWheel>", on_mousewheel)
        scroll_frame.bind("<Shift-MouseWheel>", on_shift_mousewheel)
        if hasattr(scroll_frame, '_parent_canvas'):
            scroll_frame._parent_canvas.bind("<MouseWheel>", on_mousewheel)
            scroll_frame._parent_canvas.bind("<Shift-MouseWheel>", on_shift_mousewheel)

    def apply_colors(self, colors: dict):
        self.colors = colors
        self.configure(fg_color=colors["bg"])
        self._switch_tab(self._active_tab)

    def update_units(self, temp_unit: str):
        self.temp_unit = temp_unit