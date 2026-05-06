"""
Test clicking Navigator buttons when properly logged in
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
window.set_focus()
print(f"    Connected and focused")

print("\n[2] Finding and clicking Sales button...")
children = window.children()
sales_found = False

for child in children:
    try:
        if child.window_text() == "Sales" and child.is_visible() and child.is_enabled():
            print(f"    Found Sales button")
            print(f"    Attempting click()...")
            child.click()
            sales_found = True
            break
    except Exception as e:
        pass

if not sales_found:
    print("[X] Could not find Sales button")
    exit(1)

time.sleep(2)

print("\n[3] Checking for screen changes...")
# Get updated window list
all_windows = findwindows.find_windows(title_re=".*")
print(f"    Total windows now: {len(all_windows)}")

# Look for Sales, Service, etc screens
for screen_name in ["Sales", "Service", "Accounting", "Admin", "Parts"]:
    try:
        handles = findwindows.find_windows(title_re=f".*{screen_name}.*")
        if handles:
            for h in handles:
                app_temp = Application(backend='win32').connect(handle=h)
                w_temp = app_temp.top_window()
                if w_temp.is_visible():
                    print(f"    ✓ Found: {w_temp.window_text()}")
    except:
        pass

print("\n[4] Checking MDI client for internal windows...")
try:
    # Find MDI client
    for child in window.children():
        if 'mdi' in child.class_name().lower():
            mdi_children = child.children()
            print(f"    MDI children: {len(mdi_children)}")
            for m in mdi_children:
                print(f"      - {m.window_text()}")
            break
except Exception as e:
    print(f"    Error: {e}")

print("\n[5] Taking screenshot to see actual state...")
try:
    from PIL import ImageGrab
    screenshot = ImageGrab.grab()
    screenshot.save("e:\\G2 Desktop Automation\\screenshots\\current_state.png")
    print(f"    ✓ Screenshot saved")
except Exception as e:
    print(f"    [X] Screenshot failed: {e}")

print("\nTest complete.")
