"""
Scan G2 Navigator menus using win32 backend
"""
from pywinauto.application import Application
from pywinauto import findwindows
import warnings
warnings.filterwarnings('ignore')

handles = findwindows.find_windows(title_re='.*Navigator.*')
print(f'Found {len(handles)} Navigator windows')

if handles:
    try:
        app = Application(backend='win32').connect(handle=handles[0])
        window = app.top_window()
        print('Connected with win32 backend to Navigator')
        
        # Get all children with their properties
        children = window.children()
        print(f'\nFound {len(children)} direct children:')
        
        all_texts = []
        
        for i, child in enumerate(children):
            try:
                text = child.window_text()
                class_name = child.class_name()
                handle = child.handle
                
                if text and len(text.strip()) > 0:
                    print(f'{i+1:2d}. {text} [{class_name}]')
                    all_texts.append(text)
            except:
                pass
        
        # Remove duplicates and empty
        all_texts = [t for t in all_texts if t and len(t.strip()) > 0]
        print(f'\n{len(set(all_texts))} unique non-empty items')
        
        # Check for expected menus
        expected = [
            'Sales', 'My Dashboards', 'Sales Dashboard', 'My Tasks', 'Launch CRM',
            'Manage Sales Quotes', 'Update Sales Quotes', 'Print a Purchase Agreement',
            'Maintain Customers', 'Take Backup Deposits', 'Reconcile This Till',
            'Finance', 'Unit Inventory', 'Sales Reports', 'Rentals', 'Utilities',
            'Configure Buttons'
        ]
        
        print(f'\nChecking for {len(expected)} expected items:')
        found = [item for item in expected if item in all_texts]
        print(f'Found: {len(found)}/{len(expected)}')
        
        for item in found:
            print(f'  [OK] {item}')
        
        if len(found) < len(expected):
            missing = [item for item in expected if item not in all_texts]
            print(f'\nMissing: {len(missing)}')
            for item in missing:
                print(f'  [X] {item}')
        
        print(f'\nAll found items:')
        for text in sorted(set(all_texts)):
            print(f'  - {text}')
    
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()
