# -*- coding: utf-8 -*-
"""
NamDPI alifbo - Avtomatik Yangilanish Tizimi (Auto-Updater)
GitHub Releases API orqali yangilanishlarni tekshirish va o'rnatish
Namangan davlat pedagogika instituti
Raqamli ta'lim texnologiyalari markazi (NamDPI RTTM)
"""

import os
import sys
import json
import re
import platform
import tempfile
import threading
import subprocess
import urllib.request
import urllib.error

CURRENT_VERSION = "2.0.1"
REPO_OWNER = "izzatbekulkanov"
REPO_NAME = "NamDPI-Alifbo"
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"

OS_SYSTEM = platform.system() # 'Windows', 'Darwin', 'Linux'

def parse_version(ver_str):
    """Versiya satrini (masalan 'v2.0.1') taqqoslash uchun tuple ga aylantiradi: (2, 0, 1)."""
    clean = re.sub(r'^[^\d]*', '', ver_str.strip())
    parts = []
    for part in clean.split('.'):
        digits = re.findall(r'\d+', part)
        if digits:
            parts.append(int(digits[0]))
        else:
            parts.append(0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:3])

def get_github_token():
    """Tizimdagi yoki git credential helper'dagi GitHub tokenini olish."""
    # 1. Environment variables
    for var in ("GITHUB_TOKEN", "GH_TOKEN", "HOMEBREW_GITHUB_API_TOKEN"):
        val = os.environ.get(var)
        if val:
            return val.strip()

    # 2. Git credential manager (qora oyna chiqarmaslik uchun CREATE_NO_WINDOW bayrog'i bilan)
    try:
        creationflags = subprocess.CREATE_NO_WINDOW if OS_SYSTEM == "Windows" else 0
        proc = subprocess.Popen(
            ["git", "credential", "fill"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=creationflags
        )
        out, _ = proc.communicate(input="protocol=https\nhost=github.com\n", timeout=2)
        for line in out.splitlines():
            if line.startswith("password="):
                pwd = line.split("=", 1)[1].strip()
                if pwd.startswith("gho_") or pwd.startswith("ghp_") or pwd.startswith("github_pat_"):
                    return pwd
    except Exception:
        pass

    return None

class UpdateInfo:
    def __init__(self, tag_name, name, body, html_url, assets):
        self.tag_name = tag_name
        self.version_tuple = parse_version(tag_name)
        self.name = name
        self.body = body
        self.html_url = html_url
        self.assets = assets

    def get_platform_asset(self):
        """Joriy operatsion tizim uchun mos o'rnatuvchi faylni tanlaydi."""
        if OS_SYSTEM == "Windows":
            for a in self.assets:
                if a.get("name", "").endswith(".exe"):
                    return a
        elif OS_SYSTEM == "Darwin":
            for a in self.assets:
                if a.get("name", "").endswith((".dmg", ".zip")):
                    return a
        else: # Linux
            for a in self.assets:
                if a.get("name", "").endswith(".deb"):
                    return a
            for a in self.assets:
                if a.get("name", "").endswith(".tar.gz"):
                    return a
        # Fallback: istalgan birinchi fayl
        return self.assets[0] if self.assets else None

class UpdateChecker:
    def __init__(self, current_version=CURRENT_VERSION):
        self.current_version = current_version
        self.current_tuple = parse_version(current_version)
        self.cached_update = None
        self.is_checking = False
        self._download_cancelled = False

    def check_for_updates(self):
        """GitHub Releases API orqali eng so'nggi versiyani tekshiradi."""
        token = get_github_token()
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "NamDPI-Alifbo-Updater"
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"

        req = urllib.request.Request(GITHUB_API_URL, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            # Agar unauthenticated 404 bersa va token bo'lmasa, demak repo private yoki hali reliz yo'q
            raise RuntimeError(f"GitHub API javob kodi: {e.code}")
        except Exception as e:
            raise RuntimeError(f"Internet yoki ulanish xatosi: {e}")

        tag_name = data.get("tag_name", "")
        remote_tuple = parse_version(tag_name)

        if remote_tuple > self.current_tuple:
            info = UpdateInfo(
                tag_name=tag_name,
                name=data.get("name", tag_name),
                body=data.get("body", ""),
                html_url=data.get("html_url", ""),
                assets=data.get("assets", [])
            )
            self.cached_update = info
            return True, info
        else:
            return False, None

    def check_in_background(self, on_update_found=None, on_no_update=None, on_error=None):
        """Interfeysni qotirmaslik uchun alohida fonda tekshirish."""
        if self.is_checking:
            return

        def _worker():
            self.is_checking = True
            try:
                has_update, info = self.check_for_updates()
                if has_update and info:
                    if on_update_found:
                        on_update_found(info)
                else:
                    if on_no_update:
                        on_no_update()
            except Exception as e:
                if on_error:
                    on_error(str(e))
            finally:
                self.is_checking = False

        threading.Thread(target=_worker, daemon=True).start()

    def download_and_install(self, asset, on_progress=None, on_complete=None, on_error=None):
        """Yangi o'rnatuvchi faylni yuklab olib, o'rnatishni boshlash."""
        self._download_cancelled = False

        def _download_worker():
            try:
                download_url = asset.get("browser_download_url")
                filename = asset.get("name", "NamDPI_Alifbo_Setup.exe")
                expected_size = asset.get("size", 0)

                temp_dir = tempfile.gettempdir()
                dest_path = os.path.join(temp_dir, filename)

                token = get_github_token()
                headers = {"User-Agent": "NamDPI-Alifbo-Updater"}
                # Asset download url agar private repo bo'lsa api url kerak bo'lishi mumkin
                asset_api_url = asset.get("url")
                if token and asset_api_url:
                    req_url = asset_api_url
                    headers["Authorization"] = f"Bearer {token}"
                    headers["Accept"] = "application/octet-stream"
                else:
                    req_url = download_url

                req = urllib.request.Request(req_url, headers=headers)
                with urllib.request.urlopen(req, timeout=30) as resp, open(dest_path, "wb") as f_out:
                    total_bytes = int(resp.headers.get("Content-Length") or expected_size or 0)
                    downloaded = 0
                    chunk_size = 64 * 1024

                    while True:
                        if self._download_cancelled:
                            return
                        chunk = resp.read(chunk_size)
                        if not chunk:
                            break
                        f_out.write(chunk)
                        downloaded += len(chunk)
                        if on_progress and total_bytes > 0:
                            percent = int((downloaded / total_bytes) * 100)
                            on_progress(percent, downloaded, total_bytes)

                if on_complete:
                    on_complete(dest_path)

            except Exception as e:
                if on_error:
                    on_error(str(e))

        threading.Thread(target=_download_worker, daemon=True).start()

    def launch_installer(self, installer_path):
        """Yuklab olingan o'rnatuvchini qora oyna (console) chiqarmasdan professional ishga tushirish."""
        if OS_SYSTEM == "Windows":
            try:
                # Windows Shell orqali qora konsol oynasisiz toza ishga tushirish
                os.startfile(installer_path)
            except Exception:
                creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0) | getattr(subprocess, "DETACHED_PROCESS", 0)
                subprocess.Popen([installer_path], creationflags=creationflags)
        elif OS_SYSTEM == "Darwin":
            subprocess.Popen(["open", installer_path])
        else: # Linux
            if installer_path.endswith(".deb"):
                subprocess.Popen(["xdg-open", installer_path])
            else:
                subprocess.Popen(["xdg-open", os.path.dirname(installer_path)])
