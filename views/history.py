"""
views/history.py — Search history and weather history view with tabs.
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
    Tabbed view combining Search History and Weather History.
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
        ctk.CTkLabel(
            self, text="🕒 History",
            font=FONT_TITLE, text_color=self.colors["text"],
        ).pack(anchor="w", padx=PAD_LG, pady=(PAD_LG, PAD_SM))

        # Tab buttons
        tab_bar = ctk.CTkFrame(self, fg_color="transparent")
        tab_bar.pack(fill="x", padx=PAD_LG, pady=(0, PAD_SM))

        self._tab_search_btn = ctk.CTkButton(
            tab_bar, text="Search History",
            font=FONT_BODY, width=160, height=34,
            fg_color=self.colors["accent"],
            hover_color=self.colors.get("accent_hover", self.colors["accent"]),
            text_color="#ffffff", corner_radius=6,
            command=lambda: self._switch_tab("search"),
        )
        self._tab_search_btn.pack(side="left", padx=(0, PAD_SM))

        self._tab_weather_btn = ctk.CTkButton(
            tab_bar, text="Weather History",
            font=FONT_BODY, width=160, height=34,
            fg_color=self.colors["card"],
            hover_color=self.colors["card_hover"],
            text_color=self.colors["text_dim"], corner_radius=6,
            command=lambda: self._switch_tab("weather"),
        )
        self._tab_weather_btn.pack(side="left")

        # Content area
        self._content = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self._content.pack(fill="both", expand=True)

        self._active_tab = "search"
        self._build_search_tab()

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
        toolbar = ctk.CTkFrame(self._content, fg_color="transparent")
        toolbar.pack(fill="x", padx=PAD_LG, pady=(0, PAD_SM))

        ctk.CTkLabel(
            toolbar, text="Recent Searches",
            font=FONT_MEDIUM, text_color=self.colors["text"],
        ).pack(side="left")

        ctk.CTkButton(
            toolbar, text="🗑️ Clear All",
            font=FONT_SMALL, width=100, height=30,
            fg_color="#c0392b", hover_color="#922b21",
            text_color="#ffffff", corner_radius=6,
            command=self._clear_search_history,
        ).pack(side="right")

        self._search_list = ctk.CTkScrollableFrame(
            self._content, fg_color="transparent"
        )
        self._search_list.pack(fill="both", expand=True, padx=PAD_LG, pady=0)

        self._populate_search_list()

    def _populate_search_list(self):
        for w in self._search_list.winfo_children():
            w.destroy()

        records = database.get_recent_searches(limit=50)
        if not records:
            ctk.CTkLabel(
                self._search_list,
                text="No search history yet.",
                font=FONT_BODY, text_color=self.colors["text_dim"],
            ).pack(pady=PAD_LG * 3)
            return

        for rec in records:
            self._build_search_row(rec)

    def _build_search_row(self, rec: dict):
        row = ctk.CTkFrame(
            self._search_list,
            fg_color=self.colors["card"], corner_radius=CARD_CORNER_RADIUS,
        )
        row.pack(fill="x", pady=2)

        info = ctk.CTkFrame(row, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True, padx=PAD_MD, pady=PAD_SM)

        city_text = f"{rec['city_name']}, {rec['country']}" if rec.get("country") else rec["city_name"]
        ctk.CTkLabel(
            info, text=f"📍 {city_text}",
            font=FONT_BODY, text_color=self.colors["text"], anchor="w",
        ).pack(anchor="w")
        ctk.CTkLabel(
            info,
            text=format_datetime_full(rec["searched_at"]),
            font=FONT_LABEL, text_color=self.colors["text_dim"],
        ).pack(anchor="w")

        ctk.CTkButton(
            row, text="Search Again",
            font=FONT_SMALL, width=110, height=28,
            fg_color=self.colors["accent"],
            hover_color=self.colors.get("accent_hover", self.colors["accent"]),
            text_color="#ffffff", corner_radius=6,
            command=lambda r=rec: self._re_search(r),
        ).pack(side="right", padx=PAD_MD)

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

        ctk.CTkLabel(
            self._chart_section,
            text="Historical Temperature",
            font=FONT_MEDIUM, text_color=self.colors["text"],
        ).pack(anchor="w", pady=(0, PAD_SM))

        self._chart_placeholder = ctk.CTkFrame(
            self._chart_section,
            fg_color=self.colors["card"],
            corner_radius=CARD_CORNER_RADIUS,
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
            ctk.CTkLabel(
                self._weather_list,
                text="No weather history yet.",
                font=FONT_BODY, text_color=self.colors["text_dim"],
            ).pack(pady=PAD_LG)
        else:
            for rec in records:
                self._build_weather_row(rec)

        self._build_weather_chart(records)

    def _build_weather_row(self, rec: dict):
        row = ctk.CTkFrame(
            self._weather_list,
            fg_color=self.colors["card"], corner_radius=CARD_CORNER_RADIUS,
        )
        row.pack(fill="x", pady=2)

        info = ctk.CTkFrame(row, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True, padx=PAD_MD, pady=PAD_SM)

        temp_str = format_temperature(rec["temperature"], self.temp_unit)
        ctk.CTkLabel(
            info,
            text=f"📍 {rec['city_name']}   🌡️ {temp_str}   💧 {rec['humidity']:.0f}%   💨 {rec['wind_speed']:.0f} km/h",
            font=FONT_BODY, text_color=self.colors["text"], anchor="w",
        ).pack(anchor="w")
        ctk.CTkLabel(
            info,
            text=f"{rec['weather_condition']}   •   {format_datetime_full(rec['recorded_at'])}",
            font=FONT_LABEL, text_color=self.colors["text_dim"],
        ).pack(anchor="w")

    def _build_weather_chart(self, records: list[dict]):
        """Plot historical temperature trend."""
        for w in self._chart_placeholder.winfo_children():
            w.destroy()

        if len(records) < 2:
            ctk.CTkLabel(
                self._chart_placeholder,
                text="Not enough data to draw a chart yet.",
                font=FONT_BODY, text_color=self.colors["text_dim"],
            ).pack(pady=PAD_LG)
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
        ax.plot(range(len(temps)), temps, color=line_color, linewidth=2, marker="o", markersize=4)
        ax.fill_between(range(len(temps)), temps, min(temps) - 1, alpha=0.2, color=line_color)
        ax.set_ylabel("°C", color=text_dim, fontsize=8)
        ax.tick_params(colors=text_dim, labelsize=7)
        ax.set_xticks(range(len(dates)))
        ax.set_xticklabels(dates, rotation=45, ha="right", fontsize=6)
        for spine in ax.spines.values():
            spine.set_edgecolor(self.colors.get("border", "#444"))
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
