"""Debug: use UIA to enumerate AR Payment window controls."""
import ctypes
import ctypes.wintypes
from pywinauto import findwindows, Desktop

handles = findwindows.find_windows(title_re=".*Accounts Receivable.*")
if not handles:
    handles = findwindows.find_windows(title_re=".*Payment.*")
if not handles:
    handles = findwindows.find_windows(title_re=".*SMC.*")

if not handles:
    print("ERROR: AR Payment window not found — open it first")
    exit(1)

ar_hwnd = handles[0]
print(f"AR window HWND: {ar_hwnd}")

ar_win = Desktop(backend='uia').window(handle=ar_hwnd)

print("\n--- UIA descendants (all) ---")
try:
    for elem in ar_win.descendants():
        try:
            name = elem.window_text()
            ctrl_type = elem.element_info.control_type
            auto_id = elem.element_info.automation_id
            rect = elem.rectangle()
            mid_y = (rect.top + rect.bottom) // 2
            if name or auto_id:
                print(f"  ctrl={ctrl_type:<20} name={repr(name):<40} auto_id={repr(auto_id):<20} mid_y={mid_y} left={rect.left}")
        except Exception:
            pass
except Exception as e:
    print(f"Error: {e}")

print("\n--- Edit/Custom controls near top of form ---")
try:
    for elem in ar_win.descendants():
        try:
            ctrl_type = elem.element_info.control_type
            rect = elem.rectangle()
            if ctrl_type in ('Edit', 'Custom') and rect.top < 250:
                name = elem.window_text()
                auto_id = elem.element_info.automation_id
                mid_y = (rect.top + rect.bottom) // 2
                print(f"  ctrl={ctrl_type:<20} name={repr(name):<40} auto_id={repr(auto_id):<20} top={rect.top} mid_y={mid_y} left={rect.left}")
        except Exception:
            pass
except Exception as e:
    print(f"Error: {e}")
