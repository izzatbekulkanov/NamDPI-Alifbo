# -*- coding: utf-8 -*-
"""
NamDPI alifbo - macOS Installer Package Builder (.app bundle va .command installer)
Namangan davlat pedagogika instituti
Raqamli ta'lim texnologiyalari markazi (NamDPI RTTM)
"""

import os
import sys
import time
import zipfile
import tarfile
from PIL import Image

BASE_DIR = r"I:\translate"
OUTPUT_DIR = os.path.join(BASE_DIR, "installer_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

APP_NAME = "NamDPI alifbo"
BUNDLE_NAME = "NamDPI alifbo.app"

def generate_icns(out_path):
    print("Generating Apple ICNS icon...")
    ico_path = os.path.join(BASE_DIR, "app_icon.ico")
    img = Image.open(ico_path)
    # Resize to 512x512
    img512 = img.resize((512, 512), Image.Resampling.LANCZOS)
    img512.save(out_path, format="ICNS")
    print(f"Apple ICNS created: {out_path}")

def build_mac_package():
    print("Building macOS Application Bundle and Installer...")
    icns_path = os.path.join(BASE_DIR, "app_icon.icns")
    generate_icns(icns_path)

    # Info.plist
    info_plist = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>NamDPI alifbo</string>
    <key>CFBundleDisplayName</key>
    <string>NamDPI alifbo</string>
    <key>CFBundleIdentifier</key>
    <string>uz.nspi.namdpi.alifbo</string>
    <key>CFBundleVersion</key>
    <string>2.0.2</string>
    <key>CFBundleShortVersionString</key>
    <string>2.0.2</string>
    <key>CFBundleExecutable</key>
    <string>namdpi_alifbo</string>
    <key>CFBundleIconFile</key>
    <string>app_icon.icns</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>NDPI</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSSupportsAutomaticGraphicsSwitching</key>
    <true/>
    <key>NSAppleScriptEnabled</key>
    <false/>
</dict>
</plist>
"""

    pkg_info = "APPLNDPI\n"

    # Contents/MacOS/namdpi_alifbo launcher script
    launcher_sh = """#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../Resources/src" && pwd)"
export PYTHONPATH="$DIR:$PYTHONPATH"
exec python3 "$DIR/main.py" "$@"
"""

    # Interactive 1-click Installer (.command) for macOS Finder
    installer_command = """#!/bin/bash
# NamDPI alifbo - macOS 1-Click Installer
# Namangan davlat pedagogika instituti RTTM

clear
echo "=========================================================="
echo "      NamDPI alifbo - macOS O'rnatuvchi Dastur            "
echo "      Namangan davlat pedagogika instituti RTTM           "
echo "=========================================================="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_SRC="$SCRIPT_DIR/NamDPI alifbo.app"
DEST_APP="/Applications/NamDPI alifbo.app"

if [ ! -d "$APP_SRC" ]; then
    APP_SRC="$SCRIPT_DIR"
fi

echo "[1/4] NamDPI alifbo dasturini /Applications papkasiga nusxalash..."
rm -rf "$DEST_APP"
cp -R "$APP_SRC" "$DEST_APP"
chmod +x "$DEST_APP/Contents/MacOS/namdpi_alifbo"

echo "[2/4] Zaruriy python kutubxonalarini tekshirish..."
pip3 install pynput pystray Pillow --break-system-packages 2>/dev/null || pip3 install pynput pystray Pillow 2>/dev/null || true

echo "[3/4] Ish stoli (Desktop) yorlig'ini yaratish..."
DESKTOP_DIR="$HOME/Desktop"
if [ -d "$DESKTOP_DIR" ]; then
    ln -sf "$DEST_APP" "$DESKTOP_DIR/NamDPI alifbo"
fi

echo "[4/4] macOS Xavfsizlik ruxsatnomasi (Accessibility)..."
echo "----------------------------------------------------------"
echo "DIQQAT: macOS tizimida klaviatura orqali so'zlarni avtomatik"
echo "o'girish uchun quyidagi ruxsatni yoqish lozim:"
echo "  1. 'System Settings' (Tizim sozlamalari) -> 'Privacy & Security'"
echo "  2. 'Accessibility' (Maxsus imkoniyatlar) bo'limiga kiring"
echo "  3. 'NamDPI alifbo' (yoki Terminal) ga ruxsat (ON) bering."
echo "----------------------------------------------------------"
echo ""

read -p "NamDPI alifbo dasturini hoziroq ishga tushirasizmi? (h/y): " answer
case ${answer:0:1} in
    y|Y|h|H|1 )
        echo "Dastur ishga tushirilmoqda..."
        open -a "/Applications/NamDPI alifbo.app"
    ;;
    * )
        echo "O'rnatish yakunlandi."
    ;;
esac

echo ""
echo "Tabriklaymiz! NamDPI alifbo muvaffaqiyatli o'rnatildi."
sleep 2
exit 0
"""

    install_sh = installer_command

    # Output ZIP for macOS
    zip_out = os.path.join(OUTPUT_DIR, "NamDPI_Alifbo_macOS.zip")
    cmd_out = os.path.join(OUTPUT_DIR, "NamDPI_Alifbo_macOS_Installer.command")

    # Write .command file in output directory too
    with open(cmd_out, "wb") as f:
        f.write(installer_command.encode('utf-8'))

    with zipfile.ZipFile(zip_out, "w", zipfile.ZIP_DEFLATED) as z:
        # Helper to add zip entries with permissions
        def add_file(arcname, data, mode=0o644):
            zi = zipfile.ZipInfo(arcname)
            zi.external_attr = (mode & 0xFFFF) << 16
            zi.date_time = time.localtime(time.time())[:6]
            z.writestr(zi, data)

        # 1. Installer scripts
        add_file("NamDPI_Alifbo_macOS_Installer.command", installer_command.encode('utf-8'), mode=0o755)
        add_file("install.sh", install_sh.encode('utf-8'), mode=0o755)

        # 2. App Bundle
        add_file("NamDPI alifbo.app/Contents/Info.plist", info_plist.encode('utf-8'), mode=0o644)
        add_file("NamDPI alifbo.app/Contents/PkgInfo", pkg_info.encode('utf-8'), mode=0o644)
        add_file("NamDPI alifbo.app/Contents/MacOS/namdpi_alifbo", launcher_sh.encode('utf-8'), mode=0o755)

        # 3. ICNS Icon
        with open(icns_path, "rb") as f:
            icns_data = f.read()
        add_file("NamDPI alifbo.app/Contents/Resources/app_icon.icns", icns_data, mode=0o644)

        # 4. Source files
        py_files = ["main.py", "keyboard_engine.py", "ui_widget.py", "tray_manager.py", "transliterator.py", "utils.py", "i18n.py", "updater.py", "README.md"]
        for fn in py_files:
            fp = os.path.join(BASE_DIR, fn)
            if os.path.exists(fp):
                with open(fp, "rb") as f:
                    data = f.read()
                add_file(f"NamDPI alifbo.app/Contents/Resources/src/{fn}", data, mode=0o755 if fn == "main.py" else 0o644)

    print(f"macOS package successfully created: {zip_out} ({os.path.getsize(zip_out)} bytes)")
    print(f"macOS installer command: {cmd_out}")

if __name__ == '__main__':
    build_mac_package()
