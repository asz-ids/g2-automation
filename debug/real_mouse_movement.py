"""
Try real mouse movement simulation instead of instant positioning
"""

from pywinauto import findwindows
from pywinauto.application import Application
from ctypes import windll
import time

print("[1] Finding Sales button...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()
window.set_focus()

sales_button = None
for child in window.children():
    try:
        if child.window_text() == "Sales" and child.is_visible():
            sales_button = child
            break
    except:
        pass

if not sales_button:
    print("[X] Button not found")
    exit(1)

rect = sales_button.rectangle()
target_x = (rect.left + rect.right) // 2
target_y = (rect.top + rect.bottom) // 2

print(f"    Target position: ({target_x}, {target_y})")

print(f"\n[2] Method: Gradual mouse movement to button...")
try:
    # Get current cursor position
    from ctypes import c_long, Structure, POINTER
    
    class POINT(Structure):
        _fields_ = [("x", c_long), ("y", c_long)]
    
    current_pos = POINT()
    windll.user32.GetCursorPos(POINTER(POINT)(current_pos))
    
    start_x = current_pos.x
    start_y = current_pos.y
    
    print(f"    Starting position: ({start_x}, {start_y})")
    
    # Gradually move mouse to button
    steps = 10
    for step in range(1, steps + 1):
        x = start_x + int((target_x - start_x) * (step / steps))
        y = start_y + int((target_y - start_y) * (step / steps))
        
        windll.user32.SetCursorPos(x, y)
        time.sleep(0.05)  # 50ms between steps
    
    print(f"    Moved cursor to target")
    time.sleep(0.5)
    
    # Now click
    print(f"    Clicking...")
    windll.user32.mouse_event(2, 0, 0, 0, 0)  # Left down
    time.sleep(0.1)
    windll.user32.mouse_event(4, 0, 0, 0, 0)  # Left up
    
    print(f"    Click sent")
    time.sleep(3)
    
    # Check
    sales_handles = findwindows.find_windows(title_re=".*Sales.*")
    if sales_handles:
        print(f"    ✓ SUCCESS!")
        exit(0)
    else:
        print(f"    [X] No result")

except Exception as e:
    print(f"    Error: {e}")
    import traceback
    traceback.print_exc()

print(f"\n[3] Method: Using ABSOLUTE mouse coordinates...")
try:
    # MOUSEEVENTF_ABSOLUTE flag = 0x8000
    MOUSEEVENTF_MOVE = 0x0001
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    MOUSEEVENTF_ABSOLUTE = 0x8000
    
    # Move with absolute positioning
    windll.user32.mouse_event(
        MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE,
        int(target_x * 65535 / 1920),  # Normalize to 65535 max
        int(target_y * 65535 / 1080),  # Normalize to 65535 max
        0, 0
    )
    time.sleep(0.2)
    
    # Click
    windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.05)
    windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    
    print(f"    Absolute click sent")
    time.sleep(3)
    
    sales_handles = findwindows.find_windows(title_re=".*Sales.*")
    if sales_handles:
        print(f"    ✓ SUCCESS!")
        exit(0)
        
except Exception as e:
    print(f"    Error: {e}")

print(f"\nDone.")
