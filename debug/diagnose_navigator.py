"""
Diagnose the Navigator window state and button interaction issues
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time
import warnings
warnings.filterwarnings('ignore')

print("[1] Finding Navigator window...")
handles = findwindows.find_windows(title_re=".*Navigator.*")
print(f"    Found {len(handles)} window(s) matching Navigator")

if not handles:
    print("[X] No Navigator window found!")
    print("\n[*] All G2 windows:")
    all_handles = findwindows.find_windows(title_re=".*G2.*")
    for i, h in enumerate(all_handles):
        try:
            app = Application(backend='win32').connect(handle=h)
            window = app.top_window()
            print(f"    [{i}] Title: {window.window_text()}")
            print(f"        Class: {window.class_name()}")
            print(f"        Visible: {window.is_visible()}")
        except Exception as e:
            print(f"    [{i}] Error: {e}")
    exit(1)

print("\n[2] Connecting to Navigator...")
try:
    app = Application(backend='win32').connect(handle=handles[0])
    window = app.top_window()
    print(f"    ✓ Connected")
    print(f"    Title: {window.window_text()}")
    print(f"    Class: {window.class_name()}")
    print(f"    Visible: {window.is_visible()}")
except Exception as e:
    print(f"    [X] Connection failed: {e}")
    exit(1)

print("\n[3] Scanning for buttons...")
children = window.children()
print(f"    Total children: {len(children)}")

buttons = []
for i, child in enumerate(children):
    try:
        class_name = child.class_name()
        text = child.window_text()
        is_enabled = child.is_enabled()
        is_visible = child.is_visible()
        
        # Look for button-like elements
        if 'button' in class_name.lower() or text.strip():
            buttons.append({
                'index': i,
                'text': text,
                'class': class_name,
                'enabled': is_enabled,
                'visible': is_visible,
                'handle': child.handle
            })
            print(f"    [{i}] {text:20} | Class: {class_name:30} | Enabled: {is_enabled} | Visible: {is_visible}")
    except Exception as e:
        pass

print(f"\n[4] Found {len(buttons)} button-like elements")

if buttons:
    print("\n[5] Attempting to click first button...")
    first_btn = buttons[0]
    print(f"    Target: {first_btn['text']}")
    
    try:
        # Find the actual control object
        for child in children:
            if child.window_text() == first_btn['text']:
                print(f"    Clicking...")
                child.click()
                time.sleep(1)
                print(f"    ✓ Click executed")
                break
    except Exception as e:
        print(f"    [X] Click failed: {e}")

print("\n[6] Rechecking window state...")
try:
    window.draw_outline()
    print(f"    ✓ Window is still responsive")
except Exception as e:
    print(f"    [X] Window error: {e}")

print("\nDiagnosis complete.")
