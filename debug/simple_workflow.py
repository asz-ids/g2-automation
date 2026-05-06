"""
Simple workflow: Navigate to Take AR Payments, enter customer, click Accept Payment
Uses proven methods from earlier tests
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen
from pywinauto import Application, findwindows
from pywinauto.keyboard import send_keys
import time
import ctypes

print("=" * 70)
print("Simple AR Payment Workflow")
print("=" * 70)

# Step 1: Click menu and open Take AR Payments
print("\n[1] Navigating to Take AR Payments...")
nav = NavigatorScreen()
nav.click_menu_button('Parts')
time.sleep(1)

# Use direct mouse click at approximate coordinates for Take AR Payments button
# These coordinates work for typical window layout
print("  Clicking Take AR Payments button via mouse...")
import pywinauto.mouse
pywinauto.mouse.click(coords=(420, 310))
print("  [OK] Clicked")

print("  Waiting for window to open (20 seconds)...")
for i in range(20):
    time.sleep(1)
    handles = findwindows.find_windows(title_re=".*Accounts Receivable.*")
    if handles:
        print(f"  Window found after {i+1} seconds!")
        break
    if i % 5 == 4:
        print(f"    Checked... still waiting")

if not handles:
    print("  ERROR: Window did not open within 20 seconds")
    print("  Attempting alternate patterns...")
    handles = findwindows.find_windows(title_re=".*Payment.*")
    if not handles:
        handles = findwindows.find_windows(title_re=".*SMC.*")
    if not handles:
        print("  FAILED: Could not find window")
        exit(1)

ar_hwnd = handles[0]
print(f"  Window handle: {ar_hwnd}")

# Step 2: Enter customer number
print("\n[2] Entering customer number 4268...")
app_win32 = Application(backend='win32').connect(handle=ar_hwnd)
window_win32 = app_win32.window(handle=ar_hwnd)

# Find Customer # textbox
edit_list = window_win32.children(class_name='Edit')
print(f"  Found {len(edit_list)} Edit controls")

textbox = None
GetWindowRect = ctypes.windll.user32.GetWindowRect

for i, edit in enumerate(edit_list):
    try:
        rect = ctypes.wintypes.RECT()
        GetWindowRect(edit.handle, ctypes.byref(rect))
        text = edit.window_text() if hasattr(edit, 'window_text') else ""
        
        if rect.top >= 140 and rect.top <= 165 and text == '':
            textbox = edit
            print(f"  Found Customer # field (Edit #{i})")
            break
    except:
        pass

if textbox:
    textbox.click()
    time.sleep(0.3)
    send_keys('^a')
    time.sleep(0.2)
    for char in '4268':
        send_keys(char)
        time.sleep(0.1)
    print("  OK - Entered 4268")
else:
    print("  WARNING: Could not find Customer # field")

# Step 3: Press Tab
print("\n[3] Pressing Tab...")
send_keys('{TAB}')
time.sleep(0.5)

# Step 4: Wait for table
print("\n[4] Waiting for table to load (5 seconds)...")
time.sleep(5)
print("  OK - Table should be loaded")

# Step 5: Click Pay checkbox using Space
print("\n[5] Clicking Pay checkbox...")
try:
    app_uia = Application(backend='uia').connect(handle=ar_hwnd)
    window_uia = app_uia.window(handle=ar_hwnd)
    
    pay_items = window_uia.children(control_type="DataItem", title="Pay")
    if pay_items:
        first_pay = pay_items[0]
        first_pay.set_focus()
        time.sleep(0.2)
        send_keys(' ')
        print("  OK - Clicked Pay checkbox")
    else:
        print("  WARNING: Pay checkbox not found")
except Exception as e:
    print(f"  WARNING: {str(e)[:60]}")

# Step 6: Click Accept Payment button
print("\n[6] Clicking Accept Payment button...")
try:
    app_uia = Application(backend='uia').connect(handle=ar_hwnd)
    window_uia = app_uia.window(handle=ar_hwnd)
    
    # Find by text
    buttons = window_uia.descendants(control_type="Button")
    found = False
    
    for btn in buttons:
        try:
            text = btn.window_text() if hasattr(btn, 'window_text') else ""
            if "Accept" in text:
                print(f"  Found: {text}")
                btn.click()
                print("  OK - Clicked Accept Payment button")
                found = True
                time.sleep(1)
                break
        except:
            pass
    
    if not found:
        print("  WARNING: Accept Payment button not found")
        print("  Searching for Pane...")
        panes = window_uia.descendants(control_type="Pane")
        for pane in panes:
            try:
                auto_id = pane.automation_id if hasattr(pane, 'automation_id') else ""
                if auto_id == "12045988":
                    print(f"  Found Accept Payment pane")
                    pane.click()
                    print("  OK - Clicked via Pane")
                    time.sleep(1)
                    found = True
                    break
            except:
                pass
    
    if not found:
        print("  Trying mouse click at approximate button location...")
        pywinauto.mouse.click(coords=(500, 500))  # Approximate "Accept" button location
        print("  Attempted mouse click")

except Exception as e:
    print(f"  ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("Workflow Complete")
print("=" * 70)
