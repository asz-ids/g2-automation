"""
Find the ACTUAL buttons using automation IDs
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time

print("[1] Scanning all children for automation IDs...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()

children = window.children()
button_elements = []

for i, child in enumerate(children):
    try:
        props = child.get_properties()
        auto_id = props.get('automation_id', '')
        text = child.window_text()
        
        # Look for actual button IDs
        if auto_id or 'btn' in auto_id.lower():
            print(f"    [{i:2d}] AutoID: {auto_id:30} | Text: {text:20}")
            
            if 'btn' in auto_id.lower():
                button_elements.append((i, child, auto_id))
    except:
        pass

print(f"\n    Found {len(button_elements)} button-like elements")

# Also look for elements with specific sales/service patterns
print(f"\n[2] Looking for sale/service/accounting buttons...")
for i, child in enumerate(children):
    try:
        props = child.get_properties()
        auto_id = props.get('automation_id', '')
        text = child.window_text()
        
        if any(x in auto_id.lower() for x in ['sales', 'service', 'accounting', 'admin', 'parts']):
            print(f"    [{i:2d}] AutoID: {auto_id:30} | Text: {text:20}")
            button_elements.append((i, child, auto_id))
    except:
        pass

print(f"\n[3] If buttons found, try clicking them...")
if button_elements:
    for idx, elem, auto_id in button_elements[:1]:  # Try first one
        print(f"\n    Trying to click: {auto_id}")
        try:
            elem.click()
            print(f"    Clicked")
            time.sleep(3)
            
            # Check for changes
            nav_handles2 = findwindows.find_windows(title_re=".*Navigator.*")
            app2 = Application(backend='win32').connect(handle=nav_handles2[0])
            window2 = app2.top_window()
            new_count = len(window2.children())
            
            print(f"    Navigator children: {new_count} (was {len(children)})")
            
        except Exception as e:
            print(f"    Error: {e}")

print(f"\n[4] Full automation ID scan of all children:")
print(f"    Index | AutoID")
print(f"    ------|" + "-"*40)

for i, child in enumerate(children):
    try:
        props = child.get_properties()
        auto_id = props.get('automation_id', '')
        
        if auto_id:
            print(f"    {i:2d}    | {auto_id}")
    except:
        pass

print(f"\nAnalysis complete.")
