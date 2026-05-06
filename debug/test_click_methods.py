"""
Try different click methods and keyboard navigation
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time
import warnings
from pynput.keyboard import Key, Controller
warnings.filterwarnings('ignore')

keyboard = Controller()

def test_method_1_double_click():
    """Try double-clicking"""
    print("\n[TEST 1] Double-click approach...")
    nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
    if not nav_handles:
        print("  [X] Navigator not found")
        return False
    
    app = Application(backend='win32').connect(handle=nav_handles[0])
    window = app.top_window()
    window.set_focus()
    
    children = window.children()
    for child in children:
        try:
            if child.window_text() == "Sales" and child.is_visible():
                print("  [*] Double-clicking Sales...")
                child.double_click()
                time.sleep(2)
                return True
        except:
            pass
    return False

def test_method_2_mouse_coords():
    """Try clicking by mouse coordinates"""
    print("\n[TEST 2] Mouse coordinate approach...")
    nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
    if not nav_handles:
        print("  [X] Navigator not found")
        return False
    
    app = Application(backend='win32').connect(handle=nav_handles[0])
    window = app.top_window()
    window.set_focus()
    
    children = window.children()
    for child in children:
        try:
            if child.window_text() == "Sales" and child.is_visible():
                rect = child.rectangle()
                x = (rect.left + rect.right) // 2
                y = (rect.top + rect.bottom) // 2
                print(f"  [*] Button at ({x}, {y})")
                
                # Move mouse and click
                keyboard.press(Key.alt)
                keyboard.release(Key.alt)
                time.sleep(0.3)
                
                # Use win32 approach
                from ctypes import windll
                windll.user32.SetCursorPos(x, y)
                windll.user32.mouse_event(2, 0, 0, 0, 0)  # Move
                windll.user32.mouse_event(4, 0, 0, 0, 0)  # Left down
                windll.user32.mouse_event(8, 0, 0, 0, 0)  # Left up
                time.sleep(2)
                return True
        except Exception as e:
            print(f"  Error: {e}")
            pass
    return False

def test_method_3_keyboard():
    """Try keyboard navigation with Tab and Enter"""
    print("\n[TEST 3] Keyboard navigation approach...")
    nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
    if not nav_handles:
        print("  [X] Navigator not found")
        return False
    
    app = Application(backend='win32').connect(handle=nav_handles[0])
    window = app.top_window()
    window.set_focus()
    time.sleep(0.3)
    
    print("  [*] Pressing Tab to focus first button...")
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    time.sleep(0.3)
    
    print("  [*] Pressing Space to click...")
    keyboard.press(Key.space)
    keyboard.release(Key.space)
    time.sleep(2)
    
    return True

def test_method_4_right_click():
    """Try right-click"""
    print("\n[TEST 4] Right-click approach...")
    nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
    if not nav_handles:
        print("  [X] Navigator not found")
        return False
    
    app = Application(backend='win32').connect(handle=nav_handles[0])
    window = app.top_window()
    window.set_focus()
    
    children = window.children()
    for child in children:
        try:
            if child.window_text() == "Sales" and child.is_visible():
                print("  [*] Right-clicking Sales...")
                child.right_click()
                time.sleep(2)
                # Then press Enter to select
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
                time.sleep(2)
                return True
        except:
            pass
    return False

def check_result():
    """Check if screen opened"""
    try:
        sales_handles = findwindows.find_windows(title_re=".*Sales.*")
        return len(sales_handles) > 0
    except:
        return False

print("=" * 60)
print("Testing Different Click Methods")
print("=" * 60)

methods = [
    test_method_1_double_click,
    test_method_2_mouse_coords,
    test_method_3_keyboard,
    test_method_4_right_click
]

for method in methods:
    try:
        result = method()
        if check_result():
            print(f"  ✓ SUCCESS! Screen opened!")
            break
        else:
            print(f"  Result: No screen opened")
    except Exception as e:
        print(f"  Error: {e}")
    
    time.sleep(1)

print("\n" + "=" * 60)
print("Testing complete")
print("=" * 60)
