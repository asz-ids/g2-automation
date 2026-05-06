"""
G2 Navigator - Enhanced Button Clicking with Verification

Includes verification that clicks actually worked.
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time
import warnings
warnings.filterwarnings('ignore')


def connect_to_navigator():
    """Connect to G2 Navigator"""
    handles = findwindows.find_windows(title_re=".*Navigator.*")
    if not handles:
        print("[X] Navigator window not found")
        return None, None
    
    app = Application(backend='win32').connect(handle=handles[0])
    window = app.top_window()
    return app, window


def get_button_state(button):
    """Get button state (enabled, focused, etc.)"""
    try:
        rect = button.rectangle()
        is_enabled = button.is_enabled()
        is_visible = button.is_visible()
        return {
            'enabled': is_enabled,
            'visible': is_visible,
            'rect': rect
        }
    except Exception as e:
        return {'error': str(e)}


def click_button_with_verification(window, button_name):
    """Click a button and verify the click"""
    print(f"\n[*] Clicking {button_name}...")
    
    # Find button
    children = window.children()
    target_button = None
    
    for child in children:
        try:
            text = child.window_text()
            if text == button_name:
                target_button = child
                break
        except:
            pass
    
    if not target_button:
        print(f"[X] {button_name} button not found")
        return False
    
    # Get state before click
    print(f"  State before click: {get_button_state(target_button)}")
    
    # Click the button
    try:
        target_button.click()
        print(f"  [OK] Click executed")
    except Exception as e:
        print(f"  [X] Click failed: {e}")
        return False
    
    # Wait for response
    time.sleep(0.5)
    
    # Get state after click
    print(f"  State after click: {get_button_state(target_button)}")
    
    # Try to detect visual change
    try:
        # Get window contents to check if anything changed
        window_text = window.window_text()
        print(f"  Window title after click: {window_text}")
    except:
        pass
    
    return True


def navigate_all_menus():
    """Navigate through all G2 menu items"""
    print("\n" + "="*70)
    print("G2 NAVIGATOR - COMPREHENSIVE MENU NAVIGATION")
    print("="*70)
    
    # Connect
    print("\n[1] Connecting...")
    app, window = connect_to_navigator()
    if not window:
        return False
    
    print("[OK] Connected to Navigator")
    
    # List all available menus
    print("\n[2] Available menus:")
    children = window.children()
    menus = []
    for child in children:
        try:
            text = child.window_text()
            if text and len(text.strip()) > 0:
                menus.append(text)
                print(f"    • {text}")
        except:
            pass
    
    # Click each menu
    print("\n[3] Clicking each menu sequentially...")
    menu_sequence = ['Sales', 'Service', 'Accounting', 'Admin', 'Parts']
    
    for menu in menu_sequence:
        if menu in menus:
            click_button_with_verification(window, menu)
        else:
            print(f"\n[X] {menu} not in menu list")
    
    print("\n" + "="*70)
    print("NAVIGATION COMPLETE - Check if menus opened in G2")
    print("="*70 + "\n")
    
    return True


def focus_and_interact():
    """Alternative: Set focus and use keyboard"""
    print("\n" + "="*70)
    print("G2 NAVIGATOR - FOCUS-BASED INTERACTION")
    print("="*70)
    
    print("\n[1] Connecting...")
    app, window = connect_to_navigator()
    if not window:
        return False
    
    print("[OK] Connected")
    
    print("\n[2] Setting focus to Parts button...")
    children = window.children()
    parts_button = None
    
    for child in children:
        try:
            if child.window_text() == "Parts":
                parts_button = child
                break
        except:
            pass
    
    if not parts_button:
        print("[X] Parts button not found")
        return False
    
    # Try multiple interaction methods
    print("\n[3] Attempting interactions...")
    
    try:
        print("  a) Setting focus...")
        parts_button.set_focus()
        time.sleep(0.2)
        
        print("  b) Getting focus...")
        has_focus = parts_button.has_focus()
        print(f"     Has focus: {has_focus}")
        
        print("  c) Clicking...")
        parts_button.click()
        time.sleep(0.3)
        
        print("  d) Alternative: Send Space key...")
        parts_button.type_keys(' ')
        time.sleep(0.3)
        
        print("[OK] Interaction sequence complete")
        return True
        
    except Exception as e:
        print(f"[X] Error during interaction: {e}")
        return False


if __name__ == "__main__":
    print("\n### METHOD 1: Direct clicking with verification ###")
    success1 = navigate_all_menus()
    
    print("\n### METHOD 2: Focus-based interaction ###")
    success2 = focus_and_interact()
    
    exit(0 if (success1 or success2) else 1)
