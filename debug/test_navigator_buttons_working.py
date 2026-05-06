"""
Test the updated NavigatorScreen with working button clicks
"""

import sys
import time

# Add project root to path
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen

def main():
    print("=" * 60)
    print("NavigatorScreen - Button Click Test (WORKING SOLUTION)")
    print("=" * 60)
    
    # Create navigator screen
    print("\n[1] Creating NavigatorScreen...")
    nav = NavigatorScreen(discover_from_window=True)
    
    # Check if navigator is present
    print("\n[2] Checking Navigator presence...")
    if not nav.is_navigator_present():
        print("  ERROR: Navigator window not found!")
        return False
    print("  ✓ Navigator found and connected")
    
    # Get all menus
    print("\n[3] Discovering available menus...")
    menus = nav.get_all_menu_items()
    print(f"  Found {len(menus)} menu items:")
    for menu in sorted(menus):
        if menu in nav.EXPECTED_MENU_ITEMS:
            print(f"    ✓ {menu}")
    
    # Verify all expected menus
    print("\n[4] Verifying all expected menus...")
    verification = nav.verify_all_menus()
    all_present = all(verification.values())
    
    if all_present:
        print("  ✓ All expected menus are present")
    else:
        print("  ✗ Some menus are missing:")
        for menu, is_present in verification.items():
            if not is_present:
                print(f"    - {menu}")
    
    # Get current active menu
    print("\n[5] Getting currently active menu...")
    active = nav.get_active_menu()
    print(f"  Current active menu: {active}")
    
    # Test clicking each menu
    print("\n[6] Testing menu clicks...")
    test_menus = nav.EXPECTED_MENU_ITEMS.copy()
    
    all_clicks_successful = True
    for menu_name in test_menus:
        print(f"\n  Testing: {menu_name}")
        success = nav.click_menu_button(menu_name)
        
        if success:
            time.sleep(0.5)
            active = nav.get_active_menu()
            if active == menu_name:
                print(f"    ✓ Successfully clicked {menu_name} (now active: {active})")
            else:
                print(f"    ✗ Click executed but active menu is now: {active}")
                all_clicks_successful = False
        else:
            print(f"    ✗ Failed to click {menu_name}")
            all_clicks_successful = False
    
    # Final summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"  Navigator found:       {'✓ YES' if nav.is_navigator_present() else '✗ NO'}")
    print(f"  All menus present:     {'✓ YES' if all_present else '✗ NO'}")
    print(f"  All clicks successful: {'✓ YES' if all_clicks_successful else '✗ NO'}")
    print(f"  Current active menu:   {nav.get_active_menu()}")
    
    success = nav.is_navigator_present() and all_present and all_clicks_successful
    print(f"\n  OVERALL: {'✓ PASSED' if success else '✗ FAILED'}")
    
    return success

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
