"""
Simple G2 Menu Detection Script

This script attempts to find and report all menu items visible after login.
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time


def find_g2_windows():
    """Find all G2-related windows"""
    try:
        all_windows = findwindows.find_windows()
        g2_windows = []
        
        for handle in all_windows:
            try:
                import ctypes
                GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
                GetWindowText = ctypes.windll.user32.GetWindowTextW
                length = GetWindowTextLength(handle)
                buff = ctypes.create_unicode_buffer(length + 1)
                GetWindowText(handle, buff, length + 1)
                title = buff.value
                
                if "G2" in title:
                    g2_windows.append((handle, title))
            except:
                pass
        
        return g2_windows
    except Exception as e:
        print(f"Error finding windows: {e}")
        return []


def explore_window(window_obj, depth=0, max_depth=6):
    """Recursively explore and print window elements"""
    items = []
    
    if depth > max_depth:
        return items
    
    try:
        try:
            name = window_obj.name()
            if name and len(name.strip()) > 0:
                items.append(("  " * depth) + f"• {name}")
        except:
            pass
        
        try:
            control_type = window_obj.control_type()
            if control_type:
                pass  # Suppress for cleaner output
        except:
            pass
        
        try:
            children = window_obj.children()
            for child in children:
                items.extend(explore_window(child, depth + 1, max_depth))
        except:
            pass
    except:
        pass
    
    return items


def main():
    """Main menu detection"""
    print("\n" + "="*70)
    print("G2 WINDOW AND MENU SCANNER")
    print("="*70)
    
    print("\n[1] Scanning for G2 windows...")
    g2_windows = find_g2_windows()
    
    print(f"\n    Found {len(g2_windows)} G2 windows:")
    for i, (handle, title) in enumerate(g2_windows):
        print(f"      {i+1}. Handle: {handle}, Title: {title}")
    
    # Look for Navigator window
    navigator_windows = [w for w in g2_windows if "Navigator" in w[1]]
    
    if not navigator_windows:
        print("\n[X] No G2 Navigator window found")
        print("\n    Try:")
        print("    1. Complete login in the G2 Login window")
        print("    2. Wait for the Navigator to open")
        print("    3. Run this script again")
        return False
    
    navigator_handle = navigator_windows[0][0]
    print(f"\n[2] Connecting to G2 Navigator (handle: {navigator_handle})...")
    
    try:
        app = Application(backend='uia').connect(handle=navigator_handle)
        window = app.window()
        print("    [OK] Connected successfully")
        
        print("\n[3] Scanning window structure...")
        menu_items = explore_window(window)
        
        print(f"\n    Found {len(menu_items)} menu items:\n")
        for item in menu_items:
            print(f"    {item}")
        
        # Expected items
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
        
        # Check which items were found
        found_items = []
        for item in expected_items:
            # Check if item appears in any of the menu items
            for menu_item in menu_items:
                if item in menu_item:
                    found_items.append(item)
                    break
        
        print(f"\n[4] Verification Results:")
        print(f"    Expected items: {len(expected_items)}")
        print(f"    Found items: {len(found_items)}")
        print(f"    Match rate: {(len(found_items) / len(expected_items) * 100):.1f}%")
        
        print(f"\n    [OK] Found:")
        for item in found_items:
            print(f"      ✓ {item}")
        
        if len(found_items) < len(expected_items):
            missing = [item for item in expected_items if item not in found_items]
            print(f"\n    [X] Missing ({len(missing)}):")
            for item in missing:
                print(f"      ✗ {item}")
        
        print("\n" + "="*70)
        if len(found_items) >= len(expected_items) * 0.8:
            print("RESULT: [OK] VERIFICATION PASSED (80%+ match)")
        else:
            print("RESULT: [X] VERIFICATION INCOMPLETE")
        print("="*70 + "\n")
        
        return len(found_items) >= len(expected_items) * 0.8
        
    except Exception as e:
        print(f"\n[X] Error connecting to window: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
