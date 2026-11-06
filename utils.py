# -*- coding: utf-8 -*-
"""
NamDPI alifbo - Cross-Platform Yordamchi vositalar va Avto-ishga tushish
Windows (Registry), macOS (LaunchAgents), Linux (XDG Autostart)
"""

import sys
import os
import platform

OS_SYSTEM = platform.system() # 'Windows', 'Darwin', 'Linux'
APP_NAME = "NamDPI_Alifbo"
OLD_APP_NAME = "NDPI_Alifbo_Converter"

def get_executable_path():
    """Joriy dastur .exe yoki python skript yo'lini qaytaradi."""
    if getattr(sys, 'frozen', False):
        return sys.executable
    return os.path.abspath(sys.argv[0])

def is_autostart_enabled():
    """Tizim yuklanganda avto-ishga tushish yoqilganmi?"""
    if OS_SYSTEM == "Windows":
        try:
            import winreg
            REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
            val, _ = winreg.QueryValueEx(key, APP_NAME)
            winreg.CloseKey(key)
            return bool(val)
        except Exception:
            return False
    elif OS_SYSTEM == "Darwin":
        plist_path = os.path.expanduser("~/Library/LaunchAgents/uz.nspi.namdpi.alifbo.plist")
        return os.path.exists(plist_path)
    else: # Linux
        desktop_path = os.path.expanduser("~/.config/autostart/namdpi-alifbo.desktop")
        return os.path.exists(desktop_path)

def set_autostart(enable: bool):
    """Tizim yuklanganda avto-ishga tushishni yoqish yoki o'chirish."""
    exe_path = get_executable_path()

    if OS_SYSTEM == "Windows":
        try:
            import winreg
            REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE)
            try:
                winreg.DeleteValue(key, OLD_APP_NAME)
            except Exception:
                pass

            if enable:
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{exe_path}"')
            else:
                try:
                    winreg.DeleteValue(key, APP_NAME)
                except FileNotFoundError:
                    pass
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print("Windows autostart xatosi:", e)
            return False

    elif OS_SYSTEM == "Darwin": # macOS LaunchAgent
        agent_dir = os.path.expanduser("~/Library/LaunchAgents")
        plist_path = os.path.join(agent_dir, "uz.nspi.namdpi.alifbo.plist")
        try:
            if enable:
                os.makedirs(agent_dir, exist_ok=True)
                plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>uz.nspi.namdpi.alifbo</string>
    <key>ProgramArguments</key>
    <array>
        <string>{exe_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>"""
                with open(plist_path, "w", encoding="utf-8") as f:
                    f.write(plist_content)
            else:
                if os.path.exists(plist_path):
                    os.remove(plist_path)
            return True
        except Exception as e:
            print("macOS autostart xatosi:", e)
            return False

    else: # Linux XDG Autostart
        autostart_dir = os.path.expanduser("~/.config/autostart")
        desktop_path = os.path.join(autostart_dir, "namdpi-alifbo.desktop")
        try:
            if enable:
                os.makedirs(autostart_dir, exist_ok=True)
                desktop_content = f"""[Desktop Entry]
Type=Application
Exec="{exe_path}"
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=NamDPI alifbo
Comment=Namangan davlat pedagogika instituti Alifbo Konverteri
Icon=namdpi-alifbo
Categories=Utility;Education;
"""
                with open(desktop_path, "w", encoding="utf-8") as f:
                    f.write(desktop_content)
            else:
                if os.path.exists(desktop_path):
                    os.remove(desktop_path)
            return True
        except Exception as e:
            print("Linux autostart xatosi:", e)
            return False
