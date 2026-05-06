"""
Try keyboard shortcuts to navigate modules
"""

from pywinauto import findwindows
from pywinauto.application import Application
from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

print("[1] Focusing Navigator window...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()
window.set_focus()
time.sleep(0.5)

print(f"\n[2] Trying Alt+S for Sales...")
try:
    keyboard.press(Key.alt)
    keyboard.press('s')
    keyboard.release('s')
    keyboard.release(Key.alt)
    print(f"    Alt+S sent")
    time.sleep(2)
    
    sales_handles = findwindows.find_windows(title_re=".*Sales.*")
    if sales_handles:
        print(f"    ✓ Sales screen opened!")
        exit(0)
except Exception as e:
    print(f"    Error: {e}")

print(f"\n[3] Trying Tab to navigate, then Enter...")
try:
    # Tab through elements
    for i in range(5):
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        time.sleep(0.2)
    
    # Press Enter on one
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    print(f"    Tab/Enter sequence sent")
    time.sleep(2)
    
    sales_handles = findwindows.find_windows(title_re=".*Sales.*")
    if sales_handles:
        print(f"    ✓ Screen opened!")
        exit(0)
except Exception as e:
    print(f"    Error: {e}")

print(f"\n[4] Trying F keys (F1=Sales, etc)...")
try:
    for key_num in range(1, 6):
        key_name = f'f{key_num}'
        print(f"    Trying {key_name.upper()}...")
        keyboard.press(key_name)
        keyboard.release(key_name)
        time.sleep(1)
        
        sales_handles = findwindows.find_windows(title_re=".*Sales.*|.*Service.*|.*Accounting.*")
        if sales_handles:
            print(f"    ✓ Screen opened!")
            exit(0)
except Exception as e:
    print(f"    Error: {e}")

print(f"\n[5] Trying Ctrl+Letter...")
try:
    for letter in ['s', 'v', 'a', 'p']:  # Sales, Service, Accounting, Parts
        print(f"    Trying Ctrl+{letter.upper()}...")
        keyboard.press(Key.ctrl)
        keyboard.press(letter)
        keyboard.release(letter)
        keyboard.release(Key.ctrl)
        time.sleep(1)
        
        all_wins = findwindows.find_windows(title_re=".*Sales.*|.*Service.*|.*Accounting.*|.*Admin.*|.*Parts.*")
        if len(all_wins) > 1:  # More than just Navigator
            print(f"    ✓ Screen might have opened!")
            exit(0)
except Exception as e:
    print(f"    Error: {e}")

print(f"\nNo keyboard shortcuts worked.")
