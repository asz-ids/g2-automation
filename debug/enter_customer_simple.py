"""
Test: Enter customer number - Simpler approach
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen
from pywinauto import Application, findwindows, keyboard
import time

print("=" * 70)
print("TEST: Enter Customer Number - Simple Approach")
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

# Step 3: Connect using win32 backend
print("\n[STEP 3] Connect to window (win32 backend)...")
try:
    app = Application(backend='win32').connect(handle=ar_hwnd)
    window = app.window(handle=ar_hwnd)
    print("  OK - Connected")
except Exception as e:
    print(f"  [X] Connection error: {e}")
    exit(1)

# Step 4: Find Edit controls
print("\n[STEP 4] Finding Edit controls...")
try:
    children = window.children()
    edit_ctrls = []
    
    for child in children:
        try:
            class_name = child.class_name() if hasattr(child, 'class_name') else ""
            if class_name == 'Edit' or 'Edit' in str(class_name):
                text = child.window_text() if hasattr(child, 'window_text') else ""
                edit_ctrls.append(child)
                print(f"  Found Edit control: {text}")
        except:
            pass
    
    if edit_ctrls:
        print(f"  OK - Found {len(edit_ctrls)} Edit controls")
        
        # Step 5: Enter text in first Edit control
        print("\n[STEP 5] Entering customer number 4268...")
        first_edit = edit_ctrls[0]
        
        try:
            # Click to focus
            first_edit.click()
            time.sleep(0.3)
            
            # Clear any existing text
            first_edit.send_keys('^a', pause=0.1)
            time.sleep(0.2)
            
            # Type the customer number
            first_edit.type_keys('4268', interval=0.1)
            time.sleep(0.5)
            
            print("  OK - Customer number 4268 entered")
            
            # Try to verify
            current_text = first_edit.window_text() if hasattr(first_edit, 'window_text') else ""
            print(f"  Field contains: '{current_text}'")
            
        except Exception as e2:
            print(f"  [X] Error entering text: {e2}")
    else:
        print("  [X] No Edit controls found")
        
except Exception as e:
    print(f"  [X] Error: {e}")

print("\n" + "=" * 70)
print("Done - Check the Take AR Payments window")
print("=" * 70)
