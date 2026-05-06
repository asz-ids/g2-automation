"""
G2 Navigator - Get Button Coordinates and Click

Find button positions and click using mouse coordinates.
"""

from pywinauto import findwindows
from pywinauto.application import Application
from pywinauto.actionlogger import ActionLogger
import time
import warnings
warnings.filterwarnings('ignore')


def get_button_rectangles(window):
    """Get button positions"""
    try:
        children = window.children()
        print(f"    Window has {len(children)} children")
        
        button_rects = {}
        for child in children:
            try:
                text = child.window_text()
                if text in ['Sales', 'Service', 'Accounting', 'Admin', 'Parts']:
                    try:
                        rect = child.rectangle()
                        button_rects[text] = rect
                        print(f"    {text}: {rect}")
                    except:
                        pass
            except:
                pass
        
        return button_rects
    except Exception as e:
        print(f"    Error: {e}")
        return {}


def click_button_by_coordinates(button_rect):
    """Click using mouse coordinates"""
    try:
        from pywinauto.mouse import click as mouse_click
        
        # Calculate center of button
        x = (button_rect.left + button_rect.right) // 2
        y = (button_rect.top + button_rect.bottom) // 2
        
        print(f"      Clicking at ({x}, {y})")
        mouse_click(coords=(x, y))
        time.sleep(1)
        return True
    except Exception as e:
        print(f"      Error: {e}")
        return False


def main():
    """Main demo"""
    print("\n" + "="*70)
    print("G2 NAVIGATOR - COORDINATE-BASED CLICKING")
    print("="*70)
    
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
    
    # Get button positions
    print("\n[2] Finding button positions...")
    button_rects = get_button_rectangles(window)
    
    if not button_rects:
        print("[X] No buttons found")
        return False
    
    # Click each button
    print(f"\n[3] Clicking {len(button_rects)} buttons...")
    for button_name in ['Sales', 'Service', 'Accounting', 'Admin', 'Parts']:
        if button_name in button_rects:
            print(f"\n    Clicking {button_name}...")
            click_button_by_coordinates(button_rects[button_name])
    
    print("\n" + "="*70)
    print("DONE")
    print("="*70 + "\n")
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
