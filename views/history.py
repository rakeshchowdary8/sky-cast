"""
views/history.py — Modern search history and weather history view with tabs.
"""

import customtkinter as ctk
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from config.settings import (
    FONT_TITLE, FONT_MEDIUM, FONT_BODY, FONT_SMALL, FONT_LABEL,
    PAD_LG, PAD_MD, PAD_SM, CARD_CORNER_RADIUS,
)
from database import database
from utils.helpers import format_datetime_full, format_temperature


class HistoryView(ctk.CTkFrame):
    """
    Modern tabbed view combining Search History and Weather History.
    """

    def __init__(self, parent, app, colors: dict,
                 temp_unit: str = "Celsius", **kwargs):
        super().__init__(parent, fg_color=colors["bg"], corner_radius=0, **kwargs)
        self.app = app
        self.colors = colors
        self.temp_unit = temp_unit
        self._chart_canvas = None
        self._build()

    def _build(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=PAD_LG, pady=(PAD_LG, PAD_SM))

        ctk.CTkLabel(
            header, text="🕒  History",
            font=FONT_TITLE, text_color=self.colors["text"],
        ).pack(side="left")

        ctk.CTkLabel(
            header, text="Your search and weather records",
            font=FONT_SMALL, text_color=self.colors["text_dim"],
        ).pack(side="left", padx=(PAD_MD, 0))

        # Modern tab bar
        self._tab_bar = ctk.CTkFrame(self, fg_color="transparent")
        self._tab_bar.pack(fill="x", padx=PAD_LG, pady=(0, PAD_SM))

        self._tab_search_btn = self._create_tab_button(
            self._tab_bar, "🔍  Search History", "search", active=True
        )
        self._tab_search_btn.pack(side="left", padx=(0, PAD_SM))

        self._tab_weather_btn = self._create_tab_button(
            self._tab_bar, "📊  Weather History", "weather", active=False
        )
        self._tab_weather_btn.pack(side="left")

        # Content area
        self._content = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self._content.pack(fill="both", expand=True)

        self._active_tab = "search"
        self._build_search_tab()

    def _create_tab_button(self, parent, text: str, tab_id: str, active: bool) -> ctk.CTkButton:
        """Create a styled tab button."""
        if active:
            fg = self.colors["accent"]
            text_color = "#ffffff"
        else:
            fg = self.colors["card"]
            text_color = self.colors["text_dim"]

        btn = ctk.CTkButton(
            parent, text=text,
            font=FONT_BODY, height=38,
            fg_color=fg,
            hover_color=self.colors["card_hover"],
            text_color=text_color,
            corner_radius=10,
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
            self._tab_search_btn.configure(
                fg_color=self.colors["accent"], text_color="#ffffff"
            )
            self._tab_weather_btn.configure(
                fg_color=self.colors["card"], text_color=self.colors["text_dim"]
            )
            self._build_search_tab()
        else:
            self._tab_weather_btn.configure(
                fg_color=self.colors["accent"], text_color="#ffffff"
            )
            self._tab_search_btn.configure(
                fg_color=self.colors["card"], text_color=self.colors["text_dim"]
            )
            self._build_weather_tab()

    # -----------------------------------------------------------------------
    # Search History Tab
    # -----------------------------------------------------------------------

    def _build_search_tab(self):
        # Toolbar
        toolbar = ctk.CTkFrame(self._content, fg_color="transparent")
        toolbar.pack(fill="x", padx=PAD_LG, pady=(0, PAD_SM))

        ctk.CTkLabel(
            toolbar, text="Recent Searches",
            font=FONT_MEDIUM, text_color=self.colors["text"],
        ).pack(side="left")

        clear_btn = ctk.CTkButton(
            toolbar, text="🗑️  Clear All",
            font=FONT_SMALL, width=110, height=32,
            fg_color="transparent",
            hover_color="#c0392b",
            text_color=self.colors["warning"],
            border_width=1,
            border_color=self.colors["warning"],
            corner_radius=8,
            command=self._clear_search_history,
        )
        clear_btn.pack(side="right")

        # Search list with cards
        self._search_list = ctk.CTkScrollableFrame(
            self._content, fg_color="transparent", corner_radius=0
        )
        self._search_list.pack(fill="both", expand=True, padx=PAD_LG, pady=0)

        self._populate_search_list()

    def _populate_search_list(self):
        for w in self._search_list.winfo_children():
            w.destroy()

        records = database.get_recent_searches(limit=50)
        if not records:
            self._build_empty_state(self._search_list, "🔍", "No search history yet",
                                    "Search for cities to see them here.")
            return

        for rec in records:
            self._build_search_card(rec)

    def _build_search_card(self, rec: dict):
        """Build a modern card for a search history entry."""
        card = ctk.CTkFrame(
            self._search_list,
            fg_color=self.colors["card"],
            corner_radius=CARD_CORNER_RADIUS,
            border_width=1,
            border_color=self.colors["border"],
        )
        card.pack(fill="x", pady=PAD_SM // 2)

        # Hover effect
        default_fg = self.colors["card"]
        hover_fg = self.colors["card_hover"]
        default_border = self.colors["border"]
        hover_border = self.colors["accent"]

        def on_enter(_):
            card.configure(fg_color=hover_fg, border_color=hover_border)
        def on_leave(_):
            card.configure(fg_color=default_fg, border_color=default_border)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=PAD_MD, pady=PAD_MD)

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

        # Right: Action button
        search_btn = ctk.CTkButton(
            content, text="🔍  Search Again",
            font=FONT_SMALL, width=120, height=34,
            fg_color=self.colors["accent"],
            hover_color=self.colors.get("accent_hover", self.colors["accent"]),
            text_color="#ffffff",
            corner_radius=8,
            command=lambda r=rec: self._re_search(r),
        )
        search_btn.pack(side="right", padx=PAD_SM)

        # Bind hover to card
        search_btn.bind("<Enter>", on_enter)
        search_btn.bind("<Leave>", on_leave)

    def _build_empty_state(self, parent, icon: str, title: str, message: str):
        """Show empty state illustration."""
        empty_frame = ctk.CTkFrame(
            parent, fg_color=self.colors["card"],
            corner_radius=CARD_CORNER_RADIUS, border_width=1,
            border_color=self.colors["border"],
        )
        empty_frame.pack(fill="x", pady=PAD_LG * 2)

        ctk.CTkLabel(
            empty_frame, text=icon,
            font=("Segoe UI Emoji", 48),
        ).pack(pady=(PAD_LG * 2, PAD_MD))

        ctk.CTkLabel(
            empty_frame, text=title,
            font=FONT_MEDIUM, text_color=self.colors["text"],
        ).pack()

        ctk.CTkLabel(
            empty_frame, text=message,
            font=FONT_BODY, text_color=self.colors["text_dim"],
            justify="center",
        ).pack(pady=(PAD_SM, PAD_LG * 2))

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
        filter_bar.pack(fill="x", padx=PAD_LG, pady=(0, PAD_SM))

        ctk.CTkLabel(
            filter_bar, text="Filter by city:",
            font=FONT_SMALL, text_color=self.colors["text_dim"],
        ).pack(side="left", padx=(0, PAD_SM))

        cities = ["All"] + database.get_distinct_history_cities()
        self._city_filter_var = ctk.StringVar(value="All")

        city_menu = ctk.CTkOptionMenu(
            filter_bar,
            values=cities,
            variable=self._city_filter_var,
            font=FONT_BODY,
            fg_color=self.colors["card"],
            button_color=self.colors["accent"],
            button_hover_color=self.colors.get("accent_hover", self.colors["accent"]),
            text_color=self.colors["text"],
            dropdown_fg_color=self.colors["card"],
            dropdown_hover_color=self.colors["card_hover"],
            dropdown_text_color=self.colors["text"],
            corner_radius=8,
            command=lambda _: self._refresh_weather_history(),
        )
        city_menu.pack(side="left")

        # Records list
        self._weather_list = ctk.CTkScrollableFrame(
            self._content, fg_color="transparent", height=250,
        )
        self._weather_list.pack(fill="x", padx=PAD_LG, pady=(0, PAD_SM))

        # Chart section
        self._chart_section = ctk.CTkFrame(self._content, fg_color="transparent")
        self._chart_section.pack(fill="both", expand=True, padx=PAD_LG, pady=(0, PAD_LG))

        chart_header = ctk.CTkFrame(self._chart_section, fg_color="transparent")
        chart_header.pack(fill="x", pady=(0, PAD_SM))

        ctk.CTkLabel(
            chart_header,
            text="Historical Temperature Trend",
            font=FONT_MEDIUM, text_color=self.colors["text"],
        ).pack(side="left")

        self._chart_placeholder = ctk.CTkFrame(
            self._chart_section,
            fg_color=self.colors["card"],
            corner_radius=CARD_CORNER_RADIUS,
            border_width=1,
            border_color=self.colors["border"],
        )
        self._chart_placeholder.pack(fill="both", expand=True)

        self._refresh_weather_history()

    def _refresh_weather_history(self):
        for w in self._weather_list.winfo_children():
            w.destroy()

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

        self._build_weather_chart(records)

    def _build_weather_card(self, rec: dict):
        """Build a modern card for a weather history entry."""
        card = ctk.CTkFrame(
            self._weather_list,
            fg_color=self.colors["card"],
            corner_radius=CARD_CORNER_RADIUS,
            border_width=1,
            border_color=self.colors["border"],
        )
        card.pack(fill="x", pady=PAD_SM // 2)

        # Hover effect
        default_fg = self.colors["card"]
        hover_fg = self.colors["card_hover"]
        default_border = self.colors["border"]
        hover_border = self.colors["accent"]

        def on_enter(_):
            card.configure(fg_color=hover_fg, border_color=hover_border)
        def on_leave(_):
            card.configure(fg_color=default_fg, border_color=default_border)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(fill="x", padx=PAD_MD, pady=PAD_MD)

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

    def _build_weather_chart(self, records: list[dict]):
        """Plot historical temperature trend."""
        for w in self._chart_placeholder.winfo_children():
            w.destroy()

        if len(records) < 2:
            ctk.CTkLabel(
                self._chart_placeholder,
                text="📈\nNot enough data to draw a chart yet.\nSearch for more cities to see trends.",
                font=FONT_BODY, text_color=self.colors["text_dim"],
                justify="center",
            ).pack(pady=PAD_LG * 2, expand=True)
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
            spine.set_edgecolor(self.colors.get("border", "#444"))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout(pad=0.5)

        if self._chart_canvas:
            self._chart_canvas.get_tk_widget().destroy()
        self._chart_canvas = FigureCanvasTkAgg(fig, master=self._chart_placeholder)
        self._chart_canvas.draw()
        self._chart_canvas.get_tk_widget().pack(fill="both", expand=True, padx=PAD_SM, pady=PAD_SM)
        plt.close(fig)

    # -----------------------------------------------------------------------
    # Public interface
    # -----------------------------------------------------------------------

    def on_show(self):
        self._switch_tab(self._active_tab)

    def apply_colors(self, colors: dict):
        self.colors = colors
        self.configure(fg_color=colors["bg"])
        self._switch_tab(self._active_tab)

    def update_units(self, temp_unit: str):
        self.temp_unit = temp_unit