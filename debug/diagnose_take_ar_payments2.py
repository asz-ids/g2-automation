"""
Find Take AR Payments - detailed Win32 search
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
app_win32 = Application(backend='win32').connect(handle=handles[0])
window_win32 = app_win32.window(handle=handles[0])

print("[1] All children with their texts...")
children = window_win32.children()

for i, child in enumerate(children):
    try:
        texts = child.texts() if hasattr(child, 'texts') else []
        class_name = child.class_name() if hasattr(child, 'class_name') else 'N/A'
        
        # Print first 50 with non-empty text
        if texts and texts[0]:
            print(f"  [{i:2d}] {texts[0]:40s} | {class_name}")
        elif i < 15:
            print(f"  [{i:2d}] [empty]                                  | {class_name}")
    except Exception as e:
        print(f"  [{i:2d}] Error: {e}")

print("\n[2] Searching for all items containing 'Take', 'AR', 'Payment'...")
search_terms = ['Take', 'AR', 'Payment', 'Payments', 'Button']

for search_term in search_terms:
    matches = []
    for i, child in enumerate(children):
        try:
            texts = child.texts() if hasattr(child, 'texts') else []
            if texts and search_term.lower() in str(texts[0]).lower():
                matches.append((i, texts[0]))
        except:
            pass
    
    if matches:
        print(f"\n  Searching for '{search_term}':")
        for idx, text in matches:
            print(f"    [{idx}] {text}")
    else:
        print(f"  Searching for '{search_term}': NO MATCHES")

print("\n[3] Looking at child structure - recursively...")

def explore_children(elem, depth=0, max_depth=3):
    if depth > max_depth:
        return
    
    try:
        children = elem.children()
        for i, child in enumerate(children):
            try:
                texts = child.texts() if hasattr(child, 'texts') else []
                text = texts[0] if texts else '[empty]'
                
                if 'Take' in str(text) or 'AR' in str(text) or 'Payment' in str(text):
                    indent = "  " * depth
                    print(f"{indent}[{i}] {text}")
                
                # Recurse
                explore_children(child, depth + 1, max_depth)
            except:
                pass
    except:
        pass

print("\n  Exploring hierarchy...")
explore_children(window_win32, depth=0, max_depth=4)
