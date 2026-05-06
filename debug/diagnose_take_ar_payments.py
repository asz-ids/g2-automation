"""
Diagnostic: Find Take AR Payments button in Parts menu
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen
from pywinauto import Application, findwindows
import time

# Connect to Parts menu
nav = NavigatorScreen()
nav.click_menu_button('Parts')
time.sleep(1)

# Get window
handles = findwindows.find_windows(title_re=".*Navigator.*")
if not handles:
    print("Navigator not found")
    exit(1)

print("[1] Finding all elements with 'Take' or 'Payment' in name...")
app_uia = Application(backend='uia').connect(handle=handles[0])
window_uia = app_uia.window(handle=handles[0])

count = 0
for elem in window_uia.descendants():
    try:
        if hasattr(elem, 'name'):
            name = str(elem.name) if elem.name else ''
            if 'Take' in name or 'Payment' in name or 'AR' in name:
                count += 1
                print(f"  [{count}] Name: '{name}'")
                if hasattr(elem, 'control_type'):
                    try:
                        ctype = elem.control_type()
                        print(f"       Control Type: {ctype}")
                    except:
                        pass
                if hasattr(elem, 'class_name'):
                    try:
                        cn = elem.class_name()
                        print(f"       Class: {cn}")
                    except:
                        pass
    except:
        pass

if count == 0:
    print("  No elements found with 'Take', 'Payment', or 'AR' in name")

print("\n[2] Checking Win32 backend for buttons...")
app_win32 = Application(backend='win32').connect(handle=handles[0])
window_win32 = app_win32.window(handle=handles[0])

children = window_win32.children()
print(f"  Total children: {len(children)}")

for i, child in enumerate(children):
    try:
        texts = child.texts() if hasattr(child, 'texts') else []
        if texts and 'Take' in str(texts[0]):
            print(f"  [{i}] Found: {texts[0]}")
    except:
        pass

print("\n[3] Looking for all button-like elements...")
count = 0
for elem in window_uia.descendants():
    try:
        if hasattr(elem, 'control_type'):
            ctype = elem.control_type()
            if 'Button' in str(ctype):
                if hasattr(elem, 'name'):
                    name = str(elem.name) if elem.name else '[no name]'
                    if name not in ['', '[no name]']:
                        count += 1
                        print(f"  [{count}] Button: '{name}'")
    except:
        pass

print(f"\n[4] Total buttons found: {count}")
