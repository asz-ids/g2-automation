"""
Test: Enter customer number - find correct input field
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen
from pywinauto import Application, findwindows
import time

print("=" * 70)
print("TEST: Enter Customer Number - Finding Correct Input Field")
print("=" * 70)

# Step 1: Navigate to Take AR Payments
print("\n[STEP 1] Navigate to Take AR Payments screen...")
nav = NavigatorScreen()
nav.click_menu_button('Parts')
time.sleep(1)
nav.click_explorer_bar_button('Take AR Payments')
time.sleep(2)
print("  OK - Take AR Payments screen opened")

# Step 2: Find the window
print("\n[STEP 2] Find AR Payment window...")
handles = findwindows.find_windows(title_re=".*Accounts Receivable.*")
if not handles:
    handles = findwindows.find_windows(title_re=".*Payment.*")

ar_hwnd = handles[0]
print(f"  OK - Window handle: {ar_hwnd}")

# Step 3: Connect and analyze
print("\n[STEP 3] Analyzing all Edit controls in window...")
app_uia = Application(backend='uia').connect(handle=ar_hwnd)
window_uia = app_uia.window(handle=ar_hwnd)

print("\n  All descendants with 'Edit' type or 'Enter' text:")
print("  " + "-" * 66)

edit_controls = []
for elem in window_uia.descendants():
    try:
        elem_type = elem.control_type if hasattr(elem, 'control_type') else None
        elem_text = elem.window_text() if hasattr(elem, 'window_text') else ""
        elem_class = elem.class_name if hasattr(elem, 'class_name') else ""
        
        # Look for Edit controls or fields with "customer" or "number" labels
        if elem_type == "Edit" or (elem_class == "Edit"):
            edit_controls.append((elem, elem_text, elem_class))
            print(f"  EDIT CONTROL: text='{elem_text}' class='{elem_class}'")
        
        # Look for labels/text elements near "customer" or "number"
        if elem_text and ("enter" in elem_text.lower() or "customer" in elem_text.lower() or "number" in elem_text.lower()):
            print(f"  LABEL: type={elem_type} text='{elem_text}'")
            
    except:
        pass

print("\n" + "=" * 70)

if edit_controls:
    print(f"Found {len(edit_controls)} Edit controls")
    print("\n[STEP 4] Entering customer number in first Edit control...")
    
    first_edit = edit_controls[0][0]
    try:
        # Click to focus
        first_edit.click()
        time.sleep(0.5)
        
        # Clear and enter text
        first_edit.send_keys('^a')
        time.sleep(0.2)
        first_edit.type_keys('4268', interval=0.1)
        time.sleep(0.5)
        
        print("  OK - Customer number entered")
        
        # Try to get the value
        try:
            value = first_edit.get_value() if hasattr(first_edit, 'get_value') else first_edit.window_text()
            print(f"  Field value: '{value}'")
        except:
            print("  (Could not verify field value)")
            
    except Exception as e:
        print(f"  [X] Error entering text: {e}")

else:
    print("No Edit controls found")
    print("\nTrying to get all window text content...")
    try:
        all_text = window_uia.window_text()
        print(f"Window text:\n{all_text}")
    except:
        pass

print("\n" + "=" * 70)
print("Done - Check Take AR Payments window")
print("=" * 70)
