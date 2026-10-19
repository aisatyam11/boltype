"""
Types text into whichever app is currently focused.

How: Windows' SendInput API fakes keystrokes at the OS level, so the
focused app can't tell the difference from a real keyboard. Using the
KEYEVENTF_UNICODE flag means we send raw characters — no keyboard-layout
issues, works for any language Windows can display.

No special permission needed on Windows (unlike Mac's Accessibility API).
One catch: apps running as Administrator need BolType to also run as admin.
"""
import platform
import time


class Typer:
    def __init__(self):
        self._windows = platform.system() == "Windows"

    def type_text(self, text):
        if not self._windows:
            # Lets us import/test the pipeline on Mac/Linux without crashing.
            print(f"[DRY RUN — not on Windows, would type]: {text}")
            return
        self._send_input(text)

    def _send_input(self, text):
        import ctypes
        from ctypes import wintypes

        class KEYBDINPUT(ctypes.Structure):
            _fields_ = [
                ("wVk", wintypes.WORD),
                ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", ctypes.c_void_p),
            ]

        class INPUT(ctypes.Structure):
            _fields_ = [("type", wintypes.DWORD), ("ki", KEYBDINPUT)]

        INPUT_KEYBOARD = 1
        KEYEVENTF_KEYUP = 0x0002
        KEYEVENTF_UNICODE = 0x0004

        events = []
        for ch in text:
            code = ord(ch)
            # key down, then key up — that's one typed character
            events.append(INPUT(INPUT_KEYBOARD, KEYBDINPUT(0, code, KEYEVENTF_UNICODE, 0, None)))
            events.append(INPUT(INPUT_KEYBOARD, KEYBDINPUT(0, code, KEYEVENTF_UNICODE | KEYEVENTF_KEYUP, 0, None)))

        arr = (INPUT * len(events))(*events)
        ctypes.windll.user32.SendInput(len(events), arr, ctypes.sizeof(INPUT))
        time.sleep(0.05)
