"""
Debug: Find all text elements in Take AR Payments window
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen
from pywinauto import Application, findwindows
import time

nav = NavigatorScreen()
nav.click_menu_button('Parts')
time.sleep(1)
nav.click_explorer_bar_button('Take AR Payments')
time.sleep(2)

# Find window
handles = findwindows.find_windows(title_re=".*Accounts Receivable.*")
if not handles:
    handles = findwindows.find_windows(title_re=".*Payment.*")
    
if not handles:
    print("No AR Payment window found")
    # List all windows
    all_handles = findwindows.find_windows()
    print(f"\nAll windows ({len(all_handles)}):")
    for h in all_handles[:10]:
        import ctypes
        length = ctypes.windll.user32.GetWindowTextLengthW(h)
        if length > 0:
            title = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(h, title, length + 1)
            print(f"  {h}: {title.value}")
    exit(1)

ar_hwnd = handles[0]
print(f"Window: {ar_hwnd}")

app_uia = Application(backend='uia').connect(handle=ar_hwnd)
window_uia = app_uia.window(handle=ar_hwnd)

print("\nAll text elements in window:")
print("-" * 70)

count = 0
for elem in window_uia.descendants():
    try:
        elem_text = elem.window_text() if hasattr(elem, 'window_text') else ""
        elem_type = elem.control_type if hasattr(elem, 'control_type') else ""
        
        if elem_text and elem_text.strip():
            count += 1
            print(f"[{count}] Type: {elem_type:15s} Text: {elem_text[:60]}")
            if count > 50:
                break
    except:
        pass

print(f"\n(showing first 50 text elements)")
