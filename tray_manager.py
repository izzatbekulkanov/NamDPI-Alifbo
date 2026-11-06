# -*- coding: utf-8 -*-
"""
NamDPI alifbo - System Tray menejeri (Yuqori aniqlikdagi dinamik belgilar)
Ko'p tillilik va Yangilanish tekshiruvi integratsiyasi
Namangan davlat pedagogika instituti
Raqamli ta'lim texnologiyalari markazi (NamDPI RTTM)
"""

import threading
from PIL import Image, ImageDraw, ImageFont
import pystray
from pystray import MenuItem as item
import os

from i18n import t, get_language, set_language

def create_mode_icon_image(mode, is_locked=False):
    """
    128x128 o'lchamda chizib, 32x32 ga antialiasing (LANCZOS) bilan
    kichraytiradi. Natijada Windows taskbarida belgi tiniq va professional chiqadi.
    """
    canvas_size = 128
    img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    border_color = (239, 68, 68, 255) if is_locked else (6, 182, 212, 230)

    # Gradient/Fon
    r = 28
    pad = 4
    draw.rounded_rectangle(
        [pad, pad, canvas_size - pad - 1, canvas_size - pad - 1],
        radius=r,
        fill=(15, 23, 42, 255),      # Slate 900
        outline=border_color,
        width=5
    )

    # Shrift tanlash
    font = None
    font_names = ["segoeuib.ttf", "segoeui.ttf", "arialbd.ttf", "arial.ttf"]
    for fn in font_names:
        try:
            if is_locked:
                font = ImageFont.truetype(fn, 56)
            elif mode == 'off':
                font = ImageFont.truetype(fn, 44)
            elif mode == 'lotin':
                font = ImageFont.truetype(fn, 56)
            else:
                font = ImageFont.truetype(fn, 72)
            break
        except Exception:
            continue

    if not font:
        font = ImageFont.load_default()

    if is_locked:
        color = (239, 68, 68, 255)   # Red
        text = "!"
    elif mode == 'yangi':
        color = (6, 182, 212, 255)   # Cyan
        text = "Ö"
    elif mode == 'kril':
        color = (245, 158, 11, 255)  # Amber / Gold
        text = "Ў"
    elif mode == 'lotin':
        color = (16, 185, 129, 255)  # Emerald
        text = "Oʻ"
    else:
        color = (239, 68, 68, 255)   # Red
        text = "OFF"

    # Markazga chizish
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (canvas_size - tw) // 2
    y = (canvas_size - th) // 2 - 4
    draw.text((x, y), text, font=font, fill=color)

    # 32x32 ga yuqori sifatda kichraytirish
    final_icon = img.resize((32, 32), Image.Resampling.LANCZOS)
    return final_icon


class TrayManager:
    def __init__(self, panel, engine, on_exit):
        self.panel = panel
        self.engine = engine
        self.on_exit = on_exit
        self.icon = None

    def create_menu(self):
        def set_mode_cb(m):
            return lambda: self.set_mode(m)

        def is_mode(m):
            return lambda itm: self.panel.mode_var.get() == m

        def set_lang_cb(l):
            return lambda: self.panel.change_language(l)

        def is_lang(l):
            return lambda itm: get_language() == l

        return pystray.Menu(
            item(t("app_title"), None, enabled=False),
            item(t("tray_toggle"), lambda: self.toggle_panel(), default=True),
            pystray.Menu.SEPARATOR,
            item(t("tray_mode_yangi"), set_mode_cb("yangi"), checked=is_mode("yangi")),
            item(t("tray_mode_kril"), set_mode_cb("kril"), checked=is_mode("kril")),
            item(t("tray_mode_lotin"), set_mode_cb("lotin"), checked=is_mode("lotin")),
            item(t("tray_mode_off"), set_mode_cb("off"), checked=is_mode("off")),
            pystray.Menu.SEPARATOR,
            item(t("tray_language"), pystray.Menu(
                item("Oʻzbekcha", set_lang_cb("uz"), checked=is_lang("uz")),
                item("Русский", set_lang_cb("ru"), checked=is_lang("ru")),
                item("English", set_lang_cb("en"), checked=is_lang("en"))
            )),
            item(f"🔄 {t('tray_check_update')}", lambda: self.panel.check_for_updates_manual()),
            pystray.Menu.SEPARATOR,
            item(f"⚙ {t('tray_settings')}", lambda: self.panel.show_about_dialog()),
            item(f"🚪 {t('tray_exit')}", lambda: self.exit_app())
        )

    def set_mode(self, mode):
        self.panel.select_mode(mode)
        self.update_icon(mode)

    def update_menu(self):
        """Til yoki sozlamalar o'zgarganda menyuni qayta yangilash."""
        if self.icon:
            try:
                self.icon.menu = self.create_menu()
            except Exception as e:
                print("Tray menu update error:", e)

    def update_icon(self, mode=None):
        if self.icon:
            try:
                cur_mode = mode or self.panel.mode_var.get()
                is_locked = getattr(self.panel, "is_locked", False)
                new_img = create_mode_icon_image(cur_mode, is_locked=is_locked)
                self.icon.icon = new_img

                mode_title = t(f"mode_{cur_mode}")
                if is_locked:
                    self.icon.title = f"NamDPI alifbo - {t('locked_badge')}"
                else:
                    self.icon.title = f"NamDPI alifbo - {mode_title}"
            except Exception as e:
                print("Tray update error:", e)

    def toggle_panel(self):
        if self.panel.root.state() == "withdrawn":
            self.panel.show_window()
        else:
            self.panel.hide_to_tray()

    def run(self):
        cur_mode = self.panel.mode_var.get()
        initial_image = create_mode_icon_image(cur_mode)

        self.icon = pystray.Icon(
            "NamDPI_Alifbo",
            initial_image,
            "NamDPI alifbo (Namangan davlat pedagogika instituti)",
            menu=self.create_menu()
        )
        self.icon.run()

    def start_in_thread(self):
        t = threading.Thread(target=self.run, daemon=True)
        t.start()
        return t

    def exit_app(self):
        if self.icon:
            self.icon.stop()
        if self.on_exit:
            self.on_exit()
