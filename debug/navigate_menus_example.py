"""
G2 Navigator Menu Interaction Example

Demonstrates navigating through different menu items in G2 Navigator.
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time
import warnings
warnings.filterwarnings('ignore')


def connect_to_navigator():
    """Connect to the G2 Navigator window"""
    handles = findwindows.find_windows(title_re=".*Navigator.*")
    if not handles:
        print("[X] Navigator window not found. Please log into G2 first.")
        return None
    
    app = Application(backend='win32').connect(handle=handles[0])
    window = app.top_window()
    return window


def click_menu_item(window, menu_name):
    """Click a menu item by name"""
    children = window.children()
    for child in children:
        try:
            text = child.window_text()
            if text == menu_name:
                print(f"[OK] Clicking {menu_name}...")
                child.click()
                time.sleep(1)  # Wait for menu to open
                return True
        except:
            pass
    
    print(f"[X] {menu_name} button not found")
    return False


def get_all_menu_items(window):
    """Get all available menu items"""
    menu_items = []
    children = window.children()
    for child in children:
        try:
            text = child.window_text()
            if text and len(text.strip()) > 0:
                menu_items.append(text)
        except:
            pass
    
    return sorted(list(set(menu_items)))


def main():
    """Main navigation demo"""
    print("\n" + "="*70)
    print("G2 NAVIGATOR - MENU INTERACTION DEMO")
    print("="*70)
    
    # Connect to Navigator
    print("\n[1] Connecting to G2 Navigator...")
    window = connect_to_navigator()
    if not window:
        return False
    
    print("[OK] Connected successfully")
    
    # Get all menu items
    print("\n[2] Available menu items:")
    menus = get_all_menu_items(window)
    for i, menu in enumerate(menus, 1):
        print(f"    {i}. {menu}")
    
    # Click through menus
    print("\n[3] Navigating through menus...")
    menu_sequence = ['Sales', 'Service', 'Accounting', 'Admin', 'Parts']
    
    for menu in menu_sequence:
        if menu in menus:
            click_menu_item(window, menu)
        else:
            print(f"[X] {menu} not available")
    
    print("\n" + "="*70)
    print("NAVIGATION COMPLETE")
    print("="*70 + "\n")
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
