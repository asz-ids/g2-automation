"""
Try sending click notification TO the buttons themselves
"""
import pywinauto
from pywinauto import Application
import pywinauto.findwindows
import time
import ctypes
from ctypes import wintypes

try:
    windows = pywinauto.findwindows.find_windows(title_re='.*Navigator.*')
    app = Application(backend='win32').connect(handle=windows[0])
    nav = app.window(handle=windows[0])
    children = nav.children()
    
    print("[1] Reset to Sales view...")
    
    # Make sure we're in a known state
    SW_HIDE = 0
    SW_SHOW = 5
    
    for i in [15, 26, 27, 28, 29]:
        panel = children[i]
        hwnd = panel.handle
        if i == 15:  # Sales
            ctypes.windll.user32.ShowWindow(hwnd, SW_SHOW)
        else:
            ctypes.windll.user32.ShowWindow(hwnd, SW_HIDE)
    
    time.sleep(0.5)
    
    print("  Current state: Sales visible, others hidden")
    
    print("\n[2] Attempt different ways to activate Service button...")
    
    service_btn = children[19]  # Service button
    service_btn_handle = service_btn.handle
    parent = service_btn.parent()
    parent_handle = parent.handle
    
    print(f"  Service button: handle={service_btn_handle}")
    print(f"  Parent: handle={parent_handle}")
    
    # Method 1: Send WM_COMMAND to parent with button handle as control ID
    print("\n  Method 1: WM_COMMAND from parent")
    WM_COMMAND = 0x0111
    BN_CLICKED = 0
    wparam = (BN_CLICKED << 16) | service_btn_handle
    ctypes.windll.user32.SendMessageW(parent_handle, WM_COMMAND, wparam, service_btn_handle)
    time.sleep(0.5)
    
    service_visible = children[26].is_visible()
    print(f"    Service panel visible after: {service_visible}")
    
    print("\n  Method 2: WM_LBUTTONDOWN/UP on button itself")
    ctypes.windll.user32.SendMessageW(service_btn_handle, 0x0201, 0, 0)  # WM_LBUTTONDOWN
    time.sleep(0.1)
    ctypes.windll.user32.SendMessageW(service_btn_handle, 0x0202, 0, 0)  # WM_LBUTTONUP
    time.sleep(0.5)
    
    service_visible = children[26].is_visible()
    print(f"    Service panel visible after: {service_visible}")
    
    print("\n  Method 3: Send WM_SETFOCUS then WM_KEYDOWN/KEYUP for SPACE")
    ctypes.windll.user32.SendMessageW(service_btn_handle, 0x0007, 0, 0)  # WM_SETFOCUS
    time.sleep(0.1)
    ctypes.windll.user32.SendMessageW(service_btn_handle, 0x0100, 0x20, 0)  # WM_KEYDOWN (space)
    time.sleep(0.1)
    ctypes.windll.user32.SendMessageW(service_btn_handle, 0x0101, 0x20, 0)  # WM_KEYUP (space)
    time.sleep(0.5)
    
    service_visible = children[26].is_visible()
    print(f"    Service panel visible after: {service_visible}")
    
    print("\n  Method 4: Send UIA_INVOKE_PATTERN trigger")
    # This is harder without proper UIA handling, skip for now
    
    print("\n[3] Final state:")
    for i, label in enumerate(['Sales', 'Service', 'Accounting', 'Admin', 'Parts']):
        panel_idx = [15, 26, 29, 28, 27][i]
        panel = children[panel_idx]
        is_visible = panel.is_visible()
        status = "✓" if is_visible else "✗"
        print(f"    {status} {label:12s}")
    
except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
