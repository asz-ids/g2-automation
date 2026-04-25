"""
Test: G2 Menu Verification (Standalone)

This test can be run standalone to verify menus if Navigator is already open.
It's useful for manual testing after login.
"""

import pytest
from screens.navigator_screen import NavigatorScreen


class TestMenuVerificationStandalone:
    """Tests for menu verification when Navigator is already open"""
    
    EXPECTED_MENUS = [
        'Sales',
        'Service',
        'Accounting',
        'Admin',
        'Parts',
    ]
    
    def test_navigator_window_detection(self):
        """Test that we can detect the Navigator window if it's open"""
        navigator = NavigatorScreen()
        is_present = navigator.is_navigator_present()
        
        if not is_present:
            pytest.skip("Navigator window not currently open")
        
        assert is_present, "Should detect Navigator window"
    
    def test_menu_detection(self):
        """Test that menus can be detected"""
        navigator = NavigatorScreen()
        
        if not navigator.is_navigator_present():
            pytest.skip("Navigator window not open")
        
        menus = navigator.get_all_menu_items()
        assert len(menus) > 0, "Should detect at least one menu"
        assert menus is not None, "Menu list should not be None"
    
    def test_verification_report(self):
        """Test that we can generate a verification report"""
        navigator = NavigatorScreen()
        
        if not navigator.is_navigator_present():
            pytest.skip("Navigator window not open")
        
        report = navigator.get_verification_report()
        
        # Report should have expected keys
        assert 'navigator_found' in report
        assert 'menus_found' in report
        assert 'all_menus' in report
        assert 'missing_menus' in report
        
        # If Navigator is found, should have info
        if report['navigator_found']:
            assert report['menus_found'] > 0
            assert len(report['all_menus']) > 0


class TestMenuVerificationIfOpen:
    """Conditional tests that only run if Navigator is open"""
    
    EXPECTED_MENUS = ['Sales', 'Service', 'Accounting', 'Admin', 'Parts']
    
    @pytest.fixture(autouse=True)
    def require_navigator(self):
        """Skip all tests in this class if Navigator is not open"""
        navigator = NavigatorScreen()
        if not navigator.is_navigator_present():
            pytest.skip("Navigator window not open - skipping menu verification tests")
    
    def test_all_menus_present(self):
        """Verify all expected menus are present"""
        navigator = NavigatorScreen()
        menus = navigator.get_all_menu_items()
        
        missing = [m for m in self.EXPECTED_MENUS if m not in menus]
        assert not missing, f"Missing menus: {missing}"
    
    def test_sales_menu(self):
        """Verify Sales menu"""
        navigator = NavigatorScreen()
        menus = navigator.get_all_menu_items()
        assert 'Sales' in menus
    
    def test_service_menu(self):
        """Verify Service menu"""
        navigator = NavigatorScreen()
        menus = navigator.get_all_menu_items()
        assert 'Service' in menus
    
    def test_accounting_menu(self):
        """Verify Accounting menu"""
        navigator = NavigatorScreen()
        menus = navigator.get_all_menu_items()
        assert 'Accounting' in menus
    
    def test_admin_menu(self):
        """Verify Admin menu"""
        navigator = NavigatorScreen()
        menus = navigator.get_all_menu_items()
        assert 'Admin' in menus
    
    def test_parts_menu(self):
        """Verify Parts menu"""
        navigator = NavigatorScreen()
        menus = navigator.get_all_menu_items()
        assert 'Parts' in menus


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
