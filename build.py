# -*- coding: utf-8 -*-
import subprocess
import os
import sys

BASE_DIR = r"I:\translate"
os.chdir(BASE_DIR)

cmd = [
    sys.executable, "-m", "PyInstaller",
    "--noconsole",
    "--onedir",
    "--name=NamDPI_Alifbo",
    "--icon=app_icon.ico",
    "--add-data=app_icon.ico;.",
    "--clean",
    "-y",
    "main.py"
]

print("Running PyInstaller for NamDPI alifbo:", " ".join(cmd))
res = subprocess.run(cmd)
print("PyInstaller exit code:", res.returncode)
sys.exit(res.returncode)
