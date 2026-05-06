"""
Detailed before/after inspection of clicking a button
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time
import warnings
warnings.filterwarnings('ignore')

def print_nav_state(label):
    """Print detailed state of Navigator"""
    print(f"\n{'='*60}")
    print(f"{label}")
    print(f"{'='*60}")
    
    nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
    if not nav_handles:
        print("Navigator not found!")
        return
    
    app = Application(backend='win32').connect(handle=nav_handles[0])
    window = app.top_window()
    
    print(f"Navigator title: {window.window_text()}")
    print(f"Navigator visible: {window.is_visible()}")
    print(f"Navigator enabled: {window.is_enabled()}")
    
    # Count children
    children = window.children()
    print(f"Total children: {len(children)}")
    
    # Look for MDI
    mdi_count = 0
    for child in children:
        try:
            if 'mdi' in child.class_name().lower():
                mdi_kids = child.children()
                mdi_count = len(mdi_kids)
                print(f"MDI children: {mdi_count}")
                
                if mdi_kids:
                    for m in mdi_kids:
                        print(f"  - {m.window_text()[:50]}")
        except:
            pass
    
    # Look for visible content windows
    print(f"\nTop-level windows:")
    all_windows = findwindows.find_windows(title_re=".*")
    screen_count = 0
    for h in all_windows:
        try:
            a = Application(backend='win32').connect(handle=h)
            w = a.top_window()
            title = w.window_text()
            
            # Count screen-like windows
            if any(x in title for x in ['Screen', 'View', 'Sales', 'Service', 'Accounting', 'Admin', 'Parts']):
                print(f"  - {title[:60]}")
                screen_count += 1
        except:
            pass
    
    print(f"Screen windows found: {screen_count}")

# Initial state
print_nav_state("BEFORE CLICKING")

# Find and click Sales button
print("\n[CLICKING SALES BUTTON...]")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()
window.set_focus()

children = window.children()
for child in children:
    try:
        if child.window_text() == "Sales" and child.is_visible():
            print(f"Found Sales button, executing click()...")
            child.click()
            print(f"Click executed")
            break
    except:
        pass

print("\nWaiting 3 seconds...")
time.sleep(3)

# After state
print_nav_state("AFTER CLICKING")

print("\n[DONE]")
