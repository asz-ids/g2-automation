#!/usr/bin/env python3
"""
Example usage of the working NavigatorScreen button clicking

This demonstrates the complete solution for clicking G2 Navigator menu buttons.
"""

import time
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen


def example_basic_usage():
    """Basic example of clicking menu buttons"""
    
    print("Example 1: Basic Menu Navigation")
    print("-" * 40)
    
    # Create navigator screen
    nav = NavigatorScreen()
    
    # Click Sales menu (should already be active on login)
    nav.click_menu_button('Sales')
    print("Navigated to Sales menu")
    time.sleep(1)
    
    # Click Service menu
    nav.click_menu_button('Service')
    print("Navigated to Service menu")
    time.sleep(1)
    
    # Click Accounting menu
    nav.click_menu_button('Accounting')
    print("Navigated to Accounting menu")
    time.sleep(1)


def example_with_verification():
    """Example with menu verification"""
    
    print("\nExample 2: Menu Navigation with Verification")
    print("-" * 40)
    
    nav = NavigatorScreen()
    
    # List all available menus
    menus = nav.get_all_menu_items()
    print(f"Available menus: {', '.join(menus)}")
    
    # Navigate to each menu and verify
    for menu_name in ['Sales', 'Service', 'Accounting', 'Admin', 'Parts']:
        nav.click_menu_button(menu_name)
        
        # Small delay for UI update
        time.sleep(0.5)
        
        # Verify active menu
        active = nav.get_active_menu()
        
        if active == menu_name:
            print(f"✓ {menu_name}: Successfully activated")
        else:
            print(f"✗ {menu_name}: Failed (active={active})")


def example_repeated_clicks():
    """Example of clicking same menu multiple times"""
    
    print("\nExample 3: Repeated Menu Clicks")
    print("-" * 40)
    
    nav = NavigatorScreen()
    
    for i in range(3):
        print(f"\nIteration {i+1}:")
        
        nav.click_menu_button('Admin')
        time.sleep(0.5)
        print(f"  Clicked Admin: {nav.get_active_menu()}")
        
        nav.click_menu_button('Parts')
        time.sleep(0.5)
        print(f"  Clicked Parts: {nav.get_active_menu()}")


def example_error_handling():
    """Example with error handling"""
    
    print("\nExample 4: Error Handling")
    print("-" * 40)
    
    nav = NavigatorScreen()
    
    # Check if navigator exists
    if not nav.is_navigator_present():
        print("ERROR: Navigator not found!")
        return
    
    # Try to click valid menu
    if nav.click_menu_button('Service'):
        print("✓ Successfully clicked Service menu")
    else:
        print("✗ Failed to click Service menu")
    
    # Try to click non-existent menu (should handle gracefully)
    if nav.click_menu_button('InvalidMenu'):
        print("✓ Successfully clicked InvalidMenu")
    else:
        print("✗ Failed to click InvalidMenu (expected)")
    
    # Get status
    print(f"\nFinal active menu: {nav.get_active_menu()}")


if __name__ == '__main__':
    try:
        # Make sure G2 is running and Navigator is open
        print("=" * 60)
        print("G2 Navigator Button Click Examples")
        print("=" * 60)
        
        # Uncomment examples to run:
        example_basic_usage()
        example_with_verification()
        example_repeated_clicks()
        example_error_handling()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\nExecution interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
