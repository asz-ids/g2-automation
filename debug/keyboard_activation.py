"""
Try keyboard-based button activation - give focus to button and press Space/Enter
"""

from pywinauto import findwindows
from pywinauto.application import Application
from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

print("[1] Connecting to Navigator...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()

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

print(f"    Found Sales button")

print(f"\n[3] Method 1: SetFocus on button, then press Space...")
try:
    # Use pywinauto to set focus on the actual button element
    sales_button.set_focus()
    time.sleep(0.3)
    
    print(f"    Focus set on button")
    
    # Now press Space to activate it
    keyboard.press(Key.space)
    keyboard.release(Key.space)
    print(f"    Space key pressed")
    
    time.sleep(3)
    
    # Check for changes
    after = scan_navigator_content()
    print(f"    Navigator now has {after['total_children']} children (was 34)")
    
except Exception as e:
    print(f"    Error: {e}")
    import traceback
    traceback.print_exc()

def scan_navigator_content():
    nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
    if not nav_handles:
        return {'total_children': 0}
    
    app = Application(backend='win32').connect(handle=nav_handles[0])
    window = app.top_window()
    return {'total_children': len(window.children())}

print(f"\n[4] Method 2: SetFocus on button, then press Enter...")
try:
    sales_button.set_focus()
    time.sleep(0.3)
    
    print(f"    Focus set on button")
    
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    print(f"    Enter key pressed")
    
    time.sleep(3)
    
    after = scan_navigator_content()
    print(f"    Navigator now has {after['total_children']} children (was 34)")
    
except Exception as e:
    print(f"    Error: {e}")

print(f"\n[5] Method 3: Try pywinauto's press_keys...")
try:
    sales_button.set_focus()
    time.sleep(0.2)
    
    # Try pywinauto's built-in method
    sales_button.send_keystrokes(' ')  # Space
    print(f"    send_keystrokes(' ') called")
    
    time.sleep(3)
    
    after = scan_navigator_content()
    print(f"    Navigator now has {after['total_children']} children (was 34)")
    
except Exception as e:
    print(f"    Error: {e}")
    # Try alternative syntax
    try:
        sales_button.send_keys('{SPACE}')
        print(f"    send_keys('{{SPACE}}') called")
        time.sleep(3)
    except Exception as e2:
        print(f"    Also failed: {e2}")

print(f"\nDone.")
