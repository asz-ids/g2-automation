"""
Detailed inspection of the Navigator button elements
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

print("\n[2] Analyzing each child window...")
children = window.children()
print(f"    Total children: {len(children)}")

print("\n    Detailed breakdown:")
for i, child in enumerate(children):
    try:
        text = child.window_text()
        cls = child.class_name()
        visible = child.is_visible()
        enabled = child.is_enabled()
        
        # Truncate for readability
        cls_short = cls[:50]
        text_short = text[:30] if text else "[empty]"
        
        if text or 'mdi' in cls.lower() or 'panel' in cls.lower() or 'container' in cls.lower():
            print(f"    [{i:2d}] Text: {text_short:30} | Visible: {visible} | Enabled: {enabled}")
            print(f"         Class: {cls_short}")
            
            # Check for special container types
            if 'panel' in cls.lower() or 'splitter' in cls.lower():
                try:
                    subchildren = child.children()
                    if subchildren:
                        print(f"         └─ Contains {len(subchildren)} children")
                except:
                    pass
    except Exception as e:
        print(f"    [{i:2d}] [Error: {e}]")

print("\n[3] Looking specifically for button-like elements...")
button_indices = []
for i, child in enumerate(children):
    try:
        text = child.window_text()
        if text in ["Sales", "Service", "Accounting", "Admin", "Parts"]:
            button_indices.append((i, text, child))
            print(f"    Found {text} at index {i}")
    except:
        pass

print(f"\n[4] Testing if these are actually tabs or panels...")
if button_indices:
    idx, name, elem = button_indices[0]
    print(f"    Testing {name}...")
    
    # Get parent info
    try:
        parent = elem.parent()
        print(f"    Parent class: {parent.class_name()}")
        if parent.window_text():
            print(f"    Parent text: {parent.window_text()}")
    except Exception as e:
        print(f"    Parent error: {e}")
    
    # Try to see if clicking reveals content
    print(f"\n    Looking for content area after button...")
    
    # Check siblings
    try:
        siblings = parent.children()
        print(f"    Parent has {len(siblings)} children total")
        
        # Look for a content/view area near button
        for sib_idx, sibling in enumerate(siblings):
            try:
                sib_text = sibling.window_text()
                sib_class = sibling.class_name()
                if 'view' in sib_class.lower() or 'control' in sib_class.lower() or 'panel' in sib_class.lower():
                    print(f"      [{sib_idx}] Potential content area: {sib_class[:40]}")
            except:
                pass
    except Exception as e:
        print(f"    Error: {e}")

print("\n[5] Checking window properties for hints...")
print(f"    Navigator title: {window.window_text()}")
print(f"    Navigator class: {window.class_name()}")

# Look for any scrollable or tabbed content
for i, child in enumerate(children):
    try:
        cls = child.class_name()
        if 'tab' in cls.lower() or 'tab' in child.window_text().lower():
            print(f"    [!] TAB CONTROL found at index {i}: {child.window_text()}")
    except:
        pass

print("\nAnalysis complete.")
