"""
Find the actual clickable container/button overlay
"""

from pywinauto import findwindows
from pywinauto.application import Application
from ctypes import windll
import time
import warnings
warnings.filterwarnings('ignore')

print("[1] Analyzing button region more carefully...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()

children = window.children()

# Find which child contains or overlays the buttons
print("\n[2] Looking for container/panel at button position...")
button_x, button_y = 1038, 123

for i, child in enumerate(children):
    try:
        rect = child.rectangle()
        
        # Check if this element contains the button position
        if (rect.left <= button_x <= rect.right and 
            rect.top <= button_y <= rect.bottom):
            
            text = child.window_text()
            cls = child.class_name()
            print(f"    [{i}] Contains button position")
            print(f"        Text: {text}")
            print(f"        Class: {cls}")
            print(f"        Rect: ({rect.left}, {rect.top}, {rect.right}, {rect.bottom})")
            
            # Try clicking this element
            print(f"        Trying to click this element...")
            child.click()
            time.sleep(2)
            
            # Check result
            try:
                sales_handles = findwindows.find_windows(title_re=".*Sales.*")
                if sales_handles:
                    print(f"        ✓ SUCCESS!")
                    exit(0)
            except:
                pass
    except:
        pass

print("\n[3] If no match, look for elements at button index 16...")
if len(children) > 16:
    button_elem = children[16]
    print(f"    Element at index 16:")
    print(f"      Text: {button_elem.window_text()}")
    print(f"      Class: {button_elem.class_name()}")
    rect = button_elem.rectangle()
    print(f"      Rect: {rect}")
    
    # Check parent
    try:
        parent = button_elem.parent()
        print(f"      Parent: {parent.class_name()}")
        
        # List all parent's children to find actual container
        parent_children = parent.children()
        print(f"      Parent has {len(parent_children)} children")
        
        # Look for indices around 16
        for j in range(max(0, 16-2), min(len(parent_children), 16+3)):
            ch = parent_children[j]
            print(f"        [{j}] {ch.window_text()[:20]} | {ch.class_name()[:40]}")
    except Exception as e:
        print(f"      Error: {e}")

print("\n[4] Check if buttons are actually visual only (text rendered on parent)...")
# Get the parent's handle and try clicking directly on it
try:
    # Find the main content area
    for i, child in enumerate(children):
        cls = child.class_name()
        rect = child.rectangle()
        
        # Look for a large panel/container that would be the button bar
        if (rect.left < 500 and rect.right > 1500 and 
            rect.top < 200 and rect.bottom > 50):
            
            if 'window' in cls.lower() or 'panel' in cls.lower() or 'container' in cls.lower():
                print(f"    Found candidate button bar container at index {i}")
                print(f"      Class: {cls}")
                print(f"      Rect: {rect}")
                
                # Try clicking on it
                print(f"      Clicking on container...")
                child.click()
                time.sleep(2)
                
                sales_handles = findwindows.find_windows(title_re=".*Sales.*")
                if sales_handles:
                    print(f"      ✓ SUCCESS!")
                    exit(0)
except Exception as e:
    print(f"    Error: {e}")

print("\nAnalysis complete - no clickable element found")
