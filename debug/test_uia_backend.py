"""
Try clicking using UIA backend instead of win32
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time
import warnings
warnings.filterwarnings('ignore')

print("[1] Connecting with UIA backend...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
if not nav_handles:
    print("[X] Navigator not found")
    exit(1)

try:
    app = Application(backend='uia').connect(handle=nav_handles[0])
    window = app.top_window()
    print(f"    Connected: {window.window_text()}")
except Exception as e:
    print(f"    [X] UIA connection failed: {e}")
    exit(1)

print("\n[2] Scanning UIA children...")
children = window.children()
print(f"    Total children: {len(children)}")

buttons = []
for i, child in enumerate(children):
    try:
        name = child.name
        control_type = child.control_type
        
        if name and ('Sales' in name or 'Service' in name or 'Accounting' in name or 'Admin' in name or 'Parts' in name):
            buttons.append({
                'name': name,
                'type': control_type,
                'index': i,
                'child': child
            })
            print(f"    [{i}] {name:20} | Type: {control_type}")
    except Exception as e:
        pass

print(f"\n[3] Found {len(buttons)} menu buttons")

if buttons:
    print(f"\n[4] Trying to click first button ({buttons[0]['name']})...")
    try:
        target = buttons[0]['child']
        print(f"    Invoking pattern...")
        target.invoke()
        print(f"    ✓ Invoke executed")
        time.sleep(2)
        
        # Check result
        sales_handles = findwindows.find_windows(title_re=".*Sales.*")
        if sales_handles:
            print(f"    ✓ SUCCESS! Sales screen opened!")
        else:
            print(f"    [X] No screen opened")
    except Exception as e:
        print(f"    [X] Invoke failed: {e}")
        
        # Try alternative method
        print(f"\n[5] Trying send_keys approach...")
        try:
            target = buttons[0]['child']
            window.set_focus()
            target.send_keys('{SPACE}')
            time.sleep(2)
            print(f"    Space key sent")
        except Exception as e2:
            print(f"    [X] send_keys failed: {e2}")

print("\nTest complete.")
