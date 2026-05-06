"""
Map out exact button and panel indices in current state
"""
import pywinauto
from pywinauto import Application
import pywinauto.findwindows

try:
    windows = pywinauto.findwindows.find_windows(title_re='.*Navigator.*')
    app = Application(backend='win32').connect(handle=windows[0])
    nav = app.window(handle=windows[0])
    children = nav.children()
    
    print("[1] Mapping buttons to indices by automation_id...")
    buttons_by_auto_id = {}
    
    for i, child in enumerate(children):
        try:
            auto_id_prop = child.automation_id
            if callable(auto_id_prop):
                auto_id = auto_id_prop()
            else:
                auto_id = auto_id_prop
            
            if auto_id and 'btn' in auto_id.lower():
                handle = child.handle
                buttons_by_auto_id[auto_id] = {'idx': i, 'handle': handle}
        except:
            pass
    
    print("  Buttons found:")
    for auto_id, info in sorted(buttons_by_auto_id.items()):
        print(f"    {auto_id:20s} idx={info['idx']:2d} handle={info['handle']}")
    
    print("\n[2] Mapping content panels to indices by text...")
    panels_by_text = {}
    
    for i, child in enumerate(children):
        try:
            texts = child.texts() if hasattr(child, 'texts') else []
            if texts and texts[0] in ['Sales', 'Service', 'Accounting', 'Admin', 'Parts']:
                label = texts[0]
                rect = child.rectangle()
                width = rect.right - rect.left
                height = rect.bottom - rect.top
                
                # Look for large panels (1135x134 is the content size)
                if width > 1000:
                    is_visible = child.is_visible() if hasattr(child, 'is_visible') else None
                    handle = child.handle
                    
                    if label not in panels_by_text:
                        panels_by_text[label] = []
                    
                    panels_by_text[label].append({
                        'idx': i,
                        'handle': handle,
                        'size': (width, height),
                        'visible': is_visible,
                    })
        except:
            pass
    
    print("  Content panels found:")
    for label in ['Sales', 'Service', 'Accounting', 'Admin', 'Parts']:
        if label in panels_by_text:
            for panel_info in panels_by_text[label]:
                status = "V" if panel_info['visible'] else "H"
                print(f"    {label:12s} idx={panel_info['idx']:2d} handle={panel_info['handle']:10d} size={panel_info['size']} [{status}]")
    
    print("\n[3] CURRENT MAPPING (based on automation_id):")
    print("  Buttons (by automation_id):")
    print(f"    btnSales:       idx={buttons_by_auto_id['btnSales']['idx']}")
    print(f"    btnService:     idx={buttons_by_auto_id['btnService']['idx']}")
    print(f"    btnAccounting:  idx={buttons_by_auto_id['btnAccounting']['idx']}")
    print(f"    btnAdmin:       idx={buttons_by_auto_id['btnAdmin']['idx']}")
    print(f"    btnParts:       idx={buttons_by_auto_id['btnParts']['idx']}")
    
    print("\n  Content Panels (first large one per label):")
    for label in ['Sales', 'Service', 'Accounting', 'Admin', 'Parts']:
        if label in panels_by_text:
            first_panel = panels_by_text[label][0]
            print(f"    {label:12s}: idx={first_panel['idx']}")
    
    print("\n[4] What we assumed vs reality:")
    print("  Assumed panel indices: Sales=15, Service=26, Accounting=29, Admin=28, Parts=27")
    assumed_indices = {'Sales': 15, 'Service': 26, 'Accounting': 29, 'Admin': 28, 'Parts': 27}
    
    for label in ['Sales', 'Service', 'Accounting', 'Admin', 'Parts']:
        if label in panels_by_text:
            actual_idx = panels_by_text[label][0]['idx']
            assumed_idx = assumed_indices[label]
            match = "✓" if actual_idx == assumed_idx else "✗"
            print(f"    {match} {label:12s}: assumed={assumed_idx:2d}, actual={actual_idx:2d}")

except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
