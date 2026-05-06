"""
Click Sales button using Win32 backend with proper method calling
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
    children = nav.children()
    
    print("\n[2] Looking for btnSales (handle 398226)...")
    btn_sales = None
    for i, child in enumerate(children):
        try:
            if hasattr(child, 'handle') and child.handle == 398226:
                print(f"    Found at index {i}")
                print(f"    Text: {child.text() if hasattr(child, 'text') else 'N/A'}")
                print(f"    Rectangle: {child.rectangle()}")
                print(f"    Enabled: {child.is_enabled()}")
                print(f"    Visible: {child.is_visible()}")
                btn_sales = child
                break
        except Exception as e:
            pass
    
    if not btn_sales:
        print("    NOT FOUND")
        exit(1)
    
    print("\n[3] Before click - Navigator children:", len(nav.children()))
    
    print("\n[4] Clicking with different methods...")
    
    # Method 1: Basic click
    print("\n    Method 1: click()")
    btn_sales.click()
    time.sleep(0.5)
    print(f"    Result: {len(nav.children())} children")
    
    # Method 2: click_input
    print("\n    Method 2: click_input()")
    btn_sales.click_input()
    time.sleep(0.5)
    print(f"    Result: {len(nav.children())} children")
    
    # Method 3: Double-click
    print("\n    Method 3: double_click()")
    btn_sales.double_click()
    time.sleep(0.5)
    print(f"    Result: {len(nav.children())} children")
    
    # Method 4: Set focus and send key
    print("\n    Method 4: set_focus() + Space")
    btn_sales.set_focus()
    time.sleep(0.3)
    btn_sales.send_keystrokes(' ')
    time.sleep(0.5)
    print(f"    Result: {len(nav.children())} children")
    
    # Method 5: Raw mouse coordinates
    print("\n    Method 5: pywinauto.mouse.click")
    rect = btn_sales.rectangle()
    center = (rect.left + (rect.right - rect.left) // 2, rect.top + (rect.bottom - rect.top) // 2)
    print(f"    Clicking at {center}")
    pywinauto.mouse.click(coords=center)
    time.sleep(0.5)
    print(f"    Result: {len(nav.children())} children")
    
    print("\n[5] CRITICAL: Checking if anything changed...")
    print("    Same number of children = No response to any click method")
    
except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
