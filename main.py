# -*- coding: utf-8 -*-
"""
NamDPI alifbo - Asosiy Dastur
Namangan davlat pedagogika instituti
Raqamli ta'lim texnologiyalari markazi (NamDPI RTTM)
"""

import sys
import os
import ctypes
import tkinter as tk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from keyboard_engine import KeyboardEngine
from ui_widget import TaskbarStripPanel
from tray_manager import TrayManager
from updater import UpdateChecker, CURRENT_VERSION

kernel32 = ctypes.windll.kernel32
user32 = ctypes.windll.user32
MUTEX_NAME = "Global\\NamDPI_Alifbo_SingleInstance_Mutex"

def is_already_running():
    mutex = kernel32.CreateMutexW(None, False, MUTEX_NAME)
    last_error = kernel32.GetLastError()
    ERROR_ALREADY_EXISTS = 183
    if last_error == ERROR_ALREADY_EXISTS:
        return True, mutex
    return False, mutex

def main():
    already_running, mutex_handle = is_already_running()
    if already_running:
        print("NamDPI alifbo allaqachon ishga tushirilgan!")
        sys.exit(0)

    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    root = tk.Tk()
    root.title("NamDPI alifbo")

    icon_path = os.path.join(BASE_DIR, "app_icon.ico")
    if os.path.exists(icon_path):
        try:
            root.iconbitmap(icon_path)
        except Exception:
            pass

    engine = KeyboardEngine()
    tray_holder = [None]

    def on_mode_change(mode):
        if tray_holder[0]:
            tray_holder[0].update_icon(mode)

    def on_language_change(new_lang):
        if tray_holder[0]:
            tray_holder[0].update_menu()
            tray_holder[0].update_icon()

    def cleanup_and_exit():
        try:
            engine.stop()
        except Exception:
            pass
        root.quit()
        root.destroy()
        sys.exit(0)

    # Pastki qatordagi zamonaviy panel (Taskbar Strip Panel)
    panel = TaskbarStripPanel(
        root=root,
        engine=engine,
        on_mode_changed=on_mode_change,
        on_exit=cleanup_and_exit,
        on_language_changed=on_language_change
    )

    # Hotkey (F8 yoki Ctrl+Shift+U) orqali almashtirish
    def on_cycle():
        root.after(0, panel.cycle_mode)

    engine.on_hotkey_cycle = on_cycle

    # Tray menejeri
    tray = TrayManager(
        panel=panel,
        engine=engine,
        on_exit=cleanup_and_exit
    )
    tray_holder[0] = tray
    tray.start_in_thread()

    # Klaviatura drayverini ishga tushirish
    engine.start()

    # =========================================================================
    # FONDA AVTOMATIK YANGILANISHLARNI TEKSHIRISH
    # =========================================================================
    updater = UpdateChecker(CURRENT_VERSION)

    def trigger_update_check():
        def on_found(info):
            def _apply():
                panel.set_update_required(info)
                if tray_holder[0]:
                    tray_holder[0].update_icon()
            root.after(0, _apply)

        updater.check_in_background(on_update_found=on_found)
        # Har 60 soniyada yangilanishlarni avtomatik qayta tekshirib turadi (Telegram kabi)
        root.after(60 * 1000, trigger_update_check)

    # Dastur yoqilgandan 2 soniya o'tgach darhol birinchi tekshiruv
    root.after(2000, trigger_update_check)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        cleanup_and_exit()

if __name__ == "__main__":
    main()
