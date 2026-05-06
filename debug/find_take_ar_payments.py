"""
Map the Parts explorer bar to find Take AR Payments button location
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen
from pywinauto import Application, findwindows
import time

print("=" * 70)
print("Mapping Parts Explorer Bar - Finding Take AR Payments")
print("=" * 70)

# Step 1: Navigate to Parts
print("\n[1] Navigating to Parts...")
nav = NavigatorScreen()
nav.click_menu_button('Parts')
time.sleep(1.5)

# Step 2: Get UIA window
print("\n[2] Analyzing explorer bar structure...")
handles = findwindows.find_windows(title_re=".*Navigator.*")
app_uia = Application(backend='uia').connect(handle=handles[0])
window_uia = app_uia.window(handle=handles[0])

# Step 3: Find all text elements (these could be buttons)
print("\n[3] All clickable elements in Parts menu:")
print("-" * 70)

element_list = []
for elem in window_uia.descendants():
    try:
        # Check if element has text and size
        if hasattr(elem, 'name') and elem.name and elem.name.strip():
            try:
                rect = elem.rectangle
                if rect and rect.width > 0 and rect.height > 0:
                    # Filter to reasonable sizes (buttons/items in explorer bar)
                    if 100 < rect.width < 500 and 20 < rect.height < 100:
                        element_list.append({
                            'name': elem.name,
                            'x': rect.left,
                            'y': rect.top,
                            'width': rect.width,
                            'height': rect.height,
                            'element': elem
                        })
            except:
                pass
    except:
        pass

# Remove duplicates and sort by position
seen = set()
unique_elements = []
for e in element_list:
    key = (e['name'], e['x'], e['y'])
    if key not in seen:
        seen.add(key)
        unique_elements.append(e)

unique_elements.sort(key=lambda x: (x['y'], x['x']))

for i, elem in enumerate(unique_elements):
    marker = " <-- TAKE AR PAYMENTS" if "Take AR Payments" in elem['name'] else ""
    print(f"[{i:2d}] Y:{elem['y']:4d} X:{elem['x']:4d} | W:{elem['width']:3d} H:{elem['height']:2d} | {elem['name'][:50]}{marker}")

# Find Take AR Payments specifically
print("\n" + "=" * 70)
print("Take AR Payments Button Location:")
print("=" * 70)

take_ar_elem = None
for elem in unique_elements:
    if "Take AR Payments" in elem['name']:
        take_ar_elem = elem
        break

if take_ar_elem:
    # Calculate center point
    center_x = take_ar_elem['x'] + take_ar_elem['width'] // 2
    center_y = take_ar_elem['y'] + take_ar_elem['height'] // 2
    
    print(f"\nName: {take_ar_elem['name']}")
    print(f"Position: ({take_ar_elem['x']}, {take_ar_elem['y']})")
    print(f"Size: {take_ar_elem['width']} x {take_ar_elem['height']}")
    print(f"Center: ({center_x}, {center_y})")
    print(f"\n[OK] Button found!")
    print(f"\nTo click it, use coordinates: ({center_x}, {center_y})")
    
    print(f"\n[4] Attempting to click at ({center_x}, {center_y})...")
    from pywinauto import mouse
    mouse.click(coords=(center_x, center_y))
    print("    [OK] Click sent!")
    time.sleep(2)
    
    # Check if screen changed
    print("\n[5] Checking if Take AR Payments opened...")
    print("    (Check the G2 window to see if the screen changed)")
    
else:
    print("\n[!] Take AR Payments button not found in UIA tree")
    print("\nAvailable options in explorer bar:")
    for elem in unique_elements[:10]:
        print(f"  - {elem['name']}")

print("\n" + "=" * 70)
