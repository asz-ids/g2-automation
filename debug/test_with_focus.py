"""
Test clicking menu buttons with proper window focus
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time
import warnings
warnings.filterwarnings('ignore')

print("[1] Connecting to Navigator...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
if not nav_handles:
    print("[X] Navigator not found")
    exit(1)

app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()
print(f"    Connected to: {window.window_text()}")

print("\n[2] Focusing Navigator window...")
try:
    window.set_focus()
    time.sleep(0.5)
    print(f"    Navigator focused: {window.has_focus()}")
except Exception as e:
    print(f"    Focus attempt: {e}")

print("\n[3] Clicking Sales button...")
children = window.children()
sales_button = None

for child in children:
    try:
        if child.window_text() == "Sales" and child.is_visible():
            sales_button = child
            break
    except:
        pass

if sales_button:
    print(f"    Found Sales button")
    print(f"    Enabled: {sales_button.is_enabled()}")
    print(f"    Visible: {sales_button.is_visible()}")
    
    print(f"    Clicking...")
    sales_button.click()
    time.sleep(2)
    print(f"    Click completed")
    
    print("\n[4] Checking for Sales screen...")
    try:
        sales_handles = findwindows.find_windows(title_re=".*Sales.*")
        print(f"    Sales windows found: {len(sales_handles)}")
        
        if sales_handles:
            for h in sales_handles:
                app2 = Application(backend='win32').connect(handle=h)
                window2 = app2.top_window()
                print(f"      - Title: {window2.window_text()}")
                print(f"      - Visible: {window2.is_visible()}")
                print(f"      - Enabled: {window2.is_enabled()}")
        else:
            print(f"    [X] No Sales screen found")
            
            # Check what windows ARE open
            print(f"\n[5] Checking all windows...")
            all_handles = findwindows.find_windows(title_re=".*")
            recent_windows = []
            
            for h in all_handles:
                try:
                    app_temp = Application(backend='win32').connect(handle=h)
                    w_temp = app_temp.top_window()
                    if w_temp.is_visible():
                        title = w_temp.window_text()
                        if title.strip() and 'Screen' in title:
                            recent_windows.append(title)
                            print(f"    - {title}")
                except:
                    pass
            
            if not recent_windows:
                print(f"    No screen windows detected")
    except Exception as e:
        print(f"    Error checking: {e}")
else:
    print(f"    [X] Could not find Sales button")
    print(f"    Available buttons:")
    for child in children:
        try:
            if child.is_visible():
                print(f"      - {child.window_text()}")
        except:
            pass

print("\nTest complete.")
