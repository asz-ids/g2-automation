"""Debug: inspect table rows in the AR Payment window when customer 4268 is loaded."""
import ctypes.wintypes
from pywinauto import findwindows, Desktop

handles = findwindows.find_windows(title_re=".*Accounts Receivable.*")
if not handles:
    print("ERROR: AR Payment window not found — run the workflow to step 5 first")
    exit(1)

ar_hwnd = handles[0]
ar_win = Desktop(backend='uia').window(handle=ar_hwnd)

print("--- Table structure ---")
try:
    table = ar_win.child_window(control_type="Table")
    tbl_rect = table.rectangle()
    print(f"Table rect: top={tbl_rect.top} left={tbl_rect.left} right={tbl_rect.right} bottom={tbl_rect.bottom}")

    for child in table.children():
        try:
            name = child.window_text()
            ct = child.element_info.control_type
            rect = child.rectangle()
            print(f"  child ctrl={ct} name={repr(name)} top={rect.top} left={rect.left}")

            for subchild in child.children():
                try:
                    sname = subchild.window_text()
                    sct = subchild.element_info.control_type
                    srect = subchild.rectangle()
                    print(f"    sub ctrl={sct} name={repr(sname)} top={srect.top} left={srect.left}")
                except Exception:
                    pass
        except Exception:
            pass
except Exception as e:
    print(f"Error: {e}")

print("\n--- All descendants with name ---")
try:
    for elem in ar_win.descendants():
        try:
            name = elem.window_text()
            ct = elem.element_info.control_type
            rect = elem.rectangle()
            if name and ct not in ('MenuItem', 'MenuBar', 'Button', 'Text'):
                print(f"  ctrl={ct:<20} name={repr(name):<50} top={rect.top} left={rect.left}")
        except Exception:
            pass
except Exception as e:
    print(f"Error: {e}")

print("\n--- Functions menu items ---")
try:
    fn_menu = ar_win.child_window(title="Functions", control_type="MenuItem")
    fn_menu.click_input()
    import time; time.sleep(0.5)
    d = Desktop(backend='uia')
    for item in d.descendants(control_type="MenuItem"):
        try:
            name = item.window_text()
            if name:
                print(f"  MenuItem: {repr(name)}")
        except Exception:
            pass
    import pywinauto.keyboard as kb
    kb.send_keys('{ESC}')
except Exception as e:
    print(f"Error accessing Functions menu: {e}")
