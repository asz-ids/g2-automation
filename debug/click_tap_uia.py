"""
Click Take AR Payments using UIA Button selector
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen
from pywinauto import Application, findwindows
import time

print("=" * 70)
print("Clicking Take AR Payments via UIA Button")
print("=" * 70)

# Step 1: Navigate to Parts
print("\n[1] Navigating to Parts...")
nav = NavigatorScreen()
nav.click_menu_button('Parts')
time.sleep(1.5)

# Step 2: Connect to Navigator window
print("\n[2] Connecting to Navigator window...")
handles = findwindows.find_windows(title_re=".*Navigator.*")
app_uia = Application(backend='uia').connect(handle=handles[0])
window_uia = app_uia.window(handle=handles[0])
print("    [OK] Connected")

# Step 3: Find the button using the selector
print("\n[3] Finding Take AR Payments button...")
try:
    # Method 1: Direct selector
    button = window_uia.child_window(control_type="Button", title="Take AR Payments")
    print(f"    [OK] Found button: {button}")
    
    # Step 4: Click it
    print("\n[4] Clicking button...")
    button.click()
    print("    [OK] Button clicked!")
    time.sleep(2)
    
    print("\n[OK] SUCCESS - Take AR Payments should now be open")
    
except Exception as e:
    print(f"    [ERROR] Could not find/click button: {e}")
    print("\n[5] Trying alternative method - find all buttons...")
    
    buttons = window_uia.children(control_type="Button")
    print(f"    Found {len(buttons)} buttons total")
    
    for i, btn in enumerate(buttons):
        try:
            print(f"    [{i}] {btn.window_text()}")
            if "Take AR Payments" in btn.window_text():
                print(f"        -> Clicking this one")
                btn.click()
                print("        [OK] Clicked!")
                time.sleep(2)
                break
        except:
            pass

print("\n" + "=" * 70)
