"""
Debug: Verify button handles and test one button click carefully
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
    
    print("[1] Finding and logging all button handles...")
    
    # Scan for automation_id containing 'btn'
    buttons = {}
    for i, child in enumerate(children):
        try:
            # Call automation_id as a method if it's a method
            if hasattr(child, 'automation_id'):
                auto_id_prop = child.automation_id
                # It might be a method or property
                if callable(auto_id_prop):
                    auto_id = auto_id_prop()
                else:
                    auto_id = auto_id_prop
            else:
                auto_id = None
            
            if auto_id and 'btn' in auto_id.lower():
                handle = child.handle if hasattr(child, 'handle') else None
                class_name = child.class_name()
                print(f"    [{i:2d}] {auto_id:20s} handle={handle:10d} class={class_name}")
                buttons[auto_id] = {'idx': i, 'handle': handle}
        except:
            pass
    
    print(f"\n  Found {len(buttons)} buttons")
    
    print("\n[2] Panel handles...")
    panels = {}
    for label, idx in [('Sales', 15), ('Service', 26), ('Accounting', 29), ('Admin', 28), ('Parts', 27)]:
        panel = children[idx]
        handle = panel.handle if hasattr(panel, 'handle') else None
        is_visible = panel.is_visible() if hasattr(panel, 'is_visible') else None
        print(f"    {label:12s} handle={handle:10d} visible={is_visible}")
        panels[label] = {'idx': idx, 'handle': handle}
    
    print("\n[3] Initial state - showing current content panel...")
    for label, idx in [('Sales', 15), ('Service', 26), ('Accounting', 29), ('Admin', 28), ('Parts', 27)]:
        is_visible = children[idx].is_visible()
        if is_visible:
            print(f"    Currently showing: {label}")
    
    print("\n[4] Carefully clicking Service button...")
    print("    Step 1: Get Service button")
    
    service_btn_info = buttons.get('btnService')
    if not service_btn_info:
        print("    ERROR: btnService not found!")
        print("    Available buttons:", list(buttons.keys()))
        exit(1)
    
    service_btn_idx = service_btn_info['idx']
    service_btn_handle = service_btn_info['handle']
    service_btn = children[service_btn_idx]
    
    print(f"      Index: {service_btn_idx}")
    print(f"      Handle: {service_btn_handle}")
    print(f"      Class: {service_btn.class_name()}")
    
    print("\n    Step 2: Send WM_LBUTTONDOWN to handle {service_btn_handle}")
    WM_LBUTTONDOWN = 0x0201
    WM_LBUTTONUP = 0x0202
    
    result1 = ctypes.windll.user32.SendMessageW(service_btn_handle, WM_LBUTTONDOWN, 0, 0)
    print(f"      Result: {result1}")
    
    time.sleep(0.1)
    
    print(f"\n    Step 3: Send WM_LBUTTONUP")
    result2 = ctypes.windll.user32.SendMessageW(service_btn_handle, WM_LBUTTONUP, 0, 0)
    print(f"      Result: {result2}")
    
    time.sleep(0.5)
    
    print("\n    Step 4: Check which panel is visible")
    for label, idx in [('Sales', 15), ('Service', 26), ('Accounting', 29), ('Admin', 28), ('Parts', 27)]:
        panel = children[idx]
        is_visible = panel.is_visible()
        # Need to refresh from app
        try:
            # Reconnect to get fresh state
            app2 = Application(backend='win32').connect(handle=windows[0])
            nav2 = app2.window(handle=windows[0])
            children2 = nav2.children()
            panel2 = children2[idx]
            is_visible2 = panel2.is_visible()
            print(f"      {label:12s}: {is_visible2}")
        except:
            print(f"      {label:12s}: {is_visible}")

except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
