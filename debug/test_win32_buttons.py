"""
Find and test buttons using Win32 backend
"""
import pywinauto
from pywinauto import Application
import pywinauto.findwindows
import time

try:
    windows = pywinauto.findwindows.find_windows(title_re='.*Navigator.*')
    if not windows:
        print("Navigator window not found.")
        exit(1)
    
    # Use Win32 backend
    app = Application(backend='win32').connect(handle=windows[0])
    nav = app.window(handle=windows[0])
    
    print(f"[1] Total children: {len(nav.children())}")
    
    print("\n[2] Looking for buttons...")
    children = nav.children()
    for i, child in enumerate(children):
        try:
            # Try to get automation_id
            auto_id = None
            if hasattr(child, 'automation_id'):
                auto_id = child.automation_id
            
            if auto_id and 'btn' in auto_id.lower():
                print(f"    [{i}] {child.class_name()} - automation_id: {auto_id}")
                print(f"        Rectangle: {child.rectangle()}")
                print(f"        Enabled: {child.is_enabled()}")
                print(f"        Visible: {child.is_visible()}")
        except Exception as e:
            pass
    
    print("\n[3] Listing all children with details...")
    for i, child in enumerate(children):
        try:
            auto_id = child.automation_id if hasattr(child, 'automation_id') else ''
            visible = child.is_visible() if hasattr(child, 'is_visible') else '?'
            enabled = child.is_enabled() if hasattr(child, 'is_enabled') else '?'
            print(f"    [{i:2d}] {child.class_name():50s} auto_id: {str(auto_id):20s} v:{visible} e:{enabled}")
        except Exception as e:
            print(f"    [{i:2d}] Error: {e}")
    
    print("\n[4] Testing btnSales click (index should be around 17-25)...")
    # Try indices 15-30
    for idx in range(15, 31):
        if idx < len(children):
            try:
                child = children[idx]
                auto_id = child.automation_id if hasattr(child, 'automation_id') else ''
                if auto_id and 'btnSales' in str(auto_id):
                    print(f"\n    Found btnSales at index {idx}")
                    print(f"    Clicking...")
                    child.click()
                    time.sleep(1)
                    nav_children_after = len(nav.children())
                    print(f"    Navigator children after click: {nav_children_after}")
                    break
            except Exception as e:
                pass

except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
