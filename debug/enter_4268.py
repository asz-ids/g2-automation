"""
Test: Find Customer # label and adjacent Edit box, then enter 4268
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen
from pywinauto import Application, findwindows
import time

print("=" * 70)
print("Find Customer # and Enter 4268")
print("=" * 70)

# # Navigate
# print("\n[1] Navigate to Take AR Payments...")
# nav = NavigatorScreen()
# nav.click_menu_button('Parts')
# time.sleep(1)
# nav.click_explorer_bar_button('Take AR Payments')
# time.sleep(2)

# Find window
handles = findwindows.find_windows(title_re=".*Accounts Receivable.*")
if not handles:
    handles = findwindows.find_windows(title_re=".*Payment.*")
ar_hwnd = handles[0]

app_uia = Application(backend='uia').connect(handle=ar_hwnd)
window_uia = app_uia.window(handle=ar_hwnd)

# Find Customer # label element
print("[2] Finding 'Customer #' label...")
customer_label_elem = None
for elem in window_uia.descendants():
    try:
        elem_text = elem.window_text() if hasattr(elem, 'window_text') else ""
        if elem_text == "Customer #":
            customer_label_elem = elem
            print(f"    Found at: {elem}")
            try:
                rect = elem.rectangle if hasattr(elem, 'rectangle') else None
                if rect:
                    print(f"    Position: left={rect.left}, top={rect.top}, right={rect.right}, bottom={rect.bottom}")
                    label_rect = rect
            except:
                pass
            break
    except:
        pass

if not customer_label_elem:
    print("    [X] Not found!")
    exit(1)

# Now find Edit controls and their positions
print("\n[3] Collecting all Edit controls...")
edit_controls = []
for elem in window_uia.descendants():
    try:
        elem_type = elem.control_type if hasattr(elem, 'control_type') else None
        if elem_type == "Edit":
            try:
                rect = elem.rectangle if hasattr(elem, 'rectangle') else None
                if rect:
                    # Calculate if this Edit is "next to" the Customer # label
                    is_same_row = abs(rect.top - label_rect.top) < 30  # Same vertical area
                    is_to_the_right = rect.left >= label_rect.left  # To the right of label
                    
                    edit_controls.append({
                        'elem': elem,
                        'rect': rect,
                        'is_same_row': is_same_row,
                        'is_to_right': is_to_the_right,
                        'distance_right': rect.left - label_rect.right,
                    })
                    print(f"    Edit at ({rect.left}, {rect.top}): same_row={is_same_row}, to_right={is_to_the_right}")
            except:
                pass
    except:
        pass

print(f"    Total Edit controls found: {len(edit_controls)}")

# Find the right one (same row and to the right)
target_edit = None
for ec in edit_controls:
    if ec['is_same_row'] and ec['is_to_right'] and ec['distance_right'] >= -50:  # Allow some overlap
        target_edit = ec
        print(f"    -> Selected Edit at distance_right={ec['distance_right']}")
        break

# If not found by position, just take any Edit control
if not target_edit and edit_controls:
    target_edit = edit_controls[0]
    print(f"    -> Selected first Edit control (position matching didn't work)")

if not target_edit:
    print("    [X] No Edit controls found!")
    exit(1)

# Enter the customer number
print("\n[4] Entering customer number 4268...")
try:
    elem = target_edit['elem']
    
    # Click to focus
    elem.click()
    print("    Clicked on Edit control")
    time.sleep(0.3)
    
    # Clear existing text
    elem.send_keys('^a', pause=0.1)
    print("    Cleared existing text")
    time.sleep(0.2)
    
    # Type 4268
    elem.type_keys('4268', interval=0.15)
    print("    Typed 4268")
    time.sleep(0.5)
    
    print("\n    [OK] SUCCESS - Customer number 4268 entered!")
    
except Exception as e:
    print(f"    [X] Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
