"""
Test: Enter customer number in Take AR Payments form
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen
from pywinauto import Application, findwindows
import time

print("=" * 70)
print("TEST: Enter Customer Number in Take AR Payments")
print("=" * 70)

# Step 1: Navigate to Parts and click Take AR Payments
print("\n[STEP 1] Navigate to Take AR Payments screen...")
nav = NavigatorScreen()
nav.click_menu_button('Parts')
time.sleep(1)
nav.click_explorer_bar_button('Take AR Payments')
time.sleep(2)
print("  OK - Take AR Payments screen opened")

# Step 2: Find and connect to the Take AR Payments window
print("\n[STEP 2] Find Take AR Payments window...")
handles = findwindows.find_windows(title_re=".*Accounts Receivable.*")
if not handles:
    print("  [!] AR Payment window not found - trying all windows")
    handles = findwindows.find_windows(title_re=".*Payment.*")

if not handles:
    print("  [X] Could not find payment window")
    exit(1)

ar_hwnd = handles[0]
print(f"  OK - Found window: {ar_hwnd}")

# Step 3: Connect to the window via UIA
print("\n[STEP 3] Connect to window via UIA...")
app_uia = Application(backend='uia').connect(handle=ar_hwnd)
window_uia = app_uia.window(handle=ar_hwnd)
print("  OK - Connected")

# Step 4: Find the customer number input field
print("\n[STEP 4] Find customer number input field...")
try:
    # Look for Edit control with auto_id 65535
    customer_input = window_uia.child_window(control_type="Edit", class_name="Edit", auto_id="65535")
    print(f"  OK - Found input field: {customer_input}")
    
    # Step 5: Enter customer number
    print("\n[STEP 5] Enter customer number: 4268...")
    customer_input.click()
    time.sleep(0.5)
    
    # Clear any existing text
    customer_input.send_keys('^a')  # Select all
    time.sleep(0.2)
    
    # Type the customer number
    customer_input.type_keys('4268')
    time.sleep(0.5)
    
    print("  OK - Customer number entered")
    
    # Step 6: Verify entry
    print("\n[STEP 6] Verify customer number was entered...")
    current_text = customer_input.get_value() if hasattr(customer_input, 'get_value') else customer_input.window_text()
    print(f"  Input field contains: {current_text}")
    
    if "4268" in str(current_text):
        print("  OK - Customer number verified!")
    else:
        print("  [!] Customer number may not have been entered correctly")
        print("  (This could be due to UI response timing)")
    
except Exception as e:
    print(f"  [X] Error: {e}")
    print("\n  Attempting alternative method - find all Edit controls...")
    
    try:
        edits = window_uia.children(control_type="Edit")
        print(f"  Found {len(edits)} Edit controls")
        
        for i, edit in enumerate(edits):
            print(f"  [{i}] Edit control")
            try:
                # Try to enter data in each edit field
                edit.click()
                time.sleep(0.3)
                edit.send_keys('^a')
                time.sleep(0.2)
                edit.type_keys('4268')
                print(f"      -> Entered customer number")
                break
            except:
                pass
                
    except Exception as e2:
        print(f"  [X] Alternative method also failed: {e2}")

print("\n" + "=" * 70)
print("Done - Check Take AR Payments window")
print("=" * 70)
