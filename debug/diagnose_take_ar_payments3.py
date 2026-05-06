"""
Check if Take AR Payments opens a new window or dialog
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen
from pywinauto import Application, findwindows
import time
import pywinauto.mouse
import ctypes

# Connect to Parts menu
nav = NavigatorScreen()
nav.click_menu_button('Parts')
time.sleep(1)

print("[1] Current windows before interaction...")
windows_before = findwindows.find_windows()
print(f"  Total windows: {len(windows_before)}")

# Try to move mouse to Parts area and look for visible controls
print("\n[2] Checking if explorer bar is rendered as custom control...")

# The Take AR Payments button should be somewhere in the Parts content area
# Let's try clicking in the area where it should be based on standard layout

# Typical layout: explorer bar is on the left side of the Parts panel
# Let's try clicking at approximate coordinates

print("\n[3] Attempting to interact with explorer bar area...")
print("  Note: The explorer bar may not be accessible via standard UI automation")
print("  It might require:")
print("    - Direct window message sending")
print("    - Mouse click at specific coordinates")
print("    - Or it might be a rendered/custom control")

print("\n[4] Alternative approach: Use Win32 API to enumerate all windows...")
from ctypes import windll, c_char_p, POINTER, c_int

def window_enumeration_callback(hwnd, lparam):
    if windll.user32.IsWindowVisible(hwnd):
        length = windll.user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            title = ctypes.create_unicode_buffer(length + 1)
            windll.user32.GetWindowTextW(hwnd, title, length + 1)
            if 'Take' in title.value or 'Payment' in title.value or 'AR' in title.value:
                print(f"    Found: {title.value}")
    return True

print("  Scanning for windows with 'Take', 'Payment', or 'AR'...")
windll.user32.EnumWindows(findwindows.EnumWindowsProc(window_enumeration_callback), 0)

print("\n[5] Checking if button appears in any newly opened windows...")
time.sleep(0.5)
windows_after = findwindows.find_windows()
print(f"  Total windows now: {len(windows_after)}")

new_windows = set(windows_after) - set(windows_before)
if new_windows:
    print(f"  New windows: {len(new_windows)}")
    for hw in new_windows:
        print(f"    - Handle: {hw}")
