"""Quick test to explore G2 Navigator structure"""
from pywinauto.application import Application
from pywinauto import findwindows

handles = findwindows.find_windows(title_re='.*Navigator.*')
print(f'Found {len(handles)} navigator windows')

if handles:
    app = Application(backend='uia').connect(handle=handles[0])
    window = app.top_window()
    print(f'Connected successfully')
    
    elements = []
    
    def walk(elem, depth=0, max_depth=6):
        if depth > max_depth:
            return
        try:
            name = elem.name()
            auto_id = elem.automation_id()
            control = elem.control_type()
            
            if name and len(name.strip()) > 0:
                elements.append({
                    'depth': depth,
                    'name': name,
                    'id': auto_id,
                    'type': control
                })
            
            for child in elem.children():
                walk(child, depth + 1, max_depth)
        except:
            pass
    
    walk(window)
    
    print(f'\nFound {len(elements)} total elements')
    print('\nFirst 30 elements:')
    for item in elements[:30]:
        indent = '  ' * item['depth']
        print(f"{indent}- {item['name']} [{item['type']}]")
        if item['id']:
            print(f"{indent}  ID: {item['id']}")
