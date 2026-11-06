# -*- coding: utf-8 -*-
"""
NamDPI alifbo - System Tray menejeri (Yuqori aniqlikdagi dinamik belgilar)
Namangan davlat pedagogika instituti
Raqamli ta'lim texnologiyalari markazi (NamDPI RTTM)
"""

import threading
from PIL import Image, ImageDraw, ImageFont
import pystray
from pystray import MenuItem as item
import os

def create_mode_icon_image(mode):
    """
    128x128 o'lchamda chizib, 32x32 ga antialiasing (LANCZOS) bilan
    kichraytiradi. Natijada Windows taskbarida belgi tiniq va professional chiqadi.
    """
    canvas_size = 128
    img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Gradient/Fon
    r = 28
    pad = 4
    draw.rounded_rectangle(
        [pad, pad, canvas_size - pad - 1, canvas_size - pad - 1],
        radius=r,
        fill=(15, 23, 42, 255),      # Slate 900
        outline=(6, 182, 212, 230),  # Cyan
        width=5
    )

    # Shrift tanlash
    font = None
    font_names = ["segoeuib.ttf", "segoeui.ttf", "arialbd.ttf", "arial.ttf"]
    for fn in font_names:
        try:
            if mode == 'off':
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

    if mode == 'yangi':
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

        return pystray.Menu(
            item("NamDPI alifbo", None, enabled=False),
            item("Panelni koʻrsatish / yashirish", lambda: self.toggle_panel(), default=True),
            pystray.Menu.SEPARATOR,
            item("Rejim: Yangi Lotin (Ö, Ğ, Ş, Ç)", set_mode_cb("yangi"), checked=is_mode("yangi")),
            item("Rejim: Ўзбек Кирилл", set_mode_cb("kril"), checked=is_mode("kril")),
            item("Rejim: Amaldagi Lotin", set_mode_cb("lotin"), checked=is_mode("lotin")),
            item("Rejim: Oʻchirilgan (Bypass)", set_mode_cb("off"), checked=is_mode("off")),
            pystray.Menu.SEPARATOR,
            item("Sozlamalar va Dastur haqida", lambda: self.panel.show_about_dialog()),
            item("Dasturdan chiqish", lambda: self.exit_app())
        )

    def set_mode(self, mode):
        self.panel.select_mode(mode)
        self.update_icon(mode)

    def update_icon(self, mode):
        if self.icon:
            try:
                new_img = create_mode_icon_image(mode)
                self.icon.icon = new_img
                # Tooltip update
                mode_names = {
                    "yangi": "Yangi Lotin (Ö, Ğ, Ş, Ç)",
                    "kril": "Ўзбек Кирилл",
                    "lotin": "Amaldagi Lotin",
                    "off": "Oʻchirilgan (Faol emas)"
                }
                self.icon.title = f"NamDPI alifbo - {mode_names.get(mode, mode)}"
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
