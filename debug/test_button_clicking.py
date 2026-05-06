"""
G2 Navigator - Advanced Button Clicking

Tests different clicking methods to find what works with G2.
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
        print("[X] Navigator window not found")
        return None
    
    app = Application(backend='win32').connect(handle=handles[0])
    window = app.top_window()
    return window


def click_button_method1(button):
    """Method 1: Standard click()"""
    try:
        button.click()
        return True
    except Exception as e:
        print(f"  Method 1 failed: {e}")
        return False


def click_button_method2(button):
    """Method 2: Double-click"""
    try:
        button.double_click()
        return True
    except Exception as e:
        print(f"  Method 2 failed: {e}")
        return False


def click_button_method3(button):
    """Method 3: Right-click"""
    try:
        button.right_click()
        return True
    except Exception as e:
        print(f"  Method 3 failed: {e}")
        return False


def click_button_method4(button):
    """Method 4: Click at specific offset"""
    try:
        rect = button.rectangle()
        x = (rect.left + rect.right) // 2
        y = (rect.top + rect.bottom) // 2
        
        import pyautogui
        pyautogui.click(x, y)
        return True
    except Exception as e:
        print(f"  Method 4 failed: {e}")
        return False


def click_button_method5(button):
    """Method 5: Move mouse and click"""
    try:
        rect = button.rectangle()
        x = (rect.left + rect.right) // 2
        y = (rect.top + rect.bottom) // 2
        
        import pyautogui
        pyautogui.moveTo(x, y)
        time.sleep(0.2)
        pyautogui.click()
        return True
    except Exception as e:
        print(f"  Method 5 failed: {e}")
        return False


def click_button_method6(button):
    """Method 6: Send Enter key after focusing"""
    try:
        button.set_focus()
        time.sleep(0.1)
        button.type_keys('{ENTER}')
        return True
    except Exception as e:
        print(f"  Method 6 failed: {e}")
        return False


def test_click_methods():
    """Test different clicking methods"""
    print("\n" + "="*70)
    print("G2 NAVIGATOR - BUTTON CLICKING TEST")
    print("="*70)
    
    # Connect
    print("\n[1] Connecting to Navigator...")
    window = connect_to_navigator()
    if not window:
        return False
    
    print("[OK] Connected")
    
    # Find Parts button
    print("\n[2] Finding Parts button...")
    children = window.children()
    parts_button = None
    
    for child in children:
        try:
            text = child.window_text()
            if text == "Parts":
                parts_button = child
                print(f"[OK] Found Parts button")
                break
        except:
            pass
    
    if not parts_button:
        print("[X] Parts button not found")
        return False
    
    # Try different clicking methods
    print("\n[3] Testing clicking methods...")
    methods = [
        ("Standard click()", click_button_method1),
        ("Double-click", click_button_method2),
        ("Right-click", click_button_method3),
        ("Click at offset", click_button_method4),
        ("Move and click", click_button_method5),
        ("Set focus + Enter", click_button_method6),
    ]
    
    for name, method in methods:
        print(f"\n  Testing: {name}")
        try:
            result = method(parts_button)
            if result:
                print(f"    [OK] {name} succeeded!")
                time.sleep(0.5)
                return True
        except Exception as e:
            print(f"    [X] Error: {e}")
    
    print("\n[X] All clicking methods failed")
    return False


def test_keyboard_navigation():
    """Test using keyboard navigation instead of clicking"""
    print("\n" + "="*70)
    print("G2 NAVIGATOR - KEYBOARD NAVIGATION TEST")
    print("="*70)
    
    # Connect
    print("\n[1] Connecting to Navigator...")
    window = connect_to_navigator()
    if not window:
        return False
    
    print("[OK] Connected")
    
    # Try Tab + Enter navigation
    print("\n[2] Testing Tab navigation...")
    try:
        window.set_focus()
        time.sleep(0.3)
        
        # Press Tab to cycle through buttons
        for i in range(5):
            print(f"  Tab {i+1}...")
            window.type_keys('{TAB}')
            time.sleep(0.3)
        
        # Try Enter to click
        print("  Pressing Enter...")
        window.type_keys('{ENTER}')
        print("[OK] Tab + Enter navigation completed")
        return True
        
    except Exception as e:
        print(f"[X] Keyboard navigation failed: {e}")
        return False


if __name__ == "__main__":
    success = test_click_methods()
    
    if not success:
        print("\n" + "="*70)
        print("Trying keyboard navigation...")
        print("="*70)
        success = test_keyboard_navigation()
    
    print("\n" + "="*70)
    if success:
        print("SUCCESS - Found working interaction method")
    else:
        print("All methods tested - check output for details")
    print("="*70 + "\n")
    
    exit(0 if success else 1)
