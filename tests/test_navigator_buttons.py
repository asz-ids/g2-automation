"""
Test: G2 Navigator Button Interaction

Tests for interacting with G2 Navigator menu buttons using the working
WM_LBUTTONDOWN/UP message approach.
"""

import pytest
import sys
import time
import warnings

warnings.filterwarnings('ignore')

# Add screens module to path
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen


class TestNavigatorButtonInteraction:
    """Tests for interacting with G2 Navigator buttons"""
    
    @pytest.fixture
    def navigator(self):
        """Create and connect to Navigator"""
        nav = NavigatorScreen()
        if not nav.is_navigator_present():
            pytest.skip("Navigator window not open")
        yield nav
    
    def test_navigator_present(self, navigator):
        """Verify Navigator window is open and connected"""
        assert navigator.is_navigator_present(), "Navigator should be present"
    
    def test_find_all_menu_buttons(self, navigator):
        """Find and verify all expected menu buttons exist"""
        menus = navigator.get_all_menu_items()
        
        assert len(menus) > 0, "Should find at least one menu button"
        
        expected = {'Sales', 'Service', 'Accounting', 'Admin', 'Parts'}
        found = set(menus)
        
        assert expected.issubset(found), f"Should find all expected menus. Found: {found}"
    
    def test_verify_all_menus_present(self, navigator):
        """Verify all expected menus are present in Navigator"""
        verification = navigator.verify_all_menus()
        
        all_present = all(verification.values())
        assert all_present, f"All menus should be present. Status: {verification}"
    
    def test_find_parts_button(self, navigator):
        """Find and verify the Parts button exists"""
        menus = navigator.get_all_menu_items()
        assert 'Parts' in menus, "Parts menu should be found"
    
    def test_click_parts_button(self, navigator):
        """Click the Parts button and verify it becomes active"""
        result = navigator.click_menu_button('Parts')
        assert result is True, "Parts button click should succeed"
        
        time.sleep(0.5)
        active = navigator.get_active_menu()
        assert active == 'Parts', f"Parts menu should be active, but got: {active}"
    
    def test_click_sales_button(self, navigator):
        """Click the Sales button and verify it becomes active"""
        result = navigator.click_menu_button('Sales')
        assert result is True, "Sales button click should succeed"
        
        time.sleep(0.5)
        active = navigator.get_active_menu()
        assert active == 'Sales', f"Sales menu should be active, but got: {active}"
    
    def test_click_service_button(self, navigator):
        """Click the Service button and verify it becomes active"""
        result = navigator.click_menu_button('Service')
        assert result is True, "Service button click should succeed"
        
        time.sleep(0.5)
        active = navigator.get_active_menu()
        assert active == 'Service', f"Service menu should be active, but got: {active}"
    
    def test_click_accounting_button(self, navigator):
        """Click the Accounting button and verify it becomes active"""
        result = navigator.click_menu_button('Accounting')
        assert result is True, "Accounting button click should succeed"
        
        time.sleep(0.5)
        active = navigator.get_active_menu()
        assert active == 'Accounting', f"Accounting menu should be active, but got: {active}"
    
    def test_click_admin_button(self, navigator):
        """Click the Admin button and verify it becomes active"""
        result = navigator.click_menu_button('Admin')
        assert result is True, "Admin button click should succeed"
        
        time.sleep(0.5)
        active = navigator.get_active_menu()
        assert active == 'Admin', f"Admin menu should be active, but got: {active}"
    
    def test_all_navigator_buttons_clickable(self, navigator):
        """Verify all navigator buttons are accessible and clickable"""
        expected_buttons = ['Sales', 'Service', 'Accounting', 'Admin', 'Parts']
        
        for button_name in expected_buttons:
            result = navigator.click_menu_button(button_name)
            assert result is True, f"{button_name} button should be clickable"
            
            time.sleep(0.3)
            active = navigator.get_active_menu()
            assert active == button_name, f"{button_name} should be active after click"
    
    def test_get_active_menu(self, navigator):
        """Verify get_active_menu returns the currently active menu"""
        navigator.click_menu_button('Service')
        time.sleep(0.5)
        
        active = navigator.get_active_menu()
        assert active in ['Sales', 'Service', 'Accounting', 'Admin', 'Parts'], \
            f"Active menu should be one of the valid menus, got: {active}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
