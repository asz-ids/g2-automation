"""
Find all Edit controls and their positions relative to Customer # label
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen
from pywinauto import Application, findwindows
import time

print("=" * 70)
print("Mapping All Edit Controls Near Customer # Label")
print("=" * 70)

# Navigate to Take AR Payments
print("\n[1] Navigate to Take AR Payments...")
nav = NavigatorScreen()
nav.click_menu_button('Parts')
time.sleep(1)
nav.click_explorer_bar_button('Take AR Payments')
time.sleep(2)

# Find window
handles = findwindows.find_windows(title_re=".*Accounts Receivable.*")
if not handles:
    handles = findwindows.find_windows(title_re=".*Payment.*")
ar_hwnd = handles[0]

# Connect
app_uia = Application(backend='uia').connect(handle=ar_hwnd)
window_uia = app_uia.window(handle=ar_hwnd)

# Find Customer # label
print("[2] Finding Customer # label...")
customer_label = None
label_rect = None
for elem in window_uia.descendants():
    try:
        elem_text = elem.window_text() if hasattr(elem, 'window_text') else ""
        if elem_text and "Customer #" in elem_text:
            customer_label = elem
            try:
                label_rect = elem.rectangle if hasattr(elem, 'rectangle') else None
                if label_rect:
                    print(f"    Label rect: left={label_rect.left}, right={label_rect.right}, top={label_rect.top}, bottom={label_rect.bottom}")
            except:
                pass
            break
    except:
        pass

if not customer_label:
    print("    [X] Label not found!")
    exit(1)

# Find ALL Edit controls and their positions
print("\n[3] All Edit controls in window:")
print("    " + "-" * 66)

edit_controls = []
for elem in window_uia.descendants():
    try:
        elem_type = elem.control_type if hasattr(elem, 'control_type') else None
        
        if elem_type == "Edit":
            try:
                elem_rect = elem.rectangle if hasattr(elem, 'rectangle') else None
                elem_text = elem.window_text() if hasattr(elem, 'window_text') else ""
                
                if elem_rect:
                    # Calculate distance from label
                    distance_x = elem_rect.left - (label_rect.right if label_rect else 0)
                    distance_y = elem_rect.top - (label_rect.top if label_rect else 0)
                    
                    print(f"    EDIT CONTROL:")
                    print(f"      Position: left={elem_rect.left}, top={elem_rect.top}, width={elem_rect.right-elem_rect.left}, height={elem_rect.bottom-elem_rect.top}")
                    print(f"      Distance from label: X={distance_x}, Y={distance_y}")
                    print(f"      Current text: '{elem_text}'")
                    print()
                    
                    edit_controls.append({
                        'elem': elem,
                        'rect': elem_rect,
                        'distance_x': distance_x,
                        'distance_y': distance_y,
                        'text': elem_text
                    })
            except:
                pass
    except:
        pass

print("=" * 70)

if edit_controls:
    print(f"\nFound {len(edit_controls)} Edit controls")
    
    # Find the one closest to the right of the label (likely the customer number field)
    closest = min(edit_controls, key=lambda x: abs(x['distance_x']) + abs(x['distance_y']) * 10)
    
    print(f"\nClosest Edit to Customer # label: distance_x={closest['distance_x']}, distance_y={closest['distance_y']}")
    
    # Enter the customer number
    print("\n[4] Entering customer number 4268...")
    try:
        elem = closest['elem']
        elem.click()
        time.sleep(0.3)
        
        # Clear and enter
        elem.send_keys('^a', pause=0.1)
        time.sleep(0.2)
        elem.type_keys('4268', interval=0.15)
        time.sleep(0.5)
        
        print("    OK - Customer number entered!")
        
        # Verify
        try:
            val = elem.window_text()
            print(f"    Field now contains: '{val}'")
        except:
            pass
        
    except Exception as e:
        print(f"    [X] Error: {e}")
        import traceback
        traceback.print_exc()

else:
    print("No Edit controls found!")

print("\n" + "=" * 70)
