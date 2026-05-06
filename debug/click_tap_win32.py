"""
Use Win32 inspection to find Take AR Payments button and click it
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen
from pywinauto import findwindows
import ctypes
import time

print("=" * 70)
print("Finding Take AR Payments - Win32 Inspection")
print("=" * 70)

# Step 1: Navigate to Parts
print("\n[1] Navigating to Parts...")
nav = NavigatorScreen()
nav.click_menu_button('Parts')
time.sleep(1.5)

# Step 2: Get Navigator window
handles = findwindows.find_windows(title_re=".*Navigator.*")
nav_hwnd = handles[0]
print(f"    Navigator: {nav_hwnd}")

# Step 3: Find ultraExplorerBar control
print("\n[2] Finding ultraExplorerBar control...")
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
            # Recursively get children
            results.extend(enum_child_windows(child, max_depth, current_depth + 1))
        
        # Get next sibling
        child = GetWindow(child, 0)  # GW_HWNDNEXT = 0
    
    return results

print("    Enumerating child windows...")
children = enum_child_windows(nav_hwnd, max_depth=3)
print(f"    Found {len(children)} windows/controls")

# Find explorer bar and buttons
print("\n[3] Looking for Infragistics/explorer controls...")
explorer_bars = []
for child in children:
    if 'ultraExplorerBar' in child['class'] or 'UltraExplorerBar' in child['class']:
        explorer_bars.append(child)
        print(f"    Found ultraExplorerBar: {child['hwnd']}")

# Look for button-like controls with text
print("\n[4] Looking for button/control with 'Take AR Payments' text...")
all_controls = []
for child in children:
    if 'Take' in child['text'] or 'AR' in child['text'] or 'Payments' in child['text']:
        print(f"    [{child['hwnd']}] Class: {child['class']:30s} Text: {child['text']}")
        all_controls.append(child)

# If we found controls, try clicking them
if all_controls:
    print("\n[5] Attempting to click found controls...")
    for ctrl in all_controls:
        if 'Take' in ctrl['text']:
            hwnd = ctrl['hwnd']
            print(f"    Clicking: {ctrl['text']}")
            
            # Get window rectangle
            rect = ctypes.wintypes.RECT()
            GetWindowRect(hwnd, ctypes.byref(rect))
            
            center_x = rect.left + (rect.right - rect.left) // 2
            center_y = rect.top + (rect.bottom - rect.top) // 2
            
            print(f"    Position: ({rect.left}, {rect.top}) - ({rect.right}, {rect.bottom})")
            print(f"    Center: ({center_x}, {center_y})")
            
            # Send click message to this control
            # WM_LBUTTONDOWN = 0x0201, WM_LBUTTONUP = 0x0202
            PostMessage = ctypes.windll.user32.PostMessageW
            
            # Convert screen coords to client coords relative to control
            PostMessage(hwnd, 0x0201, 0, (center_y << 16) | center_x)
            PostMessage(hwnd, 0x0202, 0, (center_y << 16) | center_x)
            
            print(f"    [OK] Click message sent to {hwnd}")
            time.sleep(1.5)
            break

else:
    print("\n[!] No controls with 'Take/AR/Payments' text found")
    print("\n[6] All available controls in explorer bar:")
    print("-" * 70)
    for child in children:
        if child['text'].strip() and child['depth'] >= 1:
            print(f"    Class: {child['class']:30s} Text: {child['text'][:40]}")

print("\n" + "=" * 70)
print("Done - Check if Take AR Payments opened")
print("=" * 70)
