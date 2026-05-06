"""
Explore the Navigator window structure with UIA backend
"""
import pywinauto
from pywinauto import Application
import pywinauto.findwindows

try:
    windows = pywinauto.findwindows.find_windows(title_re='.*Navigator.*')
    if not windows:
        print("Navigator window not found.")
        exit(1)
    
    print(f"Found {len(windows)} Navigator window(s)")
    
    # Try UIA backend
    print("\n[UIA Backend]")
    app_uia = Application(backend='uia').connect(handle=windows[0])
    nav_uia = app_uia.window(handle=windows[0])
    print(f"  Handle: {nav_uia.handle}")
    print(f"  Title: {nav_uia.title}")
    print(f"  Children: {len(nav_uia.children())}")
    
    for i, child in enumerate(nav_uia.children()):
        try:
            name = child.name() if hasattr(child, 'name') else 'N/A'
        except:
            name = 'N/A'
        print(f"    [{i}] {child.class_name()} - {name}")
        if hasattr(child, 'automation_id'):
            try:
                print(f"        automation_id: {child.automation_id}")
            except:
                pass
    
    # Try Win32 backend
    print("\n[Win32 Backend]")
    app_win32 = Application(backend='win32').connect(handle=windows[0])
    nav_win32 = app_win32.window(handle=windows[0])
    print(f"  Handle: {nav_win32.handle}")
    print(f"  Title: {nav_win32.title}")
    print(f"  Children: {len(nav_win32.children())}")
    
    for i, child in enumerate(nav_win32.children()[:10]):  # Limit to first 10
        print(f"    [{i}] {child.class_name()}")
        if 'btn' in child.class_name().lower() or 'Sales' in str(child):
            print(f"        -> This could be a button!")
    
    # Look deeper
    print("\n[Looking for buttons in Win32 descendants]")
    def find_buttons(element, depth=0, max_depth=5):
        if depth > max_depth:
            return
        try:
            for child in element.children():
                class_name = child.class_name()
                try:
                    auto_id = child.automation_id if hasattr(child, 'automation_id') else 'N/A'
                except:
                    auto_id = 'N/A'
                
                if 'Sales' in str(child) or 'btn' in auto_id.lower():
                    print(f"  {'  '*depth}[{depth}] {class_name} - automation_id: {auto_id}")
                
                find_buttons(child, depth + 1, max_depth)
        except:
            pass
    
    find_buttons(nav_win32)
    
except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
