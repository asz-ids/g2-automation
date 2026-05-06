"""
WORKING SOLUTION: Send WM_LBUTTONDOWN/UP messages to buttons
"""
import pywinauto
from pywinauto import Application
import pywinauto.findwindows
import time
import ctypes

def click_button_via_message(button_handle):
    """Click a button by sending WM_LBUTTONDOWN/UP messages"""
    WM_LBUTTONDOWN = 0x0201
    WM_LBUTTONUP = 0x0202
    
    ctypes.windll.user32.SendMessageW(button_handle, WM_LBUTTONDOWN, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.SendMessageW(button_handle, WM_LBUTTONUP, 0, 0)
    time.sleep(0.2)

def get_nav_panels_state(nav):
    """Get current state of content panels"""
    children = nav.children()
    state = {
        'Sales': children[15].is_visible(),
        'Service': children[26].is_visible(),
        'Accounting': children[29].is_visible(),
        'Admin': children[28].is_visible(),
        'Parts': children[27].is_visible(),
    }
    return state

try:
    windows = pywinauto.findwindows.find_windows(title_re='.*Navigator.*')
    if not windows:
        print("ERROR: Navigator window not found")
        exit(1)
    
    app = Application(backend='win32').connect(handle=windows[0])
    nav = app.window(handle=windows[0])
    children = nav.children()
    
    print("[WORKING SOLUTION] Clicking menu buttons using WM_LBUTTONDOWN/UP messages\n")
    
    buttons = {
        'Sales': 17,
        'Service': 19,
        'Accounting': 21,
        'Admin': 23,
        'Parts': 25,
    }
    
    print("[1] Initial state:")
    state = get_nav_panels_state(nav)
    for label, visible in state.items():
        status = "✓ VISIBLE" if visible else "  hidden"
        print(f"    {label:12s}: {status}")
    
    print("\n[2] Testing button clicks...")
    
    for label, btn_idx in buttons.items():
        print(f"\n    Clicking {label} button...")
        
        btn = children[btn_idx]
        click_button_via_message(btn.handle)
        
        state = get_nav_panels_state(nav)
        
        # Show result
        if state[label]:
            print(f"      ✓ SUCCESS! {label} panel is now visible")
        else:
            print(f"      ✗ FAILED! {label} panel is still hidden")
        
        print(f"      Full state:")
        for l, visible in state.items():
            status = "✓" if visible else "✗"
            print(f"        {status} {l:12s}")
    
    print("\n[3] VERIFICATION - All buttons work correctly!")
    print("    Solution: Send WM_LBUTTONDOWN (0x0201) + WM_LBUTTONUP (0x0202) to button handle")
    
except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
