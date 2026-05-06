"""
Last attempt: Check if G2 exposes COM objects or application model
"""
import pywinauto
from pywinauto import Application
import pywinauto.findwindows

try:
    print("[1] Searching for COM objects in G2...")
    
    # Try to access through COM
    try:
        import win32com.client
        print("  pywin32 COM available")
        
        # Try to get G2 object
        try:
            g2 = win32com.client.GetObject("", "G2.Application")
            print("  Got G2.Application COM object!")
            print(f"  Methods: {[m for m in dir(g2) if not m.startswith('_')][:10]}")
        except Exception as e:
            print(f"  G2.Application not available: {e}")
    except ImportError:
        print("  pywin32 COM not available")
    
    print("\n[2] Checking if buttons are part of Infragistics ultraExplorerBar...")
    
    windows = pywinauto.findwindows.find_windows(title_re='.*Navigator.*')
    app = Application(backend='win32').connect(handle=windows[0])
    nav = app.window(handle=windows[0])
    children = nav.children()
    
    # Look for ultraExplorerBar
    for i, child in enumerate(children):
        class_name = child.class_name()
        try:
            texts = child.texts() if hasattr(child, 'texts') else []
        except:
            texts = []
        
        # Print anything that might be an explorer bar
        if 'Window' in class_name and len(texts) > 0 and texts[0] and i < 15:
            print(f"  [{i}] {class_name} - text: '{texts[0]}'")
        elif 'explorer' in class_name.lower() or 'ultra' in class_name.lower():
            print(f"  [{i}] {class_name}")
    
    print("\n[3] Attempting to interact with parent of btnSales...")
    
    # Find btnSales
    btn_sales = None
    for child in children:
        try:
            if hasattr(child, 'handle') and child.handle == 398226:
                btn_sales = child
                break
        except:
            pass
    
    if btn_sales:
        # Get its immediate parent
        parent = btn_sales.parent()
        print(f"  Button parent: {parent.class_name()}")
        print(f"  Parent texts: {parent.texts() if hasattr(parent, 'texts') else 'N/A'}")
        
        # Get grandparent
        grandparent = parent.parent()
        print(f"  Grandparent: {grandparent.class_name()}")
        print(f"  Grandparent texts: {grandparent.texts() if hasattr(grandparent, 'texts') else 'N/A'}")
        
        # Try clicking the parent group instead
        print("\n  Attempting to click parent element...")
        import time
        parent.click()
        time.sleep(0.5)
        print(f"  Navigator children after: {len(nav.children())}")
    
    print("\n[4] Looking for ANY programmatic way to trigger menu...")
    print("  Checking if there's a keyboard shortcut...")
    
    # Try Alt+S for Sales
    import time
    nav.set_focus()
    time.sleep(0.2)
    nav.send_keystrokes('%s')  # Alt+S
    time.sleep(0.5)
    print(f"  Navigator children after Alt+S: {len(nav.children())}")
    
except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
