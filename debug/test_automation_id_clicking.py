"""
G2 Navigator - Click buttons by automation_id

Uses UIA automation IDs to find and click buttons reliably.
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time
import warnings
warnings.filterwarnings('ignore')


def click_button_by_automation_id(app, button_id):
    """Click a button using its automation_id"""
    try:
        # Build button locator by automation ID
        button = app[button_id]
        print(f"[OK] Found button {button_id}")
        
        # Try to click it
        try:
            button.click_input()
            print(f"    Clicked successfully")
            time.sleep(1.5)
            return True
        except Exception as e:
            print(f"    Error during click: {e}")
            return False
    
    except Exception as e:
        print(f"[X] Could not find button {button_id}: {e}")
        return False


def get_nav_window_info(window):
    """Get detailed window information"""
    try:
        print(f"    Window title: {window.window_text()}")
        print(f"    Window class: {window.class_name()}")
    except Exception as e:
        print(f"    Error getting info: {e}")


def main():
    """Main demo"""
    print("\n" + "="*70)
    print("G2 NAVIGATOR - AUTOMATION_ID BUTTON CLICKING")
    print("="*70)
    
    # Connect using UIA backend
    print("\n[1] Connecting to G2 Navigator...")
    handles = findwindows.find_windows(title_re=".*Navigator.*")
    
    if not handles:
        print("[X] Navigator window not found")
        return False
    
    try:
        app = Application(backend='uia').connect(handle=handles[0])
        window = app.top_window()
        print("[OK] Connected via UIA")
        get_nav_window_info(window)
    except Exception as e:
        print(f"[X] Failed to connect: {e}")
        return False
    
    # Button automation IDs based on UIA properties
    print("\n[2] Clicking buttons by automation_id...")
    
    button_ids = [
        'btnSales',
        'btnService', 
        'btnAccounting',
        'btnAdmin',
        'btnParts'
    ]
    
    for button_id in button_ids:
        print(f"\n    Attempting to click {button_id}...")
        click_button_by_automation_id(app, button_id)
    
    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70 + "\n")
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
