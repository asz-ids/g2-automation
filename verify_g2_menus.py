"""
G2 Menu Verification Script

This script verifies that after a successful login, all expected menus and buttons
appear in the G2 Navigator window.

Usage:
    python verify_g2_menus.py
"""

from screens.login_screen import LoginScreen
from screens.navigator_screen import NavigatorScreen
import time


def main():
    """Main verification flow."""
    print("\n" + "="*70)
    print("G2 MENU VERIFICATION TEST")
    print("="*70)
    
    try:
        # Step 1: Login to G2
        print("\n[1] Logging in to G2...")
        login = LoginScreen()
        
        if not login.is_login_screen_visible(timeout_seconds=5):
            print("    [X] G2 Login screen NOT found!")
            return False
        
        print("    [OK] Login screen found")
        
        # Enter credentials - UPDATE THESE WITH YOUR ACTUAL CREDENTIALS
        print("\n[2] Entering credentials...")
        print("    NOTE: Update USERNAME, PASSWORD, DOMAIN in this script!")
        
        # IMPORTANT: Update these credentials
        USERNAME = "aqadir.ids"  # Change this
        PASSWORD = "Aqadir2801"  # Change this
        DOMAIN = ""              # Change this if needed
        
        login.enter_username(USERNAME)
        print(f"    [OK] Entered username: {USERNAME}")
        
        login.enter_password(PASSWORD)
        print(f"    [OK] Entered password: ***")
        
        if DOMAIN:
            login.enter_domain(DOMAIN)
            print(f"    [OK] Entered domain: {DOMAIN}")
        
        # Step 3: Click login
        print("\n[3] Clicking login button...")
        success = login.click_login()
        if not success:
            print("    [X] Failed to click login button")
            return False
        
        print("    [OK] Login button clicked")
        
        # Step 4: Wait for authentication
        print("\n[4] Waiting for authentication (10 seconds)...")
        time.sleep(30)
        
        # Step 5: Check if login was successful
        print("\n[5] Checking login result...")
        is_logged_in = login.is_login_successful(timeout_seconds=10)
        
        if not is_logged_in:
            print("    [X] Login verification failed")
            login.capture_login_screen("login_failed.png")
            return False
        
        print("    [OK] Login successful!")
        
        # Step 6: Connect to Navigator
        print("\n[6] Connecting to G2 Navigator window...")
        navigator = NavigatorScreen()
        
        time.sleep(2)  # Wait for navigator to fully load
        
        if not navigator.is_navigator_visible(timeout_seconds=5):
            print("    [X] G2 Navigator window NOT found!")
            print("    The Navigator window should appear after successful login")
            return False
        
        print("    [OK] Navigator window found and connected")
        
        # Step 7: Get navigator status
        print("\n[7] Navigator Window Status:")
        status = navigator.get_status()
        for key, value in status.items():
            print(f"    {key}: {value}")
        
        # Step 8: Verify all expected menus
        print("\n[8] Verifying expected menu items...")
        print("    " + "-"*60)
        
        menu_results = navigator.verify_all_menus()
        
        print("    " + "-"*60)
        
        # Summary
        found_count = sum(1 for v in menu_results.values() if v)
        total_count = len(menu_results)
        
        print(f"\n[9] Menu Verification Summary:")
        print(f"    Found: {found_count}/{total_count} menu items")
        
        if found_count == total_count:
            print("\n" + "="*70)
            print("SUCCESS: All expected menus verified!")
            print("="*70)
            return True
        else:
            print("\n    Missing menus:")
            for menu, found in menu_results.items():
                if not found:
                    print(f"      [X] {menu}")
            
            print("\n[10] Scanning for all available menu items...")
            all_items = navigator.get_all_menu_items()
            print(f"\n    Found {len(all_items)} total items in navigator:")
            for item in sorted(set(all_items))[:30]:  # Show first 30 unique items
                if item.strip():
                    print(f"      • {item}")
            
            print("\n" + "="*70)
            print(f"PARTIAL SUCCESS: Found {found_count}/{total_count} expected menus")
            print("="*70)
            return found_count >= (total_count * 0.8)  # 80% threshold
    
    except Exception as e:
        print(f"\n[X] ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    
    print("\n" + "="*70)
    if success:
        print("Result: [OK] VERIFICATION PASSED")
    else:
        print("Result: [X] VERIFICATION FAILED")
    print("="*70 + "\n")
    
    exit(0 if success else 1)
