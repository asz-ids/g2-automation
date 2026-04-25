"""
G2 UIA Structure Diagnostic

This script helps diagnose the actual UIA properties of the G2 Login
application to ensure the framework is correctly mapped to your version.

Run this when:
1. Login screen is not found
2. Elements cannot be clicked
3. Text is not being entered
4. You want to verify element structure

Usage:
    python g2_diagnostic.py
"""

from drivers.uia_driver import UIADriver
from core.locator import Locator
from core.element import Element, UIAProperty
import json
from pathlib import Path

def diagnose_g2_login():
    """Diagnose G2 login screen structure."""
    print("\n" + "="*70)
    print("G2 UIA STRUCTURE DIAGNOSTIC")
    print("="*70)
    
    try:
        # Initialize UIA driver
        print("\n[1] Initializing UIA Driver...")
        driver = UIADriver()
        print("    ✓ UIA Driver initialized")
        
        # Try to find G2 Login window by title
        print("\n[2] Searching for G2 Login window...")
        g2_windows = driver.find_elements_by_property(
            property_name="Title",
            property_value="G2 Login",
            partial_match=True
        )
        
        if not g2_windows:
            print("    ✗ G2 Login window NOT found")
            print("\n    Possible issues:")
            print("    • G2 application is not running")
            print("    • Login window is minimized")
            print("    • Window title is different than 'G2 Login'")
            print("\n    Searching for any top-level windows...")
            
            # Find all top windows to help debug
            try:
                from pywinauto import desktop
                windows = desktop.windows()
                print(f"\n    Found {len(windows)} open windows:")
                for i, w in enumerate(windows[:15]):  # Show first 15
                    print(f"      {i+1}. {w.title} (ID: {w.handle})")
            except Exception as e:
                print(f"    Could not enumerate windows: {e}")
            
            return False
        
        print(f"    ✓ Found {len(g2_windows)} window(s)")
        
        # Analyze first G2 window
        print("\n[3] Analyzing G2 Login window structure...")
        g2_window = g2_windows[0]
        
        # Get window details
        print(f"\n    Window Details:")
        print(f"    • Name: {g2_window.name}")
        print(f"    • AutomationId: {g2_window.automation_id}")
        print(f"    • ControlType: {g2_window.control_type}")
        print(f"    • ClassName: {g2_window.class_name}")
        
        # Find all child elements
        print("\n[4] Scanning for child elements...")
        children = g2_window.children
        print(f"    ✓ Found {len(children)} direct children")
        
        # Build hierarchy
        print("\n[5] Building hierarchy structure...")
        hierarchy = {
            "window": {
                "name": g2_window.name,
                "automation_id": g2_window.automation_id,
                "control_type": g2_window.control_type,
                "children": []
            }
        }
        
        # Scan children recursively
        def scan_element(elem, parent_dict, depth=0, max_depth=4):
            """Recursively scan element hierarchy."""
            if depth > max_depth:
                return
            
            try:
                for child in elem.children:
                    child_info = {
                        "name": child.name,
                        "automation_id": child.automation_id,
                        "control_type": child.control_type,
                        "class_name": child.class_name,
                        "children": []
                    }
                    
                    # Look for key elements we expect
                    if any(key in str(child.automation_id or "").lower() 
                           for key in ["user", "pwd", "domain", "login", "cancel"]):
                        child_info["is_key_element"] = True
                    
                    parent_dict.append(child_info)
                    
                    # Recurse
                    scan_element(child, child_info["children"], depth + 1, max_depth)
            except:
                pass
        
        scan_element(g2_window, hierarchy["window"]["children"])
        
        # Find key elements
        print("\n[6] Searching for expected login controls...")
        expected_elements = {
            "Domain field": ["txtdomain", "domain"],
            "Username field": ["txtuser", "user"],
            "Password field": ["txtpwd", "password", "pwd"],
            "Login button": ["btnlogin", "login"],
            "Cancel button": ["btncancel", "cancel"]
        }
        
        def find_element_recursive(elem, keywords):
            """Find element by keywords in automation_id or name."""
            results = []
            try:
                id_str = (str(elem.automation_id or "")).lower()
                name_str = (str(elem.name or "")).lower()
                
                for keyword in keywords:
                    if keyword in id_str or keyword in name_str:
                        results.append(elem)
                        break
                
                for child in elem.children:
                    results.extend(find_element_recursive(child, keywords))
            except:
                pass
            
            return results
        
        element_map = {}
        for elem_name, keywords in expected_elements.items():
            found = find_element_recursive(g2_window, keywords)
            if found:
                element = found[0]
                element_map[elem_name] = {
                    "name": element.name,
                    "automation_id": element.automation_id,
                    "control_type": element.control_type,
                    "class_name": element.class_name
                }
                print(f"    ✓ {elem_name}:")
                print(f"        automation_id: {element.automation_id}")
                print(f"        control_type: {element.control_type}")
            else:
                print(f"    ✗ {elem_name}: NOT FOUND")
                print(f"        (searching for: {keywords})")
        
        # Save hierarchy to file
        print("\n[7] Saving detailed hierarchy...")
        output_file = Path("g2_hierarchy.json")
        with open(output_file, "w") as f:
            json.dump(hierarchy, f, indent=2)
        print(f"    ✓ Saved to: {output_file}")
        
        # Summary
        print("\n" + "="*70)
        print("DIAGNOSTIC SUMMARY")
        print("="*70)
        print(f"✓ G2 Login window found and analyzed")
        print(f"✓ Total elements in hierarchy: {len(children)} (direct children)")
        print(f"✓ Key elements found: {len(element_map)}/{len(expected_elements)}")
        
        if len(element_map) == len(expected_elements):
            print("\n✓ SUCCESS: All expected elements found!")
            print("\nYour G2 version appears compatible with the framework.")
        else:
            print(f"\n⚠ WARNING: Only {len(element_map)} of {len(expected_elements)} elements found")
            print("\nPossible actions:")
            print("1. Check g2_hierarchy.json for actual structure")
            print("2. Update LoginScreen._setup_elements_manual() with actual IDs")
            print("3. Use Inspect.exe for detailed UIA property inspection")
        
        # Save element map
        element_map_file = Path("g2_element_map.json")
        with open(element_map_file, "w") as f:
            json.dump(element_map, f, indent=2)
        print(f"\n✓ Element map saved to: {element_map_file}")
        
        return True
    
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_element_interaction():
    """Test if we can interact with found elements."""
    print("\n" + "="*70)
    print("ELEMENT INTERACTION TEST")
    print("="*70)
    
    try:
        from screens.login_screen import LoginScreen
        
        print("\n[1] Creating LoginScreen instance...")
        login = LoginScreen()
        print("    ✓ LoginScreen created")
        
        print("\n[2] Checking screen visibility...")
        is_visible = login.is_login_screen_visible(timeout_seconds=3)
        
        if not is_visible:
            print("    ✗ Login screen NOT visible")
            return False
        
        print("    ✓ Login screen is visible")
        
        print("\n[3] Getting login status...")
        status = login.get_login_status()
        print(f"    Status: {json.dumps(status, indent=6)}")
        
        print("\n✓ Element interaction test successful!")
        return True
    
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\nG2 Automation Framework Diagnostic Tool")
    print("This will analyze your G2 application's UIA structure.\n")
    
    input("Press Enter to start diagnosis (ensure G2 Login screen is visible)...\n")
    
    # Run diagnosis
    success = diagnose_g2_login()
    
    if success:
        print("\n" + "="*70)
        test_success = test_element_interaction()
        print("="*70 + "\n")
        
        if test_success:
            print("✓ All diagnostics passed!")
            print("✓ Framework should work with your G2 version")
            print("\nYou can now run: python g2_login_example.py")
        else:
            print("⚠ Diagnostics found issues")
            print("Check the output above and g2_hierarchy.json for details")
    else:
        print("\n✗ Diagnostics failed")
        print("Please verify:")
        print("  1. G2 application is running")
        print("  2. Login screen is visible (not minimized)")
        print("  3. Check g2_hierarchy.json for structure details")
