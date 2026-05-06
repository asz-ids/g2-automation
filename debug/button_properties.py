"""
Deep dive into the button element properties
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time
import warnings
warnings.filterwarnings('ignore')

print("[1] Finding Sales button...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()

sales_button = None
for child in window.children():
    try:
        if child.window_text() == "Sales" and child.is_visible():
            sales_button = child
            break
    except:
        pass

if not sales_button:
    print("[X] Sales button not found")
    exit(1)

print(f"[2] Sales button found - Full property dump:")
print(f"    window_text: {sales_button.window_text()}")
print(f"    class_name: {sales_button.class_name()}")
print(f"    is_enabled: {sales_button.is_enabled()}")
print(f"    is_visible: {sales_button.is_visible()}")
try:
    print(f"    has_focus: {sales_button.has_focus()}")
except:
    print(f"    has_focus: [error]")
print(f"    rectangle: {sales_button.rectangle()}")

print(f"\n[3] Checking what methods are available:")
# Get all non-private methods
methods = [m for m in dir(sales_button) if not m.startswith('_') and callable(getattr(sales_button, m))]
print(f"    Available methods ({len(methods)}):")
for method in sorted(methods)[:30]:
    print(f"      - {method}")

print(f"\n[4] Trying drag_mouse_input:")
try:
    # Maybe it needs a drag?
    sales_button.drag_mouse_input(dx=1, dy=1)
    print(f"    drag_mouse_input executed")
    time.sleep(1)
except Exception as e:
    print(f"    drag_mouse_input failed: {e}")

print(f"\n[5] Trying right_click:")
try:
    sales_button.right_click()
    print(f"    right_click executed")
    time.sleep(1)
except Exception as e:
    print(f"    right_click failed: {e}")

print(f"\n[6] Trying move_mouse:")
try:
    sales_button.move_mouse()
    print(f"    move_mouse executed")
    time.sleep(1)
except Exception as e:
    print(f"    move_mouse failed: {e}")

print(f"\n[7] Checking if it's actually a container/panel:")
try:
    children = sales_button.children()
    print(f"    Has children: {len(children)}")
    for i, child in enumerate(children[:5]):
        print(f"      [{i}] {child.window_text()[:40]} ({child.class_name()[:30]})")
except Exception as e:
    print(f"    No children: {e}")

print(f"\n[8] Getting element_info:")
try:
    elem_info = sales_button.element_info
    print(f"    Element info type: {type(elem_info)}")
    print(f"    Element info: {elem_info}")
except Exception as e:
    print(f"    Error: {e}")

print(f"\n[9] Checking for special automation properties:")
try:
    # Try to access via UIA
    from pywinauto.uia_element_info import UIAElementInfo
    uia_elem = UIAElementInfo(sales_button.element_info.element if hasattr(sales_button.element_info, 'element') else sales_button)
    print(f"    Name: {uia_elem.name if hasattr(uia_elem, 'name') else 'N/A'}")
    print(f"    AutomationId: {uia_elem.automation_id if hasattr(uia_elem, 'automation_id') else 'N/A'}")
except Exception as e:
    print(f"    UIA access failed: {e}")

print("\nAnalysis complete.")
