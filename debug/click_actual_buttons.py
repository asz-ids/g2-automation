"""
Click the actual buttons by automation ID and try different click methods
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time

print("[1] Getting the actual btnSales element...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()

children = window.children()
btn_sales = None

# Find by automation ID
for i, child in enumerate(children):
    try:
        props = child.get_properties()
        if props.get('automation_id') == 'btnSales':
            btn_sales = child
            print(f"    Found btnSales at index {i}")
            print(f"    Properties: {props}")
            break
    except:
        pass

if not btn_sales:
    print("[X] Could not find btnSales")
    exit(1)

print(f"\n[2] Method 1: Regular click()...")
try:
    btn_sales.click()
    print(f"    Clicked")
    time.sleep(3)
    
    nav_handles2 = findwindows.find_windows(title_re=".*Navigator.*")
    app2 = Application(backend='win32').connect(handle=nav_handles2[0])
    window2 = app2.top_window()
    print(f"    Result: {len(window2.children())} children")
    
except Exception as e:
    print(f"    Error: {e}")

print(f"\n[3] Method 2: click_input()...")
try:
    btn_sales.click_input()
    print(f"    Clicked")
    time.sleep(3)
    
    nav_handles2 = findwindows.find_windows(title_re=".*Navigator.*")
    app2 = Application(backend='win32').connect(handle=nav_handles2[0])
    window2 = app2.top_window()
    print(f"    Result: {len(window2.children())} children")
    
except Exception as e:
    print(f"    Error: {e}")

print(f"\n[4] Method 3: double_click()...")
try:
    btn_sales.double_click()
    print(f"    Double-clicked")
    time.sleep(3)
    
    nav_handles2 = findwindows.find_windows(title_re=".*Navigator.*")
    app2 = Application(backend='win32').connect(handle=nav_handles2[0])
    window2 = app2.top_window()
    print(f"    Result: {len(window2.children())} children")
    
except Exception as e:
    print(f"    Error: {e}")

print(f"\n[5] Method 4: Detailed properties after button found...")
try:
    rect = btn_sales.rectangle()
    print(f"    Rectangle: {rect}")
    print(f"    Size: {rect.width()} x {rect.height()}")
    print(f"    Center: ({(rect.left + rect.right)//2}, {(rect.top + rect.bottom)//2})")
    print(f"    Enabled: {btn_sales.is_enabled()}")
    print(f"    Visible: {btn_sales.is_visible()}")
    
    # Try right-click to see if there's a context menu
    print(f"\n    Trying right_click...")
    btn_sales.right_click()
    time.sleep(2)
    
    nav_handles2 = findwindows.find_windows(title_re=".*Navigator.*")
    app2 = Application(backend='win32').connect(handle=nav_handles2[0])
    window2 = app2.top_window()
    print(f"    Result: {len(window2.children())} children")
    
except Exception as e:
    print(f"    Error: {e}")

print(f"\nDone.")
