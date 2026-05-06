"""
Check if these are Infragistics or custom painted controls
"""
import pywinauto
from pywinauto import Application
import pywinauto.findwindows

try:
    windows = pywinauto.findwindows.find_windows(title_re='.*Navigator.*')
    app = Application(backend='uia').connect(handle=windows[0])
    nav = app.window(handle=windows[0])
    
    print("[1] Navigator children via UIA...")
    children = nav.children()
    print(f"    Total: {len(children)}")
    
    for i, child in enumerate(children[:10]):
        try:
            control_type = child.control_type() if hasattr(child, 'control_type') else 'Unknown'
            name = child.name if hasattr(child, 'name') else 'N/A'
            print(f"    [{i}] {control_type}: {name}")
        except Exception as e:
            print(f"    [{i}] Error: {e}")
    
    print("\n[2] Looking for interactive elements in UIA tree...")
    def explore_uia(elem, depth=0, max_depth=4):
        if depth > max_depth:
            return
        try:
            for child in elem.children():
                control_type = child.control_type() if hasattr(child, 'control_type') else 'Unknown'
                try:
                    name = child.name
                except:
                    name = 'N/A'
                
                # Look for buttons or clickable elements
                if 'Button' in str(control_type) or 'Invoke' in str(child):
                    print(f"  {'  '*depth}[{depth}] {control_type}: {name}")
                
                explore_uia(child, depth + 1, max_depth)
        except:
            pass
    
    explore_uia(nav)
    
    print("\n[3] Looking at Win32 explorer_bar or toolbar controls...")
    app_win32 = Application(backend='win32').connect(handle=windows[0])
    nav_win32 = app_win32.window(handle=windows[0])
    children_win32 = nav_win32.children()
    
    # Look for "ultraExplorerBar" or toolbar-like classes
    for i, child in enumerate(children_win32):
        class_name = child.class_name()
        if 'ExplorerBar' in class_name or 'ToolBar' in class_name or 'Bar' in class_name:
            print(f"    [{i}] {class_name}")
    
    print("\n[4] Checking all window class names for patterns...")
    for i, child in enumerate(children_win32):
        class_name = child.class_name()
        if 'ultraControls' in class_name.lower() or 'infragistics' in class_name.lower():
            print(f"    [{i}] {class_name}")
    
    print("\n[5] Try UIA Invoke pattern on elements containing 'Sales'...")
    def find_and_invoke(elem, target='Sales', depth=0, max_depth=6):
        if depth > max_depth:
            return False
        try:
            for child in elem.children():
                try:
                    name = child.name if hasattr(child, 'name') else ''
                except:
                    name = ''
                
                if target in str(name):
                    print(f"  {'  '*depth}Found '{name}'")
                    # Try to invoke if it has invoke pattern
                    try:
                        if hasattr(child, 'invoke'):
                            print(f"  {'  '*depth}  -> Has invoke pattern, calling...")
                            child.invoke()
                            return True
                    except Exception as e:
                        print(f"  {'  '*depth}  -> Invoke failed: {e}")
                
                if find_and_invoke(child, target, depth + 1, max_depth):
                    return True
        except:
            pass
        return False
    
    find_and_invoke(nav, 'Sales')
    
except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
