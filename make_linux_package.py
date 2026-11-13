# -*- coding: utf-8 -*-
"""
NamDPI alifbo - Linux Installer Package Builder (.deb va Universal .tar.gz)
Namangan davlat pedagogika instituti
Raqamli ta'lim texnologiyalari markazi (NamDPI RTTM)
"""

import os
import sys
import io
import time
import tarfile
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "installer_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

APP_NAME = "NamDPI alifbo"
PKG_NAME = "namdpi-alifbo"
VERSION = "2.0.3"

# 1. 256x256 PNG icon yaratish
def generate_png_icon(out_path):
    ico_path = os.path.join(BASE_DIR, "app_icon.ico")
    img = Image.open(ico_path)
    img = img.resize((256, 256), Image.Resampling.LANCZOS)
    img.save(out_path, format="PNG")
    print(f"PNG icon generated: {out_path}")

# AR header creator
def create_ar_member(name, data, mode=0o100644, mtime=None):
    if mtime is None:
        mtime = int(time.time())
    header = io.BytesIO()
    header.write(name.encode('ascii').ljust(16)[:16])
    header.write(str(mtime).encode('ascii').ljust(12)[:12])
    header.write(b"0".ljust(6))
    header.write(b"0".ljust(6))
    header.write(oct(mode)[2:].rjust(6, '0').encode('ascii').ljust(8)[:8])
    header.write(str(len(data)).encode('ascii').ljust(10)[:10])
    header.write(b"`\n")

    body = data
    if len(body) % 2 != 0:
        body += b"\n"
    return header.getvalue() + body


def build_deb_package():
    print("Building Debian/Ubuntu .deb package...")
    deb_path = os.path.join(OUTPUT_DIR, "NamDPI_Alifbo_Linux_Ubuntu_Debian.deb")
    icon_png_path = os.path.join(BASE_DIR, "app_icon.png")
    generate_png_icon(icon_png_path)

    # 1. debian-binary
    deb_binary_data = b"2.0\n"

    # 2. control.tar.gz
    control_buf = io.BytesIO()
    with tarfile.open(fileobj=control_buf, mode="w:gz") as tar:
        # control file
        control_text = f"""Package: {PKG_NAME}
Version: {VERSION}
Section: utils
Priority: optional
Architecture: all
Maintainer: Namangan davlat pedagogika instituti Raqamli ta'lim texnologiyalari markazi <info@nspi.uz>
Depends: python3 (>= 3.8), python3-tk, python3-pil, python3-pip
Homepage: https://nspi.uz
Description: NamDPI alifbo - O'zbek alifbosi avto-konverteri
 Namangan davlat pedagogika instituti Raqamli ta'lim texnologiyalari markazi
 tomonidan ishlab chiqilgan O'zbekistonning yangi lotin alifbosi (Ö, Ğ, Ş, Ç)
 va kirill alifbosi o'rtasida matn terishda avtomatik almashtiruvchi dastur.
"""
        ti = tarfile.TarInfo(name="./control")
        ti.size = len(control_text.encode('utf-8'))
        ti.mode = 0o644
        ti.mtime = int(time.time())
        tar.addfile(ti, io.BytesIO(control_text.encode('utf-8')))

        # postinst
        postinst_text = """#!/bin/sh
set -e
chmod +x /usr/bin/namdpi-alifbo
chmod +x /opt/namdpi-alifbo/main.py

# Zarur python kutubxonalari
pip3 install pynput pystray --break-system-packages 2>/dev/null || pip3 install pynput pystray 2>/dev/null || true

# Desktop database update
if which update-desktop-database >/dev/null 2>&1; then
    update-desktop-database -q || true
fi

echo "=========================================================="
echo " NamDPI alifbo muvaffaqiyatli o'rnatildi!"
echo " Ishga tushirish uchun: namdpi-alifbo"
echo " Namangan davlat pedagogika instituti RTTM"
echo "=========================================================="
exit 0
"""
        ti = tarfile.TarInfo(name="./postinst")
        ti.size = len(postinst_text.encode('utf-8'))
        ti.mode = 0o755
        ti.mtime = int(time.time())
        tar.addfile(ti, io.BytesIO(postinst_text.encode('utf-8')))

        # prerm
        prerm_text = """#!/bin/sh
set -e
pkill -f "namdpi-alifbo" || true
exit 0
"""
        ti = tarfile.TarInfo(name="./prerm")
        ti.size = len(prerm_text.encode('utf-8'))
        ti.mode = 0o755
        ti.mtime = int(time.time())
        tar.addfile(ti, io.BytesIO(prerm_text.encode('utf-8')))

    control_tar_gz = control_buf.getvalue()

    # 3. data.tar.gz
    data_buf = io.BytesIO()
    with tarfile.open(fileobj=data_buf, mode="w:gz") as tar:
        # /usr/bin/namdpi-alifbo launcher
        launcher_sh = """#!/bin/sh
exec python3 /opt/namdpi-alifbo/main.py "$@"
"""
        ti = tarfile.TarInfo(name="./usr/bin/namdpi-alifbo")
        ti.size = len(launcher_sh.encode('utf-8'))
        ti.mode = 0o755
        ti.mtime = int(time.time())
        tar.addfile(ti, io.BytesIO(launcher_sh.encode('utf-8')))

        # /usr/share/applications/namdpi-alifbo.desktop
        desktop_text = """[Desktop Entry]
Type=Application
Name=NamDPI alifbo
GenericName=Alifbo Konverteri
Comment=Namangan davlat pedagogika instituti Alifbo Konverteri
Exec=/usr/bin/namdpi-alifbo
Icon=namdpi-alifbo
Terminal=false
Categories=Utility;Education;TextTools;
Keywords=alifbo;lotin;kril;namdpi;translate;
StartupNotify=true
"""
        ti = tarfile.TarInfo(name="./usr/share/applications/namdpi-alifbo.desktop")
        ti.size = len(desktop_text.encode('utf-8'))
        ti.mode = 0o644
        ti.mtime = int(time.time())
        tar.addfile(ti, io.BytesIO(desktop_text.encode('utf-8')))

        # /usr/share/icons/hicolor/256x256/apps/namdpi-alifbo.png
        with open(icon_png_path, "rb") as f:
            icon_data = f.read()
        ti = tarfile.TarInfo(name="./usr/share/icons/hicolor/256x256/apps/namdpi-alifbo.png")
        ti.size = len(icon_data)
        ti.mode = 0o644
        ti.mtime = int(time.time())
        tar.addfile(ti, io.BytesIO(icon_data))

        # /opt/namdpi-alifbo/ files
        py_files = ["main.py", "keyboard_engine.py", "ui_widget.py", "tray_manager.py", "transliterator.py", "utils.py", "i18n.py", "updater.py", "README.md"]
        for fn in py_files:
            fp = os.path.join(BASE_DIR, fn)
            if os.path.exists(fp):
                with open(fp, "rb") as f:
                    content = f.read()
                ti = tarfile.TarInfo(name=f"./opt/namdpi-alifbo/{fn}")
                ti.size = len(content)
                ti.mode = 0o755 if fn == "main.py" else 0o644
                ti.mtime = int(time.time())
                tar.addfile(ti, io.BytesIO(content))

        # add icon in opt too
        ti = tarfile.TarInfo(name="./opt/namdpi-alifbo/app_icon.png")
        ti.size = len(icon_data)
        ti.mode = 0o644
        ti.mtime = int(time.time())
        tar.addfile(ti, io.BytesIO(icon_data))

    data_tar_gz = data_buf.getvalue()

    # Combine into .deb AR archive
    with open(deb_path, "wb") as deb:
        deb.write(b"!<arch>\n")
        deb.write(create_ar_member("debian-binary", deb_binary_data, mode=0o100644))
        deb.write(create_ar_member("control.tar.gz", control_tar_gz, mode=0o100644))
        deb.write(create_ar_member("data.tar.gz", data_tar_gz, mode=0o100644))

    print(f"Linux .deb package successfully created: {deb_path} ({os.path.getsize(deb_path)} bytes)")


def build_universal_linux_tar():
    print("Building Universal Linux installer (.tar.gz)...")
    tar_out = os.path.join(OUTPUT_DIR, "NamDPI_Alifbo_Linux_Universal.tar.gz")
    icon_png_path = os.path.join(BASE_DIR, "app_icon.png")

    install_sh = """#!/bin/bash
# NamDPI alifbo - Universal Linux Installer
# Namangan davlat pedagogika instituti RTTM

set -e

if [ "$EUID" -ne 0 ]; then
  echo "Iltimos, o'rnatish uchun sudo bilan ishga tushiring:"
  echo "  sudo ./install.sh"
  exit 1
fi

echo "=========================================================="
echo " NamDPI alifbo - Linux tizimiga o'rnatilmoqda..."
echo " Namangan davlat pedagogika instituti RTTM"
echo "=========================================================="

APP_DIR="/opt/namdpi-alifbo"
mkdir -p "$APP_DIR"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp -r "$SCRIPT_DIR/src/"* "$APP_DIR/"
chmod +x "$APP_DIR/main.py"

# Launcher
cat << 'EOF' > /usr/local/bin/namdpi-alifbo
#!/bin/sh
exec python3 /opt/namdpi-alifbo/main.py "$@"
EOF
chmod +x /usr/local/bin/namdpi-alifbo

# Icon
mkdir -p /usr/share/icons/hicolor/256x256/apps/
cp "$APP_DIR/app_icon.png" /usr/share/icons/hicolor/256x256/apps/namdpi-alifbo.png

# Desktop entry
cat << 'EOF' > /usr/share/applications/namdpi-alifbo.desktop
[Desktop Entry]
Type=Application
Name=NamDPI alifbo
GenericName=Alifbo Konverteri
Comment=Namangan davlat pedagogika instituti Alifbo Konverteri
Exec=/usr/local/bin/namdpi-alifbo
Icon=namdpi-alifbo
Terminal=false
Categories=Utility;Education;TextTools;
StartupNotify=true
EOF

# Pip packages
echo "Kerakli python kutubxonalari tekshirilmoqda..."
pip3 install pynput pystray Pillow --break-system-packages 2>/dev/null || pip3 install pynput pystray Pillow 2>/dev/null || true

if which update-desktop-database >/dev/null 2>&1; then
    update-desktop-database -q || true
fi

echo ""
echo "=========================================================="
echo " MUVAFFAQIYATLI O'RNATILDI!"
echo " Dasturni ishga tushirish:"
echo "   namdpi-alifbo"
echo " yoki Ilovalar menyusidan 'NamDPI alifbo' ni bosing."
echo "=========================================================="
"""

    uninstall_sh = """#!/bin/bash
# NamDPI alifbo - Linux Uninstaller
set -e
if [ "$EUID" -ne 0 ]; then
  echo "sudo bilan ishga tushiring: sudo ./uninstall.sh"
  exit 1
fi

pkill -f "namdpi-alifbo" || true
rm -rf /opt/namdpi-alifbo
rm -f /usr/local/bin/namdpi-alifbo
rm -f /usr/share/applications/namdpi-alifbo.desktop
rm -f /usr/share/icons/hicolor/256x256/apps/namdpi-alifbo.png

if which update-desktop-database >/dev/null 2>&1; then
    update-desktop-database -q || true
fi

echo "NamDPI alifbo to'liq o'chirildi."
"""

    with tarfile.open(tar_out, "w:gz") as tar:
        # install.sh
        ti = tarfile.TarInfo(name="NamDPI_Alifbo_Linux/install.sh")
        ti.size = len(install_sh.encode('utf-8'))
        ti.mode = 0o755
        ti.mtime = int(time.time())
        tar.addfile(ti, io.BytesIO(install_sh.encode('utf-8')))

        # uninstall.sh
        ti = tarfile.TarInfo(name="NamDPI_Alifbo_Linux/uninstall.sh")
        ti.size = len(uninstall_sh.encode('utf-8'))
        ti.mode = 0o755
        ti.mtime = int(time.time())
        tar.addfile(ti, io.BytesIO(uninstall_sh.encode('utf-8')))

        # src files
        py_files = ["main.py", "keyboard_engine.py", "ui_widget.py", "tray_manager.py", "transliterator.py", "utils.py", "i18n.py", "updater.py", "README.md"]
        for fn in py_files:
            fp = os.path.join(BASE_DIR, fn)
            if os.path.exists(fp):
                with open(fp, "rb") as f:
                    data = f.read()
                ti = tarfile.TarInfo(name=f"NamDPI_Alifbo_Linux/src/{fn}")
                ti.size = len(data)
                ti.mode = 0o755 if fn == "main.py" else 0o644
                ti.mtime = int(time.time())
                tar.addfile(ti, io.BytesIO(data))

        with open(icon_png_path, "rb") as f:
            icon_data = f.read()
        ti = tarfile.TarInfo(name="NamDPI_Alifbo_Linux/src/app_icon.png")
        ti.size = len(icon_data)
        ti.mode = 0o644
        ti.mtime = int(time.time())
        tar.addfile(ti, io.BytesIO(icon_data))

    print(f"Universal Linux tar.gz successfully created: {tar_out} ({os.path.getsize(tar_out)} bytes)")


if __name__ == '__main__':
    build_deb_package()
    build_universal_linux_tar()
