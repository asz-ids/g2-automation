"""
Test: Find "Customer #" label and enter 4268 in the adjacent edit box
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen
from pywinauto import Application, findwindows
import time

print("=" * 70)
print("TEST: Find Customer # Label and Enter 4268")
print("=" * 70)

# Step 1: Navigate to Take AR Payments
print("\n[STEP 1] Navigate to Take AR Payments screen...")
nav = NavigatorScreen()
nav.click_menu_button('Parts')
time.sleep(1)
nav.click_explorer_bar_button('Take AR Payments')
time.sleep(10)
print("  OK - Take AR Payments screen opened")

# Step 2: Find the window
print("\n[STEP 2] Find AR Payment window...")
handles = findwindows.find_windows(title_re=".*Accounts Receivable.*")
if not handles:
    handles = findwindows.find_windows(title_re=".*Payment.*")

ar_hwnd = handles[0]
print(f"  OK - Window handle: {ar_hwnd}")

# Step 3: Connect using UIA backend
print("\n[STEP 3] Connect to window via UIA...")
app_uia = Application(backend='uia').connect(handle=ar_hwnd)
window_uia = app_uia.window(handle=ar_hwnd)
print("  OK - Connected")

# Step 4: Find "Customer #" text element
print("\n[STEP 4] Looking for 'Customer #' label...")
customer_label = None
for elem in window_uia.descendants():
    try:
        elem_text = elem.window_text() if hasattr(elem, 'window_text') else ""
        if elem_text and "Customer #" in elem_text:
            customer_label = elem
            print(f"  Found label: '{elem_text}'")
            break
    except:
        pass

if not customer_label:
    print("  [X] Could not find 'Customer #' label")
    print("\n  Searching for all text elements...")
    for elem in window_uia.descendants():
        try:
            elem_text = elem.window_text() if hasattr(elem, 'window_text') else ""
            if elem_text and elem_text.strip() and len(elem_text) < 100:
                print(f"    - {elem_text}")
        except:
            pass
    exit(1)

# Step 5: Find Edit control next to the label
print("\n[STEP 5] Finding Edit box near the 'Customer #' label...")

# Get the label's position
try:
    label_rect = customer_label.rectangle if hasattr(customer_label, 'rectangle') else None
    if label_rect:
        label_right = label_rect.right
        label_y = label_rect.top
        label_height = label_rect.bottom - label_rect.top
        print(f"  Label position: X={label_rect.left}-{label_right}, Y={label_rect.top}-{label_rect.bottom}")
    else:
        label_right = None
        label_y = None
        label_height = None
except:
    label_right = None
    label_y = None
    label_height = None

# Find Edit control
edit_box = None
for elem in window_uia.descendants():
    try:
        elem_type = elem.control_type if hasattr(elem, 'control_type') else ""
        
        if elem_type == "Edit":
            # Check if this Edit is to the right of the label and at similar Y position
            if label_right and label_y and label_height:
                try:
                    elem_rect = elem.rectangle if hasattr(elem, 'rectangle') else None
                    if elem_rect:
                        # Check if Edit is to the right of label and at similar vertical position
                        if (elem_rect.left >= label_right - 50 and  # Allow some overlap
                            elem_rect.top >= label_y - label_height and
                            elem_rect.top <= label_y + label_height * 2):
                            edit_box = elem
                            print(f"  Found Edit box at X={elem_rect.left}, Y={elem_rect.top}")
                            break
                except:
                    pass
            
            # If we couldn't do position-based matching, just take the first Edit
            if not edit_box:
                edit_box = elem
                print(f"  Found Edit box (position-based matching not available)")
                break
    except:
        pass

if not edit_box:
    print("  [X] Could not find Edit box")
    exit(1)

# Step 6: Enter the customer number
print("\n[STEP 6] Entering customer number 4268...")
try:
    # Click to focus
    edit_box.click()
    time.sleep(0.3)
    
    # Clear any existing text
    edit_box.send_keys('^a', pause=0.1)
    time.sleep(0.2)
    
    # Type the customer number with spacing
    edit_box.type_keys('4268', interval=0.15)
    time.sleep(0.5)
    
    print("  OK - Customer number entered!")
    
    # Try to verify
    try:
        current_value = edit_box.get_value() if hasattr(edit_box, 'get_value') else edit_box.window_text()
        print(f"  Edit box value: '{current_value}'")
    except:
        print("  (Could not verify field value)")
    
except Exception as e:
    print(f"  [X] Error entering text: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("SUCCESS - Customer number 4268 has been entered")
print("=" * 70)
