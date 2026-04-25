"""
Inspect G2 Navigator using UIA element traversal
"""
from pywinauto.application import Application
from pywinauto import findwindows

handles = findwindows.find_windows(title_re='.*Navigator.*')
print(f'Found {len(handles)} navigator windows')

if handles:
    try:
        app = Application(backend='uia').connect(handle=handles[0])
        window = app.top_window()
        print(f'Connected to Navigator window')
        
        # Access element_info property
        elem_info = window.element_info
        print(f'Element info type: {type(elem_info)}')
        print(f'Element name: {elem_info.name}')
        print(f'Element type: {elem_info.control_type}')
        print(f'Element ID: {elem_info.automation_id}')
        
        # Now try to walk the tree
        print(f'\nTraversing element tree:')
        
        def walk_tree(elem, depth=0, max_depth=6):
            if depth > max_depth:
                return []
            
            items = []
            try:
                name = elem.name
                if name and len(str(name).strip()) > 0:
                    items.append((depth, name, elem.control_type))
            except:
                pass
            
            try:
                # Get children from element
                children = elem.children
                for child in children:
                    items.extend(walk_tree(child, depth + 1, max_depth))
            except Exception as e:
                pass
            
            return items
        
        all_items = walk_tree(elem_info)
        print(f'Found {len(all_items)} elements total')
        
        print('\nElement tree (first 30):')
        for depth, name, ctrl_type in all_items[:30]:
            indent = '  ' * depth
            print(f'{indent}- {name} [{ctrl_type}]')
        
        # Look for menu items
        print('\nLooking for expected menu items:')
        expected = [
            'Sales', 'My Dashboards', 'Sales Dashboard', 'My Tasks', 'Launch CRM',
            'Manage Sales Quotes', 'Update Sales Quotes', 'Print a Purchase Agreement',
            'Maintain Customers', 'Take Backup Deposits', 'Reconcile This Till',
            'Finance', 'Unit Inventory', 'Sales Reports', 'Rentals', 'Utilities',
            'Configure Buttons'
        ]
        
        names = [name for depth, name, ctrl_type in all_items]
        found = [item for item in expected if item in names]
        
        print(f'\nFound {len(found)}/{len(expected)} expected items:')
        for item in found:
            print(f'  [OK] {item}')
        
        if len(found) < len(expected):
            missing = [item for item in expected if item not in names]
            print(f'\nMissing ({len(missing)}):')
            for item in missing:
                print(f'  [X] {item}')
    
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()
