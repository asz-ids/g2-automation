"""
Reverse engineer what message/event triggers panel switching
"""
import pywinauto
from pywinauto import Application
import pywinauto.findwindows
import time
import ctypes

try:
    windows = pywinauto.findwindows.find_windows(title_re='.*Navigator.*')
    app = Application(backend='win32').connect(handle=windows[0])
    nav = app.window(handle=windows[0])
    children = nav.children()
    
    print("[1] Button and panel info...")
    buttons = {
        'Sales': {'idx': 17, 'handle': 398226},
        'Service': {'idx': 19, 'handle': 332738},
        'Accounting': {'idx': 21, 'handle': 2560478},
        'Admin': {'idx': 23, 'handle': 9178540},
        'Parts': {'idx': 25, 'handle': 463506},
    }
    
    panels = {
        'Sales': 15,
        'Service': 26,
        'Accounting': 29,
        'Admin': 28,
        'Parts': 27,
    }
    
    print("  Buttons:")
    for label, info in buttons.items():
        btn = children[info['idx']]
        print(f"    {label:12s} button[{info['idx']}] handle={btn.handle}")
    
    print("  Panels:")
    for label, idx in panels.items():
        panel = children[idx]
        print(f"    {label:12s} panel[{idx}] handle={panel.handle}")
    
    print("\n[2] Method 1: Send WM_COMMAND from Navigator to itself...")
    
    nav_handle = nav.handle
    
    # Try sending WM_COMMAND for each button
    WM_COMMAND = 0x0111
    
    for label, info in buttons.items():
        print(f"\n    Testing {label}...")
        
        # Try different notification codes
        for notif_code in [0, 1, 256]:  # BN_CLICKED, BN_PAINT, etc.
            wparam = (notif_code << 16) | info['handle']
            lparam = info['handle']
            
            print(f"      Sending WM_COMMAND with notif_code={notif_code}...")
            result = ctypes.windll.user32.SendMessageW(nav_handle, WM_COMMAND, wparam, lparam)
            
            time.sleep(0.3)
            
            # Check if panel changed
            sales_visible = children[15].is_visible()
            service_visible = children[26].is_visible()
            
            if label == 'Service' and service_visible and not sales_visible:
                print(f"      ✓ SUCCESS! Service panel is now visible!")
                break
            elif label == 'Sales' and sales_visible and not service_visible:
                print(f"      ✓ SUCCESS! Sales panel is now visible!")
                break
    
    print("\n[3] Checking final state...")
    for label, idx in panels.items():
        panel = children[idx]
        is_visible = panel.is_visible()
        status = "✓ VISIBLE" if is_visible else "  hidden"
        print(f"    {label:12s}: {status}")
    
    print("\n[4] Conclusion: What's needed to make buttons work?")
    print("    The buttons are custom controls that need:")
    print("    - Proper event routing/sink")
    print("    - Or specific window message handling")
    print("    - Or COM interface implementation")
    print("\n    WORKAROUND: We CAN manually switch panels using ShowWindow API")
    print("    This effectively 'simulates' button clicks!")

except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
