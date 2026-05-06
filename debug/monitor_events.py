"""
Try using WinEventHook to detect what happens when we click
"""

from pywinauto import findwindows
from pywinauto.application import Application
from ctypes import windll, c_uint, WINFUNCTYPE, c_int, c_long, c_char_p
import time
import warnings
warnings.filterwarnings('ignore')

# Define event hook callback
events_detected = []

def event_hook(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
    try:
        if event in [3, 4, 6, 7]:  # EVENT_SYSTEM_FOREGROUND, EVENT_SYSTEM_FOCUS, etc.
            events_detected.append((event, hwnd))
    except:
        pass
    return 0

print("[1] Setting up event hook...")
WinEventHookType = WINFUNCTYPE(c_int, c_int, c_uint, c_long, c_long, c_long, c_uint, c_uint)
hook_callback = WinEventHookType(event_hook)

try:
    hook = windll.user32.SetWinEventHook(
        3,  # EVENT_SYSTEM_FOREGROUND
        7,  # EVENT_SYSTEM_FOCUS  
        None,
        hook_callback,
        0, 0,
        0   # WINEVENT_OUTOFCONTEXT
    )
    print(f"    Hook installed: {hook != 0}")
except Exception as e:
    print(f"    [X] Hook failed: {e}")

print("\n[2] Connecting to Navigator...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()
window.set_focus()

print("\n[3] Clicking Sales button...")
children = window.children()
for child in children:
    try:
        if child.window_text() == "Sales" and child.is_visible():
            print(f"    Clicking...")
            child.click()
            break
    except:
        pass

print("\n[4] Waiting for events...")
time.sleep(3)

print(f"\n[5] Events detected: {len(events_detected)}")
for evt, hwnd in events_detected[:10]:
    try:
        app_temp = Application(backend='win32').connect(handle=hwnd)
        w_temp = app_temp.top_window()
        print(f"    Event {evt}: {w_temp.window_text()}")
    except:
        print(f"    Event {evt}: HWND {hwnd}")

# Clean up hook
if 'hook' in locals():
    windll.user32.UnhookWinEvent(hook)

print("\nMonitoring complete.")
