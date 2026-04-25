"""
Keyboard input handling for the automation framework.
Simulates keyboard interactions with the application.
"""

import time
from typing import List, Optional
from enum import Enum


class KeyCode(Enum):
    """Enumeration of special key codes."""
    BACKSPACE = "BackSpace"
    TAB = "Tab"
    CLEAR = "Clear"
    ENTER = "Return"
    SHIFT = "Shift_L"
    CTRL = "Control_L"
    ALT = "Alt_L"
    PAUSE = "Pause"
    CAPSLOCK = "Caps_Lock"
    ESCAPE = "Escape"
    SPACE = "space"
    PAGE_UP = "Page_Up"
    PAGE_DOWN = "Page_Down"
    END = "End"
    HOME = "Home"
    LEFT = "Left"
    UP = "Up"
    RIGHT = "Right"
    DOWN = "Down"
    INSERT = "Insert"
    DELETE = "Delete"
    F1 = "F1"
    F2 = "F2"
    F3 = "F3"
    F4 = "F4"
    F5 = "F5"
    F6 = "F6"
    F7 = "F7"
    F8 = "F8"
    F9 = "F9"
    F10 = "F10"
    F11 = "F11"
    F12 = "F12"


class KeyboardHandler:
    """
    Handles keyboard input for application automation.
    Supports typing, key presses, and key combinations.
    """

    def __init__(self):
        """Initialize KeyboardHandler."""
        try:
            import pynput.keyboard as kb
            self.keyboard = kb
            self.controller = kb.Controller()
            self.keyboard_available = True
        except ImportError:
            self.keyboard_available = False
            print("Warning: pynput not available. Install with: pip install pynput")

    def type_text(self, text: str, interval: float = 0.05) -> None:
        """
        Type text character by character.

        Args:
            text: Text to type
            interval: Time between keystrokes (seconds)
        """
        if not self.keyboard_available:
            print(f"Mock typing: {text}")
            return

        for char in text:
            try:
                self.controller.type(char)
                time.sleep(interval)
            except Exception as e:
                print(f"Error typing character '{char}': {e}")

    def type_text_fast(self, text: str) -> None:
        """
        Type text quickly (no delay between characters).

        Args:
            text: Text to type
        """
        if not self.keyboard_available:
            print(f"Mock fast typing: {text}")
            return

        try:
            self.controller.type(text)
        except Exception as e:
            print(f"Error typing text: {e}")

    def press_key(self, key: str) -> None:
        """
        Press a single key.

        Args:
            key: Key name or KeyCode enum value
        """
        if not self.keyboard_available:
            print(f"Mock key press: {key}")
            return

        try:
            # Try to get key from KeyCode enum first
            try:
                key_code = KeyCode[key.upper()].value
                key = key_code
            except KeyError:
                pass

            if hasattr(self.keyboard, 'Key'):
                key_obj = getattr(self.keyboard.Key, key.lower(), None)
                if key_obj:
                    self.controller.press(key_obj)
                    time.sleep(0.1)
                    self.controller.release(key_obj)
                else:
                    # Try as regular character
                    self.controller.press(key)
                    time.sleep(0.1)
                    self.controller.release(key)
            else:
                self.controller.press(key)
                time.sleep(0.1)
                self.controller.release(key)
        except Exception as e:
            print(f"Error pressing key '{key}': {e}")

    def press_and_hold(self, key: str, duration: float = 1.0) -> None:
        """
        Press and hold a key for a specified duration.

        Args:
            key: Key to hold
            duration: How long to hold (seconds)
        """
        if not self.keyboard_available:
            print(f"Mock hold key: {key} for {duration}s")
            return

        try:
            key_obj = getattr(self.keyboard.Key, key.lower(), None)
            if key_obj:
                self.controller.press(key_obj)
                time.sleep(duration)
                self.controller.release(key_obj)
        except Exception as e:
            print(f"Error holding key: {e}")

    def key_combination(self, *keys: str) -> None:
        """
        Press a combination of keys simultaneously.

        Args:
            *keys: Keys to press together (e.g., 'ctrl', 'a')
        """
        if not self.keyboard_available:
            print(f"Mock key combination: {' + '.join(keys)}")
            return

        try:
            key_objects = []
            for key in keys:
                key_obj = getattr(self.keyboard.Key, key.lower(), None)
                if key_obj:
                    key_objects.append(key_obj)
                    self.controller.press(key_obj)

            time.sleep(0.1)

            for key_obj in reversed(key_objects):
                self.controller.release(key_obj)
        except Exception as e:
            print(f"Error with key combination: {e}")

    def key_sequence(self, keys: List[str], interval: float = 0.2) -> None:
        """
        Press a sequence of keys with delay between each.

        Args:
            keys: List of keys to press in sequence
            interval: Time between key presses (seconds)
        """
        if not self.keyboard_available:
            print(f"Mock key sequence: {keys}")
            return

        for key in keys:
            self.press_key(key)
            time.sleep(interval)

    def clear_field(self) -> None:
        """Clear a text field using Ctrl+A then Delete."""
        if not self.keyboard_available:
            print("Mock clear field")
            return

        self.key_combination('ctrl', 'a')
        time.sleep(0.1)
        self.press_key('delete')

    def clear_line(self) -> None:
        """Clear current line using Home and Shift+End then Delete."""
        if not self.keyboard_available:
            print("Mock clear line")
            return

        self.press_key('home')
        time.sleep(0.1)
        self.key_combination('shift', 'end')
        time.sleep(0.1)
        self.press_key('delete')

    def send_tab(self, count: int = 1) -> None:
        """
        Send Tab key press(es).

        Args:
            count: Number of times to press Tab
        """
        if not self.keyboard_available:
            print(f"Mock Tab x{count}")
            return

        for _ in range(count):
            self.press_key('tab')
            time.sleep(0.1)

    def send_enter(self) -> None:
        """Send Enter key press."""
        if not self.keyboard_available:
            print("Mock Enter key")
            return

        self.press_key('enter')

    def send_escape(self) -> None:
        """Send Escape key press."""
        if not self.keyboard_available:
            print("Mock Escape key")
            return

        self.press_key('escape')

    def send_backspace(self, count: int = 1) -> None:
        """
        Send Backspace key press(es).

        Args:
            count: Number of times to press Backspace
        """
        if not self.keyboard_available:
            print(f"Mock Backspace x{count}")
            return

        for _ in range(count):
            self.press_key('backspace')
            time.sleep(0.05)

    def send_delete(self, count: int = 1) -> None:
        """
        Send Delete key press(es).

        Args:
            count: Number of times to press Delete
        """
        if not self.keyboard_available:
            print(f"Mock Delete x{count}")
            return

        for _ in range(count):
            self.press_key('delete')
            time.sleep(0.05)

    def copy_to_clipboard(self) -> None:
        """Copy selection to clipboard (Ctrl+C)."""
        if not self.keyboard_available:
            print("Mock Ctrl+C")
            return

        self.key_combination('ctrl', 'c')

    def paste_from_clipboard(self) -> None:
        """Paste from clipboard (Ctrl+V)."""
        if not self.keyboard_available:
            print("Mock Ctrl+V")
            return

        self.key_combination('ctrl', 'v')

    def cut_to_clipboard(self) -> None:
        """Cut selection to clipboard (Ctrl+X)."""
        if not self.keyboard_available:
            print("Mock Ctrl+X")
            return

        self.key_combination('ctrl', 'x')

    def select_all(self) -> None:
        """Select all (Ctrl+A)."""
        if not self.keyboard_available:
            print("Mock Ctrl+A")
            return

        self.key_combination('ctrl', 'a')
