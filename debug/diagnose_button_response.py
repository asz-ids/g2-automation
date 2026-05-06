"""
Diagnose why buttons aren't responding - check for event handlers
"""
import pywinauto
from pywinauto import Application
import time

try:
    # Try to find the navigator window with various title patterns
    import pywinauto.findwindows
    windows = pywinauto.findwindows.find_windows(title_re='.*Navigator.*')
    if not windows:
        print("Navigator window not found. Available windows:")
        all_wins = pywinauto.findwindows.find_windows()
        for w in all_wins[:10]:
            try:
                print(f"  - {w}")
            except:
                pass
        exit(1)
    
    app = Application(backend='uia').connect(handle=windows[0])
    navigator = app.window(handle=windows[0])
    
    print("[1] Getting Navigator window details...")
    print(f"    Window Handle: {navigator.handle}")
    print(f"    Children count: {len(navigator.children())}")
    
    print("\n[2] Finding btnSales...")
    children = navigator.children()
    for i, child in enumerate(children):
        try:
            if hasattr(child, 'automation_id') and child.automation_id == 'btnSales':
                print(f"    Found at index {i}")
                btn = child
                break
        except:
            pass
    else:
        print("    NOT FOUND")
        exit(1)
    
    print("\n[3] Checking button's window class and style...")
    print(f"    Class: {btn.class_name()}")
    print(f"    Window style: {btn.get_style()}")
    print(f"    Window ex-style: {btn.get_ex_style()}")
    
    print("\n[4] Checking if button has child windows...")
    try:
        btn_children = btn.children()
        print(f"    Button children count: {len(btn_children)}")
        for bc in btn_children:
            print(f"      - {bc.class_name()}")
    except Exception as e:
        print(f"    Error getting children: {e}")
    
    print("\n[5] Getting button's parent...")
    try:
        parent = btn.parent()
        print(f"    Parent class: {parent.class_name()}")
        print(f"    Parent children: {len(parent.children())}")
    except Exception as e:
        print(f"    Error: {e}")
    
    print("\n[6] Checking button's rect and visibility...")
    rect = btn.rectangle()
    print(f"    Rectangle: {rect}")
    print(f"    Width: {rect.width()}, Height: {rect.height()}")
    print(f"    Is visible: {btn.is_visible()}")
    print(f"    Is enabled: {btn.is_enabled()}")
    
    print("\n[7] Trying different interaction methods...")
    
    # Method 1: Move mouse to center and click
    center = rect.mid_point()
    print(f"    Center point: {center}")
    
    print("\n    Attempting: set_focus() then space bar...")
    btn.set_focus()
    time.sleep(0.5)
    btn.send_keystrokes(' ')
    time.sleep(0.5)
    children_after = len(navigator.children())
    print(f"    Children after: {children_after} (before was 34)")
    
    print("\n    Attempting: direct rectangle click...")
    pywinauto.mouse.click(button='left', coords=(center[0], center[1]))
    time.sleep(0.5)
    children_after = len(navigator.children())
    print(f"    Children after: {children_after} (before was 34)")
    
    print("\n[8] Checking for dialogs or hidden windows...")
    import pywinauto.findwindows
    all_windows = pywinauto.findwindows.find_windows()
    print(f"    Total windows on screen: {len(all_windows)}")
    for w in all_windows:
        if 'G2' in str(w) or 'Navigator' in str(w) or 'Sales' in str(w):
            print(f"      - {w}")
    
    print("\n[9] Checking button's notification context...")
    print(f"    Button text: '{btn.text()}'")
    print(f"    Button name: '{btn.name()}'")
    try:
        print(f"    Button friendly_class: {btn.friendly_class_name()}")
    except:
        pass
    
    print("\nDiagnosis complete.")

except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
