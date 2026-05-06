"""
Use Win32 API directly to bypass pywinauto coordinate issues
"""

from ctypes import windll, c_int, wintypes, Structure, POINTER, c_long
from pywinauto import findwindows
from pywinauto.application import Application
import time
import warnings
warnings.filterwarnings('ignore')

# Win32 API structures
class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

class RECT(Structure):
    _fields_ = [("left", c_long), ("top", c_long), ("right", c_long), ("bottom", c_long)]

def get_window_rect(hwnd):
    """Get actual window rectangle using Win32 API"""
    rect = RECT()
    windll.user32.GetWindowRect(hwnd, POINTER(RECT)(rect))
    return rect

def click_button_by_hwnd(hwnd):
    """Click button using Win32 API"""
    # Get the window's actual position
    rect = get_window_rect(hwnd)
    
    x = (rect.left + rect.right) // 2
    y = (rect.top + rect.bottom) // 2
    
    print(f"    Window rect: ({rect.left}, {rect.top}) to ({rect.right}, {rect.bottom})")
    print(f"    Center point: ({x}, {y})")
    
    # Set cursor position
    windll.user32.SetCursorPos(x, y)
    time.sleep(0.2)
    
    # Send left mouse button down
    windll.user32.mouse_event(2, 0, 0, 0, 0)
    time.sleep(0.1)
    
    # Send left mouse button up
    windll.user32.mouse_event(4, 0, 0, 0, 0)
    time.sleep(0.5)

print("[1] Finding Navigator window...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
if not nav_handles:
    print("[X] Navigator not found")
    exit(1)

nav_hwnd = nav_handles[0]
print(f"    Navigator HWND: {nav_hwnd}")

print("\n[2] Connecting to Navigator...")
app = Application(backend='win32').connect(handle=nav_hwnd)
window = app.top_window()
window.set_focus()
time.sleep(0.5)

print("\n[3] Finding buttons...")
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
    print("[X] Could not find Sales button")
    exit(1)

print(f"    Found Sales button")

print("\n[4] Clicking Sales button using Win32 API...")
try:
    click_button_by_hwnd(sales_button.handle)
    print(f"    ✓ Click executed")
    time.sleep(2)
except Exception as e:
    print(f"    [X] Error: {e}")

print("\n[5] Checking for result...")
try:
    sales_handles = findwindows.find_windows(title_re=".*Sales.*")
    if sales_handles:
        print(f"    ✓ SUCCESS! Sales screen opened!")
    else:
        print(f"    [X] No screen opened yet")
        
        # List what windows exist now
        print(f"\n[6] Checking all windows...")
        all_handles = findwindows.find_windows(title_re=".*")
        print(f"    Total windows: {len(all_handles)}")
        
        # Look for any new screens
        screen_windows = []
        for h in all_handles:
            try:
                app_temp = Application(backend='win32').connect(handle=h)
                w_temp = app_temp.top_window()
                title = w_temp.window_text()
                if 'Screen' in title or 'View' in title:
                    screen_windows.append(title)
            except:
                pass
        
        if screen_windows:
            print(f"    Screen windows found: {screen_windows}")
        else:
            print(f"    No screen windows found")
except Exception as e:
    print(f"    Error: {e}")

print("\nTest complete.")
