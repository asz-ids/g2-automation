"""
Monitor content area changes in Navigator
"""
import pywinauto
from pywinauto import Application
import pywinauto.findwindows
import time

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
    
    print("[1] Scanning all Navigator children for content areas...")
    print("    (Looking for large panes, panels, or content containers)\n")
    
    content_areas = []
    for i, child in enumerate(children):
        try:
            class_name = child.class_name()
            rect = child.rectangle()
            
            # Look for large panes or content containers
            width = rect.right - rect.left
            height = rect.bottom - rect.top
            
            # Size threshold - content areas are usually large
            if width > 100 and height > 100:
                try:
                    texts = child.texts() if hasattr(child, 'texts') else []
                    vis = child.is_visible()
                    enabled = child.is_enabled()
                except:
                    texts = []
                    vis = '?'
                    enabled = '?'
                
                content_areas.append({
                    'idx': i,
                    'class': class_name,
                    'rect': (width, height),
                    'texts': texts[:2] if texts else [],
                    'visible': vis,
                    'enabled': enabled,
                })
                
                print(f"    [{i:2d}] {width:4d}x{height:4d}  {class_name}")
                print(f"         visible={vis}, enabled={enabled}")
                if texts and texts[0]:
                    print(f"         text: {texts[0][:60]}")
        except Exception as e:
            pass
    
    print(f"\n    Total potential content areas: {len(content_areas)}")
    
    print("\n[2] Getting detailed info on each content area BEFORE click...")
    
    def snapshot_content_areas():
        snapshot = []
        for i, child in enumerate(children):
            try:
                class_name = child.class_name()
                rect = child.rectangle()
                width = rect.right - rect.left
                height = rect.bottom - rect.top
                
                if width > 100 and height > 100:
                    # Deep inspection
                    info = {
                        'idx': i,
                        'class': class_name,
                        'child_count': len(child.children()) if hasattr(child, 'children') else 0,
                        'texts': child.texts() if hasattr(child, 'texts') else [],
                    }
                    snapshot.append(info)
            except:
                pass
        return snapshot
    
    before = snapshot_content_areas()
    for info in before:
        print(f"  [{info['idx']}] children: {info['child_count']}, texts: {info['texts'][:1]}")
    
    print("\n[3] CLICKING btnSales...")
    btn_sales.click()
    time.sleep(1)
    
    print("[4] State AFTER click...")
    after = snapshot_content_areas()
    for info in after:
        print(f"  [{info['idx']}] children: {info['child_count']}, texts: {info['texts'][:1]}")
    
    print("\n[5] COMPARISON - What changed?")
    
    changed_idx = []
    for i, (b, a) in enumerate(zip(before, after)):
        if b['child_count'] != a['child_count']:
            print(f"  ✓ Index {b['idx']}: children changed from {b['child_count']} to {a['child_count']}")
            changed_idx.append(b['idx'])
        
        if b['texts'] != a['texts']:
            print(f"  ✓ Index {b['idx']}: text changed from {b['texts']} to {a['texts']}")
            changed_idx.append(b['idx'])
    
    if not changed_idx:
        print("  ✗ NO CHANGES DETECTED IN LARGE CONTENT AREAS")
        print("\n  This means:")
        print("    - Either the click didn't work (confirmed)")
        print("    - Or the content changes are in a different location")
        print("    - Or the content is rendered differently (custom paint?)")
    
    print("\n[6] Checking Internet Explorer area (welcome page)...")
    for i, child in enumerate(children):
        try:
            class_name = child.class_name()
            if 'Internet Explorer' in class_name:
                print(f"  [{i}] {class_name}")
                rect = child.rectangle()
                print(f"       Position: {rect.left},{rect.top} - {rect.right},{rect.bottom}")
                print(f"       Size: {rect.right-rect.left}x{rect.bottom-rect.top}")
        except:
            pass
    
    print("\n[7] Looking for MDI child windows inside Navigator...")
    for i, child in enumerate(children):
        try:
            class_name = child.class_name()
            if 'MDI' in class_name:
                print(f"  [{i}] {class_name}")
                child_children = child.children() if hasattr(child, 'children') else []
                print(f"       Contains {len(child_children)} children")
                for j, cc in enumerate(child_children[:5]):
                    print(f"         [{j}] {cc.class_name()}")
        except Exception as e:
            pass

except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
