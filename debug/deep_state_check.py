"""
Check if clicking works but content appears elsewhere
"""
import pywinauto
from pywinauto import Application
import pywinauto.findwindows
import time
import ctypes

try:
    windows = pywinauto.findwindows.find_windows(title_re='.*Navigator.*')
    app = Application(backend='win32').connect(handle=windows[0])
    nav = app.window(handle=windows[0])
    children = nav.children()
    
    # Find btnSales
    btn_sales = None
    for child in children:
        try:
            if hasattr(child, 'handle') and child.handle == 398226:
                btn_sales = child
                break
        except:
            pass
    
    if not btn_sales:
        print("btnSales not found")
        exit(1)
    
    print("[1] Deep snapshot of Navigator state before click...")
    
    def get_nav_state():
        state = {
            'children_count': len(nav.children()),
            'visible_windows': [],
            'child_texts': [],
            'mdi_info': None,
        }
        
        # Scan all children for text content
        for i, c in enumerate(nav.children()):
            try:
                texts = c.texts() if hasattr(c, 'texts') else []
                if texts and texts[0]:
                    state['child_texts'].append({
                        'idx': i,
                        'class': c.class_name(),
                        'text': texts[0][:50],  # First 50 chars
                    })
            except:
                pass
        
        # Check for any new windows
        try:
            all_windows = ctypes.windll.user32.GetWindowTextW
            # Just count visible windows
            import pywinauto.findwindows as fw
            visible_wins = fw.find_windows()
            state['visible_windows'] = len(visible_wins)
        except:
            pass
        
        return state
    
    state_before = get_nav_state()
    print(f"  Children: {state_before['children_count']}")
    print(f"  Visible windows: {state_before['visible_windows']}")
    print(f"  Child texts found: {len(state_before['child_texts'])}")
    for ct in state_before['child_texts']:
        print(f"    - {ct['text']}")
    
    print("\n[2] Clicking btnSales with mouse...")
    rect = btn_sales.rectangle()
    x = rect.left + (rect.right - rect.left) // 2
    y = rect.top + (rect.bottom - rect.top) // 2
    
    # Move cursor
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(0.1)
    # Click
    btn_sales.click()
    time.sleep(1)
    
    print("[3] State AFTER click...")
    state_after = get_nav_state()
    print(f"  Children: {state_after['children_count']}")
    print(f"  Visible windows: {state_after['visible_windows']}")
    print(f"  Child texts found: {len(state_after['child_texts'])}")
    for ct in state_after['child_texts']:
        print(f"    - {ct['text']}")
    
    print("\n[4] Detailed comparison...")
    if state_before['children_count'] != state_after['children_count']:
        print("  ✓ Children count CHANGED!")
        print(f"    Before: {state_before['children_count']}")
        print(f"    After: {state_after['children_count']}")
    else:
        print("  ✗ Children count unchanged")
    
    if state_before['visible_windows'] != state_after['visible_windows']:
        print("  ✓ Visible windows CHANGED!")
        print(f"    Before: {state_before['visible_windows']}")
        print(f"    After: {state_after['visible_windows']}")
    else:
        print("  ✗ Visible windows unchanged")
    
    # Check for new text content
    new_texts = [t for t in state_after['child_texts'] if t not in state_before['child_texts']]
    if new_texts:
        print(f"  ✓ NEW TEXT FOUND ({len(new_texts)} items):")
        for t in new_texts:
            print(f"    - {t['text']}")
    else:
        print("  ✗ No new text content")
    
    print("\n[5] Wait and check again (delayed response)...")
    time.sleep(3)
    state_delayed = get_nav_state()
    print(f"  Children after 3sec: {state_delayed['children_count']}")
    
    if state_delayed['children_count'] != state_before['children_count']:
        print("  ✓ DELAYED RESPONSE DETECTED!")
    
except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
