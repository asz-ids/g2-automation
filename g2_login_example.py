"""
G2 Login Automation Example Script

This script demonstrates how to use the LoginScreen class to automate
login to the G2 application with the real running instance.

Before running:
1. Start the G2 application
2. Leave login screen visible
3. Run: python g2_login_example.py
"""

from screens.login_screen import LoginScreen
import time
from pathlib import Path

def main():
    """Main login automation flow."""
    print("\n" + "="*60)
    print("G2 LOGIN AUTOMATION EXAMPLE")
    print("="*60)
    
    try:
        # Step 1: Check if G2 login screen is visible
        print("\n[1] Checking for G2 Login screen...")
        login = LoginScreen()
        
        if not login.is_login_screen_visible(timeout_seconds=5):
            print("    ✗ G2 Login screen NOT found!")
            print("    → Please start G2 application and show login screen")
            print("    → Then run this script again")
            return False
        
        print("    ✓ G2 Login screen found!")
        
        # Step 2: Get login screen status
        print("\n[2] Getting screen information...")
        status = login.get_login_status()
        print(f"    Screen name: {status['screen_name']}")
        print(f"    Root element: {status['root_element']}")
        print(f"    Elements found: {status['elements_count']}")
        print(f"    Is visible: {status['is_visible']}")
        
        # Step 3: Capture initial screenshot
        print("\n[3] Capturing initial screenshot...")
        screenshot1 = login.capture_login_screen("01_login_screen_initial.png")
        print(f"    ✓ Saved: {screenshot1}")
        
        # Step 4: Enter credentials
        print("\n[4] Entering login credentials...")
        
        # IMPORTANT: Update these with your actual test credentials
        # Format for domain: "DOMAIN\\username" or just "username"
        DOMAIN = "DOMAIN"
        USERNAME = "aqadir.ids"
        PASSWORD = "Aqadir2801"
        
        print(f"    → Username: {USERNAME}")
        print(f"    → Domain: {DOMAIN}")
        
        # Enter username
        print("    Entering username...")
        login.enter_username(USERNAME)
        time.sleep(0.5)
        
        # Enter password
        print("    Entering password...")
        login.enter_password(PASSWORD)
        time.sleep(0.5)
        
        # # Enter domain if specified
        # if DOMAIN:
        #     print("    Entering domain...")
        #     login.enter_domain(DOMAIN)
        #     time.sleep(0.5)
        
        # Step 5: Capture before login
        print("\n[5] Capturing screenshot before login...")
        screenshot2 = login.capture_login_screen("02_login_credentials_entered.png")
        print(f"    ✓ Saved: {screenshot2}")
        
        # Step 6: Click login button
        print("\n[6] Clicking login button...")
        success = login.click_login()
        if success:
            print("    ✓ Login button clicked")
        else:
            print("    ✗ Failed to click login button")
            return False
        
        # Step 7: Wait for authentication
        print("\n[7] Waiting for authentication (30 seconds)...")
        time.sleep(30)
        
        # Step 8: Check if login was successful
        print("\n[8] Checking login result...")
        is_successful = login.is_login_successful(timeout_seconds=10)
        
        if is_successful:
            print("    ✓ LOGIN SUCCESSFUL!")
            print("\n" + "="*60)
            print("SUCCESS: User authenticated to G2")
            print("="*60)
            
            # Capture success
            screenshot3 = login.capture_login_screen("03_login_successful.png")
            print(f"\n    ✓ Success screenshot saved: {screenshot3}")
            return True
        else:
            print("    ✗ Login may have failed or timed out")
            print("\n" + "="*60)
            print("FAILURE: Could not verify successful login")
            print("="*60)
            
            # Capture failure
            screenshot3 = login.capture_login_screen("03_login_failed.png")
            print(f"\n    ✓ Failure screenshot saved: {screenshot3}")
            print("\nPossible reasons:")
            print("    • Invalid credentials provided")
            print("    • Network connectivity issue")
            print("    • Authentication server not responding")
            print("    • Check screenshot for error message")
            return False
    
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        print(f"    Type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    
    print("\n" + "="*60)
    if success:
        print("Result: ✓ AUTOMATION COMPLETED SUCCESSFULLY")
    else:
        print("Result: ✗ AUTOMATION FAILED OR INCOMPLETE")
    print("="*60 + "\n")
