"""
Analyze button structure - are these actual buttons or labels?
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time
import warnings
warnings.filterwarnings('ignore')

print("[1] Connecting to Navigator...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()

print("\n[2] Analyzing button structure...")
children = window.children()

# Find all "Sales" related elements
print("\nAll 'Sales' elements:")
sales_elements = []
for i, child in enumerate(children):
    try:
        if child.window_text() == "Sales":
            sales_elements.append((i, child))
            cls = child.class_name()
            print(f"  [{i}] Class: {cls}")
            print(f"      Enabled: {child.is_enabled()}")
            print(f"      Visible: {child.is_visible()}")
            
            # Check if it has children (might be a container)
            try:
                subchildren = child.children()
                print(f"      Children: {len(subchildren)}")
                for j, sub in enumerate(subchildren):
                    print(f"        [{j}] {sub.window_text()} ({sub.class_name()})")
            except:
                print(f"      No children")
            
            print()
    except Exception as e:
        print(f"  Error on [{i}]: {e}")

if sales_elements:
    print(f"[3] Testing different interaction methods on first Sales element...")
    idx, sales = sales_elements[0]
    
    # Try get_properties for special methods
    print(f"\n    Looking for special properties...")
    try:
        # Check if it's a real button with invoke pattern
        print(f"    Trying click_input()...")
        sales.click_input()
        print(f"      ✓ click_input executed")
        time.sleep(2)
    except Exception as e:
        print(f"      [X] click_input failed: {e}")
    
    # Check MDI after click_input
    try:
        mdi = window.children()[27]  # MDI client index
        if 'mdi' in mdi.class_name().lower():
            mdi_children = mdi.children()
            if mdi_children:
                print(f"    MDI now has {len(mdi_children)} children!")
                for m in mdi_children:
                    print(f"      - {m.window_text()}")
            else:
                print(f"    MDI still empty")
    except:
        pass

print("\n[4] Looking for parent/container of Sales button...")
if sales_elements:
    idx, sales = sales_elements[0]
    try:
        parent = sales.parent()
        print(f"    Parent class: {parent.class_name()}")
        print(f"    Parent text: {parent.window_text()}")
        
        # Try clicking parent
        print(f"\n    Trying to click parent...")
        parent.click()
        print(f"    ✓ Parent clicked")
        time.sleep(2)
    except Exception as e:
        print(f"    Error: {e}")

print("\nAnalysis complete.")
