"""Debug: open the Functions menu in the AR Payment window and list its items."""
import ctypes
import ctypes.wintypes
import time
from pywinauto import findwindows, Desktop
from pywinauto.keyboard import send_keys

handles = findwindows.find_windows(title_re=".*Accounts Receivable.*")
if not handles:
    print("ERROR: AR Payment window not found")
    exit(1)

ar_hwnd = handles[0]
ar_win = Desktop(backend='uia').window(handle=ar_hwnd)

print(f"AR window HWND: {ar_hwnd}")

# Bring to front
ctypes.windll.user32.SetForegroundWindow(ar_hwnd)
ctypes.windll.user32.BringWindowToTop(ar_hwnd)
time.sleep(0.5)

# Click the Functions menu item in the menu bar
print("\nClicking Functions menu item...")
try:
    fn_item = ar_win.child_window(title="Functions", control_type="MenuItem")
    fn_item.click_input()
    time.sleep(0.8)
    print("Clicked Functions")
except Exception as e:
    print(f"Failed to click Functions: {e}")
    # Try keyboard approach
    send_keys('{F10}')
    time.sleep(0.3)
    send_keys('f')
    time.sleep(0.3)

# Look for popup menu windows (class #32768 = standard menu)
print("\nLooking for popup menu...")
menu_handles = findwindows.find_windows(class_name="#32768")
print(f"Standard menu windows: {len(menu_handles)}")
for mh in menu_handles:
    print(f"  HWND={mh}")
    menu_win = Desktop(backend='uia').window(handle=mh)
    try:
        for item in menu_win.descendants(control_type="MenuItem"):
            name = item.window_text()
            print(f"    MenuItem: {repr(name)}")
    except Exception as e:
        print(f"  UIA descendants error: {e}")

# Also check all currently visible windows
print("\nAll current windows with titles:")
WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
buf = ctypes.create_unicode_buffer(256)
def _cb(hwnd, _):
    if ctypes.windll.user32.IsWindowVisible(hwnd):
        ctypes.windll.user32.GetWindowTextW(hwnd, buf, 256)
        if buf.value:
            print(f"  HWND={hwnd} title={repr(buf.value)}")
    return True
ctypes.windll.user32.EnumWindows(WNDENUMPROC(_cb), 0)

# Close menu with ESC
send_keys('{ESC}')
time.sleep(0.3)

# Check bottom buttons via coordinate click info
print("\nBottom action buttons (asCommandCtlClassU) from Win32 debug:")
print("  left=1105, mid_y=884 — could be 'Accept Payment' or 'Post'")
print("  left=805, mid_y=884")
print("  left=605, mid_y=884")
print("  left=475, mid_y=884")
print("  left=345, mid_y=884")

print("\nTrying to get UIA names for bottom panes (y>800)...")
try:
    for elem in ar_win.descendants():
        try:
            rect = elem.rectangle()
            if rect.top > 800:
                ct = elem.element_info.control_type
                name = elem.window_text()
                auto_id = elem.element_info.automation_id
                print(f"  ctrl={ct} name={repr(name)} auto_id={repr(auto_id)} left={rect.left} top={rect.top}")
        except Exception:
            pass
except Exception as e:
    print(f"Error: {e}")
