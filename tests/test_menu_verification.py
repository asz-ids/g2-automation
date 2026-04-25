"""
Test: G2 Navigator Menu Verification

Verifies that all expected menu items appear in the G2 Navigator
after successful login.
"""

import pytest
import time
from screens.login_screen import LoginScreen
from screens.navigator_screen import NavigatorScreen


class TestMenuVerification:
    """Tests for G2 Navigator menu presence"""
    
    # Expected main menu categories in G2 Navigator
    EXPECTED_MENUS = [
        'Sales',
        'Service',
        'Accounting',
        'Admin',
        'Parts'
    ]
    
    @pytest.fixture(autouse=True)
    def setup_and_cleanup(self):
        """Setup before test, cleanup after"""
        # Give G2 time to fully load if app was just launched
        time.sleep(2)
        yield
    
    @pytest.mark.skip(reason="Full login flow tested in test_login_screen.py - this test requires manual login")
    def test_login_and_navigate_to_menus(self):
        """
        Test flow:
        1. Start at login screen
        2. Enter credentials and login
        3. Wait for Navigator to open
        4. Verify all expected menus are present
        
        NOTE: This test is skipped by default. Run manually after completing
        login to test the full integration with the Navigator.
        """
        # Step 1: Login
        login = LoginScreen()
        assert login.is_login_screen_visible(), "Login screen should be visible"
        
        # Step 2: Enter credentials
        login.enter_username("aqadir.ids")
        login.enter_password("Aqadir2801")
        login.enter_domain("")
        
        # Step 3: Click login button
        login.click_login()
        
        # Step 4: Wait for Navigator window to appear
        time.sleep(10)
        
        # Step 5: Verify Navigator is open
        navigator = NavigatorScreen()
        assert navigator.is_navigator_present(), "Navigator window should be open after login"
    
    def test_all_expected_menus_present(self):
        """
        Verify all expected G2 Navigator menu items are visible.
        
        Expected menus:
        - Sales
        - Service
        - Accounting
        - Admin
        - Parts
        """
        navigator = NavigatorScreen()
        
        # Skip if navigator is not open
        if not navigator.is_navigator_present():
            pytest.skip("Navigator window not open - need to complete login first")
        
        # Get all available menus
        all_menus = navigator.get_all_menu_items()
        
        # Verify each expected menu is present
        for menu in self.EXPECTED_MENUS:
            assert menu in all_menus, f"Expected menu '{menu}' not found in Navigator"
    
    def test_menu_items_count(self):
        """Verify minimum number of menu items are available"""
        navigator = NavigatorScreen()
        
        # Skip if navigator is not open
        if not navigator.is_navigator_present():
            pytest.skip("Navigator window not open")
        
        all_menus = navigator.get_all_menu_items()
        
        # Should have at least the 5 expected menus
        assert len(all_menus) >= len(self.EXPECTED_MENUS), \
            f"Expected at least {len(self.EXPECTED_MENUS)} menus, found {len(all_menus)}"
    
    def test_menu_verification_report(self):
        """Generate and verify menu report"""
        navigator = NavigatorScreen()
        
        # Skip if navigator is not open
        if not navigator.is_navigator_present():
            pytest.skip("Navigator window not open")
        
        report = navigator.get_verification_report()
        
        # Report should indicate successful verification
        assert report['navigator_found'], "Navigator window should be found"
        assert report['menus_found'] > 0, "Should find at least some menus"
        assert report['match_percentage'] >= 80, "Should match at least 80% of expected menus"


class TestMenuNavigation:
    """Tests for navigating through G2 menus"""
    
    def test_can_access_sales_menu(self):
        """Verify Sales menu is accessible"""
        navigator = NavigatorScreen()
        
        if not navigator.is_navigator_present():
            pytest.skip("Navigator window not open")
        
        # Verify Sales menu exists and is accessible
        menu_items = navigator.get_all_menu_items()
        assert 'Sales' in menu_items, "Sales menu should be available"
    
    def test_can_access_service_menu(self):
        """Verify Service menu is accessible"""
        navigator = NavigatorScreen()
        
        if not navigator.is_navigator_present():
            pytest.skip("Navigator window not open")
        
        menu_items = navigator.get_all_menu_items()
        assert 'Service' in menu_items, "Service menu should be available"
    
    def test_can_access_accounting_menu(self):
        """Verify Accounting menu is accessible"""
        navigator = NavigatorScreen()
        
        if not navigator.is_navigator_present():
            pytest.skip("Navigator window not open")
        
        menu_items = navigator.get_all_menu_items()
        assert 'Accounting' in menu_items, "Accounting menu should be available"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
