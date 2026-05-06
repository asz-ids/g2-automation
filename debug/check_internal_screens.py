"""
Check if screens open as child windows or inside the Navigator
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time
import warnings
warnings.filterwarnings('ignore')

print("[1] Initial Navigator state...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()

print(f"    Title: {window.window_text()}")
print(f"    Children count: {len(window.children())}")

# Get initial child windows
initial_children = [str(c.window_text()) for c in window.children() if c.window_text().strip()]
print(f"    Initial child texts: {initial_children[:10]}")

print("\n[2] Clicking Sales button...")
children = window.children()
for child in children:
    try:
        if child.window_text() == "Sales" and child.is_visible():
            child.click()
            break
    except:
        pass

time.sleep(3)

print("\n[3] Checking Navigator after click...")
# Reconnect to get fresh state
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()

print(f"    Title: {window.window_text()}")
new_children_count = len(window.children())
print(f"    Children count: {new_children_count}")

# Get new child windows
new_children = [str(c.window_text()) for c in window.children() if c.window_text().strip()]
print(f"    Child texts: {new_children[:10]}")

# Check for MDI or internal screens
print("\n[4] Looking for MDI client or internal screens...")
try:
    for child in window.children():
        cls = child.class_name()
        if 'mdi' in cls.lower():
            print(f"    Found MDI client: {cls}")
            mdi_children = child.children()
            print(f"    MDI children count: {len(mdi_children)}")
            for mdi_child in mdi_children:
                print(f"      - {mdi_child.window_text()}")
except Exception as e:
    print(f"    Error checking MDI: {e}")

print("\n[5] Checking for any content/panel changes...")
# Look for visible content areas
try:
    for i, child in enumerate(window.children()):
        text = child.window_text()
        cls = child.class_name()
        
        # Look for content containers
        if 'panel' in cls.lower() or 'container' in cls.lower() or 'control' in cls.lower():
            if text.strip():
                print(f"    [{i}] {text:40} | {cls[:50]}")
except Exception as e:
    print(f"    Error: {e}")

print("\n[6] Checking if there's an error or message...")
all_windows = findwindows.find_windows(title_re=".*")
for h in all_windows:
    try:
        a = Application(backend='win32').connect(handle=h)
        w = a.top_window()
        title = w.window_text()
        if 'error' in title.lower() or 'warning' in title.lower() or 'message' in title.lower():
            if title.strip():
                print(f"    [!] Found: {title}")
    except:
        pass

print("\nInspection complete.")
