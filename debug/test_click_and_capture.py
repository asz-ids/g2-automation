"""
G2 Navigator - Click and Capture Verification

Clicks buttons and captures screenshots to verify screens are opening.
"""

from pywinauto import findwindows
from pywinauto.application import Application
from PIL import ImageGrab
import time
import os
import warnings
warnings.filterwarnings('ignore')


def take_screenshot(filename):
    """Take a screenshot of the entire screen"""
    try:
        screenshot = ImageGrab.grab()
        screenshot.save(filename)
        return True
    except Exception as e:
        print(f"    [X] Screenshot error: {e}")
        return False


def click_and_verify(window, button_name, screenshot_path):
    """Click a button and take screenshot to verify"""
    print(f"\n  {button_name}:")
    
    # Find and click button
    children = window.children()
    for child in children:
        try:
            text = child.window_text()
            if text == button_name:
                print(f"    [OK] Found button")
                child.click()
                print(f"    [OK] Clicked")
                
                time.sleep(2)  # Wait for screen to update
                
                # Take screenshot
                screenshot_file = os.path.join(screenshot_path, f"{button_name.lower()}_screen.png")
                if take_screenshot(screenshot_file):
                    print(f"    [OK] Screenshot: {screenshot_file}")
                
                return True
        except:
            pass
    
    print(f"    [X] Button not found")
    return False


def main():
    """Main demo"""
    print("\n" + "="*70)
    print("G2 NAVIGATOR - CLICK & CAPTURE VERIFICATION")
    print("="*70)
    
    # Create screenshots directory
    screenshot_dir = "screenshots/navigator_clicks"
    os.makedirs(screenshot_dir, exist_ok=True)
    
    # Connect
    print("\n[1] Connecting to G2 Navigator...")
    handles = findwindows.find_windows(title_re=".*Navigator.*")
    
    if not handles:
        print("[X] Navigator not found")
        return False
    
    try:
        app = Application(backend='win32').connect(handle=handles[0])
        window = app.top_window()
        print("[OK] Connected")
    except Exception as e:
        print(f"[X] Error: {e}")
        return False
    
    # Take initial screenshot
    print("\n[2] Taking initial screenshot...")
    initial_file = os.path.join(screenshot_dir, "00_initial.png")
    if take_screenshot(initial_file):
        print(f"    [OK] Initial screenshot: {initial_file}")
    
    # Click each button and capture
    print("\n[3] Clicking buttons and capturing screens...")
    buttons = ['Sales', 'Service', 'Accounting', 'Admin', 'Parts']
    
    for i, button in enumerate(buttons, 1):
        print(f"\n  [{i}/{len(buttons)}] {button}")
        click_and_verify(window, button, screenshot_dir)
    
    print("\n" + "="*70)
    print(f"COMPLETE - Screenshots saved to: {screenshot_dir}")
    print("="*70 + "\n")
    
    # List generated files
    try:
        files = sorted(os.listdir(screenshot_dir))
        print(f"Generated {len(files)} screenshot(s):")
        for f in files:
            print(f"  - {f}")
    except:
        pass
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
