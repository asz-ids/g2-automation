"""
Use Win32 to find and click the Customer # input field
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from pywinauto import findwindows
import ctypes
import time

print("Finding Customer # textbox and entering 4268...\n")

# Find window
handles = findwindows.find_windows(title_re=".*Accounts Receivable.*")
if not handles:
    handles = findwindows.find_windows(title_re=".*Payment.*")

ar_hwnd = handles[0]
print(f"AR Payments window: {ar_hwnd}")

# Win32 APIs
GetWindow = ctypes.windll.user32.GetWindow
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
GetClassName = ctypes.windll.user32.GetClassNameW
GetWindowRect = ctypes.windll.user32.GetWindowRect
SetFocus = ctypes.windll.user32.SetFocus
PostMessage = ctypes.windll.user32.PostMessageW

def get_text(hwnd):
    length = GetWindowTextLength(hwnd)
    if length == 0:
        return ""
    buf = ctypes.create_unicode_buffer(length + 1)
    GetWindowText(hwnd, buf, length + 1)
    return buf.value

def get_class(hwnd):
    buf = ctypes.create_unicode_buffer(256)
    GetClassName(hwnd, buf, 256)
    return buf.value

# Find all child windows
print("\nSearching for Edit controls...\n")

def find_children(hwnd, depth=0, max_depth=5):
    if depth > max_depth:
        return
    
    child = GetWindow(hwnd, 5)  # GW_CHILD
    while child:
        cls = get_class(child)
        txt = get_text(child)
        
        if cls == 'Edit':
            print(f"EDIT CONTROL FOUND: '{txt}'")
            print(f"  Handle: {child}")
            print(f"  Class: {cls}")
        
        if txt == "Customer #":
            print(f"LABEL FOUND: 'Customer #'")
            print(f"  Handle: {child}")
            
        # Check next sibling
        next_child = GetWindow(child, 0)  # GW_HWNDNEXT
        
        # Also recurse into children
        find_children(child, depth + 1, max_depth)
        
        child = next_child

find_children(ar_hwnd)

print("\nDone searching")
