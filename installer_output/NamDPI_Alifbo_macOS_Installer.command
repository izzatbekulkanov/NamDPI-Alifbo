#!/bin/bash
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
