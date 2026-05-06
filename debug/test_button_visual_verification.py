"""
G2 Navigator - Click with Visual Verification

Captures screenshots before/after clicking to verify visual changes.
"""

from pywinauto import findwindows
from pywinauto.application import Application
from PIL import ImageGrab
import time
import os
import warnings
warnings.filterwarnings('ignore')


def connect_to_navigator():
    """Connect to G2 Navigator"""
    handles = findwindows.find_windows(title_re=".*Navigator.*")
    if not handles:
        return None, None
    
    app = Application(backend='win32').connect(handle=handles[0])
    window = app.top_window()
    return app, window


def capture_screenshot(filename):
    """Capture screenshot to file"""
    try:
        # Capture entire screen
        screenshot = ImageGrab.grab()
        
        # Create screenshots directory if needed
        os.makedirs('screenshots', exist_ok=True)
        
        filepath = os.path.join('screenshots', filename)
        screenshot.save(filepath)
        print(f"  Screenshot saved: {filepath}")
        return filepath
    except Exception as e:
        print(f"  Screenshot failed: {e}")
        return None


def click_and_capture(window, button_name, index=1):
    """Click button and capture before/after screenshots"""
    print(f"\n[*] Testing: {button_name} (#{index})")
    
    # Find button
    children = window.children()
    count = 0
    target_button = None
    
    for child in children:
        try:
            text = child.window_text()
            if text == button_name:
                count += 1
                if count == index:
                    target_button = child
                    break
        except:
            pass
    
    if not target_button:
        print(f"  [X] {button_name} button #{index} not found")
        return False
    
    # Capture before
    print("  Capturing before state...")
    before_file = capture_screenshot(f"before_{button_name}_{index}.png")
    
    # Click
    print(f"  Clicking {button_name}...")
    try:
        target_button.click()
    except Exception as e:
        print(f"  [X] Click failed: {e}")
        return False
    
    # Wait for any UI response
    time.sleep(0.8)
    
    # Capture after
    print("  Capturing after state...")
    after_file = capture_screenshot(f"after_{button_name}_{index}.png")
    
    print("  [OK] Click captured")
    return True


def main():
    print("\n" + "="*70)
    print("G2 NAVIGATOR - VISUAL VERIFICATION OF CLICKS")
    print("="*70)
    
    print("\n[1] Connecting...")
    app, window = connect_to_navigator()
    if not window:
        print("[X] Navigator not found")
        return False
    
    print("[OK] Connected")
    
    # Click each menu and capture
    print("\n[2] Clicking menus with screenshot capture...")
    menus = ['Sales', 'Service', 'Accounting', 'Admin', 'Parts']
    
    for menu in menus:
        click_and_capture(window, menu)
    
    print("\n" + "="*70)
    print("CAPTURE COMPLETE")
    print("Screenshots saved to: screenshots/")
    print("Check screenshots to verify clicks worked visually")
    print("="*70 + "\n")
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
