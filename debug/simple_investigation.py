"""
Simple investigation - find what makes these buttons work
"""
import pywinauto
from pywinauto import Application
import pywinauto.findwindows
import time

try:
    windows = pywinauto.findwindows.find_windows(title_re='.*Navigator.*')
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
    
    print("[1] Button properties...")
    props = btn_sales.get_properties() if hasattr(btn_sales, 'get_properties') else {}
    for key, value in props.items():
        if key not in ['rect', 'fonts']:  # Skip verbose ones
            print(f"    {key}: {value}")
    
    print("\n[2] Parent chain...")
    current = btn_sales
    depth = 0
    while current and depth < 5:
        try:
            parent = current.parent()
            if parent:
                print(f"    [Level {depth}] {parent.class_name()} - title: '{parent.texts() if hasattr(parent, 'texts') else 'N/A'}'")
                current = parent
                depth += 1
            else:
                break
        except:
            break
    
    print("\n[3] Checking if button responds to ANY event...")
    print("    Monitoring window for any changes...")
    
    initial_children = len(nav.children())
    print(f"    Initial Navigator children: {initial_children}")
    
    # Try the ultimate click
    print("\n    Attempting: Focus + Left Mouse Button (raw)...")
    btn_sales.set_focus()
    time.sleep(0.2)
    
    import ctypes
    # Simulate left mouse button down and up at button center
    rect = btn_sales.rectangle()
    x = rect.left + (rect.right - rect.left) // 2
    y = rect.top + (rect.bottom - rect.top) // 2
    
    # Move mouse and click
    import ctypes.wintypes as wt
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(0.1)
    ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)  # Left down
    time.sleep(0.05)
    ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)  # Left up
    time.sleep(0.5)
    
    print(f"    Navigator children after: {len(nav.children())}")
    
    if len(nav.children()) != initial_children:
        print("\n    SUCCESS! Button responded!")
    else:
        print("\n    Button still doesn't respond - checking if there's a timeout or delayed event...")
        time.sleep(2)
        print(f"    Navigator children after 2sec: {len(nav.children())}")
    
    print("\n[4] Last resort - try to find what ELSE in Navigator responds to clicks...")
    print("    Testing different indices...")
    for idx in [0, 1, 2, 11, 12]:
        try:
            test_child = children[idx]
            test_child.click()
            time.sleep(0.3)
            if len(nav.children()) != initial_children:
                print(f"    Index {idx} caused change! ({test_child.class_name()})")
        except:
            pass
    
except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
