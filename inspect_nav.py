"""
Inspect G2 Navigator using UIA inspection directly
"""
from pywinauto.application import Application
from pywinauto import findwindows
from pywinauto.uia_element_info import UIAElementInfo

handles = findwindows.find_windows(title_re='.*Navigator.*')
print(f'Found {len(handles)} navigator windows: {handles}')

if handles:
    try:
        app = Application(backend='uia').connect(handle=handles[0])
        window = app.top_window()
        print(f'Connected successfully')
        print(f'Window type: {type(window)}')
        print(f'Has element: {hasattr(window, "element_info")}')
        
        if hasattr(window, "element_info"):
            elem_info = window.element_info()
            print(f'Element info: {elem_info}')
            print(f'Element type: {type(elem_info)}')
            
            # Try different ways to get children
            try:
                print(f'\nTrying .children():')
                children = window.children()
                print(f'Got {len(children)} children')
                for i, child in enumerate(children[:5]):
                    print(f'  Child {i}: {type(child)}')
            except Exception as e:
                print(f'Error with .children(): {e}')
            
            try:
                print(f'\nTrying direct property access:')
                props = dir(window)
                menu_props = [p for p in props if 'menu' in p.lower() or 'child' in p.lower()]
                print(f'Menu/child props: {menu_props}')
            except Exception as e:
                print(f'Error: {e}')
    
    except Exception as e:
        print(f'Connection error: {e}')
        import traceback
        traceback.print_exc()
