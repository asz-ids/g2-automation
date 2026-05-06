"""
Find Customer # text element and determine which Edit is next to it
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen
from pywinauto import Application, findwindows
import time

# nav = NavigatorScreen()
# nav.click_menu_button('Parts')
# time.sleep(1)
# nav.click_explorer_bar_button('Take AR Payments')
# time.sleep(2)

handles = findwindows.find_windows(title_re=".*Accounts Receivable.*")
if not handles:
    handles = findwindows.find_windows(title_re=".*Payment.*")
ar_hwnd = handles[0]

app_uia = Application(backend='uia').connect(handle=ar_hwnd)
window_uia = app_uia.window(handle=ar_hwnd)

# Find "Customer #" text in UIA
print("Looking for 'Customer #' in UIA...")
customer_rect = None
for elem in window_uia.descendants():
    try:
        text = elem.window_text() if hasattr(elem, 'window_text') else ""
        if text == "Customer #":
            print(f"Found: {elem}")
            try:
                rect_obj = elem.rectangle
                if callable(rect_obj):
                    customer_rect = rect_obj()
                else:
                    customer_rect = rect_obj
                    
                if customer_rect:
                    print(f"Position: X={customer_rect.left:4d}-{customer_rect.right:4d}, Y={customer_rect.top:4d}-{customer_rect.bottom:4d}")
            except:
                pass
            break
    except:
        pass

if not customer_rect:
    print("Not found in UIA, using coordinates from output above.")
    print("Customer # label is visible at top-left area")
    print("Looking for Edit near Y=99-129...")
    customer_rect_y = 99

# Now get Edit controls
app_win32 = Application(backend='win32').connect(handle=ar_hwnd)
window_win32 = app_win32.window(handle=ar_hwnd)
edit_list = window_win32.children(class_name='Edit')

import ctypes
GetWindowRect = ctypes.windll.user32.GetWindowRect

print("\n\nAll Edit controls:")
print("-" * 70)
candidates = []

for i, edit in enumerate(edit_list):
    try:
        rect = ctypes.wintypes.RECT()
        GetWindowRect(edit.handle, ctypes.byref(rect))
        text = edit.window_text() if hasattr(edit, 'window_text') else ""
        
        # Look for Edit controls on the same row as Customer # (around Y=99-129, but could vary)
        # And positioned to the right
        if rect.top >= 90 and rect.top <= 160:  # Top area where Customer # likely is
            print(f"[{i}] *CANDIDATE* X={rect.left:4d}, Y={rect.top:4d}, Width={rect.right-rect.left:3d}, Text: '{text}'")
            candidates.append((i, rect, text))
        else:
            print(f"[{i}]  X={rect.left:4d}, Y={rect.top:4d}, Text: '{text}'")
    except Exception as e:
        print(f"[{i}] Error: {e}")

print("\n" + "=" * 70)
if candidates:
    print(f"Found {len(candidates)} candidate Edit controls on Customer # row:")
    for idx, rect, text in candidates:
        print(f"  [{idx}] at X={rect.left}, Y={rect.top}, empty={text==''}  <- {'BEST (empty)' if text == '' else ''}")
        
    # Pick the empty one on the right
    empty_candidates = [(idx, rect, text) for idx, rect, text in candidates if text == '']
    if empty_candidates:
        # Get the one furthest to the right 
        best_idx, best_rect, _ = max(empty_candidates, key=lambda x: x[1].left)
        print(f"\n  BEST CHOICE: Edit[{best_idx}] at X={best_rect.left}")
