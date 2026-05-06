"""
Check the fresh Navigator state after restart
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time
import warnings
warnings.filterwarnings('ignore')

print("[1] Looking for windows...")
all_handles = findwindows.find_windows(title_re=".*")
print(f"    Total windows: {len(all_handles)}")

print("\n[2] Looking for G2 windows...")
g2_handles = findwindows.find_windows(title_re=".*G2.*")
print(f"    G2 windows found: {len(g2_handles)}")

for h in g2_handles[:10]:
    try:
        app = Application(backend='win32').connect(handle=h)
        w = app.top_window()
        print(f"      - {w.window_text()} ({w.class_name()})")
    except Exception as e:
        print(f"      - [Error: {e}]")

print("\n[3] Looking for Login window...")
login_handles = findwindows.find_windows(title_re=".*Login.*|.*login.*")
print(f"    Login windows: {len(login_handles)}")

print("\n[4] Looking for Navigator window...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
print(f"    Navigator windows: {len(nav_handles)}")

if nav_handles:
    print("\n[5] Navigator Details...")
    app = Application(backend='win32').connect(handle=nav_handles[0])
    window = app.top_window()
    print(f"    Title: {window.window_text()}")
    print(f"    Visible: {window.is_visible()}")
    print(f"    Enabled: {window.is_enabled()}")
    
    # Check for combobox (module selector)
    children = window.children()
    print(f"    Children: {len(children)}")
    
    for child in children[:5]:
        print(f"      - {child.window_text()} ({child.class_name()[:30]})")

print("\nCheck complete.")
