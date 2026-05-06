"""
Use pywinauto click_input with debugging to see what it's actually doing
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time

print("[1] Connecting to Navigator...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()
window.set_focus()
time.sleep(0.5)

print("[2] Finding Sales button...")
children = window.children()
sales_button = None

for child in children:
    try:
        if child.window_text() == "Sales" and child.is_visible():
            sales_button = child
            break
    except:
        pass

if not sales_button:
    print("[X] Button not found")
    exit(1)

print("[3] Getting button element info...")
print(f"    Text: {sales_button.window_text()}")
print(f"    Class: {sales_button.class_name()}")
print(f"    Rect: {sales_button.rectangle()}")

print("[4] Using pywinauto click_input (debugged)...")

# Check what click_input actually does
import inspect
print(f"\n    click_input signature:")
sig = inspect.signature(sales_button.click_input)
print(f"    {sig}")

try:
    # Try with no parameters
    print(f"\n    Calling click_input()...")
    sales_button.click_input()
    print(f"    click_input() executed")
    time.sleep(3)
    
    sales_handles = findwindows.find_windows(title_re=".*Sales.*")
    if sales_handles:
        print(f"    ✓ SUCCESS!")
        exit(0)
    else:
        print(f"    [X] No result from click_input()")

except Exception as e:
    print(f"    Error: {e}")
    import traceback
    traceback.print_exc()

print("[5] Let me check what's the EXACT sequence you do manually...")
print(f"    When you click the Sales button manually in G2:")
print(f"    - Does a NEW window open?")
print(f"    - Does content appear INSIDE the Navigator?")
print(f"    - Does a menu/popup appear?")
print(f"    - Does anything visual change?")
print(f"\n    Please describe what you see...")

