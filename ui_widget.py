# -*- coding: utf-8 -*-
"""
NamDPI alifbo - Professional Pastki Panel (Taskbar Dock Panel)
Ko'p tillilik (UZ / RU / EN) va Avtomatik Yangilanish Tizimi
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
import platform

from i18n import t, set_language, get_language, LANGUAGES
from updater import UpdateChecker, CURRENT_VERSION

OS_SYSTEM = platform.system() # 'Windows', 'Darwin', 'Linux'

if OS_SYSTEM == "Windows":
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
    "pos_offset_x": 0,
    "language": "uz"
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


class UpdateCornerDialog(tk.Toplevel):
    """
    Ekranning pastki burchagida majburiy ko'rsatiladigan yangilanish darchasi.
    Foydalanuvchi yangilamaguncha dastur klaviatura transliteratsiyasini to'xtatib turadi.
    """
    def __init__(self, parent_panel, update_info):
        super().__init__(parent_panel.root)
        self.parent_panel = parent_panel
        self.update_info = update_info
        self.updater = parent_panel.updater

        self.title(t("update_available_title"))
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(bg="#0F172A")

        self.win_width = 410
        self.win_height = 280
        self._position_in_corner()
        self._build_ui()

    def _position_in_corner(self):
        """Ekranning pastki o'ng burchagiga (dock panelning ustiga) joylashtirish."""
        try:
            if OS_SYSTEM == "Windows":
                rect = RECT()
                user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)
                x = max(10, rect.right - self.win_width - 16)
                y = max(10, rect.bottom - self.win_height - 48)
            else:
                sw = self.winfo_screenwidth()
                sh = self.winfo_screenheight()
                x = max(10, sw - self.win_width - 16)
                y = max(10, sh - self.win_height - 60)
            self.geometry(f"{self.win_width}x{self.win_height}+{x}+{y}")
        except Exception:
            self.geometry(f"{self.win_width}x{self.win_height}+100+100")

    def _build_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Tashqi chegarali asosiy karta (Qizil/To'q sariq urg'u bilan)
        card = tk.Frame(
            self,
            bg="#0F172A",
            bd=2,
            relief="solid",
            highlightbackground="#EF4444", # Urgent Red
            highlightthickness=1
        )
        card.pack(fill="both", expand=True, padx=2, pady=2)

        # 1. Header (Ogohlantirish va Til almashtirish)
        hdr = tk.Frame(card, bg="#1E293B", padx=12, pady=8)
        hdr.pack(fill="x")

        lbl_icon = tk.Label(hdr, text="🚀", bg="#1E293B", font=("Segoe UI", 12))
        lbl_icon.pack(side="left", padx=(0, 6))

        lbl_title = tk.Label(
            hdr,
            text=t("update_available_title"),
            fg="#F8FAFC",
            bg="#1E293B",
            font=("Segoe UI", 10, "bold")
        )
        lbl_title.pack(side="left")

        # Tilni o'zgartirish tugmalari (UZ, RU, EN)
        lang_frame = tk.Frame(hdr, bg="#1E293B")
        lang_frame.pack(side="right")

        for l_code, l_label in [("uz", "UZ"), ("ru", "RU"), ("en", "EN")]:
            is_active = (get_language() == l_code)
            btn_l = tk.Label(
                lang_frame,
                text=l_label,
                fg="#F8FAFC" if is_active else "#94A3B8",
                bg="#06B6D4" if is_active else "#334155",
                font=("Segoe UI", 7, "bold"),
                padx=4,
                pady=1,
                cursor="hand2"
            )
            btn_l.pack(side="left", padx=1)
            def make_change_lang(c=l_code):
                return lambda e: self.on_lang_click(c)
            btn_l.bind("<Button-1>", make_change_lang())

        # 2. Tanasi
        body = tk.Frame(card, bg="#0F172A", padx=14, pady=10)
        body.pack(fill="both", expand=True)

        # Versiya tafsiloti
        ver_text = t("update_version_label", new_ver=self.update_info.tag_name, cur_ver=CURRENT_VERSION)
        lbl_ver = tk.Label(
            body,
            text=ver_text,
            fg="#38BDF8",
            bg="#0F172A",
            font=("Segoe UI", 9, "bold")
        )
        lbl_ver.pack(anchor="w", pady=(0, 4))

        # Majburiy pauza ogohlantirishi
        warn_box = tk.Frame(body, bg="#450A0A", padx=8, pady=6, bd=1, relief="solid", highlightbackground="#EF4444")
        warn_box.pack(fill="x", pady=(2, 8))

        lbl_warn = tk.Label(
            warn_box,
            text=t("update_paused_warning"),
            fg="#FCA5A5",
            bg="#450A0A",
            font=("Segoe UI", 8, "bold"),
            wraplength=350,
            justify="left"
        )
        lbl_warn.pack(anchor="w")

        # Status va Progress Bar
        self.status_lbl = tk.Label(
            body,
            text=t("locked_desc"),
            fg="#94A3B8",
            bg="#0F172A",
            font=("Segoe UI", 8),
            wraplength=360,
            justify="left"
        )
        self.status_lbl.pack(anchor="w", pady=(0, 6))

        # Progress bar foni
        self.progress_frame = tk.Frame(body, bg="#334155", height=8)
        self.progress_bar = tk.Frame(self.progress_frame, bg="#06B6D4", height=8, width=0)
        self.progress_bar.place(x=0, y=0, relheight=1.0, width=0)

        # 3. Tugmalar paneli
        self.actions_frame = tk.Frame(card, bg="#1E293B", padx=12, pady=10)
        self.actions_frame.pack(fill="x", side="bottom")

        self.btn_download = tk.Button(
            self.actions_frame,
            text=f"📥  {t('update_download_btn')}",
            command=self.start_download,
            bg="#059669", # Emerald
            fg="#FFFFFF",
            activebackground="#10B981",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            pady=6,
            cursor="hand2"
        )
        self.btn_download.pack(fill="x")

    def on_lang_click(self, lang_code):
        self.parent_panel.change_language(lang_code)
        self._build_ui()

    def start_download(self):
        asset = self.update_info.get_platform_asset()
        if not asset:
            self.status_lbl.configure(text=t("update_error", err="Fayl topilmadi"), fg="#EF4444")
            return

        self.btn_download.configure(state="disabled", bg="#475569")
        self.progress_frame.pack(fill="x", pady=(2, 6))

        def on_prog(percent, received, total):
            def _ui():
                rec_mb = f"{received / (1024*1024):.1f} MB"
                tot_mb = f"{total / (1024*1024):.1f} MB"
                self.status_lbl.configure(
                    text=t("update_downloading", percent=percent, received=rec_mb, total=tot_mb),
                    fg="#38BDF8"
                )
                bar_width = int((self.win_width - 40) * (percent / 100.0))
                self.progress_bar.place_configure(width=bar_width)
            self.after(0, _ui)

        def on_done(dest_path):
            def _ui():
                self.status_lbl.configure(text=t("update_launching"), fg="#10B981")
                self.after(1000, lambda: self._launch_and_exit(dest_path))
            self.after(0, _ui)

        def on_err(err_msg):
            def _ui():
                self.status_lbl.configure(text=t("update_error", err=err_msg), fg="#EF4444")
                self.btn_download.configure(state="normal", text=t("update_retry"), bg="#DC2626")
            self.after(0, _ui)

        self.updater.download_and_install(
            asset=asset,
            on_progress=on_prog,
            on_complete=on_done,
            on_error=on_err
        )

    def _launch_and_exit(self, installer_path):
        try:
            self.updater.launch_installer(installer_path)
        except Exception as e:
            print("Installer launch error:", e)
        if self.parent_panel.on_exit:
            self.parent_panel.on_exit()
        else:
            self.parent_panel.root.destroy()
            sys.exit(0)


class TaskbarStripPanel:
    """Pastdagi qatorda (Taskbar ustida) doimiy turuvchi professional NamDPI alifbo paneli."""
    def __init__(self, root, engine, on_mode_changed=None, on_exit=None, on_language_changed=None):
        self.root = root
        self.engine = engine
        self.on_mode_changed = on_mode_changed
        self.on_exit = on_exit
        self.on_language_changed = on_language_changed

        self.config = load_config()
        set_language(self.config.get("language", "uz"))

        self.updater = UpdateChecker(CURRENT_VERSION)
        self.update_corner_dlg = None
        self.is_locked = False
        self.update_info = None

        self.mode_var = tk.StringVar(value=self.config.get("mode", "yangi"))
        self.engine.set_mode(self.mode_var.get())

        self.is_compact = self.config.get("compact", False)
        self.full_width = 490
        self.compact_width = 170
        self.panel_height = 36

        self._setup_window()
        self._build_ui()
        self._setup_drag()

    def _get_dock_position(self, width):
        offset_x = self.config.get("pos_offset_x", 0)

        if OS_SYSTEM == "Windows":
            rect = RECT()
            user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)
            base_x = rect.right - width - 16
            x = max(10, min(rect.right - width - 5, base_x + offset_x))
            y = max(10, rect.bottom - self.panel_height - 6)
        elif OS_SYSTEM == "Darwin":
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
        for widget in self.root.winfo_children():
            widget.destroy()

        # Asosiy ramka (Fluent Card)
        border_color = "#EF4444" if self.is_locked else "#06B6D4"
        self.main_card = tk.Frame(
            self.root,
            bg="#0F172A",
            bd=1,
            relief="solid",
            highlightbackground=border_color,
            highlightthickness=1
        )
        self.main_card.pack(fill="both", expand=True)

        # Ichki qatlam
        self.inner_bar = tk.Frame(self.main_card, bg="#1E293B")
        self.inner_bar.pack(fill="both", expand=True, padx=2, pady=2)

        # 1. NamDPI Brendi va Monogrammasi
        self.brand_frame = tk.Frame(self.inner_bar, bg="#1E293B", cursor="hand2")
        self.brand_frame.pack(side="left", padx=(6, 4), pady=2)
        self.brand_frame.bind("<Button-1>", lambda e: self.on_brand_click())

        # Indicator dot
        dot_color = "#EF4444" if self.is_locked else "#06B6D4"
        self.dot_lbl = tk.Label(self.brand_frame, text="●", fg=dot_color, bg="#1E293B", font=("Segoe UI", 9))
        self.dot_lbl.pack(side="left", padx=(0, 2))

        # Brand title
        self.title_lbl = tk.Label(
            self.brand_frame,
            text="NamDPI" if not self.is_locked else "NamDPI [⚠️]",
            fg="#F8FAFC",
            bg="#1E293B",
            font=("Segoe UI", 9, "bold")
        )
        self.title_lbl.pack(side="left")

        # 2. Rejimlar tugmalari konteyneri
        self.modes_container = tk.Frame(self.inner_bar, bg="#1E293B")
        if not self.is_compact:
            self.modes_container.pack(side="left", fill="y", padx=3)

        # Rejimlar ta'rifi (i18n orqali olinadi)
        self.buttons = {}
        self.modes_data = [
            ("yangi", "mode_yangi", "#0891B2", "#00FFF0"),       # Cyan
            ("kril", "mode_kril", "#D97706", "#FDE047"),         # Amber
            ("lotin", "mode_lotin", "#059669", "#6EE7B7"),       # Emerald
            ("off", "mode_off", "#475569", "#CBD5E1")           # Slate
        ]

        for code, label_key, active_bg, active_fg in self.modes_data:
            label_text = t(label_key)
            btn = tk.Label(
                self.modes_container,
                text=label_text,
                bg="#334155",
                fg="#CBD5E1",
                font=("Segoe UI", 8, "bold"),
                padx=6,
                pady=2,
                cursor="hand2" if not self.is_locked else "no",
                relief="flat"
            )
            btn.pack(side="left", padx=2, pady=2)

            def make_handler(m=code):
                return lambda e: self.select_mode(m)

            btn.bind("<Button-1>", make_handler())

            def make_enter(w=btn, c=code):
                return lambda e: self._on_btn_hover(w, c, True)
            def make_leave(w=btn, c=code):
                return lambda e: self._on_btn_hover(w, c, False)

            btn.bind("<Enter>", make_enter())
            btn.bind("<Leave>", make_leave())

            self.buttons[code] = {
                "widget": btn,
                "label_key": label_key,
                "active_bg": active_bg,
                "active_fg": active_fg
            }

        # Compact badge (agar ixcham rejimda bo'lsa)
        self.compact_badge = tk.Label(
            self.inner_bar,
            text=t(f"mode_{self.mode_var.get()}"),
            bg="#0891B2",
            fg="#FFFFFF",
            font=("Segoe UI", 8, "bold"),
            padx=6,
            pady=2,
            cursor="hand2"
        )
        self.compact_badge.bind("<Button-1>", lambda e: self.cycle_mode())
        if self.is_compact:
            self.compact_badge.pack(side="left", padx=3)

        # 3. O'ng tarafdagi boshqaruv paneli (🌐 Til, F8, ⚙, Minimize)
        self.ctrl_frame = tk.Frame(self.inner_bar, bg="#1E293B")
        self.ctrl_frame.pack(side="right", padx=(2, 4))

        # Til tugmasi (🌐 UZ / RU / EN)
        self.lang_badge = tk.Label(
            self.ctrl_frame,
            text=get_language().upper(),
            fg="#38BDF8",
            bg="#0F172A",
            font=("Segoe UI", 7, "bold"),
            padx=4,
            pady=1,
            cursor="hand2"
        )
        self.lang_badge.pack(side="left", padx=(1, 2))
        self.lang_badge.bind("<Button-1>", lambda e: self.cycle_language())

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
        self.hotkey_badge.pack(side="left", padx=(1, 2))
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

        # Compact toggle
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

    def on_brand_click(self):
        if self.is_locked:
            self.show_update_dialog()
        else:
            self.show_about_dialog()

    def _on_btn_hover(self, widget, code, is_hover):
        if self.is_locked:
            return
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
        if OS_SYSTEM == "Windows":
            rect = RECT()
            user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)
            base_x = rect.right - self.root.winfo_width() - 16
        else:
            base_x = self.root.winfo_screenwidth() - self.root.winfo_width() - 16
        offset = self.root.winfo_x() - base_x
        self.config["pos_offset_x"] = offset
        save_config(self.config)

    def toggle_compact(self):
        self.is_compact = not self.is_compact
        self.config["compact"] = self.is_compact
        save_config(self.config)

        w = self.compact_width if self.is_compact else self.full_width
        x, y = self._get_dock_position(w)
        self.root.geometry(f"{w}x{self.panel_height}+{x}+{y}")

        self.btn_compact.configure(text="»" if self.is_compact else "«")

        if self.is_compact:
            self.modes_container.pack_forget()
            self.compact_badge.pack(side="left", padx=3)
        else:
            self.compact_badge.pack_forget()
            self.modes_container.pack(side="left", fill="y", padx=3)

        self._update_ui_state()

    def select_mode(self, mode):
        if self.is_locked:
            self.show_update_dialog()
            return
        self.mode_var.set(mode)
        self.engine.set_mode(mode)
        self.config["mode"] = mode
        save_config(self.config)
        self._update_ui_state()
        if self.on_mode_changed:
            self.on_mode_changed(mode)

    def cycle_mode(self):
        if self.is_locked:
            self.show_update_dialog()
            return
        order = ["yangi", "kril", "lotin", "off"]
        cur = self.mode_var.get()
        if cur in order:
            nxt = order[(order.index(cur) + 1) % len(order)]
        else:
            nxt = "yangi"
        self.select_mode(nxt)

    def cycle_language(self):
        """UZ -> RU -> EN -> UZ ketma-ketlikda almashtirish."""
        langs = ["uz", "ru", "en"]
        cur = get_language()
        nxt = langs[(langs.index(cur) + 1) % len(langs)]
        self.change_language(nxt)

    def change_language(self, new_lang):
        set_language(new_lang)
        self.config["language"] = new_lang
        save_config(self.config)
        self.refresh_ui_text()
        if self.on_language_changed:
            self.on_language_changed(new_lang)

    def refresh_ui_text(self):
        self.lang_badge.configure(text=get_language().upper())
        for code, data in self.buttons.items():
            data["widget"].configure(text=t(data["label_key"]))
        self._update_ui_state()

    def _update_ui_state(self):
        active = self.mode_var.get()

        if self.is_locked:
            self.dot_lbl.configure(fg="#EF4444")
            self.title_lbl.configure(text="NamDPI [⚠️]")
            for code, data in self.buttons.items():
                data["widget"].configure(bg="#27272A", fg="#71717A")
            self.compact_badge.configure(text=t("locked_badge"), bg="#DC2626", fg="#FFFFFF")
            return

        dot_colors = {
            "yangi": "#06B6D4",
            "kril": "#F59E0B",
            "lotin": "#10B981",
            "off": "#64748B"
        }
        self.dot_lbl.configure(fg=dot_colors.get(active, "#06B6D4"))
        self.title_lbl.configure(text="NamDPI")

        for code, data in self.buttons.items():
            w = data["widget"]
            if code == active:
                w.configure(bg=data["active_bg"], fg=data["active_fg"])
            else:
                w.configure(bg="#334155", fg="#CBD5E1")

        active_label = t(f"mode_{active}")
        active_btn = self.buttons.get(active, self.buttons["yangi"])
        self.compact_badge.configure(
            text=active_label,
            bg=active_btn["active_bg"],
            fg=active_btn["active_fg"]
        )

    # =========================================================================
    # YANGILANISH (UPDATE) BOSHQARUVI
    # =========================================================================

    def set_update_required(self, update_info):
        """Yangilanish mavjud bo'lganda dasturni qulflaydi va burchakda oynani ko'rsatadi."""
        self.is_locked = True
        self.update_info = update_info
        self.engine.lock("update_required")
        self._update_ui_state()
        self.show_update_dialog()

    def show_update_dialog(self):
        if not self.update_info:
            return
        if self.update_corner_dlg and self.update_corner_dlg.winfo_exists():
            self.update_corner_dlg.deiconify()
            self.update_corner_dlg.lift()
            return
        self.update_corner_dlg = UpdateCornerDialog(self, self.update_info)

    def check_for_updates_manual(self):
        """Foydalanuvchi menyudan tekshirganda."""
        def on_found(info):
            self.root.after(0, lambda: self.set_update_required(info))

        def on_none():
            self.root.after(0, lambda: messagebox.showinfo(
                t("app_title"),
                t("update_up_to_date", cur_ver=CURRENT_VERSION)
            ))

        def on_err(err):
            self.root.after(0, lambda: messagebox.showwarning(
                t("app_title"),
                f"{t('update_check_failed')}\n({err})"
            ))

        self.updater.check_in_background(on_found, on_none, on_err)

    def hide_to_tray(self):
        self.root.withdraw()

    def show_window(self):
        self.root.deiconify()
        self.root.attributes("-topmost", True)

    def show_about_dialog(self):
        from utils import is_autostart_enabled, set_autostart

        dlg = tk.Toplevel(self.root)
        dlg.title(t("settings_title"))
        dlg.geometry("500x520")
        dlg.resizable(False, False)
        dlg.configure(bg="#0F172A")
        dlg.attributes("-topmost", True)

        rx = max(20, self.root.winfo_x() - 40)
        ry = max(20, self.root.winfo_y() - 500)
        dlg.geometry(f"+{rx}+{ry}")

        # Header card
        hdr = tk.Frame(dlg, bg="#1E293B", padx=16, pady=12)
        hdr.pack(fill="x", padx=16, pady=(16, 8))

        title = tk.Label(
            hdr,
            text=f"{t('app_title')}  v{CURRENT_VERSION}",
            font=("Segoe UI", 13, "bold"),
            fg="#06B6D4",
            bg="#1E293B"
        )
        title.pack(anchor="w")

        sub = tk.Label(
            hdr,
            text=f"{t('org_name')}\n{t('dept_name')}",
            font=("Segoe UI", 9),
            fg="#94A3B8",
            bg="#1E293B",
            justify="left"
        )
        sub.pack(anchor="w", pady=(2, 0))

        # Alifbo qoidalari cheat-sheet
        rules_card = tk.Frame(dlg, bg="#1E293B", padx=14, pady=8)
        rules_card.pack(fill="x", padx=16, pady=4)

        rules_title = tk.Label(
            rules_card,
            text=t("rules_heading"),
            font=("Segoe UI", 9, "bold"),
            fg="#F8FAFC",
            bg="#1E293B"
        )
        rules_title.pack(anchor="w", pady=(0, 2))

        tk.Label(
            rules_card,
            text=t("rules_content"),
            font=("Consolas", 9),
            fg="#38BDF8",
            bg="#1E293B",
            justify="left"
        ).pack(anchor="w")

        # Sozlamalar kartasi
        opt_card = tk.Frame(dlg, bg="#1E293B", padx=14, pady=8)
        opt_card.pack(fill="x", padx=16, pady=4)

        # 1. Til tanlash
        lang_row = tk.Frame(opt_card, bg="#1E293B")
        lang_row.pack(fill="x", pady=(2, 6))

        tk.Label(
            lang_row,
            text=t("language_label"),
            bg="#1E293B",
            fg="#CBD5E1",
            font=("Segoe UI", 8, "bold")
        ).pack(side="left")

        lang_btns_frame = tk.Frame(lang_row, bg="#1E293B")
        lang_btns_frame.pack(side="right")

        for l_code, l_name in LANGUAGES.items():
            is_cur = (get_language() == l_code)
            lbl_btn = tk.Label(
                lang_btns_frame,
                text=l_name,
                bg="#06B6D4" if is_cur else "#334155",
                fg="#0F172A" if is_cur else "#F8FAFC",
                font=("Segoe UI", 8, "bold"),
                padx=6,
                pady=2,
                cursor="hand2"
            )
            lbl_btn.pack(side="left", padx=2)
            def make_l_setter(c=l_code, d=dlg):
                return lambda e: [self.change_language(c), d.destroy(), self.show_about_dialog()]
            lbl_btn.bind("<Button-1>", make_l_setter())

        # 2. Avtomatik ishga tushish
        autostart_var = tk.BooleanVar(value=is_autostart_enabled())
        def toggle_autostart():
            val = autostart_var.get()
            set_autostart(val)
            self.config["autostart"] = val
            save_config(self.config)

        chk_auto = tk.Checkbutton(
            opt_card,
            text=t("autostart_label"),
            variable=autostart_var,
            command=toggle_autostart,
            bg="#1E293B",
            fg="#F1F5F9",
            selectcolor="#0F172A",
            activebackground="#1E293B",
            activeforeground="#06B6D4",
            font=("Segoe UI", 8)
        )
        chk_auto.pack(anchor="w", pady=2)

        # 3. Shaffoflik
        op_row = tk.Frame(opt_card, bg="#1E293B")
        op_row.pack(fill="x", pady=(4, 0))
        tk.Label(
            op_row,
            text=t("opacity_label"),
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

        # 4. Yangilanishni tekshirish tugmasi
        btn_chk_update = tk.Button(
            opt_card,
            text=f"🔄 {t('check_updates_btn')}",
            command=lambda: [dlg.destroy(), self.check_for_updates_manual()],
            bg="#334155",
            fg="#38BDF8",
            font=("Segoe UI", 8, "bold"),
            relief="flat",
            padx=10,
            pady=3,
            cursor="hand2"
        )
        btn_chk_update.pack(anchor="w", pady=(8, 2))

        # Tezkor klavishlar eslatmasi
        hotkey_hint = tk.Label(
            dlg,
            text=t("hotkey_hint"),
            font=("Segoe UI", 8, "bold"),
            fg="#F59E0B",
            bg="#0F172A"
        )
        hotkey_hint.pack(pady=4)

        # Tugmalar
        btn_bar = tk.Frame(dlg, bg="#0F172A")
        btn_bar.pack(pady=(6, 12))

        btn_close = tk.Button(
            btn_bar,
            text=t("close_btn"),
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
                text=t("exit_btn"),
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
