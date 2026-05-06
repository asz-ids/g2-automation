"""
Send WM_COMMAND directly with button control ID
"""

from pywinauto import findwindows
from pywinauto.application import Application
from ctypes import windll, c_int
import time

print("[1] Getting button details...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()
nav_hwnd = nav_handles[0]

children = window.children()
btn_sales = None
btn_sales_id = None

for i, child in enumerate(children):
    try:
        props = child.get_properties()
        if props.get('automation_id') == 'btnSales':
            btn_sales = child
            btn_sales_id = props.get('control_id')
            print(f"    Found btnSales")
            print(f"    Control ID: {btn_sales_id}")
            print(f"    Handle: {btn_sales.handle}")
            break
    except:
        pass

if not btn_sales:
    print("[X] Button not found")
    exit(1)

print(f"\n[2] Sending WM_COMMAND with BN_CLICKED...")
try:
    WM_COMMAND = 273
    BN_CLICKED = 0
    
    # Send WM_COMMAND to Navigator window
    # wParam = (BN_CLICKED << 16) | control_id
    # lParam = button_hwnd
    
    wparam = (BN_CLICKED << 16) | btn_sales_id
    lparam = btn_sales.handle
    
    print(f"    WM_COMMAND with:")
    print(f"      wParam: {wparam:08x}")
    print(f"      lParam: {lparam}")
    
    windll.user32.SendMessageA(nav_hwnd, WM_COMMAND, wparam, lparam)
    print(f"    Message sent")
    time.sleep(3)
    
    # Check result
    app2 = Application(backend='win32').connect(handle=nav_handles[0])
    window2 = app2.top_window()
    print(f"    Children: {len(window2.children())}")
    
except Exception as e:
    print(f"    Error: {e}")
    import traceback
    traceback.print_exc()

print(f"\n[3] Trying with different wParam values...")
try:
    WM_COMMAND = 273
    
    # Try different notification codes
    for notif_code in [0, 1, 0x8001]:  # BN_CLICKED, BN_PAINT, etc
        print(f"    Trying notification code {notif_code}...")
        
        wparam = (notif_code << 16) | btn_sales_id
        lparam = btn_sales.handle
        
        windll.user32.SendMessageA(nav_hwnd, WM_COMMAND, wparam, lparam)
        time.sleep(1)
        
        app2 = Application(backend='win32').connect(handle=nav_handles[0])
        window2 = app2.top_window()
        if len(window2.children()) != 34:
            print(f"      ✓ SUCCESS!")
            exit(0)

except Exception as e:
    print(f"    Error: {e}")

print(f"\nNo WM_COMMAND approach worked.")
