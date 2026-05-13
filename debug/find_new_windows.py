"""
Clicks Sales -> Unit Inventory -> Maintain Units via ultraExplorerBar1,
then prints every new window that appeared so we know the exact title.
"""
import sys, time, ctypes, ctypes.wintypes
sys.path.insert(0, r'E:\G2 Desktop Automation')
from pywinauto import Desktop, findwindows

def _title(hwnd):
    n = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
    buf = ctypes.create_unicode_buffer(n + 1)
    ctypes.windll.user32.GetWindowTextW(hwnd, buf, n + 1)
    return buf.value.strip()

def all_titled():
    return {h: _title(h) for h in findwindows.find_windows() if _title(h)}

def click_in_explorer(explorer, title):
    btn = explorer.child_window(title=title, control_type='Button')
    btn.wait('exists visible', timeout=5)
    btn.click_input()
    print(f"  [OK] Clicked '{title}'")

nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
if not nav_handles:
    print("ERROR: Navigator not found"); sys.exit(1)

nav_hwnd = nav_handles[0]
ctypes.windll.user32.ShowWindow(nav_hwnd, 9)
ctypes.windll.user32.SetForegroundWindow(nav_hwnd)
time.sleep(0.5)

nav_win  = Desktop(backend='uia').window(handle=nav_hwnd)
explorer = nav_win.child_window(auto_id='ultraExplorerBar1', control_type='Tree')

before = all_titled()
print(f"Snapshot: {len(before)} windows open.\n")

# Try btnSales first (toolbar button), fall back to explorer bar
print("Clicking Sales...")
try:
    nav_win.child_window(auto_id='btnSales', control_type='Button').click_input()
    print("  [OK] Clicked Sales via btnSales")
except Exception:
    click_in_explorer(explorer, 'Sales')
time.sleep(2)

print("Clicking Unit Inventory...")
click_in_explorer(explorer, 'Unit Inventory')
time.sleep(2)

print("Clicking Maintain Units...")
click_in_explorer(explorer, 'Maintain Units')

print("\nWaiting up to 15s for new window...")
for i in range(15):
    after  = all_titled()
    new    = {h: t for h, t in after.items() if h not in before}
    if new:
        print(f"\nNew windows after {i+1}s:")
        for hwnd, title in new.items():
            print(f"  HWND {hwnd}  title={title!r}")
        break
    time.sleep(1)
else:
    print("\nNo new windows after 15s. All current windows:")
    for hwnd, title in all_titled().items():
        print(f"  HWND {hwnd}  title={title!r}")
