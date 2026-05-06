"""
Enter 4268 in Customer # textbox (use existing window)
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from pywinauto import Application, findwindows
import time

print("=" * 70)
print("Enter Customer Number 4268")
print("=" * 70)

# Step 1: Find AR Payments window
print("\n[STEP 1] Find AR Payments window...")
handles = findwindows.find_windows(title_re=".*Accounts Receivable.*")
if not handles:
    handles = findwindows.find_windows(title_re=".*Payment.*")

if not handles:
    print("  ERROR: AR Payments window not found")
    print("  Please open Take AR Payments first")
    exit(1)

ar_hwnd = handles[0]
print(f"  OK - Window: {ar_hwnd}")

# Step 2: Connect
print("\n[STEP 2] Connect to window...")
app_uia = Application(backend='uia').connect(handle=ar_hwnd)
window_uia = app_uia.window(handle=ar_hwnd)
print("  OK - Connected")

# Step 3: Find Customer # label
print("\n[STEP 3] Find 'Customer #' label...")
label_rect = None

for elem in window_uia.descendants():
    try:
        text = elem.window_text() if hasattr(elem, 'window_text') else ""
        if text == "Customer #":
            try:
                label_rect = elem.rectangle if hasattr(elem, 'rectangle') else None
                if label_rect:
                    print(f"  OK - Label at X={label_rect.left}-{label_rect.right}, Y={label_rect.top}-{label_rect.bottom}")
            except:
                pass
            break
    except:
        pass

if not label_rect:
    print("  ERROR: Could not find Customer # label")
    exit(1)

# Step 4: Find Edit textbox next to it
print("\n[STEP 4] Find textbox next to label...")
textbox = None

for elem in window_uia.descendants():
    try:
        elem_type = elem.control_type if hasattr(elem, 'control_type') else None
        
        if elem_type == "Edit":
            try:
                rect = elem.rectangle if hasattr(elem, 'rectangle') else None
                if rect:
                    # Check if this Edit is on the same row, to the right of the label
                    y_diff = abs(rect.top - label_rect.top)
                    x_start = rect.left - label_rect.right
                    
                    # Should be within 25 pixels vertically, and very close horizontally (to the right)
                    if y_diff < 25 and x_start > -100 and x_start < 150:
                        textbox = elem
                        print(f"  OK - Found textbox at X={rect.left}, Y={rect.top}")
                        break
            except:
                pass
    except:
        pass

if not textbox:
    print("  WARNING: Could not find textbox using position matching")
    print("  Trying to find ANY Edit control...")
    
    for elem in window_uia.descendants():
        try:
            if elem.control_type == "Edit":
                textbox = elem
                print(f"  OK - Found Edit control")
                break
        except:
            pass

if not textbox:
    print("  ERROR: No Edit controls found!")
    exit(1)

# Step 5: Enter the customer number
print("\n[STEP 5] Enter 4268...")
try:
    textbox.click()
    print("  Clicked textbox")
    time.sleep(0.3)
    
    textbox.send_keys('^a', pause=0.1)
    time.sleep(0.2)
    
    textbox.type_keys('4268', interval=0.1)
    time.sleep(0.5)
    
    print("  OK - Typed 4268")
    
except Exception as e:
    print(f"  ERROR: {e}")
    exit(1)

print("\n" + "=" * 70)
print("SUCCESS!")
print("=" * 70)
