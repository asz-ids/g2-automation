"""
Deep inspection of G2 Navigator state
"""

from pywinauto import findwindows
from pywinauto.application import Application
from pywinauto.uia_element_info import UIAElementInfo
import time
import warnings
warnings.filterwarnings('ignore')

print("[1] Getting Navigator window...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
if not nav_handles:
    print("[X] Navigator not found")
    exit(1)

app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()

print(f"    Title: {window.window_text()}")
print(f"    Class: {window.class_name()}")
print(f"    Visible: {window.is_visible()}")
print(f"    Enabled: {window.is_enabled()}")

print("\n[2] Scanning ALL window text...")
print(f"    Full window text:\n{window.window_text()}")

print("\n[3] Looking for labels, status messages, or text...")
children = window.children()
text_elements = []
for i, child in enumerate(children):
    try:
        class_name = child.class_name()
        text = child.window_text()
        
        # Look for status or message text
        if text.strip() and len(text) < 200:
            text_elements.append((i, text, class_name))
    except:
        pass

print(f"    Found {len(text_elements)} text elements:")
for idx, text, cls in text_elements[:30]:
    print(f"    [{idx:2d}] {text:30} | {cls[:40]}")

print("\n[4] Checking if this is a module or workspace selector...")
try:
    comboboxes = []
    for child in children:
        if 'combobox' in child.class_name().lower():
            comboboxes.append(child.window_text())
    
    if comboboxes:
        print(f"    Comboboxes found: {comboboxes}")
        print(f"    [!] This might be a module/workspace selector, not a menu!")
except:
    pass

print("\n[5] Checking button properties...")
for i, child in enumerate(children):
    try:
        if child.window_text() == "Sales":
            print(f"    Sales Button Properties:")
            print(f"      Class: {child.class_name()}")
            print(f"      Enabled: {child.is_enabled()}")
            print(f"      Visible: {child.is_visible()}")
            print(f"      Text: {child.window_text()}")
            
            # Try to get more properties
            try:
                rect = child.rectangle()
                print(f"      Position: ({rect.left}, {rect.top}) to ({rect.right}, {rect.bottom})")
                print(f"      Size: {rect.width()} x {rect.height()}")
            except:
                pass
            
            # Check for automation ID
            try:
                # Use UIA backend to get automation ID
                from pywinauto.ui_automation_types import UIA
                elem = UIAElementInfo(child.element_info.element)
                print(f"      AutomationID: {elem.automation_id}")
            except:
                pass
            
            break
    except:
        pass

print("\n[6] Checking window hierarchy...")
print(f"    Window type: {window.__class__.__name__}")
print(f"    Backend: {window.__class__.__module__}")

print("\n[7] Looking for parent window that might be blocking...")
try:
    parent = window.parent()
    if parent:
        print(f"    Parent: {parent.window_text()}")
        print(f"    Parent Class: {parent.class_name()}")
except:
    print("    No parent window")

print("\nInspection complete.")
