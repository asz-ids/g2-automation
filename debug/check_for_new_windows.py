"""
Look for any error messages or hidden windows after clicking
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time
import warnings
warnings.filterwarnings('ignore')

print("[1] Before click - all windows:")
before_windows = set()
all_handles = findwindows.find_windows(title_re=".*")
for h in all_handles:
    try:
        a = Application(backend='win32').connect(handle=h)
        w = a.top_window()
        title = w.window_text()
        before_windows.add(title)
    except:
        pass

print(f"    Total: {len(before_windows)}")

# Click Sales
print("\n[2] Clicking Sales...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()
window.set_focus()

children = window.children()
for child in children:
    try:
        if child.window_text() == "Sales" and child.is_visible():
            child.click()
            break
    except:
        pass

time.sleep(3)

print("\n[3] After click - looking for NEW windows:")
after_windows = set()
all_handles = findwindows.find_windows(title_re=".*")
for h in all_handles:
    try:
        a = Application(backend='win32').connect(handle=h)
        w = a.top_window()
        title = w.window_text()
        after_windows.add(title)
    except:
        pass

print(f"    Total: {len(after_windows)}")

new_windows = after_windows - before_windows
if new_windows:
    print(f"    NEW windows found:")
    for title in sorted(new_windows):
        print(f"      - {title}")
else:
    print(f"    [X] No new windows")

print("\n[4] Looking for any visible windows we might have missed:")
all_handles = findwindows.find_windows(title_re=".*")
for i, h in enumerate(all_handles):
    try:
        a = Application(backend='win32').connect(handle=h)
        w = a.top_window()
        
        # Check if visible
        if w.is_visible():
            title = w.window_text()
            
            # Print interesting ones
            if any(x in title for x in ['Sales', 'Service', 'Screen', 'View', 'List', 'Error', 'Message', 'Dialog', 'Input', 'Prompt']):
                print(f"    [{i}] {title[:70]} (Visible: {w.is_visible()})")
    except:
        pass

print("\n[5] Checking Navigator's parent and related windows:")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
if nav_handles:
    app = Application(backend='win32').connect(handle=nav_handles[0])
    window = app.top_window()
    
    try:
        parent = window.parent()
        print(f"    Navigator parent: {parent.window_text()}")
    except:
        print(f"    No parent")
    
    # Get siblings
    try:
        parent = window.parent()
        siblings = parent.children()
        print(f"    Siblings: {len(siblings)}")
        for sib in siblings:
            text = sib.window_text()
            if text and text != "G2 Navigator":
                print(f"      - {text[:50]}")
    except:
        pass

print("\nInspection complete.")
