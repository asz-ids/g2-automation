"""
Test: Enter customer number using Win32 window inspection
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen
from pywinauto import Application, findwindows
import ctypes
import time

print("=" * 70)
print("TEST: Enter Customer Number - Win32 Method")
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

# Step 3: Use Win32 to find Edit controls
print("\n[STEP 3] Finding Edit controls using Win32...")

GetWindow = ctypes.windll.user32.GetWindow
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
GetClassName = ctypes.windll.user32.GetClassNameW
GetWindowRect = ctypes.windll.user32.GetWindowRect

def get_window_text(hwnd):
    length = GetWindowTextLength(hwnd)
    if length == 0:
        return ""
    buffer = ctypes.create_unicode_buffer(length + 1)
    GetWindowText(hwnd, buffer, length + 1)
    return buffer.value

def get_class_name(hwnd):
    buffer = ctypes.create_unicode_buffer(256)
    GetClassName(hwnd, buffer, 256)
    return buffer.value

def enum_child_windows(hwnd, max_depth=5, current_depth=0):
    """Recursively find all child windows"""
    results = []
    
    child = GetWindow(hwnd, 5)  # GW_CHILD = 5
    
    while child:
        class_name = get_class_name(child)
        text = get_window_text(child)
        
        results.append({
            'hwnd': child,
            'class': class_name,
            'text': text,
            'depth': current_depth
        })
        
        if current_depth < max_depth:
            results.extend(enum_child_windows(child, max_depth, current_depth + 1))
        
        child = GetWindow(child, 0)  # GW_HWNDNEXT = 0
    
    return results

children = enum_child_windows(ar_hwnd, max_depth=4)
print(f"  Found {len(children)} total windows/controls")

# Find Edit controls
print("\n[STEP 4] Edit controls found:")
print("  " + "-" * 66)
edit_controls = []
for child in children:
    if child['class'] == 'Edit':
        edit_controls.append(child)
        rect = ctypes.wintypes.RECT()
        GetWindowRect(child['hwnd'], ctypes.byref(rect))
        print(f"  [{child['hwnd']}] Text: '{child['text'][:40]}' | Pos: ({rect.left}, {rect.top})")

if not edit_controls:
    print("  No Edit controls found via Win32 either")
    print("\n  All controls in window:")
    for child in children[:20]:
        print(f"    Class: {child['class']:20s} Text: {child['text'][:40]}")
else:
    print(f"\n  Found {len(edit_controls)} Edit controls")
    
    # Try to enter text in the first Edit control
    print("\n[STEP 5] Entering customer number 4268 in first Edit control...")
    first_edit = edit_controls[0]['hwnd']
    
    try:
        # Set focus to the control
        ctypes.windll.user32.SetFocus(first_edit)
        time.sleep(0.3)
        
        # Send the text
        from pywinauto import keyboard
        keyboard.write('4268', interval=0.1)
        time.sleep(0.5)
        
        # Verify
        text = get_window_text(first_edit)
        print(f"  OK - Entered text")
        print(f"  Control text now: '{text}'")
        
    except Exception as e:
        print(f"  [X] Error: {e}")

print("\n" + "=" * 70)
print("Done - Check Take AR Payments window")
print("=" * 70)
