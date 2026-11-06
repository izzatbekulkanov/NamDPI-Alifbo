# -*- coding: utf-8 -*-
"""
NamDPI alifbo - Professional Pastki Panel (Taskbar Dock Panel)
Namangan davlat pedagogika instituti
Raqamli ta'lim texnologiyalari markazi (NamDPI RTTM)
"""

import tkinter as tk
from tkinter import messagebox
import json
import os
import sys
import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
SPI_GETWORKAREA = 0x0030

class RECT(ctypes.Structure):
    _fields_ = [
        ("left", wintypes.LONG),
        ("top", wintypes.LONG),
        ("right", wintypes.LONG),
        ("bottom", wintypes.LONG)
    ]

CONFIG_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "NamDPI_Alifbo")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "mode": "yangi",
    "opacity": 0.98,
    "autostart": True,
    "compact": False,
    "sound_effect": False,
    "pos_offset_x": 0
}

def load_config():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                DEFAULT_CONFIG.update(data)
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(cfg):
    try:
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("Config save error:", e)


class TaskbarStripPanel:
    """Pastdagi qatorda (Taskbar ustida) doimiy turuvchi professional NamDPI alifbo paneli."""
    def __init__(self, root, engine, on_mode_changed=None, on_exit=None):
        self.root = root
        self.engine = engine
        self.on_mode_changed = on_mode_changed
        self.on_exit = on_exit
        self.config = load_config()

        self.mode_var = tk.StringVar(value=self.config.get("mode", "yangi"))
        self.engine.set_mode(self.mode_var.get())

        self.is_compact = self.config.get("compact", False)
        self.full_width = 460
        self.compact_width = 160
        self.panel_height = 36

        self._setup_window()
        self._build_ui()
        self._setup_drag()

    def _get_dock_position(self, width):
        offset_x = self.config.get("pos_offset_x", 0)
        import platform
        os_sys = platform.system()

        if os_sys == "Windows":
            rect = RECT()
            user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)
            base_x = rect.right - width - 16
            x = max(10, min(rect.right - width - 5, base_x + offset_x))
            y = max(10, rect.bottom - self.panel_height - 6)
        elif os_sys == "Darwin":
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            base_x = sw - width - 20
            x = max(10, base_x + offset_x)
            y = max(10, sh - self.panel_height - 75)
        else: # Linux
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            base_x = sw - width - 16
            x = max(10, base_x + offset_x)
            y = max(10, sh - self.panel_height - 48)
        return x, y

    def _setup_window(self):
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", self.config.get("opacity", 0.98))

        w = self.compact_width if self.is_compact else self.full_width
        x, y = self._get_dock_position(w)
        self.root.geometry(f"{w}x{self.panel_height}+{x}+{y}")
        self.root.configure(bg="#0F172A")

    def _build_ui(self):
        # Asosiy ramka (Fluent Card)
        self.main_card = tk.Frame(
            self.root,
            bg="#0F172A",
            bd=1,
            relief="solid",
            highlightbackground="#06B6D4", # Cyan accent
            highlightthickness=1
        )
        self.main_card.pack(fill="both", expand=True)

        # Ichki qatlam
        self.inner_bar = tk.Frame(self.main_card, bg="#1E293B")
        self.inner_bar.pack(fill="both", expand=True, padx=2, pady=2)

        # 1. NamDPI Brendi va Monogrammasi
        self.brand_frame = tk.Frame(self.inner_bar, bg="#1E293B", cursor="hand2")
        self.brand_frame.pack(side="left", padx=(6, 4), pady=2)
        self.brand_frame.bind("<Button-1>", lambda e: self.show_about_dialog())

        # Indicator dot
        self.dot_lbl = tk.Label(self.brand_frame, text="●", fg="#06B6D4", bg="#1E293B", font=("Segoe UI", 9))
        self.dot_lbl.pack(side="left", padx=(0, 2))

        # Brand title
        self.title_lbl = tk.Label(
            self.brand_frame,
            text="NamDPI",
            fg="#F8FAFC",
            bg="#1E293B",
            font=("Segoe UI", 9, "bold")
        )
        self.title_lbl.pack(side="left")

        # 2. Rejimlar tugmalari konteyneri
        self.modes_container = tk.Frame(self.inner_bar, bg="#1E293B")
        if not self.is_compact:
            self.modes_container.pack(side="left", fill="y", padx=4)

        # Rejimlar ta'rifi
        self.buttons = {}
        self.modes_data = [
            ("yangi", "Ö Yangi", "#0891B2", "#00FFF0"),       # Cyan
            ("kril", "Ў Кирилл", "#D97706", "#FDE047"),       # Amber
            ("lotin", "Oʻ Lotin", "#059669", "#6EE7B7"),      # Emerald
            ("off", "✕ Oʻchiq", "#475569", "#CBD5E1")         # Slate
        ]

        for code, label, active_bg, active_fg in self.modes_data:
            btn = tk.Label(
                self.modes_container,
                text=label,
                bg="#334155",
                fg="#CBD5E1",
                font=("Segoe UI", 8, "bold"),
                padx=8,
                pady=2,
                cursor="hand2",
                relief="flat"
            )
            btn.pack(side="left", padx=2, pady=2)

            def make_handler(m=code):
                return lambda e: self.select_mode(m)

            btn.bind("<Button-1>", make_handler())

            # Hover effekti
            def make_enter(w=btn, c=code):
                return lambda e: self._on_btn_hover(w, c, True)
            def make_leave(w=btn, c=code):
                return lambda e: self._on_btn_hover(w, c, False)

            btn.bind("<Enter>", make_enter())
            btn.bind("<Leave>", make_leave())

            self.buttons[code] = {
                "widget": btn,
                "label": label,
                "active_bg": active_bg,
                "active_fg": active_fg
            }

        # Compact badge (agar ixcham rejimda bo'lsa)
        self.compact_badge = tk.Label(
            self.inner_bar,
            text="Ö Yangi",
            bg="#0891B2",
            fg="#FFFFFF",
            font=("Segoe UI", 8, "bold"),
            padx=8,
            pady=2,
            cursor="hand2"
        )
        self.compact_badge.bind("<Button-1>", lambda e: self.cycle_mode())
        if self.is_compact:
            self.compact_badge.pack(side="left", padx=4)

        # 3. O'ng tarafdagi boshqaruv paneli (F8, ⚙, Minimize)
        self.ctrl_frame = tk.Frame(self.inner_bar, bg="#1E293B")
        self.ctrl_frame.pack(side="right", padx=(2, 4))

        # Hotkey badge [F8]
        self.hotkey_badge = tk.Label(
            self.ctrl_frame,
            text="F8",
            fg="#94A3B8",
            bg="#0F172A",
            font=("Segoe UI", 7, "bold"),
            padx=4,
            pady=1,
            cursor="hand2"
        )
        self.hotkey_badge.pack(side="left", padx=(1, 3))
        self.hotkey_badge.bind("<Button-1>", lambda e: self.cycle_mode())

        # Settings icon
        btn_settings = tk.Label(
            self.ctrl_frame,
            text="⚙",
            fg="#94A3B8",
            bg="#1E293B",
            font=("Segoe UI", 9),
            width=2,
            cursor="hand2"
        )
        btn_settings.pack(side="left", padx=1)
        btn_settings.bind("<Button-1>", lambda e: self.show_about_dialog())
        btn_settings.bind("<Enter>", lambda e: btn_settings.configure(fg="#38BDF8"))
        btn_settings.bind("<Leave>", lambda e: btn_settings.configure(fg="#94A3B8"))

        # Compact toggle / Minimize button
        btn_compact = tk.Label(
            self.ctrl_frame,
            text="«" if not self.is_compact else "»",
            fg="#94A3B8",
            bg="#1E293B",
            font=("Segoe UI", 9, "bold"),
            width=2,
            cursor="hand2"
        )
        btn_compact.pack(side="left", padx=1)
        btn_compact.bind("<Button-1>", lambda e: self.toggle_compact())
        btn_compact.bind("<Enter>", lambda e: btn_compact.configure(fg="#F8FAFC"))
        btn_compact.bind("<Leave>", lambda e: btn_compact.configure(fg="#94A3B8"))
        self.btn_compact = btn_compact

        # Tray hide button
        btn_min = tk.Label(
            self.ctrl_frame,
            text="▼",
            fg="#94A3B8",
            bg="#1E293B",
            font=("Segoe UI", 7),
            width=2,
            cursor="hand2"
        )
        btn_min.pack(side="left", padx=1)
        btn_min.bind("<Button-1>", lambda e: self.hide_to_tray())
        btn_min.bind("<Enter>", lambda e: btn_min.configure(fg="#F87171"))
        btn_min.bind("<Leave>", lambda e: btn_min.configure(fg="#94A3B8"))

        self._update_ui_state()

    def _on_btn_hover(self, widget, code, is_hover):
        if code != self.mode_var.get():
            if is_hover:
                widget.configure(bg="#475569", fg="#F8FAFC")
            else:
                widget.configure(bg="#334155", fg="#CBD5E1")

    def _setup_drag(self):
        """Panelni pastki qator bo'ylab gorizontal siljitish imkoniyati."""
        self.brand_frame.bind("<ButtonPress-1>", self._start_drag)
        self.brand_frame.bind("<ButtonRelease-1>", self._stop_drag)
        self.brand_frame.bind("<B1-Motion>", self._on_drag)

    def _start_drag(self, event):
        self._drag_start_x = event.x_root

    def _on_drag(self, event):
        dx = event.x_root - self._drag_start_x
        self._drag_start_x = event.x_root
        new_x = self.root.winfo_x() + dx
        self.root.geometry(f"+{new_x}+{self.root.winfo_y()}")

    def _stop_drag(self, event):
        rect = RECT()
        user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)
        base_x = rect.right - self.root.winfo_width() - 16
        offset = self.root.winfo_x() - base_x
        self.config["pos_offset_x"] = offset
        save_config(self.config)

    def toggle_compact(self):
        """Ixcham (mini-kapsula) va to'liq rejim o'rtasida almashtirish."""
        self.is_compact = not self.is_compact
        self.config["compact"] = self.is_compact
        save_config(self.config)

        w = self.compact_width if self.is_compact else self.full_width
        x, y = self._get_dock_position(w)
        self.root.geometry(f"{w}x{self.panel_height}+{x}+{y}")

        self.btn_compact.configure(text="»" if self.is_compact else "«")

        if self.is_compact:
            self.modes_container.pack_forget()
            self.compact_badge.pack(side="left", padx=4)
        else:
            self.compact_badge.pack_forget()
            self.modes_container.pack(side="left", fill="y", padx=4)

        self._update_ui_state()

    def select_mode(self, mode):
        self.mode_var.set(mode)
        self.engine.set_mode(mode)
        self.config["mode"] = mode
        save_config(self.config)
        self._update_ui_state()
        if self.on_mode_changed:
            self.on_mode_changed(mode)

    def cycle_mode(self):
        """F8 yoki Ctrl+Shift+U orqali tezkor navbatma-navbat almashtirish."""
        order = ["yangi", "kril", "lotin", "off"]
        cur = self.mode_var.get()
        if cur in order:
            nxt = order[(order.index(cur) + 1) % len(order)]
        else:
            nxt = "yangi"
        self.select_mode(nxt)

    def _update_ui_state(self):
        active = self.mode_var.get()

        # Dot rangi
        dot_colors = {
            "yangi": "#06B6D4", # Cyan
            "kril": "#F59E0B",  # Amber
            "lotin": "#10B981", # Emerald
            "off": "#64748B"    # Slate
        }
        self.dot_lbl.configure(fg=dot_colors.get(active, "#06B6D4"))

        # Tugmalar holati
        for code, data in self.buttons.items():
            w = data["widget"]
            if code == active:
                w.configure(bg=data["active_bg"], fg=data["active_fg"])
            else:
                w.configure(bg="#334155", fg="#CBD5E1")

        # Compact badge matni
        mode_labels = {
            "yangi": "Ö Yangi",
            "kril": "Ў Кирилл",
            "lotin": "Oʻ Lotin",
            "off": "✕ Oʻchiq"
        }
        active_label = mode_labels.get(active, "Ö Yangi")
        self.compact_badge.configure(
            text=active_label,
            bg=self.buttons[active]["active_bg"],
            fg=self.buttons[active]["active_fg"]
        )

    def hide_to_tray(self):
        self.root.withdraw()

    def show_window(self):
        self.root.deiconify()
        self.root.attributes("-topmost", True)

    def show_about_dialog(self):
        from utils import is_autostart_enabled, set_autostart

        dlg = tk.Toplevel(self.root)
        dlg.title("NamDPI alifbo - Sozlamalar va Ma'lumot")
        dlg.geometry("480x460")
        dlg.resizable(False, False)
        dlg.configure(bg="#0F172A")
        dlg.attributes("-topmost", True)

        # Markazga chiroyli joylashtirish
        rx = max(20, self.root.winfo_x() - 40)
        ry = max(20, self.root.winfo_y() - 440)
        dlg.geometry(f"+{rx}+{ry}")

        # Header card
        hdr = tk.Frame(dlg, bg="#1E293B", padx=16, pady=12)
        hdr.pack(fill="x", padx=16, pady=(16, 10))

        title = tk.Label(
            hdr,
            text="NamDPI alifbo",
            font=("Segoe UI", 14, "bold"),
            fg="#06B6D4",
            bg="#1E293B"
        )
        title.pack(anchor="w")

        sub = tk.Label(
            hdr,
            text="Namangan davlat pedagogika instituti\nRaqamli ta'lim texnologiyalari markazi (NamDPI RTTM)",
            font=("Segoe UI", 9),
            fg="#94A3B8",
            bg="#1E293B",
            justify="left"
        )
        sub.pack(anchor="w", pady=(2, 0))

        # Alifbo qoidalari cheat-sheet
        rules_card = tk.Frame(dlg, bg="#1E293B", padx=14, pady=10)
        rules_card.pack(fill="x", padx=16, pady=6)

        rules_title = tk.Label(
            rules_card,
            text="✨ Yangi Oʻzbek Lotin alifbosi (2026):",
            font=("Segoe UI", 9, "bold"),
            fg="#F8FAFC",
            bg="#1E293B"
        )
        rules_title.pack(anchor="w", pady=(0, 4))

        rules_text = (
            "  •  sh  ➔  ş    (masalan:  shabnam  ➔  şabnam)\n"
            "  •  ch  ➔  ç    (masalan:  choy  ➔  çoy)\n"
            "  •  oʻ, o'  ➔  ö  (masalan:  o'zbekiston  ➔  özbekiston)\n"
            "  •  gʻ, g'  ➔  ğ  (masalan:  bog'  ➔  boğ,  g'alaba  ➔  ğalaba)\n"
            "  •  Kirill  ➔  shanba  ➔  шанба,  shabnam  ➔  шабнам"
        )
        tk.Label(
            rules_card,
            text=rules_text,
            font=("Consolas", 9),
            fg="#38BDF8",
            bg="#1E293B",
            justify="left"
        ).pack(anchor="w")

        # Sozlamalar
        opt_card = tk.Frame(dlg, bg="#1E293B", padx=14, pady=10)
        opt_card.pack(fill="x", padx=16, pady=6)

        autostart_var = tk.BooleanVar(value=is_autostart_enabled())
        def toggle_autostart():
            val = autostart_var.get()
            set_autostart(val)
            self.config["autostart"] = val
            save_config(self.config)

        chk_auto = tk.Checkbutton(
            opt_card,
            text="Windows bilan birga avtomatik ishga tushish",
            variable=autostart_var,
            command=toggle_autostart,
            bg="#1E293B",
            fg="#F1F5F9",
            selectcolor="#0F172A",
            activebackground="#1E293B",
            activeforeground="#06B6D4",
            font=("Segoe UI", 8, "bold")
        )
        chk_auto.pack(anchor="w", pady=2)

        # Shaffoflik
        op_row = tk.Frame(opt_card, bg="#1E293B")
        op_row.pack(fill="x", pady=(4, 0))
        tk.Label(
            op_row,
            text="Panel shaffofligi:",
            bg="#1E293B",
            fg="#94A3B8",
            font=("Segoe UI", 8)
        ).pack(side="left")

        def on_opacity_change(val):
            alpha = float(val) / 100.0
            self.root.attributes("-alpha", alpha)
            self.config["opacity"] = alpha
            save_config(self.config)

        cur_op = int(self.config.get("opacity", 0.98) * 100)
        scale_op = tk.Scale(
            op_row,
            from_=60,
            to=100,
            orient="horizontal",
            command=on_opacity_change,
            bg="#1E293B",
            fg="#06B6D4",
            highlightthickness=0,
            length=180,
            font=("Segoe UI", 7)
        )
        scale_op.set(cur_op)
        scale_op.pack(side="right")

        # Tezkor klavishlar eslatmasi
        hotkey_hint = tk.Label(
            dlg,
            text="💡 Tezkor almashtirish:  F8  yoki  Ctrl + Shift + U",
            font=("Segoe UI", 8, "bold"),
            fg="#F59E0B",
            bg="#0F172A"
        )
        hotkey_hint.pack(pady=4)

        # Tugmalar
        btn_bar = tk.Frame(dlg, bg="#0F172A")
        btn_bar.pack(pady=(8, 12))

        btn_close = tk.Button(
            btn_bar,
            text="Yopish",
            command=dlg.destroy,
            bg="#06B6D4",
            fg="#0F172A",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=16,
            pady=4,
            cursor="hand2"
        )
        btn_close.pack(side="left", padx=8)

        if self.on_exit:
            btn_exit = tk.Button(
                btn_bar,
                text="Dasturdan chiqish",
                command=self.on_exit,
                bg="#EF4444",
                fg="#FFFFFF",
                font=("Segoe UI", 9, "bold"),
                relief="flat",
                padx=16,
                pady=4,
                cursor="hand2"
            )
            btn_exit.pack(side="left", padx=8)
