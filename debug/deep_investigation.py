"""
Deep investigation - check what type of controls these actually are
"""
import pywinauto
from pywinauto import Application
import pywinauto.findwindows
import ctypes
from ctypes import wintypes

try:
    windows = pywinauto.findwindows.find_windows(title_re='.*Navigator.*')
    if not windows:
        print("Navigator window not found.")
        exit(1)
    
    app = Application(backend='win32').connect(handle=windows[0])
    nav = app.window(handle=windows[0])
    children = nav.children()
    
    # Find btnSales
    btn_sales = None
    for child in children:
        try:
            if hasattr(child, 'handle') and child.handle == 398226:
                btn_sales = child
                break
        except:
            pass
    
    if not btn_sales:
        print("btnSales not found")
        exit(1)
    
    print("[1] Basic properties...")
    print(f"    Handle: {btn_sales.handle}")
    print(f"    Class: {btn_sales.class_name()}")
    print(f"    Text: {btn_sales.texts() if hasattr(btn_sales, 'texts') else 'N/A'}")
    print(f"    Rectangle: {btn_sales.rectangle()}")
    
    print("\n[2] Window style and ex-style...")
    style = btn_sales.style if hasattr(btn_sales, 'style') else btn_sales.get_properties().get('style', 0)
    ex_style = btn_sales.exstyle if hasattr(btn_sales, 'exstyle') else btn_sales.get_properties().get('exstyle', 0)
    print(f"    Style: {style} (0x{style:08X})")
    print(f"    Ex-style: {ex_style} (0x{ex_style:08X})")
    
    # Common styles
    WS_CHILD = 0x40000000
    WS_VISIBLE = 0x10000000
    WS_DISABLED = 0x08000000
    WS_TABSTOP = 0x00010000
    WS_GROUP = 0x00020000
    
    print(f"\n    WS_CHILD: {bool(style & WS_CHILD)}")
    print(f"    WS_VISIBLE: {bool(style & WS_VISIBLE)}")
    print(f"    WS_DISABLED: {bool(style & WS_DISABLED)}")
    print(f"    WS_TABSTOP: {bool(style & WS_TABSTOP)}")
    print(f"    WS_GROUP: {bool(style & WS_GROUP)}")
    
    print("\n[3] Checking parent...")
    try:
        parent = btn_sales.parent()
        print(f"    Parent class: {parent.class_name()}")
        print(f"    Parent children: {len(parent.children())}")
        print(f"    Parent handle: {parent.handle}")
    except Exception as e:
        print(f"    Error: {e}")
    
    print("\n[4] Trying parent message sending...")
    # Get parent window
    parent_handle = ctypes.windll.user32.GetParent(btn_sales.handle)
    print(f"    Parent handle (from GetParent): {parent_handle}")
    
    # Send WM_COMMAND to parent with button's control ID
    WM_COMMAND = 0x0111
    control_id = btn_sales.handle  # Using handle as control ID
    notification_code = 0  # BN_CLICKED
    lparam = btn_sales.handle
    wparam = (notification_code << 16) | control_id
    
    print(f"\n    Sending WM_COMMAND to parent...")
    print(f"    Parent: {parent_handle}")
    print(f"    wParam: {wparam} (0x{wparam:08X})")
    print(f"    lParam: {lparam}")
    
    result = ctypes.windll.user32.SendMessageW(parent_handle, WM_COMMAND, wparam, lparam)
    print(f"    Result: {result}")
    
    import time
    time.sleep(0.5)
    print(f"    Navigator children now: {len(nav.children())}")
    
    print("\n[5] Trying WM_COMMAND with zero control ID...")
    wparam2 = 0  # Zero control ID
    result2 = ctypes.windll.user32.SendMessageW(parent_handle, WM_COMMAND, wparam2, lparam)
    print(f"    Result: {result2}")
    time.sleep(0.5)
    print(f"    Navigator children now: {len(nav.children())}")
    
    print("\n[6] Trying WM_COMMAND with different notification codes...")
    for notif_code in [0, 1, 256, 1024]:
        wparam = (notif_code << 16) | control_id
        print(f"    Trying notification code {notif_code}...")
        ctypes.windll.user32.SendMessageW(parent_handle, WM_COMMAND, wparam, lparam)
        time.sleep(0.3)
    
    print(f"    Navigator children now: {len(nav.children())}")
    
    print("\n[7] Check if Navigator's child count ever changes...")
    # Try clicking the parent instead
    print("    Clicking the parent element...")
    parent_elem = btn_sales.parent()
    parent_elem.click()
    time.sleep(0.5)
    print(f"    Navigator children now: {len(nav.children())}")
    
except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
