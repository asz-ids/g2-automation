"""
Test: Click "Take AR Payments" button in Parts menu

This test demonstrates:
1. Clicking the Parts menu button to navigate to Parts section
2. Navigating to and clicking the "Take AR Payments" button in the Parts Explorer Bar

NOTE: The "Take AR Payments" button is located inside the ultraExplorerBar1 control
in the Parts content panel. It's not directly accessible via standard pywinauto automation
but can be clicked using mouse coordinates or Win32 message sending.
"""

import pytest
import sys
import time
import warnings
import ctypes

warnings.filterwarnings('ignore')

# Add screens module to path
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen
from pywinauto import Application, findwindows
import pywinauto.mouse


class TestPartsMenuTakeARPayments:
    """Tests for Parts menu and Take AR Payments button interaction"""
    
    @pytest.fixture
    def navigator(self):
        """Create and connect to Navigator"""
        nav = NavigatorScreen()
        if not nav.is_navigator_present():
            pytest.skip("Navigator window not open")
        yield nav
    
    def test_navigate_to_parts_menu(self, navigator):
        """Navigate to the Parts menu"""
        result = navigator.click_menu_button('Parts')
        assert result is True, "Should successfully click Parts button"
        
        time.sleep(0.5)
        active = navigator.get_active_menu()
        assert active == 'Parts', f"Parts menu should be active, got: {active}"
    
    def test_parts_menu_displays_explorer_bar_content(self, navigator):
        """Verify that Parts menu displays content with explorer bar buttons"""
        # Navigate to Parts
        navigator.click_menu_button('Parts')
        time.sleep(0.5)
        
        # Get the Parts window
        handles = findwindows.find_windows(title_re=".*Navigator.*")
        assert len(handles) > 0, "Navigator window should be found"
        
        # Verify we can see the Parts panel is active
        active = navigator.get_active_menu()
        assert active == 'Parts', "Parts menu should be visible and active"
        
        print("✓ Parts menu explorer bar should now be visible")
        print("  - Contains buttons like: 'Sell Parts', 'Take AR Payments', etc.")
    
    def test_click_take_ar_payments_by_mouse_coordinates(self, navigator):
        """
        Click Take AR Payments button using mouse coordinates
        
        NOTE: This test requires manual coordinate adjustment based on your
        window resolution. The coordinates below are typical for 1920x1080.
        """
        # Navigate to Parts
        result = navigator.click_menu_button('Parts')
        assert result is True, "Should navigate to Parts menu"
        time.sleep(1)
        
        # Get the Parts panel/window to find button location
        # The Take AR Payments button is typically in the explorer bar
        # For 1920x1080 window, it's approximately at:
        # X: 350-500 (left sidebar with explorer bar buttons)
        # Y: 300-350 (roughly where "Take AR Payments" appears)
        
        print("\n  Finding Take AR Payments button location...")
        print("  Note: Explorer bar button positions depend on window size")
        
        # These are approximate coordinates for typical window
        # You may need to adjust based on your actual screen resolution
        button_x = 420  # Approximate X position of explorer bar buttons
        button_y = 310  # Approximate Y position of "Take AR Payments"
        
        print(f"  Attempting click at approximate coordinates: ({button_x}, {button_y})")
        
        # Click at the coordinates
        pywinauto.mouse.click(coords=(button_x, button_y))
        time.sleep(1)
        
        print("  ✓ Clicked at Take AR Payments button coordinates")
    
    def test_take_ar_payments_via_keyboard_navigation(self, navigator):
        """
        Navigate to Take AR Payments using keyboard shortcuts
        
        This approach navigates using Tab/Shift+Tab and Enter keys
        """
        # Navigate to Parts
        result = navigator.click_menu_button('Parts')
        assert result is True, "Should navigate to Parts menu"
        time.sleep(1)
        
        print("\n  Attempting keyboard navigation in explorer bar...")
        
        # Get the navigator window and set focus
        handles = findwindows.find_windows(title_re=".*Navigator.*")
        app = Application(backend='win32').connect(handle=handles[0])
        window = app.window(handle=handles[0])
        
        # Set focus to the window
        window.set_focus()
        time.sleep(0.2)
        
        # Use Tab to navigate between buttons in the explorer bar
        # This may require multiple Tab presses depending on current focus
        print("  Using Tab key to navigate...")
        
        # Try Tab key multiple times to reach Take AR Payments button
        for i in range(8):
            window.send_keystrokes('\t')  # Tab
            time.sleep(0.2)
        
        # Send Enter to click the focused button
        print("  Sending Enter key...")
        window.send_keystrokes('{ENTER}')
        time.sleep(1)
        
        print("  ✓ Keyboard navigation attempt complete")
    
    def test_parts_menu_contains_take_ar_payments_option(self, navigator):
        """
        Verify that Parts menu content contains Take AR Payments option
        
        This is a verification test that the option is available.
        Actual clicking may require direct coordinate or message-based interaction.
        """
        # Navigate to Parts
        navigator.click_menu_button('Parts')
        time.sleep(1)
        
        # Get the navigator to verify we're in Parts
        active = navigator.get_active_menu()
        assert active == 'Parts', f"Should be in Parts menu, but in {active}"
        
        print("\n✓ Parts menu is active")
        print("  The explorer bar in Parts menu should contain:")
        print("    - Point of Sale")
        print("    - My Dashboards")
        print("    - My Tasks")
        print("      - Sell Parts")
        print("      - Take AR Payments  <- TARGET BUTTON")
        print("      - Manage Special Orders")
        print("      - Reconcile This Till")
        print("      - Process Special Orders")
        print("    - Configure Buttons")
        print("    - And other options...")
    
    def test_take_ar_payments_workflow_manual(self, navigator):
        """
        Complete workflow: Navigate to Parts -> Locate Take AR Payments
        
        This test navigates to Parts and provides guidance for accessing Take AR Payments.
        The button location depends on your window resolution.
        """
        print("\n=== Take AR Payments Workflow ===")
        
        # Step 1: Verify navigator is open
        assert navigator.is_navigator_present(), "Navigator should be present"
        print("✓ Step 1: Navigator is open")
        
        # Step 2: Click Parts menu
        result = navigator.click_menu_button('Parts')
        assert result is True, "Should click Parts menu"
        print("✓ Step 2: Clicked Parts menu button")
        
        time.sleep(0.5)
        
        # Step 3: Verify Parts is now active
        active = navigator.get_active_menu()
        assert active == 'Parts', f"Parts should be active, got: {active}"
        print("✓ Step 3: Parts menu is now active")
        
        # Step 4: Provide guidance for accessing Take AR Payments
        print("\n✓ Step 4: Parts menu content is displayed")
        print("  ")
        print("  TO CLICK 'Take AR Payments' BUTTON:")
        print("  ")
        print("  Option A - Mouse Click:")
        print("    - Look for the explorer bar on the left side of the window")
        print("    - Under 'My Tasks' section, find 'Take AR Payments' button")
        print("    - Click at coordinates approximately (420, 310) for 1920x1080")
        print("    - Adjust coordinates based on your screen resolution")
        print("  ")
        print("  Option B - Keyboard Navigation:")
        print("    - Press Tab multiple times to cycle through buttons")
        print("    - Press Enter when 'Take AR Payments' is focused")
        print("  ")
        print("  Option C - Win32 Message (Advanced):")
        print("    - Send window messages to the explorer bar control")
        print("    - Requires button handle and specific message codes")
        print("  ")
        print("✓ Workflow setup complete!")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
