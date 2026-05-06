# G2 Navigator Button Click Solution - WORKING

## Problem
The G2 Navigator menu buttons (Sales, Service, Accounting, Admin, Parts) were not responding to standard pywinauto click methods. All approaches failed:
- `button.click()`
- `button.click_input()`
- Mouse events
- Keyboard shortcuts
- WM_COMMAND messages
- Even with 32-bit Python (after discovering the 64-bit app mismatch)

## Root Cause
These buttons are **custom WindowsForms controls** in an Infragistics UI framework that:
1. Don't respond to standard Win32 click simulation
2. Don't expose proper UIA interfaces for event triggering
3. Require specific window message handling

## Solution
Send **WM_LBUTTONDOWN (0x0201) and WM_LBUTTONUP (0x0202)** messages directly to the button handles using `ctypes.windll.user32.SendMessageW()`.

## Implementation Details

### Key Discovery
- Buttons are WindowsForms controls with automation IDs: `btnSales`, `btnService`, `btnAccounting`, `btnAdmin`, `btnParts`
- Content panels are toggled by visibility (1135x134 sized elements)
- Panels have text labels matching menu names: 'Sales', 'Service', 'Accounting', 'Admin', 'Parts'

### Code Solution
```python
import ctypes
import time

def click_button_via_message(button_handle: int):
    """Click button by sending WM_LBUTTONDOWN/UP messages"""
    WM_LBUTTONDOWN = 0x0201
    WM_LBUTTONUP = 0x0202
    
    ctypes.windll.user32.SendMessageW(button_handle, WM_LBUTTONDOWN, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.SendMessageW(button_handle, WM_LBUTTONUP, 0, 0)
    time.sleep(0.3)
```

## Updated NavigatorScreen Methods

### `click_menu_button(menu_name: str) -> bool`
Clicks a menu button to navigate to that menu.
- Parameters: menu_name (Sales, Service, Accounting, Admin, Parts)
- Returns: True if successful and menu became active
- Example: `nav.click_menu_button('Service')`

### `get_active_menu() -> Optional[str]`
Gets the currently active menu.
- Returns: Name of active menu or None
- Example: `current = nav.get_active_menu()` → returns 'Service'

### `_find_button_by_automation_id(automation_id: str) -> Optional[Dict]`
Finds a button by automation ID (internal use).
- Searches through Navigator children for matching automation ID

### `_find_panel_by_label(menu_name: str) -> Optional[Dict]`
Finds a content panel by its menu label (internal use).
- Looks for large content panels (>1000 width) with matching text

### `_click_button_via_message(button_handle: int) -> bool`
Sends message-based click to button (internal use).
- Uses ctypes to send WM_LBUTTONDOWN and WM_LBUTTONUP

## Testing Results
All 5 menu buttons tested and working:
✓ Sales
✓ Service  
✓ Accounting
✓ Admin
✓ Parts

## Files Modified
1. `screens/navigator_screen.py` - Added button click methods
2. `screens/navigator_screen_fixed.py` - Standalone working implementation (for reference)

## Usage Example
```python
from screens.navigator_screen import NavigatorScreen

nav = NavigatorScreen()

# Click Service menu
nav.click_menu_button('Service')

# Check what's active
active = nav.get_active_menu()  # Returns: 'Service'

# Click another menu
nav.click_menu_button('Accounting')

active = nav.get_active_menu()  # Returns: 'Accounting'
```

## Key Learnings
1. Not all Windows automation issues are solvable with standard approaches
2. Custom UI frameworks may require message-level interaction
3. Window handles and automation IDs are essential for direct messaging
4. Testing with actual window messages revealed the working solution
5. 32-bit vs 64-bit wasn't the real issue - it was the control type

## What Didn't Work (for reference)
- pywinauto click() methods
- Mouse coordinate clicking
- Keyboard activation
- WM_COMMAND messages to parent
- UIA invoke patterns
- ShowWindow API toggle (panel visibility can be toggled but doesn't trigger button logic)
- Different click notification codes

## Conclusion
The solution is robust, efficient, and properly integrated into the NavigatorScreen class. All G2 Navigator menu navigation now works reliably through automation.
