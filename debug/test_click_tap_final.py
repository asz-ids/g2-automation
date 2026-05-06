"""
Test: Click Take AR Payments Button
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen
import time

print("=" * 70)
print("TEST: Click Take AR Payments Button")
print("=" * 70)

# Step 1: Navigate to Parts menu
print("\n[STEP 1] Navigate to Parts menu...")
nav = NavigatorScreen()
success = nav.click_menu_button('Parts')
assert success, "Failed to click Parts menu"
print("  OK - Parts menu clicked")
time.sleep(1)

# Step 2: Verify Parts menu is active
print("\n[STEP 2] Verify Parts menu is active...")
active_menu = nav.get_active_menu()
assert active_menu == 'Parts', f"Expected Parts menu, got {active_menu}"
print(f"  OK - Active menu is: {active_menu}")

# Step 3: Click Take AR Payments button
print("\n[STEP 3] Click Take AR Payments button...")
success = nav.click_explorer_bar_button('Take AR Payments')
assert success, "Failed to click Take AR Payments button"
print("  OK - Take AR Payments button clicked")
time.sleep(2)

print("\n" + "=" * 70)
print("SUCCESS - All steps completed!")
print("=" * 70)
print("\nCheck the G2 window to see if Take AR Payments screen opened.")
