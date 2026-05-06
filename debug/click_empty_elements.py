"""
Try clicking the EMPTY elements instead of the text labels
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time

print("[1] Finding the button container...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()

# Get all children and find Sales button
children = window.children()
sales_container = None

for i, child in enumerate(children):
    try:
        if child.window_text() == "Sales" and child.is_visible():
            # Get its parent
            parent = child.parent()
            parent_children = parent.children()
            print(f"    Found Sales at index {i}")
            print(f"    Parent has {len(parent_children)} children")
            
            # The parent should have the empty button elements
            sales_container = parent
            break
    except:
        pass

if not sales_container:
    print("[X] Could not find sales container")
    exit(1)

print(f"\n[2] Trying to click on empty button element (should be index 2)...")
try:
    parent_children = sales_container.children()
    
    # Element [2] is the empty element right after "Sales" text
    # This might be the actual clickable button
    if len(parent_children) > 2:
        empty_button = parent_children[2]
        print(f"    Found element: {empty_button.window_text()[:20] if empty_button.window_text() else '[EMPTY]'}")
        
        rect = empty_button.rectangle()
        print(f"    Position: {rect}")
        
        print(f"    Clicking...")
        empty_button.click()
        print(f"    ✓ Clicked")
        time.sleep(3)
        
        # Check result
        print(f"\n[3] Checking for result...")
        sales_handles = findwindows.find_windows(title_re=".*Sales.*")
        if sales_handles:
            print(f"    ✓ SUCCESS! Sales screen opened!")
        else:
            print(f"    [X] No Sales screen")
    else:
        print(f"    [X] Not enough children")

except Exception as e:
    print(f"    [X] Error: {e}")
    import traceback
    traceback.print_exc()

print(f"\n[4] If that didn't work, trying all empty elements...")
try:
    parent_children = sales_container.children()
    
    empty_elements = []
    for i, elem in enumerate(parent_children):
        if not elem.window_text():
            empty_elements.append((i, elem))
    
    print(f"    Found {len(empty_elements)} empty elements")
    
    for idx, elem in empty_elements:
        print(f"    Trying element {idx}...")
        try:
            elem.click()
            time.sleep(1)
            
            # Check
            sales_handles = findwindows.find_windows(title_re=".*Sales.*")
            if sales_handles:
                print(f"      ✓ SUCCESS on element {idx}!")
                exit(0)
        except Exception as e:
            print(f"      Failed: {e}")

except Exception as e:
    print(f"    Error: {e}")

print(f"\nDone.")
