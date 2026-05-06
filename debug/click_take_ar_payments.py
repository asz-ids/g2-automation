"""
Test: Actually click Take AR Payments button and capture results
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen
from pywinauto import Application, findwindows
import pywinauto.mouse
import time

print("=" * 60)
print("Clicking Take AR Payments Button")
print("=" * 60)

# Step 1: Navigate to Parts
print("\n[1] Navigating to Parts menu...")
nav = NavigatorScreen()
result = nav.click_menu_button('Parts')
print(f"    Parts button clicked: {result}")
time.sleep(1)

active = nav.get_active_menu()
print(f"    Active menu: {active}")

# Step 2: Get window info
print("\n[2] Getting window information...")
handles = findwindows.find_windows(title_re=".*Navigator.*")
if handles:
    print(f"    Navigator handle: {handles[0]}")
else:
    print("    ERROR: Navigator not found")
    exit(1)

# Step 3: Try to find button via UIA
print("\n[3] Attempting to find Take AR Payments button via UIA...")
app_uia = Application(backend='uia').connect(handle=handles[0])
window_uia = app_uia.window(handle=handles[0])

button_found = False
button_elem = None

# Search all descendants
for elem in window_uia.descendants():
    try:
        if hasattr(elem, 'name') and elem.name:
            if 'Take AR Payments' in str(elem.name):
                button_found = True
                button_elem = elem
                print(f"    ✓ Found via UIA: {elem.name}")
                break
    except:
        pass

if not button_found:
    print("    ✗ Not found via UIA (expected - button is in custom control)")

# Step 4: Click using mouse coordinates
print("\n[4] Clicking Take AR Payments by mouse coordinates...")
print("    Coordinates: (420, 310)")
pywinauto.mouse.click(coords=(420, 310))
print("    ✓ Click sent")
time.sleep(2)

# Step 5: Check what happened
print("\n[5] Checking what opened after click...")

# Look for new windows
all_windows = findwindows.find_windows()
print(f"    Total windows: {len(all_windows)}")

# Look for dialogs or new content
print("\n    Checking for common Take AR Payments window patterns...")

search_patterns = [
    ".*Take.*",
    ".*AR.*",
    ".*Payment.*",
    ".*Receipt.*",
    ".*Customer.*",
    ".*Dialog.*",
]

found_new = False
for pattern in search_patterns:
    new_wins = findwindows.find_windows(title_re=pattern)
    if new_wins:
        print(f"    Found windows matching '{pattern}':")
        for hw in new_wins:
            try:
                # Get window title
                import ctypes
                length = ctypes.windll.user32.GetWindowTextLengthW(hw)
                if length > 0:
                    title = ctypes.create_unicode_buffer(length + 1)
                    ctypes.windll.user32.GetWindowTextW(hw, title, length + 1)
                    print(f"      - {title.value}")
                    found_new = True
            except:
                pass

if not found_new:
    print("    No new windows detected")

# Step 6: Check Navigator state
print("\n[6] Navigator state after click...")
try:
    nav2 = NavigatorScreen()
    active_now = nav2.get_active_menu()
    print(f"    Active menu: {active_now}")
except:
    print("    Could not determine active menu")

print("\n" + "=" * 60)
print("Click execution complete")
print("=" * 60)
print("\nNOTE: If no new window appeared, the Take AR Payments screen")
print("may be displayed within the current window or hidden.")
print("\nTo find the exact coordinates, look for:")
print("  - Explorer bar buttons on the left side")
print("  - Under 'My Tasks' section")
print("  - Adjust X,Y coordinates if needed for your resolution")
