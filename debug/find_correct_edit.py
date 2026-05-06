"""
Debug: List all Edit controls and their positions to find the Customer # field
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen
from pywinauto import Application, findwindows
import time

# nav = NavigatorScreen()
# nav.click_menu_button('Parts')
# time.sleep(1)
# nav.click_explorer_bar_button('Take AR Payments')
# time.sleep(2)

# Find window
handles = findwindows.find_windows(title_re=".*Accounts Receivable.*")
if not handles:
    handles = findwindows.find_windows(title_re=".*Payment.*")
ar_hwnd = handles[0]

# Connect with win32
app_win32 = Application(backend='win32').connect(handle=ar_hwnd)
window_win32 = app_win32.window(handle=ar_hwnd)

# Find all Edit controls with their positions
edit_list = window_win32.children(class_name='Edit')
print(f"Found {len(edit_list)} Edit controls:\n")

import ctypes
GetWindowRect = ctypes.windll.user32.GetWindowRect

for i, edit in enumerate(edit_list):
    try:
        rect = ctypes.wintypes.RECT()
        GetWindowRect(edit.handle, ctypes.byref(rect))
        text = edit.window_text() if hasattr(edit, 'window_text') else ""
        print(f"[{i}] Position: X={rect.left:4d}, Y={rect.top:4d}  Text: '{text}'")
    except Exception as e:
        print(f"[{i}] Error: {e}")

print("\n Looking for 'Customer #' label in UIA...")

app_uia = Application(backend='uia').connect(handle=ar_hwnd)
window_uia = app_uia.window(handle=ar_hwnd)

# Find Customer # Pane
try:
    customer_pane = window_uia.child_window(control_type="Pane", auto_id="9953220")
    rect_obj = customer_pane.rectangle
    if callable(rect_obj):
        label_rect = rect_obj()
    else:
        label_rect = rect_obj
    print(f"Customer # Pane at: X={label_rect.left:4d}, Y={label_rect.top:4d}")
    
    # Find the Edit control closest to it on the right
    print(f"\nEdits to the right of Customer # label:")
    for i, edit in enumerate(edit_list):
        try:
            rect = ctypes.wintypes.RECT()
            GetWindowRect(edit.handle, ctypes.byref(rect))
            
            if rect.top >= label_rect.top - 10 and rect.top <= label_rect.bottom + 10:
                distance = rect.left - label_rect.right
                if distance >= -50 and distance <= 200:
                    print(f"  [{i}] Distance={distance:3d}, Y-diff={rect.top - label_rect.top:3d}")
        except:
            pass
            
except Exception as e:
    print(f"Error: {e}")
