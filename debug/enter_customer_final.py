"""
Enter 4268 in the textbox right next to "Customer #" label
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen
from pywinauto import Application, findwindows
import time

print("=" * 70)
print("Enter Customer Number 4268")
print("=" * 70)

# # Step 1: Navigate to Take AR Payments
# print("\n[STEP 1] Navigate to Take AR Payments...")
# nav = NavigatorScreen()
# nav.click_menu_button('Parts')
# time.sleep(1)
# nav.click_explorer_bar_button('Take AR Payments')
# time.sleep(2)
# print("  OK - Take AR Payments opened")

# Step 2: Get the AR Payments window
print("\n[STEP 2] Get AR Payments window handle...")
handles = findwindows.find_windows(title_re=".*Accounts Receivable.*")
if not handles:
    handles = findwindows.find_windows(title_re=".*Payment.*")

if not handles:
    print("  ERROR: Could not find AR Payments window")
    exit(1)

ar_hwnd = handles[0]
print(f"  OK - Window: {ar_hwnd}")

# Step 3: Connect via UIA
print("\n[STEP 3] Connect to window...")
app_uia = Application(backend='uia').connect(handle=ar_hwnd)
window_uia = app_uia.window(handle=ar_hwnd)
print("  OK - Connected")

# Step 4: Find Customer # label and get its location
print("\n[STEP 4] Find 'Customer #' Pane (auto_id=9953220)...")
label_elem = None
label_rect = None

try:
    # Find the Customer # Pane using its auto_id
    label_elem = window_uia.child_window(control_type="Pane", auto_id="9953220")
    print("  OK - Found Customer # Pane")
    
    try:
        # rectangle might be a method or property
        if hasattr(label_elem, 'rectangle'):
            rect_obj = label_elem.rectangle
            if callable(rect_obj):
                label_rect = rect_obj()
            else:
                label_rect = rect_obj
        else:
            label_rect = None
            
        if label_rect:
            print(f"  OK - Position: X={label_rect.left}-{label_rect.right}, Y={label_rect.top}-{label_rect.bottom}")
    except Exception as rect_err:
        print(f"  Warning getting rectangle: {rect_err}")
        label_rect = None
except Exception as e:
    print(f"  ERROR: {e}")
    # Fallback: search by text
    print("  Falling back to text search...")
    label_elem = None
    label_rect = None
    for elem in window_uia.descendants():
        try:
            text = elem.window_text() if hasattr(elem, 'window_text') else ""
            if text == "Customer #":
                label_elem = elem
                try:
                    if hasattr(elem, 'rectangle'):
                        rect_obj = elem.rectangle
                        if callable(rect_obj):
                            label_rect = rect_obj()
                        else:
                            label_rect = rect_obj
                    if label_rect:
                        print(f"  Found label at X={label_rect.left}, Y={label_rect.top}")
                except:
                    pass
                break
        except:
            pass

if not label_elem or not label_rect:
    print("  ERROR: Could not find Customer # label")
    print("  Will proceed to find Edit control directly...")

# Step 5: Find Edit box for Customer #
print("\n[STEP 5] Finding Customer # textbox...")

# We'll skip the label position detection and just look for the empty Edit on the top row
textbox = None

try:
    # Connect using win32 backend instead
    app_win32 = Application(backend='win32').connect(handle=ar_hwnd)
    window_win32 = app_win32.window(handle=ar_hwnd)
    
    # Find Edit controls
    edit_list = window_win32.children(class_name='Edit')
    print(f"  Found {len(edit_list)} Edit controls via win32")
    
    if edit_list:
        # Find an enabled Edit control on the Customer # row (around Y=152)
        # that is empty (not the date field)
        target_edit = None
        
        for edit in edit_list:
            try:
                    import ctypes
                    rect = ctypes.wintypes.RECT()
                    ctypes.windll.user32.GetWindowRect(edit.handle, ctypes.byref(rect))
                    text = edit.window_text() if hasattr(edit, 'window_text') else ""
                    
                    # Look for Edit on same row as Customer # (Y around 152)
                    # and it should be empty
                    if (rect.top >= 140 and rect.top <= 165 and 
                        text == ''):
                        target_edit = edit
                        print(f"  Selected Edit at X={rect.left}, Y={rect.top} (Customer # field)")
                        break
                except:
                    pass
            
            if target_edit:
                textbox = target_edit
            else:
                # Fallback: find any enabled Edit
                for edit in edit_list:
                    try:
                        if hasattr(edit, 'is_enabled'):
                            is_enabled = edit.is_enabled()
                        else:
                            is_enabled = True
                        
                        if is_enabled:
                            textbox = edit
                            print(f"  Selected first enabled Edit (fallback)")
                            break
                    except:
                        textbox = edit
                        print(f"  Selected Edit (fallback)")
                        break
    except Exception as e:
        print(f"  Error with win32 backend: {e}")
        textbox = None

if not textbox:
    print("  Trying alternative: search for any input element...")

if not textbox or textbox is True:
    if textbox is True:
        print("  SUCCESS - Customer number entered!")
    else:
        print("  ERROR: No Edit controls found at all!")
        exit(1)
else:
    # Step 6: Enter the customer number
    print("\n[STEP 6] Entering 4268 into textbox...")
    try:
        # Click on the textbox to focus it (with error handling)
        try:
            textbox.click()
            print("  Clicked on textbox")
        except Exception as click_err:
            print(f"  Click failed ({click_err}), trying to set focus directly...")
            try:
                textbox.set_focus()
                print("  Set focus directly")
            except:
                print("  Could not click or set focus, proceeding anyway...")
        
        time.sleep(0.3)
        
        # Clear and type using pywinauto keyboard
        from pywinauto.keyboard import send_keys
        
        # Clear existing text (Ctrl+A to select all)
        send_keys('^a')
        time.sleep(0.2)
        
        # Type the customer number character by character
        for char in '4268':
            send_keys(char)
            time.sleep(0.15)
        time.sleep(0.5)
        
        print("  OK - Entered 4268")
        
        # Try to verify
        try:
            current_value = textbox.get_value() if hasattr(textbox, 'get_value') else textbox.window_text()
            print(f"  Textbox value: '{current_value}'")
        except:
            pass
        
    except Exception as e:
        print(f"  ERROR entering text: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
