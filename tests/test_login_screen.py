"""
Example test for the login screen.
Demonstrates how to write tests using the automation framework.
"""

try:
    import pytest
except ImportError:
    pytest = None

from screens.login_screen import LoginScreen


class TestLoginScreen:
    """Test suite for login screen functionality."""

    def test_login_screen_loads(self, login_screen):
        """Test that login screen loads successfully."""
        assert login_screen is not None
        assert login_screen.screen_name == "G2LoginScreen"

    def test_enter_username(self, login_screen):
        """Test entering username."""
        username = "testuser"
        login_screen.enter_username(username)
        # In real test, would verify username was entered

    def test_enter_password(self, login_screen):
        """Test entering password."""
        password = "testpass123"
        login_screen.enter_password(password)
        # In real test, would verify password was entered

    def test_enter_domain(self, login_screen):
        """Test entering domain."""
        domain = "DOMAIN"
        login_screen.enter_domain(domain)
        # In real test, would verify domain was entered

    def test_capture_screenshot(self, login_screen):
        """Test capturing screenshot of login screen."""
        screenshot_path = login_screen.capture_login_screen()
        assert screenshot_path is not None
        assert "login_screen" in screenshot_path

    @pytest.mark.smoke
    def test_login_flow(self, login_screen):
        """Test the complete login flow."""
        # Enter credentials
        login_screen.enter_username("aqadir.ids")
        login_screen.enter_password("Aqadir2801")
        
        # Click login
        login_screen.click_login()
        
        # In real test, would wait for success and verify navigation

    @pytest.mark.functional
    def test_cancel_login(self, login_screen):
        """Test canceling login."""
        # Enter credentials
        login_screen.enter_username("testuser")
        
        # Click cancel
        login_screen.click_cancel()
        
        # In real test, would verify return to previous screen


class TestLoginScreenElements:
    """Test suite for login screen element interactions."""

    def test_find_username_field(self, login_screen):
        """Test finding username field."""
        from core.locator import Locator
        username_element = Locator.by_auto_id("txtUser").find(login_screen._root_element)
        assert username_element is not None
        assert username_element.properties.auto_id == "txtUser"

    def test_find_password_field(self, login_screen):
        """Test finding password field."""
        from core.locator import Locator
        password_element = Locator.by_auto_id("txtPwd").find(login_screen._root_element)
        assert password_element is not None
        assert password_element.properties.auto_id == "txtPwd"

    def test_find_login_button(self, login_screen):
        """Test finding login button."""
        from core.locator import Locator
        login_button = Locator.by_auto_id("btnLogin").find(login_screen._root_element)
        assert login_button is not None
        assert login_button.properties.title == "Login"

    def test_find_all_buttons(self, login_screen):
        """Test finding all buttons."""
        from core.locator import Locator
        buttons = Locator.by_control_type("Button").find_all(login_screen._root_element)
        assert len(buttons) >= 2  # At least Login and Cancel buttons


class TestLocatorBuilder:
    """Test suite for locator builder."""

    def test_build_selector_with_auto_id(self):
        """Test building selector with auto_id."""
        from core.locator import LocatorBuilder
        builder = LocatorBuilder()
        builder.with_auto_id("txtUser")
        selector = builder.build_selector()
        assert 'auto_id="txtUser"' in selector

    def test_build_selector_multiple_conditions(self):
        """Test building selector with multiple conditions."""
        from core.locator import LocatorBuilder
        builder = LocatorBuilder()
        builder.with_control_type("Edit").with_auto_id("txtUser")
        selector = builder.build_selector()
        assert 'control_type="Edit"' in selector
        assert 'auto_id="txtUser"' in selector

    def test_build_locator_from_builder(self):
        """Test building locator from builder."""
        from core.locator import LocatorBuilder
        builder = LocatorBuilder()
        builder.with_auto_id("btnLogin")
        locator = builder.build_locator()
        assert locator is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
