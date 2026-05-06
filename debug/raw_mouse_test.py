"""
Debug the exact pixel location and try raw mouse events
"""

from pywinauto import findwindows
from pywinauto.application import Application
from ctypes import windll, c_int
import time
import warnings
warnings.filterwarnings('ignore')

print("[1] Connecting to Navigator...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()

print(f"    Window position: {window.rectangle()}")
print(f"    Window text: {window.window_text()}")

print("\n[2] Finding Sales button...")
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
    print("[X] Sales button not found")
    exit(1)

print(f"    Found Sales button")

print("\n[3] Getting button rectangle...")
rect = sales_button.rectangle()
print(f"    Button rect: {rect}")
print(f"    Width: {rect.width()}, Height: {rect.height()}")

# Check if coordinates are valid
if rect.left < 0 or rect.top < 0:
    print(f"    [!] WARNING: Negative coordinates detected!")
    print(f"        This might be a display/DPI scaling issue")

print("\n[4] Trying raw click with correct screen coordinates...")
# Get screen coordinates of button center
x = (rect.left + rect.right) // 2
y = (rect.top + rect.bottom) // 2

print(f"    Target coordinates: ({x}, {y})")

# Try to click using SetCursorPos and mouse_event
print(f"    Step 1: Setting cursor position...")
windll.user32.SetCursorPos(x, y)
time.sleep(0.3)

print(f"    Step 2: Simulating mouse down...")
windll.user32.mouse_event(2, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTDOWN
time.sleep(0.2)

print(f"    Step 3: Simulating mouse up...")
windll.user32.mouse_event(4, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTUP
time.sleep(2)

print(f"\n[5] Checking if anything changed...")
# Check MDI
try:
    for child in window.children():
        if 'mdi' in child.class_name().lower():
            mdi_kids = child.children()
            print(f"    MDI children: {len(mdi_kids)}")
            if mdi_kids:
                for m in mdi_kids:
                    print(f"      - {m.window_text()}")
except:
    pass

# Check for new windows
try:
    sales_handles = findwindows.find_windows(title_re=".*Sales.*")
    if sales_handles:
        print(f"    Sales window found!")
    else:
        print(f"    No Sales window")
except:
    pass

print(f"\n[6] Trying alternative: double-click...")
windll.user32.SetCursorPos(x, y)
time.sleep(0.1)
windll.user32.mouse_event(2, 0, 0, 0, 0)  # Down
time.sleep(0.05)
windll.user32.mouse_event(4, 0, 0, 0, 0)  # Up
time.sleep(0.05)
windll.user32.mouse_event(2, 0, 0, 0, 0)  # Down
time.sleep(0.05)
windll.user32.mouse_event(4, 0, 0, 0, 0)  # Up
time.sleep(2)

print(f"    Double-click complete")

# Check result
try:
    sales_handles = findwindows.find_windows(title_re=".*Sales.*")
    if sales_handles:
        print(f"    ✓ Sales window found after double-click!")
    else:
        print(f"    Still no Sales window")
except:
    pass

print("\nTest complete.")
