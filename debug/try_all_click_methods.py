"""
Try clicking using proper Windows API approach for WindowsForms controls
"""

from pywinauto import findwindows
from pywinauto.application import Application
from ctypes import windll, c_int, c_long, c_void_p
import time

print("[1] Finding Sales button handle...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()

sales_button = None
for child in window.children():
    try:
        if child.window_text() == "Sales" and child.is_visible():
            sales_button = child
            break
    except:
        pass

if not sales_button:
    print("[X] Sales button not found")
    exit(1)

sales_hwnd = sales_button.handle
print(f"    Sales button HWND: {sales_hwnd}")

print(f"\n[2] Method 1: SendMessage with WM_LBUTTONDOWN + WM_LBUTTONUP...")
try:
    WM_LBUTTONDOWN = 513
    WM_LBUTTONUP = 514
    
    # Send to the button control itself
    windll.user32.SendMessageA(sales_hwnd, WM_LBUTTONDOWN, 0, 0)
    time.sleep(0.1)
    windll.user32.SendMessageA(sales_hwnd, WM_LBUTTONUP, 0, 0)
    
    print(f"    Sent WM_LBUTTON messages")
    time.sleep(2)
    
    sales_handles = findwindows.find_windows(title_re=".*Sales.*")
    if sales_handles:
        print(f"    ✓ SUCCESS!")
        exit(0)
except Exception as e:
    print(f"    Error: {e}")

print(f"\n[3] Method 2: SetFocus + SendMessage...")
try:
    # Focus the button
    windll.user32.SetFocus(sales_hwnd)
    time.sleep(0.2)
    
    # Send click
    WM_LBUTTONDOWN = 513
    WM_LBUTTONUP = 514
    
    windll.user32.SendMessageA(sales_hwnd, WM_LBUTTONDOWN, 1, 0)  # wParam=1 for left button
    time.sleep(0.1)
    windll.user32.SendMessageA(sales_hwnd, WM_LBUTTONUP, 0, 0)
    
    print(f"    Sent focused click")
    time.sleep(2)
    
    sales_handles = findwindows.find_windows(title_re=".*Sales.*")
    if sales_handles:
        print(f"    ✓ SUCCESS!")
        exit(0)
except Exception as e:
    print(f"    Error: {e}")

print(f"\n[4] Method 3: Send WM_LBUTTONDOWN to parent (might be a tab control)...")
try:
    parent = sales_button.parent()
    parent_hwnd = parent.handle
    
    print(f"    Parent HWND: {parent_hwnd}")
    
    # Send to parent with child's handle info
    WM_LBUTTONDOWN = 513
    WM_LBUTTONUP = 514
    
    # Prepare coordinate within parent
    rect = sales_button.rectangle()
    x = (rect.left + rect.right) // 2 - 471  # Offset from parent
    y = (rect.top + rect.bottom) // 2 - 56
    
    lparam = (y << 16) | (x & 0xFFFF)
    
    windll.user32.SendMessageA(parent_hwnd, WM_LBUTTONDOWN, 0, lparam)
    time.sleep(0.1)
    windll.user32.SendMessageA(parent_hwnd, WM_LBUTTONUP, 0, lparam)
    
    print(f"    Sent click to parent at ({x}, {y})")
    time.sleep(2)
    
    sales_handles = findwindows.find_windows(title_re=".*Sales.*")
    if sales_handles:
        print(f"    ✓ SUCCESS!")
        exit(0)
except Exception as e:
    print(f"    Error: {e}")

print(f"\n[5] Method 4: Direct pixel click using Windows API...")
try:
    rect = sales_button.rectangle()
    x = (rect.left + rect.right) // 2
    y = (rect.top + rect.bottom) // 2
    
    print(f"    Target pixel: ({x}, {y})")
    
    # Move cursor
    windll.user32.SetCursorPos(x, y)
    time.sleep(0.1)
    
    # Perform click with actual mouse event
    windll.user32.mouse_event(2, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTDOWN
    time.sleep(0.05)
    windll.user32.mouse_event(4, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTUP
    
    print(f"    Sent pixel click")
    time.sleep(2)
    
    sales_handles = findwindows.find_windows(title_re=".*Sales.*")
    if sales_handles:
        print(f"    ✓ SUCCESS!")
        exit(0)
except Exception as e:
    print(f"    Error: {e}")

print(f"\n[6] Method 5: Try click_input with different parameters...")
try:
    # pywinauto's click_input might have special handling
    sales_button.click_input()
    print(f"    click_input() executed")
    time.sleep(2)
    
    sales_handles = findwindows.find_windows(title_re=".*Sales.*")
    if sales_handles:
        print(f"    ✓ SUCCESS!")
        exit(0)
except Exception as e:
    print(f"    Error: {e}")

print(f"\nNo method worked. The buttons might need special G2-specific interaction.")
