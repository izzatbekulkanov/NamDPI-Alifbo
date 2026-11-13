Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "D:\Github\NamDPI-Alifbo"
WshShell.Run """D:\Python312\pythonw.exe"" ""D:\Github\NamDPI-Alifbo\main.py""", 0, False
