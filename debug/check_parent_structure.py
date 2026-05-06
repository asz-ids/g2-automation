"""
Check the parent and sibling structure
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time

print("[1] Finding Navigator and Sales button...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()

sales_button = None
sales_index = None

children = window.children()
for i, child in enumerate(children):
    try:
        if child.window_text() == "Sales" and child.is_visible():
            sales_button = child
            sales_index = i
            break
    except:
        pass

print(f"Sales button at index: {sales_index}")

print(f"\n[2] Parent hierarchy:")
try:
    parent = sales_button.parent()
    print(f"    Parent class: {parent.class_name()}")
    print(f"    Parent text: {parent.window_text()}")
    
    # Get parent's children
    parent_children = parent.children()
    print(f"    Parent has {len(parent_children)} children")
    
    # Show layout
    print(f"\n[3] Parent's children layout:")
    for i, child in enumerate(parent_children):
        text = child.window_text()[:20] if child.window_text() else "[empty]"
        rect = child.rectangle()
        print(f"    [{i:2d}] {text:20} | Rect: ({rect.left}, {rect.top}, {rect.right}, {rect.bottom})")
except Exception as e:
    print(f"    Error: {e}")

print(f"\n[4] Checking Navigator window structure:")
# The window itself might be the parent
print(f"    Navigator has {len(window.children())} children")

# Check indices around Sales
if sales_index is not None:
    print(f"\n[5] Elements around Sales (index {sales_index}):")
    for i in range(max(0, sales_index-2), min(len(window.children()), sales_index+3)):
        child = window.children()[i]
        text = child.window_text()[:20] if child.window_text() else "[empty]"
        cls = child.class_name()[:40]
        try:
            children_count = len(child.children())
        except:
            children_count = 0
        print(f"    [{i:2d}] {text:20} | Class: {cls:40} | Children: {children_count}")

print(f"\n[6] Looking for a tab control or button container:")
for i, child in enumerate(window.children()):
    try:
        cls = child.class_name()
        text = child.window_text()[:20] if child.window_text() else ""
        
        # Look for tab or button container
        if any(x in cls for x in ['Tab', 'Button', 'Group', 'Panel', 'Bar', 'Strip']):
            print(f"    [{i}] Found: {cls:50} Text: {text}")
            
            # If it contains multiple menu items, show children
            try:
                kids = child.children()
                if len(kids) > 3:
                    print(f"         Has {len(kids)} children - looks like a container!")
                    for k in kids[:5]:
                        ktext = k.window_text()[:15] if k.window_text() else ""
                        print(f"           - {ktext}")
            except:
                pass
    except:
        pass

print("\nAnalysis complete.")
