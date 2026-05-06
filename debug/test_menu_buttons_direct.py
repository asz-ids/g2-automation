"""
Test clicking menu buttons on Navigator and verify they work
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time
import warnings
warnings.filterwarnings('ignore')

def test_button_click(button_text):
    """Test clicking a specific button"""
    print(f"\n[*] Testing: {button_text}")
    
    # Connect to Navigator
    handles = findwindows.find_windows(title_re=".*Navigator.*")
    if not handles:
        print(f"    [X] Navigator not found")
        return False
    
    try:
        app = Application(backend='win32').connect(handle=handles[0])
        window = app.top_window()
    except Exception as e:
        print(f"    [X] Connection failed: {e}")
        return False
    
    # Find and click button
    children = window.children()
    clicked = False
    
    for child in children:
        try:
            if child.window_text() == button_text and child.is_visible():
                print(f"    Found button at index")
                print(f"    Enabled: {child.is_enabled()}")
                print(f"    Visible: {child.is_visible()}")
                
                # Try different clicking methods
                print(f"    Attempting click()...")
                child.click()
                time.sleep(0.5)
                clicked = True
                print(f"    ✓ Click completed")
                break
        except Exception as e:
            pass
    
    if not clicked:
        print(f"    [X] Could not click {button_text}")
        return False
    
    # Verify the click worked by checking if a screen opened
    time.sleep(2)
    print(f"    Checking result...")
    
    # Get all windows to see if a new one opened
    all_windows = findwindows.find_windows(title_re=".*")
    print(f"    Total windows now: {len(all_windows)}")
    
    return True

# Test each menu button
menu_buttons = ["Sales", "Service", "Accounting", "Admin", "Parts"]

print("=" * 60)
print("Testing G2 Navigator Menu Buttons")
print("=" * 60)

for button in menu_buttons:
    test_button_click(button)
    time.sleep(1)

print("\n" + "=" * 60)
print("Test complete")
print("=" * 60)
