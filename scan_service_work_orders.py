# scan_service_work_orders.py
"""
Run with G2 open and navigated to Service → Work Orders.
Prints all UIA element IDs found in that window.
"""
import sys
sys.path.insert(0, r'E:\G2 Desktop Automation')

import time
from pywinauto import findwindows
from pywinauto.application import Application

# Patterns to try — one of these should match the WO Manager window
TITLE_PATTERNS = [
    r".*Work Order.*",
    r".*Service.*",
    r".*WO.*",
]

def scan_window(title_re: str):
    windows = findwindows.find_windows(title_re=title_re)
    if not windows:
        return None, []
    app = Application(backend='uia').connect(handle=windows[0])
    win = app.window()
    return win.window_text(), win

def print_element_tree(elem, depth=0, max_depth=5, found=None):
    if found is None:
        found = []
    if depth > max_depth:
        return found
    try:
        auto_id = elem.automation_id() if callable(getattr(elem, 'automation_id', None)) else getattr(elem, 'automation_id', '')
        ctrl_type = elem.element_info.control_type if hasattr(elem, 'element_info') else ''
        title = elem.window_text() if hasattr(elem, 'window_text') else ''
        indent = "  " * depth
        line = f"{indent}auto_id={repr(auto_id)!s:<35} ctrl={ctrl_type!s:<15} title={repr(title)}"
        print(line)
        if auto_id:
            found.append({'auto_id': auto_id, 'ctrl_type': ctrl_type, 'title': title})
    except Exception:
        pass
    try:
        for child in elem.children():
            print_element_tree(child, depth + 1, max_depth, found)
    except Exception:
        pass
    return found

print("Scanning for Work Orders window...")
win_title, win = None, None
for pattern in TITLE_PATTERNS:
    win_title, win = scan_window(pattern)
    if win:
        print(f"Found window: '{win_title}' (pattern: {pattern})")
        break

if not win:
    print("ERROR: No matching window found. Open G2 and navigate to Service → Work Orders first.")
    sys.exit(1)

print(f"\n{'='*70}")
print(f"Element tree for: {win_title}")
print(f"{'='*70}\n")
found_elements = print_element_tree(win)

print(f"\n{'='*70}")
print(f"Summary: {len(found_elements)} elements with auto_ids")
print(f"{'='*70}")
for e in found_elements:
    print(f"  {e['auto_id']}")
