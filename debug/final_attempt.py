"""
Final attempt: Use UIA backend with proper element search
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time

print("[1] Try connecting with UIA backend specifically...")
try:
    nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
    
    # Try UIA backend
    app_uia = Application(backend='uia').connect(handle=nav_handles[0])
    window_uia = app_uia.top_window()
    
    print(f"    Connected with UIA")
    print(f"    Window name: {window_uia.name}")
    
    # Get children
    children = window_uia.children()
    print(f"    UIA children: {len(children)}")
    
    # Look for clickable elements
    for child in children:
        try:
            name = child.name if hasattr(child, 'name') else ""
            control_type = child.control_type if hasattr(child, 'control_type') else ""
            
            if 'sales' in name.lower() or 'sales' in str(control_type).lower():
                print(f"    Found: {name} ({control_type})")
        except:
            pass
    
except Exception as e:
    print(f"    UIA Error: {e}")
    import traceback
    traceback.print_exc()

print(f"\n[2] Last resort: Use win32 backend but try get_properties method...")
try:
    nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
    app = Application(backend='win32').connect(handle=nav_handles[0])
    window = app.top_window()
    
    children = window.children()
    for child in children:
        try:
            if child.window_text() == "Sales" and child.is_visible():
                print(f"    Found Sales button")
                print(f"    Getting properties...")
                
                props = child.get_properties()
                print(f"    Properties: {props}")
                
                # Check if there's something we can invoke
                if hasattr(child, 'GetWindowText'):
                    print(f"    Has GetWindowText")
                
                break
        except:
            pass

except Exception as e:
    print(f"    Error: {e}")

print(f"\n[3] Check if button has children that might be the actual clickable element...")
try:
    nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
    app = Application(backend='win32').connect(handle=nav_handles[0])
    window = app.top_window()
    
    children = window.children()
    for i, child in enumerate(children):
        try:
            if child.window_text() == "Sales" and child.is_visible():
                print(f"    Found Sales at index {i}")
                
                # Check for children
                try:
                    subchildren = child.children()
                    print(f"    Has {len(subchildren)} children")
                    
                    for j, subchild in enumerate(subchildren):
                        print(f"      [{j}] {subchild.window_text()[:30] if subchild.window_text() else '[empty]'}")
                        
                        # Try clicking on each child
                        try:
                            print(f"          Trying to click...")
                            subchild.click()
                            time.sleep(2)
                            
                            nav_handles2 = findwindows.find_windows(title_re=".*Navigator.*")
                            app2 = Application(backend='win32').connect(handle=nav_handles2[0])
                            window2 = app2.top_window()
                            new_children = len(window2.children())
                            
                            if new_children > 34:
                                print(f"          ✓ SUCCESS! Children: {new_children}")
                                exit(0)
                        except:
                            pass
                except:
                    print(f"    No children")
                
                break
        except:
            pass

except Exception as e:
    print(f"    Error: {e}")
    import traceback
    traceback.print_exc()

print(f"\nNo solution found.")
