"""
Try making hidden panels visible (toggle visibility)
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
    
    print("[1] Listing all visible and hidden panels...")
    
    panels = {}
    for i, child in enumerate(children):
        try:
            texts = child.texts() if hasattr(child, 'texts') else []
            if texts and texts[0] in ['Sales', 'Service', 'Accounting', 'Admin', 'Parts']:
                vis = child.is_visible() if hasattr(child, 'is_visible') else None
                
                label = texts[0]
                if label not in panels:
                    panels[label] = []
                
                rect = child.rectangle()
                size = (rect.right - rect.left, rect.bottom - rect.top)
                
                panels[label].append({
                    'idx': i,
                    'visible': vis,
                    'size': size,
                    'class': child.class_name(),
                })
                
                print(f"    [{i:2d}] {label:12s} visible={vis:5} size={size}")
        except:
            pass
    
    print("\n[2] Identified panel structure:")
    for label, items in panels.items():
        print(f"  {label}:")
        for item in items:
            print(f"    - Index {item['idx']}: visible={item['visible']}, size={item['size']}")
    
    print("\n[3] The LARGE content areas are likely at indices:")
    large_panels = {}
    for i, child in enumerate(children):
        try:
            rect = child.rectangle()
            width = rect.right - rect.left
            height = rect.bottom - rect.top
            
            if width > 1000 and height > 100:
                texts = child.texts() if hasattr(child, 'texts') else []
                label = texts[0] if texts and texts[0] else f"UnnamedPanel[{i}]"
                vis = child.is_visible() if hasattr(child, 'is_visible') else None
                
                large_panels[label] = {
                    'idx': i,
                    'visible': vis,
                    'size': (width, height),
                }
                
                print(f"    [{i:2d}] {label:12s} visible={vis} size=({width},{height})")
        except:
            pass
    
    print("\n[4] THEORY: Hidden panels need to be made visible")
    print("    Attempting to toggle visibility on hidden Service/Parts/Admin/Accounting panels...")
    
    # Find the hidden panels and try to show them
    for i, child in enumerate(children):
        try:
            texts = child.texts() if hasattr(child, 'texts') else []
            if texts and texts[0] in ['Service', 'Parts', 'Admin', 'Accounting']:
                vis = child.is_visible() if hasattr(child, 'is_visible') else None
                
                if vis == False:
                    print(f"\n    Found hidden '{texts[0]}' panel at index {i}")
                    print(f"    Attempting to show it...")
                    
                    # Try different methods to show
                    try:
                        # Method 1: Direct click
                        child.click()
                        time.sleep(0.5)
                        
                        new_vis = child.is_visible() if hasattr(child, 'is_visible') else None
                        print(f"      After click(): visible={new_vis}")
                    except Exception as e:
                        print(f"      click() failed: {e}")
        except:
            pass
    
    print("\n[5] Checking state now...")
    for i, child in enumerate(children):
        try:
            texts = child.texts() if hasattr(child, 'texts') else []
            if texts and texts[0] in ['Service', 'Parts', 'Admin', 'Accounting', 'Sales']:
                vis = child.is_visible() if hasattr(child, 'is_visible') else None
                print(f"    [{i:2d}] {texts[0]:12s} visible={vis}")
        except:
            pass
    
    print("\n[6] Now try clicking the SALES button again...")
    
    # Find btnSales
    btn_sales = None
    for child in children:
        try:
            if hasattr(child, 'handle') and child.handle == 398226:
                btn_sales = child
                break
        except:
            pass
    
    if btn_sales:
        print("    Clicking btnSales...")
        btn_sales.click()
        time.sleep(1)
        
        print("    Checking if any panels became visible/changed...")
        for i, child in enumerate(children):
            try:
                texts = child.texts() if hasattr(child, 'texts') else []
                if texts and texts[0] in ['Service', 'Parts', 'Admin', 'Accounting', 'Sales']:
                    vis = child.is_visible() if hasattr(child, 'is_visible') else None
                    print(f"      [{i:2d}] {texts[0]:12s} visible={vis}")
            except:
                pass

except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
