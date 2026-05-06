"""
Log in to G2, then test Navigator buttons
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time
import warnings
warnings.filterwarnings('ignore')

print("[1] Connecting to G2 Login window...")
login_handles = findwindows.find_windows(title_re=".*Login.*")
if not login_handles:
    print("[X] Login window not found")
    exit(1)

app = Application(backend='win32').connect(handle=login_handles[0])
login_window = app.top_window()
print(f"    Connected to: {login_window.window_text()}")

print("\n[2] Finding login fields...")
children = login_window.children()
print(f"    Total children: {len(children)}")

username_field = None
password_field = None
login_button = None

for child in children:
    try:
        text = child.window_text()
        cls = child.class_name()
        
        if 'textbox' in cls.lower() or 'edit' in cls.lower():
            if not username_field:
                username_field = child
                print(f"    Found username field")
            elif not password_field:
                password_field = child
                print(f"    Found password field")
        
        if 'button' in cls.lower() and ('ok' in text.lower() or 'login' in text.lower() or 'sign' in text.lower()):
            login_button = child
            print(f"    Found login button: {text}")
    except:
        pass

if not username_field or not password_field:
    print("\n    Looking for text input more carefully...")
    for i, child in enumerate(children):
        try:
            if child.is_visible() and child.is_enabled():
                text = child.window_text()
                cls = child.class_name()
                if text or 'textbox' in cls.lower() or 'edit' in cls.lower():
                    print(f"    [{i}] {text:20} | {cls[:40]}")
        except:
            pass

print("\n[3] Entering credentials...")
if username_field:
    username_field.set_focus()
    username_field.type_keys('admin', interval=0.05)
    print(f"    Username entered")
    time.sleep(0.5)

if password_field:
    password_field.set_focus()
    password_field.type_keys('password', interval=0.05)
    print(f"    Password entered")
    time.sleep(0.5)

print("\n[4] Clicking login button...")
if login_button:
    login_button.click()
    print(f"    Login clicked")
    time.sleep(5)
else:
    # Try pressing Enter
    print(f"    Login button not found, pressing Enter...")
    from pynput.keyboard import Key, Controller
    Controller().press(Key.enter)
    Controller().release(Key.enter)
    time.sleep(5)

print("\n[5] Checking for Navigator window...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
if nav_handles:
    print(f"    ✓ Navigator window found!")
    
    print("\n[6] Now testing button clicks on Navigator...")
    app2 = Application(backend='win32').connect(handle=nav_handles[0])
    window = app2.top_window()
    window.set_focus()
    time.sleep(0.5)
    
    # Test Sales button
    children = window.children()
    for child in children:
        try:
            if child.window_text() == "Sales" and child.is_visible():
                print(f"    Found Sales button, clicking...")
                child.click()
                time.sleep(3)
                
                # Check if screen opened
                screen_handles = findwindows.find_windows(title_re=".*Sales.*")
                if screen_handles:
                    print(f"    ✓ SUCCESS! Sales screen opened!")
                else:
                    print(f"    [X] No Sales screen")
                break
        except:
            pass
else:
    print(f"    [X] Navigator not found after login")
    
    # Check what windows exist
    all_handles = findwindows.find_windows(title_re=".*")
    print(f"\n    Current windows:")
    for h in all_handles[-10:]:
        try:
            a = Application(backend='win32').connect(handle=h)
            w = a.top_window()
            if w.is_visible():
                print(f"      - {w.window_text()}")
        except:
            pass

print("\nTest complete.")
