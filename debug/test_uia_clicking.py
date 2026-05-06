"""
G2 Navigator - UIA-based Button Clicking

Uses UIA backend for more reliable button interaction and screen opening.
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time
import warnings
warnings.filterwarnings('ignore')


def click_button_via_uia(window, button_name):
    """Click a button using UIA backend for better interaction"""
    try:
        # Try to find and click using UIA
        children = window.children()
        
        for child in children:
            try:
                # Check by text
                name = child.name()
                if name == button_name:
                    print(f"[OK] Found {button_name} via UIA")
                    
                    # Try multiple click methods
                    try:
                        # Method 1: Direct click
                        child.click_input()
                        print(f"    Clicked with click_input()")
                        time.sleep(1)
                        return True
                    except:
                        pass
                    
                    try:
                        # Method 2: Set focus and send keys
                        child.set_focus()
                        child.send_keystrokes("{SPACE}")
                        print(f"    Clicked with Space key")
                        time.sleep(1)
                        return True
                    except:
                        pass
            except:
                pass
        
        print(f"[X] {button_name} not found")
        return False
    
    except Exception as e:
        print(f"[X] Error clicking button: {e}")
        return False


def get_window_content(window):
    """Get current window content/state"""
    try:
        children = window.children()
        print(f"\n    Window currently has {len(children)} visible elements:")
        for i, child in enumerate(children[:10]):  # Show first 10
            try:
                name = child.name()
                control_type = child.control_type()
                print(f"      {i+1}. {name} ({control_type})")
            except:
                pass
    except Exception as e:
        print(f"    Could not read window content: {e}")


def main():
    """Main demo"""
    print("\n" + "="*70)
    print("G2 NAVIGATOR - UIA BUTTON CLICKING TEST")
    print("="*70)
    
    # Connect using UIA backend
    print("\n[1] Connecting to G2 Navigator (UIA backend)...")
    handles = findwindows.find_windows(title_re=".*Navigator.*")
    
    if not handles:
        print("[X] Navigator window not found")
        return False
    
    try:
        app = Application(backend='uia').connect(handle=handles[0])
        window = app.top_window()
        print("[OK] Connected via UIA")
    except Exception as e:
        print(f"[X] Failed to connect: {e}")
        return False
    
    # Show current state
    print("\n[2] Current Navigator state:")
    get_window_content(window)
    
    # Click buttons
    print("\n[3] Clicking menu buttons...")
    buttons_to_click = ['Sales', 'Service', 'Accounting', 'Admin', 'Parts']
    
    for button in buttons_to_click:
        print(f"\n    Clicking {button}...")
        click_button_via_uia(window, button)
        
        # Show state after click
        print(f"    State after clicking {button}:")
        get_window_content(window)
        time.sleep(0.5)
    
    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70 + "\n")
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
