"""
Enter 4268 in the Customer # textbox in Take AR Payments
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen
from pywinauto import Application, findwindows
import time

print("=" * 70)
print("Enter Customer Number 4268")
print("=" * 70)

# Step 1: Navigate to Take AR Payments
# print("\n[STEP 1] Navigate to Take AR Payments...")
# nav = NavigatorScreen()
# nav.click_menu_button('Parts')
# time.sleep(1)
# nav.click_explorer_bar_button('Take AR Payments')
# print("  Waiting for window to open...")
# time.sleep(15)  # Wait longer for the window to fully open
# print("  OK - Take AR Payments opened")

# Step 2: Get the AR Payments window
print("\n[STEP 2] Get AR Payments window handle...")
handles = findwindows.find_windows(title_re=".*Accounts Receivable.*")
if not handles:
    handles = findwindows.find_windows(title_re=".*Payment.*")

if not handles:
    print("  ERROR: Could not find AR Payments window")
    print("  (Make sure Take AR Payments window is open)")
    exit(1)

ar_hwnd = handles[0]
print(f"  OK - Window: {ar_hwnd}")

# Verify it's the right window
print("\n[VERIFY] Checking window title...")
app_uia = Application(backend='uia').connect(handle=ar_hwnd)
window_uia = app_uia.window(handle=ar_hwnd)
window_title = window_uia.window_text() if hasattr(window_uia, 'window_text') else ""
print(f"  Window title: '{window_title}'")

if "Accounts Receivable" not in window_title and "Payment" not in window_title:
    print("  WARNING: This may not be the AR Payment window!")
    print("  Proceeding anyway...")

# Step 3: Connect to window via win32 backend
print("\n[STEP 3] Connect to window (win32 backend)...")
app_win32 = Application(backend='win32').connect(handle=ar_hwnd)
window_win32 = app_win32.window(handle=ar_hwnd)
print("  OK - Connected")

# Step 4: Find all Edit controls
print("\n[STEP 4] Finding Edit controls...")
edit_list = window_win32.children(class_name='Edit')
print(f"  Found {len(edit_list)} Edit controls")

# Step 5: Find the Customer # textbox (empty Edit on row Y=152)
print("\n[STEP 5] Selecting Customer # textbox...")
textbox = None
import ctypes
GetWindowRect = ctypes.windll.user32.GetWindowRect

for i, edit in enumerate(edit_list):
    try:
        rect = ctypes.wintypes.RECT()
        GetWindowRect(edit.handle, ctypes.byref(rect))
        text = edit.window_text() if hasattr(edit, 'window_text') else ""
        
        # Look for empty Edit on the Customer # row (around Y=152)
        if (rect.top >= 140 and rect.top <= 165 and text == ''):
            textbox = edit
            print(f"  OK - Selected Edit #{i} at X={rect.left}, Y={rect.top}")
            break
    except:
        pass

if not textbox:
    print("  ERROR: Could not find Customer # textbox")
    exit(1)

# Step 6: Enter the customer number
print("\n[STEP 6] Entering 4268...")
try:
    # Click to focus
    textbox.click()
    print("  Clicked on textbox")
    time.sleep(0.3)
    
    # Clear existing text (Ctrl+A)
    from pywinauto.keyboard import send_keys
    send_keys('^a')
    time.sleep(0.2)
    
    # Type the customer number
    for char in '4268':
        send_keys(char)
        time.sleep(0.15)
    
    time.sleep(0.5)
    print("  OK - Entered 4268")
    
    # Verify
    try:
        value = textbox.window_text() if hasattr(textbox, 'window_text') else ""
        print(f"  Textbox value: '{value}'")
    except:
        pass
    
    # Press Tab to move to the next field
    print("\n[STEP 7] Pressing Tab...")
    from pywinauto.keyboard import send_keys
    send_keys('{TAB}')
    time.sleep(0.5)
    print("  OK - Tab pressed")
    
    # Wait for table to load with data
    print("\n[STEP 8] Waiting for table to load...")
    time.sleep(5)  # Wait longer for data to populate
    print("  OK - Table should be loaded")
    
    # Step 9: Click checkbox on first row
    print("\n[STEP 9] Finding and clicking checkbox on first row...")
    
    # Reconnect to window to get updated structure
    app_uia = Application(backend='uia').connect(handle=ar_hwnd)
    window_uia = app_uia.window(handle=ar_hwnd)
    
    # Find all "Pay" DataItems and click the first one
    try:
        # Find the first row's Pay checkbox
        pay_items = window_uia.children(control_type="DataItem", title="Pay")
        if pay_items:
            # Get the first one
            first_pay = pay_items[0]
            print(f"  Found first 'Pay' DataItem")
            
            # Use Space key to toggle checkbox (confirmed working)
            first_pay.set_focus()
            time.sleep(0.2)
            from pywinauto.keyboard import send_keys
            send_keys(' ')  # Space to toggle checkbox
            print("  OK - Pressed Space on first row checkbox")
            time.sleep(0.5)
        else:
            print("  No Pay DataItems found")
            
    except Exception as e:
        print(f"  ERROR: {e}")
        print("  Trying alternative: search all DataItems...")
        
        try:
            # Get all DataItems
            all_items = window_uia.descendants(control_type="DataItem")
            
            # Find the first one that is a "Pay" checkbox
            for item in all_items:
                try:
                    text = item.window_text() if hasattr(item, 'window_text') else ""
                    if text == "Pay":
                        print(f"  Found first Pay item")
                        item.click()
                        print("  OK - Clicked checkbox")
                        time.sleep(0.5)
                        break
                except:
                    pass
                    
        except Exception as e2:
            print(f"  Alternative also failed: {e2}")
    
except Exception as e:
    print(f"  ERROR: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "=" * 70)
print("SUCCESS - Customer number 4268 entered in textbox")
print("=" * 70)

# Step 10: Click Accept Payment button
print("\n[STEP 10] Finding and clicking Accept Payment button...")
try:
    # Get updated window structure
    app_uia = Application(backend='uia').connect(handle=ar_hwnd)
    window_uia = app_uia.window(handle=ar_hwnd)
    
    # Look for the Accept Payment button/pane (auto_id 12045988)
    # Try finding by control type
    buttons = window_uia.descendants(control_type="Button")
    found_button = False
    
    for btn in buttons:
        try:
            text = btn.window_text() if hasattr(btn, 'window_text') else ""
            if "Accept" in text and "Payment" in text:
                print(f"  Found: {text}")
                btn.click()
                print("  OK - Clicked Accept Payment button")
                found_button = True
                time.sleep(1)
                break
        except:
            pass
    
    if not found_button:
        # Try Pane with specific auto_id
        print("  Button not found by text, trying Pane...")
        panes = window_uia.descendants(control_type="Pane")
        for pane in panes:
            try:
                auto_id = pane.automation_id if hasattr(pane, 'automation_id') else ""
                if auto_id == "12045988":
                    print(f"  Found Pane with auto_id 12045988")
                    pane.click()
                    print("  OK - Clicked Accept Payment pane")
                    time.sleep(1)
                    found_button = True
                    break
            except:
                pass
    
    if not found_button:
        print("  WARNING: Could not find Accept Payment button")
        print("  Available buttons:")
        for btn in buttons[:5]:
            try:
                text = btn.window_text() if hasattr(btn, 'window_text') else ""
                print(f"    - {text}")
            except:
                pass
    
except Exception as e:
    print(f"  ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("Workflow Complete")
print("=" * 70)
