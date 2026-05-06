"""
Monitor the Navigator window INSIDE for content changes after clicking
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time
import warnings
warnings.filterwarnings('ignore')

def scan_navigator_content():
    """Scan Navigator for all content and return details"""
    nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
    if not nav_handles:
        return None
    
    app = Application(backend='win32').connect(handle=nav_handles[0])
    window = app.top_window()
    
    all_children = window.children()
    content = {
        'total_children': len(all_children),
        'text_elements': [],
        'mdi_info': {'children': 0, 'visible': False},
        'panel_info': []
    }
    
    # Look for all text content
    for i, child in enumerate(all_children):
        try:
            text = child.window_text()
            if text and len(text.strip()) > 0 and text not in ['G2 Navigator', 'SMC - Sunset Marine']:
                content['text_elements'].append({
                    'index': i,
                    'text': text[:50],
                    'class': child.class_name()[:40]
                })
        except:
            pass
    
    # Check MDI
    for i, child in enumerate(all_children):
        try:
            if 'mdi' in child.class_name().lower():
                mdi_children = child.children()
                content['mdi_info']['children'] = len(mdi_children)
                content['mdi_info']['visible'] = child.is_visible()
                content['mdi_info']['index'] = i
                
                if mdi_children:
                    for m in mdi_children:
                        content['text_elements'].append({
                            'mdi_child': True,
                            'text': m.window_text()[:50]
                        })
        except:
            pass
    
    # Check for large panel/container elements
    for i, child in enumerate(all_children):
        try:
            cls = child.class_name()
            if any(x in cls for x in ['Panel', 'Container', 'View', 'Splitter']):
                rect = child.rectangle()
                size = (rect.width(), rect.height())
                content['panel_info'].append({
                    'index': i,
                    'class': cls[:40],
                    'size': size
                })
        except:
            pass
    
    return content

print("="*70)
print("BEFORE CLICKING SALES")
print("="*70)

before = scan_navigator_content()
print(f"Total children: {before['total_children']}")
print(f"MDI children: {before['mdi_info']['children']}")
print(f"Text elements: {len(before['text_elements'])}")
if before['text_elements']:
    print("  Text found:")
    for elem in before['text_elements'][:10]:
        if 'mdi_child' in elem:
            print(f"    - [MDI] {elem['text']}")
        else:
            print(f"    - {elem['text']}")

print(f"\nPanels: {len(before['panel_info'])}")
if before['panel_info']:
    for panel in before['panel_info']:
        print(f"  - {panel['class']} at size {panel['size']}")

print("\n" + "="*70)
print("CLICKING SALES BUTTON...")
print("="*70)

nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()
window.set_focus()

children = window.children()
for child in children:
    try:
        if child.window_text() == "Sales" and child.is_visible():
            print(f"Found and clicking Sales button...")
            child.click()
            print(f"Click executed")
            break
    except:
        pass

print(f"Waiting 3 seconds...")
time.sleep(3)

print("\n" + "="*70)
print("AFTER CLICKING SALES")
print("="*70)

after = scan_navigator_content()
print(f"Total children: {after['total_children']}")
print(f"MDI children: {after['mdi_info']['children']}")
print(f"Text elements: {len(after['text_elements'])}")
if after['text_elements']:
    print("  Text found:")
    for elem in after['text_elements'][:10]:
        if 'mdi_child' in elem:
            print(f"    - [MDI] {elem['text']}")
        else:
            print(f"    - {elem['text']}")

print(f"\nPanels: {len(after['panel_info'])}")
if after['panel_info']:
    for panel in after['panel_info']:
        print(f"  - {panel['class']} at size {panel['size']}")

print("\n" + "="*70)
print("COMPARISON")
print("="*70)

if before['mdi_info']['children'] != after['mdi_info']['children']:
    print(f"✓ MDI CHANGED: {before['mdi_info']['children']} → {after['mdi_info']['children']}")
else:
    print(f"[X] MDI unchanged: {before['mdi_info']['children']} children")

if len(before['text_elements']) != len(after['text_elements']):
    print(f"✓ TEXT CHANGED: {len(before['text_elements'])} → {len(after['text_elements'])}")
    
    # Show new elements
    before_texts = {e['text'] for e in before['text_elements'] if 'text' in e}
    after_texts = {e['text'] for e in after['text_elements'] if 'text' in e}
    new_texts = after_texts - before_texts
    
    if new_texts:
        print(f"  New content:")
        for text in sorted(new_texts):
            print(f"    - {text}")
else:
    print(f"[X] TEXT unchanged: {len(before['text_elements'])} elements")

if len(before['panel_info']) != len(after['panel_info']):
    print(f"✓ PANELS CHANGED: {len(before['panel_info'])} → {len(after['panel_info'])}")
else:
    print(f"[X] PANELS unchanged: {len(before['panel_info'])} panels")

print("\n" + "="*70)

# If nothing changed, do a full dump
if (before['total_children'] == after['total_children'] and
    len(before['text_elements']) == len(after['text_elements']) and
    before['mdi_info']['children'] == after['mdi_info']['children']):
    
    print("NO CHANGES DETECTED")
    print("="*70)
    print("\nFull Navigator structure AFTER click:")
    nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
    app = Application(backend='win32').connect(handle=nav_handles[0])
    window = app.top_window()
    
    for i, child in enumerate(window.children()):
        try:
            text = child.window_text()[:30] if child.window_text() else "[empty]"
            cls = child.class_name()[:50]
            
            # Try to get some indication of content
            try:
                subchildren = child.children()
                sub_count = len(subchildren)
            except:
                sub_count = 0
            
            print(f"[{i:2d}] {text:30} | {cls:50} | Children: {sub_count}")
        except:
            pass
