"""
Inspect what happens after clicking - check for modal dialogs, popups, or blocking windows
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time
import warnings
warnings.filterwarnings('ignore')

print("[1] Getting all visible windows...")
all_handles = findwindows.find_windows(title_re=".*")
visible_windows = []

for handle in all_handles:
    try:
        app = Application(backend='win32').connect(handle=handle)
        window = app.top_window()
        if window.is_visible():
            title = window.window_text()
            class_name = window.class_name()
            if title.strip() and len(title) > 0:
                visible_windows.append({
                    'title': title,
                    'class': class_name,
                    'handle': handle
                })
    except:
        pass

print(f"\nFound {len(visible_windows)} visible windows:")
for i, w in enumerate(visible_windows[:20]):  # Show first 20
    print(f"  [{i}] {w['title']:40} | {w['class'][:40]}")

print("\n[2] Looking for dialog windows...")
dialogs = findwindows.find_windows(class_name_re=".*Dialog.*")
print(f"    Dialog windows found: {len(dialogs)}")
for h in dialogs[:5]:
    try:
        app = Application(backend='win32').connect(handle=h)
        window = app.top_window()
        print(f"      - {window.window_text()}")
    except:
        pass

print("\n[3] Looking for message boxes...")
msgboxes = findwindows.find_windows(class_name_re=".*Message.*")
print(f"    Message boxes found: {len(msgboxes)}")

print("\n[4] Looking for popups or alerts...")
try:
    popups = findwindows.find_windows(title_re=".*alert.*|.*error.*|.*warning.*")
    print(f"    Alert/warning windows found: {len(popups)}")
except Exception as e:
    print(f"    Could not search: {e}")

print("\n[5] Checking Navigator window details...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
if nav_handles:
    app = Application(backend='win32').connect(handle=nav_handles[0])
    window = app.top_window()
    print(f"    Navigator is enabled: {window.is_enabled()}")
    print(f"    Navigator is visible: {window.is_visible()}")
    print(f"    Navigator is focused: {window.has_focus()}")
    
    # Get text from the Navigator
    children = window.children()
    print(f"    Navigator children: {len(children)}")
    
    # Look for any status or error messages
    for child in children:
        try:
            text = child.window_text()
            class_name = child.class_name()
            if 'error' in text.lower() or 'warning' in text.lower() or 'message' in text.lower():
                print(f"    [!] Potential error message: {text}")
        except:
            pass

print("\n[6] Checking for Sales screen...")
sales_handles = findwindows.find_windows(title_re=".*Sales.*", title_re_flags=2)
print(f"    Sales windows found: {len(sales_handles)}")
for h in sales_handles:
    try:
        app = Application(backend='win32').connect(handle=h)
        window = app.top_window()
        print(f"      - {window.window_text()} (Visible: {window.is_visible()})")
    except:
        pass

print("\nInspection complete.")
