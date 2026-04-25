"""
G2 NAVIGATOR MENU VERIFICATION - Real Structure

Verifies that the expected menu categories appear after successful login.
Uses the actual G2 Navigator structure found via win32 backend.
"""

from pywinauto.application import Application
from pywinauto import findwindows
import time
import warnings
warnings.filterwarnings('ignore')

# Expected main menu categories (based on actual G2 Navigator structure)
EXPECTED_MENUS = [
    'Sales',
    'Service',
    'Accounting', 
    'Admin',
    'Parts'
]

# Additional items that might appear
OPTIONAL_MENUS = [
    'Utilities',
    'Configure Buttons',
    'Finance',
    'Reports',
    'Dashboard',
    'My Tasks'
]


def verify_navigator_menus():
    """
    Verify that G2 Navigator is open and contains expected menu items.
    """
    print("\n" + "="*70)
    print("G2 NAVIGATOR MENU VERIFICATION")
    print("="*70)
    
    # Find Navigator window
    print("\n[1] Looking for G2 Navigator window...")
    handles = findwindows.find_windows(title_re='.*Navigator.*')
    
    if not handles:
        print("[X] G2 Navigator window not found")
        print("    Please log in to G2 first")
        return False
    
    print(f"[OK] Found G2 Navigator window (handle: {handles[0]})")
    
    # Connect and scan menus
    print("\n[2] Connecting to Navigator and scanning menus...")
    try:
        app = Application(backend='win32').connect(handle=handles[0])
        window = app.top_window()
        
        # Get all window texts
        children = window.children()
        all_texts = set()
        
        for child in children:
            try:
                text = child.window_text()
                if text and len(text.strip()) > 0:
                    all_texts.add(text)
            except:
                pass
        
        print(f"[OK] Found {len(all_texts)} unique menu items")
        
        # Check for expected menus
        print("\n[3] Verifying expected menu items...")
        found_expected = []
        missing_expected = []
        
        for menu in EXPECTED_MENUS:
            if menu in all_texts:
                found_expected.append(menu)
                print(f"    [OK] {menu}")
            else:
                missing_expected.append(menu)
                print(f"    [X] {menu}")
        
        # Check optional menus
        print("\n[4] Checking optional items...")
        found_optional = []
        for menu in OPTIONAL_MENUS:
            if menu in all_texts:
                found_optional.append(menu)
                print(f"    [OK] {menu}")
        
        # Summary
        print("\n[5] Summary:")
        match_rate = (len(found_expected) / len(EXPECTED_MENUS) * 100) if EXPECTED_MENUS else 0
        print(f"    Expected items: {len(found_expected)}/{len(EXPECTED_MENUS)} ({match_rate:.0f}%)")
        print(f"    Optional items: {len(found_optional)}/{len(OPTIONAL_MENUS)}")
        print(f"    Total items found: {len(all_texts)}")
        
        # Full list
        print("\n[6] All menu items available:")
        for item in sorted(all_texts):
            print(f"    • {item}")
        
        # Result
        print("\n" + "="*70)
        if len(found_expected) >= len(EXPECTED_MENUS) * 0.8:
            print("RESULT: [OK] MENU VERIFICATION PASSED")
            print(f"        {len(found_expected)}/{len(EXPECTED_MENUS)} expected items found")
            print("="*70 + "\n")
            return True
        else:
            print("RESULT: [X] VERIFICATION FAILED")
            print(f"        {len(missing_expected)} expected items missing")
            print("="*70 + "\n")
            return False
    
    except Exception as e:
        print(f"\n[X] Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = verify_navigator_menus()
    exit(0 if success else 1)
