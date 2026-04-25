"""
Enhanced G2 Menu Detection Script - Uses UIA tree inspection
"""

from pywinauto.application import Application
import ctypes


def find_g2_navigator():
    """Find G2 Navigator window by title"""
    try:
        app = Application(backend='uia')
        windows = app.windows()
        
        for window in windows:
            try:
                title = window.name()
                if "G2 Navigator" in title or "Navigator" in title:
                    return window
            except:
                pass
    except:
        pass
    
    return None


def element_to_dict(elem, depth=0, max_depth=8):
    """Convert UIA element to dict with all properties"""
    result = {}
    
    if depth > max_depth:
        return None
    
    try:
        # Basic properties
        try:
            result['name'] = elem.name()
        except:
            result['name'] = "[No name]"
        
        try:
            result['auto_id'] = elem.automation_id()
        except:
            result['auto_id'] = "[No ID]"
        
        try:
            result['control_type'] = elem.control_type()
        except:
            result['control_type'] = "[Unknown]"
        
        try:
            result['class_name'] = elem.class_name()
        except:
            result['class_name'] = "[Unknown]"
        
        # Try to get visible text content
        try:
            if hasattr(elem, 'text_'):
                result['text'] = elem.text()
            elif hasattr(elem, 'value_pattern'):
                result['text'] = "has_value_pattern"
        except:
            pass
    
    except Exception as e:
        return None
    
    # Get children
    children = []
    try:
        elem_children = elem.children()
        for child in elem_children:
            child_dict = element_to_dict(child, depth + 1, max_depth)
            if child_dict:
                children.append(child_dict)
    except:
        pass
    
    if children:
        result['children'] = children
    
    return result


def print_tree(elem, depth=0, max_depth=6):
    """Print element tree structure"""
    if depth > max_depth:
        return
    
    try:
        name = elem.name()
        auto_id = elem.automation_id()
        control = elem.control_type()
        
        indent = "  " * depth
        print(f"{indent}├─ {name}")
        if auto_id:
            print(f"{indent}│  ID: {auto_id}")
        print(f"{indent}│  Type: {control}")
        
        children = elem.children()
        for child in children:
            print_tree(child, depth + 1, max_depth)
    except:
        pass


def main():
    """Main menu detection"""
    print("\n" + "="*70)
    print("G2 NAVIGATOR - ENHANCED MENU SCANNER (v2)")
    print("="*70)
    
    print("\n[1] Finding G2 Navigator window...")
    nav_window = find_g2_navigator()
    
    if not nav_window:
        print("[X] G2 Navigator window not found")
        print("    Please log in to G2 first")
        return False
    
    print("[OK] G2 Navigator found")
    print(f"    Window name: {nav_window.name()}")
    
    print("\n[2] Analyzing window structure (up to depth 6)...")
    print("\n" + "-"*70)
    print_tree(nav_window, depth=0, max_depth=6)
    print("-"*70)
    
    print("\n[3] Extracting menu items...")
    
    # Get all descendants (not just children)
    all_items = []
    
    def collect_items(elem, depth=0, max_depth=8):
        if depth > max_depth:
            return
        
        try:
            name = elem.name()
            auto_id = elem.automation_id()
            
            # Skip empty names and common non-menu elements
            if name and len(name.strip()) > 0:
                if name not in ["G2 Navigator", "[No name]", ""]:
                    all_items.append({
                        'name': name,
                        'auto_id': auto_id,
                        'depth': depth
                    })
            
            children = elem.children()
            for child in children:
                collect_items(child, depth + 1, max_depth)
        except:
            pass
    
    collect_items(nav_window)
    
    # Remove duplicates
    unique_items = {}
    for item in all_items:
        unique_items[item['name']] = item
    
    print(f"\n    Found {len(unique_items)} unique items:")
    for name, item in sorted(unique_items.items()):
        print(f"      • {name}")
        if item['auto_id']:
            print(f"        ID: {item['auto_id']}")
    
    # Check for expected items
    expected_items = [
        "Sales",
        "My Dashboards", 
        "Sales Dashboard",
        "My Tasks",
        "Launch CRM",
        "Manage Sales Quotes",
        "Update Sales Quotes",
        "Print a Purchase Agreement",
        "Maintain Customers",
        "Take Backup Deposits",
        "Reconcile This Till",
        "Finance",
        "Unit Inventory",
        "Sales Reports",
        "Rentals",
        "Utilities",
        "Configure Buttons",
    ]
    
    print("\n[4] Checking expected menu items...")
    found_expected = []
    for expected in expected_items:
        if expected in unique_items:
            found_expected.append(expected)
            print(f"    [OK] {expected}")
        else:
            print(f"    [X] {expected}")
    
    print(f"\n    Match rate: {len(found_expected)}/{len(expected_items)} ({(len(found_expected)/len(expected_items)*100):.0f}%)")
    
    print("\n" + "="*70)
    if len(found_expected) >= len(expected_items) * 0.8:
        print("RESULT: [OK] MENU VERIFICATION PASSED")
    else:
        print("RESULT: [!] PARTIAL - Some menus found")
    print("="*70 + "\n")
    
    return len(found_expected) >= len(expected_items) * 0.5


if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n[X] Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
