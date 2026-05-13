"""
Clicks Sales in the Navigator, then prints the full UIA tree so we can see
every element name, control type, and screen rect.
Run while G2 Navigator is open.
"""
import sys, time, ctypes, ctypes.wintypes
sys.path.insert(0, r'E:\G2 Desktop Automation')
from pywinauto import Desktop, findwindows

def walk(info, depth=0):
    try:
        name = info.name or ''
        ctype = info.control_type or ''
        try:
            r = info.rectangle
            rect = f"({r.left},{r.top})-({r.right},{r.bottom})"
        except Exception:
            rect = '?'
        indent = '  ' * depth
        print(f"{indent}[{ctype}] {name!r:40s}  {rect}")
        for child in info.children():
            walk(child, depth + 1)
    except Exception as e:
        print(f"{'  '*depth}!! {e}")

nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
if not nav_handles:
    print("ERROR: Navigator not found"); sys.exit(1)

nav_hwnd = nav_handles[0]
ctypes.windll.user32.ShowWindow(nav_hwnd, 9)
ctypes.windll.user32.SetForegroundWindow(nav_hwnd)
time.sleep(0.5)

nav_win = Desktop(backend='uia').window(handle=nav_hwnd)

# Click Sales to expand the section
print("Clicking Sales...")
try:
    nav_win.child_window(auto_id='btnSales', control_type='Button').click_input()
    print("  Clicked via btnSales")
except Exception:
    print("  btnSales not found, trying title...")
    try:
        nav_win.child_window(title='Sales', control_type='Button').click_input()
        print("  Clicked via title")
    except Exception as e:
        print(f"  Could not click Sales: {e}")

time.sleep(2)

print("\n=== Navigator UIA Tree (after clicking Sales) ===\n")
walk(nav_win.element_info)
