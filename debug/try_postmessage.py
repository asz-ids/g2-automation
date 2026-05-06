"""
Send WM_COMMAND messages to trigger button actions
"""

from pywinauto import findwindows
from pywinauto.application import Application
from ctypes import windll, c_int
import time
import warnings
warnings.filterwarnings('ignore')

# Common button commands
WM_COMMAND = 273
BN_CLICKED = 0

print("[1] Connecting to Navigator...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()
nav_hwnd = nav_handles[0]

print(f"    Navigator HWND: {nav_hwnd}")

print("\n[2] Enumerating child windows to find button IDs...")
children = window.children()
print(f"    Total children: {len(children)}")

# Get all child window handles
child_handles = {}
for i, child in enumerate(children):
    try:
        text = child.window_text()
        handle = child.handle
        cls = child.class_name()
        
        if text in ["Sales", "Service", "Accounting", "Admin", "Parts"]:
            child_handles[text] = (handle, i)
            print(f"    Found {text}: HWND={handle}, Index={i}")
    except:
        pass

print(f"\n[3] Trying different message approaches...")

if child_handles:
    sales_hwnd, sales_idx = child_handles['Sales']
    
    print(f"\n    Sales button HWND: {sales_hwnd}")
    
    # Method 1: PostMessage with WM_LBUTTONUP/DOWN
    print(f"\n    Method 1: WM_LBUTTON messages...")
    try:
        WM_LBUTTONDOWN = 513
        WM_LBUTTONUP = 514
        
        windll.user32.PostMessageW(sales_hwnd, WM_LBUTTONDOWN, 0, 0)
        time.sleep(0.1)
        windll.user32.PostMessageW(sales_hwnd, WM_LBUTTONUP, 0, 0)
        time.sleep(2)
        
        print(f"      Posted WM_LBUTTON messages")
    except Exception as e:
        print(f"      Error: {e}")
    
    # Check result
    try:
        sales_handles = findwindows.find_windows(title_re=".*Sales.*")
        if sales_handles:
            print(f"      ✓ SUCCESS! Sales screen opened!")
            exit(0)
    except:
        pass
    
    # Method 2: BM_CLICK
    print(f"\n    Method 2: BM_CLICK...")
    try:
        BM_CLICK = 245
        windll.user32.PostMessageW(sales_hwnd, BM_CLICK, 0, 0)
        time.sleep(2)
        print(f"      Posted BM_CLICK")
    except Exception as e:
        print(f"      Error: {e}")
    
    # Check result
    try:
        sales_handles = findwindows.find_windows(title_re=".*Sales.*")
        if sales_handles:
            print(f"      ✓ SUCCESS! Sales screen opened!")
            exit(0)
    except:
        pass
    
    # Method 3: WM_COMMAND to parent
    print(f"\n    Method 3: WM_COMMAND to parent...")
    try:
        # Try control IDs (guessing based on index)
        for control_id in [sales_idx, 1001, 1000+sales_idx, sales_hwnd & 0xFFFF]:
            print(f"      Trying control ID: {control_id}")
            lparam = (sales_hwnd & 0xFFFF) | ((sales_hwnd >> 16) << 16)
            windll.user32.PostMessageW(nav_hwnd, WM_COMMAND, (BN_CLICKED << 16) | control_id, lparam)
            time.sleep(1)
            
            sales_handles = findwindows.find_windows(title_re=".*Sales.*")
            if sales_handles:
                print(f"        ✓ SUCCESS with ID {control_id}!")
                exit(0)
    except Exception as e:
        print(f"      Error: {e}")

print("\nNo method worked")
