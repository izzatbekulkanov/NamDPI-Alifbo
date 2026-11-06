# -*- coding: utf-8 -*-
"""
NamDPI alifbo - Cross-Platform Klaviatura drayveri
Windows (Win32 Hook), macOS (Quartz EventTap/pynput), Linux (X11/pynput)
Namangan davlat pedagogika instituti
Raqamli ta'lim texnologiyalari markazi (NamDPI RTTM)
"""

import sys
import os
import time
import queue
import threading
import platform

from transliterator import convert_word

OS_SYSTEM = platform.system() # 'Windows', 'Darwin', 'Linux'

if OS_SYSTEM == "Windows":
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    WH_KEYBOARD_LL = 13
    WM_KEYDOWN = 0x0100
    WM_KEYUP = 0x0101
    WM_SYSKEYDOWN = 0x0104
    WM_SYSKEYUP = 0x0105

    VK_BACK = 0x08
    VK_TAB = 0x09
    VK_RETURN = 0x0D
    VK_SHIFT = 0x10
    VK_CONTROL = 0x11
    VK_MENU = 0x12
    VK_ESCAPE = 0x1B
    VK_SPACE = 0x20
    VK_LEFT = 0x25
    VK_UP = 0x26
    VK_RIGHT = 0x27
    VK_DOWN = 0x28
    VK_DELETE = 0x2E
    VK_LWIN = 0x5B
    VK_RWIN = 0x5C
    VK_F8 = 0x77

    INPUT_KEYBOARD = 1
    KEYEVENTF_KEYUP = 0x0002
    KEYEVENTF_UNICODE = 0x0004
    EXTRA_MAGIC = 0x555A42

    class MOUSEINPUT(ctypes.Structure):
        _fields_ = [
            ("dx", wintypes.LONG),
            ("dy", wintypes.LONG),
            ("mouseData", wintypes.DWORD),
            ("dwFlags", wintypes.DWORD),
            ("time", wintypes.DWORD),
            ("dwExtraInfo", ctypes.c_ulonglong)
        ]

    class KEYBDINPUT(ctypes.Structure):
        _fields_ = [
            ("wVk", wintypes.WORD),
            ("wScan", wintypes.WORD),
            ("dwFlags", wintypes.DWORD),
            ("time", wintypes.DWORD),
            ("dwExtraInfo", ctypes.c_ulonglong)
        ]

    class HARDWAREINPUT(ctypes.Structure):
        _fields_ = [
            ("uMsg", wintypes.DWORD),
            ("wParamL", wintypes.WORD),
            ("wParamH", wintypes.WORD)
        ]

    class INPUT(ctypes.Structure):
        class _INPUT(ctypes.Union):
            _fields_ = [
                ("mi", MOUSEINPUT),
                ("ki", KEYBDINPUT),
                ("hi", HARDWAREINPUT)
            ]
        _anonymous_ = ("_input",)
        _fields_ = [
            ("type", wintypes.DWORD),
            ("_input", _INPUT)
        ]

    user32.SendInput.argtypes = (wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int)
    user32.SendInput.restype = wintypes.UINT

    class KBDLLHOOKSTRUCT(ctypes.Structure):
        _fields_ = [
            ("vkCode", wintypes.DWORD),
            ("scanCode", wintypes.DWORD),
            ("flags", wintypes.DWORD),
            ("time", wintypes.DWORD),
            ("dwExtraInfo", ctypes.c_ulonglong)
        ]

    HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_longlong, ctypes.c_int, wintypes.WPARAM, ctypes.POINTER(KBDLLHOOKSTRUCT))


class KeyboardEngine:
    def __init__(self, on_hotkey_cycle=None):
        self.mode = "yangi"       # 'yangi', 'kril', 'lotin', 'off'
        self.buffer = []          # Terilayotgan so'z harflari
        self.on_hotkey_cycle = on_hotkey_cycle

        self.replace_queue = queue.Queue()
        self._is_running = False
        self._worker_thread = None

        # Windows hook parametrlari
        if OS_SYSTEM == "Windows":
            self.hook_handle = None
            self._hook_proc = None
            self._pump_thread = None
            self._hook_thread_id = 0
        else:
            # macOS va Linux uchun pynput
            self._posix_listener = None
            self._posix_controller = None
            self._is_replacing_posix = False

    def set_mode(self, mode: str):
        self.mode = mode
        self.buffer.clear()

    def get_mode(self) -> str:
        return self.mode

    def _worker(self):
        """Orqa fonda almashtirishni xavfsiz bajaruvchi oqim."""
        while self._is_running:
            try:
                item = self.replace_queue.get(timeout=0.2)
            except queue.Empty:
                continue

            if item is None:
                break

            backspace_count, replacement_text = item
            if OS_SYSTEM == "Windows":
                self._execute_replacement_win(backspace_count, replacement_text)
            else:
                self._execute_replacement_posix(backspace_count, replacement_text)
            self.replace_queue.task_done()

    # =========================================================================
    # WINDOWS NATIVE IMPLEMENTATION
    # =========================================================================
    def _execute_replacement_win(self, backspaces_count, text):
        """Windows: SendInput orqali o'chirish va yangi matnni kiritish."""
        # 1. Backspaces
        bs_inputs = []
        for _ in range(backspaces_count):
            d = INPUT(type=INPUT_KEYBOARD)
            d.ki.wVk = VK_BACK
            d.ki.dwExtraInfo = EXTRA_MAGIC
            u = INPUT(type=INPUT_KEYBOARD)
            u.ki.wVk = VK_BACK
            u.ki.dwFlags = KEYEVENTF_KEYUP
            u.ki.dwExtraInfo = EXTRA_MAGIC
            bs_inputs.append(d)
            bs_inputs.append(u)

        if bs_inputs:
            arr_bs = (INPUT * len(bs_inputs))(*bs_inputs)
            user32.SendInput(len(bs_inputs), arr_bs, ctypes.sizeof(INPUT))

        time.sleep(0.005)

        # 2. Yangi matnni Unicode formatida kiritish
        txt_inputs = []
        for ch in text:
            d = INPUT(type=INPUT_KEYBOARD)
            d.ki.wVk = 0
            d.ki.wScan = ord(ch)
            d.ki.dwFlags = KEYEVENTF_UNICODE
            d.ki.dwExtraInfo = EXTRA_MAGIC

            u = INPUT(type=INPUT_KEYBOARD)
            u.ki.wVk = 0
            u.ki.wScan = ord(ch)
            u.ki.dwFlags = KEYEVENTF_UNICODE | KEYEVENTF_KEYUP
            u.ki.dwExtraInfo = EXTRA_MAGIC

            txt_inputs.append(d)
            txt_inputs.append(u)

        if txt_inputs:
            arr_txt = (INPUT * len(txt_inputs))(*txt_inputs)
            user32.SendInput(len(txt_inputs), arr_txt, ctypes.sizeof(INPUT))

    def _get_char_from_vk_win(self, vk, scan_code):
        shift = bool(user32.GetKeyState(VK_SHIFT) & 0x8000)
        caps = bool(user32.GetKeyState(0x14) & 1)
        is_upper = shift ^ caps

        if 0x41 <= vk <= 0x5A:
            return chr(vk) if is_upper else chr(vk + 32)
        if 0x30 <= vk <= 0x39 and not shift:
            return chr(vk)
        if vk == 0xDE and not shift:
            return "'"

        hwnd = user32.GetForegroundWindow()
        tid = user32.GetWindowThreadProcessId(hwnd, None) if hwnd else 0
        hkl = user32.GetKeyboardLayout(tid) if tid else 0

        state = (ctypes.c_uint8 * 256)()
        if shift: state[VK_SHIFT] = 0x80
        if caps: state[0x14] = 0x01
        buf = (wintypes.WCHAR * 16)()

        res = 0
        if hkl:
            res = user32.ToUnicodeEx(vk, scan_code or 0, state, buf, 16, 4, hkl)
        if res <= 0:
            res = user32.ToUnicode(vk, scan_code or 0, state, buf, 16, 0)
            if res < 0:
                user32.ToUnicode(vk, scan_code or 0, state, buf, 16, 0)

        if res > 0:
            return buf.value
        return ""

    def _hook_callback_win(self, nCode, wParam, lParam):
        if nCode >= 0:
            info = lParam.contents

            if info.dwExtraInfo == EXTRA_MAGIC:
                return user32.CallNextHookEx(None, nCode, wParam, lParam)

            if wParam in (WM_KEYDOWN, WM_SYSKEYDOWN):
                vk = info.vkCode
                scan = info.scanCode

                ctrl_down = bool(user32.GetKeyState(VK_CONTROL) & 0x8000)
                shift_down = bool(user32.GetKeyState(VK_SHIFT) & 0x8000)
                alt_down = bool(user32.GetKeyState(VK_MENU) & 0x8000)
                win_down = bool(user32.GetKeyState(VK_LWIN) & 0x8000) or bool(user32.GetKeyState(VK_RWIN) & 0x8000)

                # Hotkey: F8 yoki Ctrl+Shift+U
                if (ctrl_down and shift_down and vk == 0x55) or (vk == VK_F8 and not ctrl_down and not alt_down):
                    if self.on_hotkey_cycle:
                        threading.Thread(target=self.on_hotkey_cycle, daemon=True).start()
                    return 1

                if ctrl_down or alt_down or win_down:
                    self.buffer.clear()
                    return user32.CallNextHookEx(None, nCode, wParam, lParam)

                if vk in (VK_LEFT, VK_RIGHT, VK_UP, VK_DOWN, VK_ESCAPE, VK_TAB, VK_DELETE):
                    self.buffer.clear()
                    return user32.CallNextHookEx(None, nCode, wParam, lParam)

                if vk == VK_BACK:
                    if self.buffer:
                        self.buffer.pop()
                    return user32.CallNextHookEx(None, nCode, wParam, lParam)

                # Probel yoki Enter
                if vk in (VK_SPACE, VK_RETURN):
                    if self.mode != 'off' and self.buffer:
                        raw_word = "".join(self.buffer)
                        converted = convert_word(raw_word, self.mode)
                        if converted != raw_word:
                            delimiter = " " if vk == VK_SPACE else "\n"
                            self.replace_queue.put((len(self.buffer) + 1, converted + delimiter))
                    self.buffer.clear()
                    return user32.CallNextHookEx(None, nCode, wParam, lParam)

                # Oddiy belgi
                char = self._get_char_from_vk_win(vk, scan)
                if char:
                    if char in ".,!?;:":
                        if self.mode != 'off' and self.buffer:
                            raw_word = "".join(self.buffer)
                            converted = convert_word(raw_word, self.mode)
                            if converted != raw_word:
                                self.replace_queue.put((len(self.buffer) + 1, converted + char))
                        self.buffer.clear()
                    elif char.isalnum() or char in "'ʻʼ`‘’\"":
                        self.buffer.append(char)
                    else:
                        self.buffer.clear()

        return user32.CallNextHookEx(None, nCode, wParam, lParam)

    def _message_loop_win(self):
        self._hook_thread_id = kernel32.GetCurrentThreadId()
        self._hook_proc = HOOKPROC(self._hook_callback_win)
        self.hook_handle = user32.SetWindowsHookExW(WH_KEYBOARD_LL, self._hook_proc, None, 0)

        if not self.hook_handle:
            print("SetWindowsHookExW xatosi:", kernel32.GetLastError())
            return

        msg = wintypes.MSG()
        while self._is_running:
            ret = user32.GetMessageW(ctypes.byref(msg), 0, 0, 0)
            if ret <= 0:
                break
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))

        if self.hook_handle:
            user32.UnhookWindowsHookEx(self.hook_handle)
            self.hook_handle = None

    # =========================================================================
    # macOS & LINUX (POSIX) IMPLEMENTATION
    # =========================================================================
    def _execute_replacement_posix(self, backspaces_count, text):
        """macOS va Linux: pynput controller orqali almashtirish."""
        if not self._posix_controller:
            return

        self._is_replacing_posix = True
        try:
            from pynput.keyboard import Key

            # 1. Backspaces
            for _ in range(backspaces_count):
                self._posix_controller.press(Key.backspace)
                self._posix_controller.release(Key.backspace)
                time.sleep(0.003)

            time.sleep(0.01)

            # 2. Yangi matn
            self._posix_controller.type(text)
        finally:
            self._is_replacing_posix = False

    def _on_press_posix(self, key, *args):
        if self._is_replacing_posix:
            return

        from pynput.keyboard import Key

        # Hotkey: F8
        if key == Key.f8:
            if self.on_hotkey_cycle:
                threading.Thread(target=self.on_hotkey_cycle, daemon=True).start()
            return

        # Delimiters
        if key == Key.space:
            if self.mode != 'off' and self.buffer:
                raw_word = "".join(self.buffer)
                converted = convert_word(raw_word, self.mode)
                if converted != raw_word:
                    self.replace_queue.put((len(self.buffer) + 1, converted + " "))
            self.buffer.clear()
            return

        if key == Key.enter:
            if self.mode != 'off' and self.buffer:
                raw_word = "".join(self.buffer)
                converted = convert_word(raw_word, self.mode)
                if converted != raw_word:
                    self.replace_queue.put((len(self.buffer) + 1, converted + "\n"))
            self.buffer.clear()
            return

        if key == Key.backspace:
            if self.buffer:
                self.buffer.pop()
            return

        if key in (Key.tab, Key.esc, Key.left, Key.right, Key.up, Key.down,
                   Key.delete, Key.home, Key.end, Key.page_up, Key.page_down):
            self.buffer.clear()
            return

        # Characters
        try:
            if hasattr(key, 'char') and key.char:
                ch = key.char
                if ch in ".,!?;:":
                    if self.mode != 'off' and self.buffer:
                        raw_word = "".join(self.buffer)
                        converted = convert_word(raw_word, self.mode)
                        if converted != raw_word:
                            self.replace_queue.put((len(self.buffer) + 1, converted + ch))
                    self.buffer.clear()
                elif ch.isalnum() or ch in "'ʻʼ`‘’\"":
                    self.buffer.append(ch)
                else:
                    self.buffer.clear()
        except Exception:
            pass

    # =========================================================================
    # START / STOP
    # =========================================================================
    def start(self):
        if self._is_running:
            return
        self._is_running = True
        self._worker_thread = threading.Thread(target=self._worker, daemon=True)
        self._worker_thread.start()

        if OS_SYSTEM == "Windows":
            self._pump_thread = threading.Thread(target=self._message_loop_win, daemon=True)
            self._pump_thread.start()
        else:
            try:
                from pynput import keyboard
                self._posix_controller = keyboard.Controller()
                self._posix_listener = keyboard.Listener(on_press=self._on_press_posix)
                self._posix_listener.start()
            except Exception as e:
                print("POSIX keyboard listener start error:", e)

    def stop(self):
        self._is_running = False
        self.replace_queue.put(None)

        if OS_SYSTEM == "Windows":
            if self._hook_thread_id:
                user32.PostThreadMessageW(self._hook_thread_id, 0x0012, 0, 0)
            if self.hook_handle:
                user32.UnhookWindowsHookEx(self.hook_handle)
                self.hook_handle = None
        else:
            if self._posix_listener:
                try:
                    self._posix_listener.stop()
                except Exception:
                    pass
                self._posix_listener = None
