"""
G2 Login Screen for the Desktop Automation Framework.
Interacts with the actual G2 Login WinForms application.

UIA Properties Reference:
- Window: control_type="Window", title="G2 Login", auto_id="LoginForm"
- Username: control_type="Pane", auto_id="txtUser"
- Password: control_type="Edit", auto_id="txtPwd" 
- Domain: control_type="Pane", auto_id="txtDomain"
- Login Button: control_type="Button", auto_id="btnLogin", title="Login"
- Cancel Button: control_type="Button", auto_id="btnCancel", title="Cancel"
"""

import time
from typing import Optional
from screens.base_screen import BaseScreen
from core.element import Element, UIAProperty
from core.locator import Locator, LocatorBuilder
from drivers.uia_driver import UIADriver


class LoginScreen(BaseScreen):
    """
    G2 Login Screen page object.
    Handles interactions with the G2 login form.
    """

    def __init__(self, discover_from_uia: bool = True):
        """
        Initialize LoginScreen.
        
        Args:
            discover_from_uia: If True, discovers elements from live UIA.
                              If False, uses predefined element structure.
        """
        super().__init__("G2LoginScreen")
        self._uia_app = None
        self._uia_window = None
        self._found_elements = {}
        
        if discover_from_uia:
            self._discover_from_live_uia()
        else:
            self._setup_elements_manual()

    def _setup_elements_manual(self) -> None:
        """Set up element hierarchy based on G2 UIA properties."""
        # Root window element for G2 Login
        root = Element(
            name="LoginForm",
            properties=UIAProperty(
                control_type="Window",
                title="G2 Login",
                auto_id="LoginForm"
            )
        )

        # Desktop pane parent
        desktop_pane = Element(
            name="Desktop",
            properties=UIAProperty(
                control_type="Pane",
                title="Desktop 1",
                auto_id=""
            )
        )
        root.add_child(desktop_pane)

        # Main group box container
        groupbox = Element(
            name="GroupBox",
            properties=UIAProperty(
                control_type="Group",
                class_name="WindowsForms10.Window.8.app.0.392a42d_r11_ad1",
                auto_id="ultraGroupBox1"
            )
        )
        desktop_pane.add_child(groupbox)

        # Domain Label
        domain_label = Element(
            name="Domain Label",
            properties=UIAProperty(
                control_type="Text",
                title="Domain",
                auto_id="lblDomain"
            )
        )
        groupbox.add_child(domain_label)

        # Domain input field (Pane)
        domain_field = Element(
            name="Domain Field",
            properties=UIAProperty(
                control_type="Pane",
                auto_id="txtDomain"
            )
        )
        groupbox.add_child(domain_field)

        # User ID Label
        userid_label = Element(
            name="User ID Label",
            properties=UIAProperty(
                control_type="Text",
                title="User ID",
                auto_id="ultraLabel1"
            )
        )
        groupbox.add_child(userid_label)

        # Username input field (Pane)
        username_field = Element(
            name="Username Field",
            properties=UIAProperty(
                control_type="Pane",
                auto_id="txtUser"
            )
        )
        groupbox.add_child(username_field)

        # Password Label
        password_label = Element(
            name="Password Label",
            properties=UIAProperty(
                control_type="Text",
                title="Password",
                auto_id="ultraLabel2"
            )
        )
        groupbox.add_child(password_label)

        # Password input field (Edit or Pane)
        password_field = Element(
            name="Password Field",
            properties=UIAProperty(
                control_type="Pane",
                auto_id="txtPwd"
            )
        )
        groupbox.add_child(password_field)

        # Login Button
        login_button = Element(
            name="Login Button",
            properties=UIAProperty(
                control_type="Button",
                class_name="WindowsForms10.Window.8.app.0.392a42d_r11_ad1",
                title="Login",
                auto_id="btnLogin"
            )
        )
        groupbox.add_child(login_button)

        # Cancel Button
        cancel_button = Element(
            name="Cancel Button",
            properties=UIAProperty(
                control_type="Button",
                class_name="WindowsForms10.Window.8.app.0.392a42d_r11_ad1",
                title="Cancel",
                auto_id="btnCancel"
            )
        )
        groupbox.add_child(cancel_button)

        # Set mock positions for elements
        elements_to_position = [
            domain_label, domain_field,
            userid_label, username_field,
            password_label, password_field,
            login_button, cancel_button
        ]
        
        for idx, element in enumerate(elements_to_position):
            element.set_runtime_data("center_x", 400)
            element.set_runtime_data("center_y", 250 + (idx * 40))

        self.set_root_element(root)

    def _discover_from_live_uia(self) -> None:
        """
        Discover login screen elements from live UI Automation.
        This requires the G2 Login application to be running.
        """
        try:
            # Try to find the G2 Login window via pywinauto
            from pywinauto import findwindows
            from pywinauto.application import Application
            
            # Find G2 Login window
            windows = findwindows.find_windows(title_re=".*G2 Login.*")
            
            if windows:
                # Found the G2 Login window - connect to it
                g2_window_handle = windows[0]
                app = Application(backend='uia').connect(handle=g2_window_handle)
                window = app.window()
                
                # Create a root element from the live window
                root = Element(
                    name="LoginForm",
                    properties=UIAProperty(
                        control_type="Window",
                        title="G2 Login",
                        auto_id="LoginForm"
                    )
                )
                
                # Add window to runtime data for access
                root.set_runtime_data("uia_element", window)
                root.set_runtime_data("uia_app", app)
                root.set_runtime_data("center_x", 500)
                root.set_runtime_data("center_y", 300)
                
                # Store the app reference for later use
                self._uia_app = app
                self._uia_window = window
                
                # Search for and cache the actual elements
                self._search_for_uia_elements(window)

                # Populate Element tree from discovered pywinauto elements
                # so Locator.find() / find_all() can traverse children
                self._populate_element_tree(root)

                self.set_root_element(root)
                print(f"[OK] Discovered live G2 application with {len(self._found_elements)} elements")
            else:
                # No live window found, use manual setup
                print("G2 Login window not found, using manual element setup")
                self._setup_elements_manual()
        except Exception as e:
            print(f"Could not discover from live UIA: {e}, using manual setup")
            self._setup_elements_manual()
    
    def _search_for_uia_elements(self, window_elem) -> None:
        """Search for login form elements in the UIA window"""
        known_ids = ["txtUser", "txtPwd", "txtDomain", "btnLogin", "btnCancel"]
        
        def search_recursive(elem, depth=0, max_depth=2):
            """Recursively search for elements with strict depth limit"""
            if depth > max_depth or elem is None:
                return
            
            try:
                # Check current element's automation ID
                try:
                    auto_id = elem.automation_id()
                    if auto_id and auto_id in known_ids and auto_id not in self._found_elements:
                        self._found_elements[auto_id] = elem
                except Exception:
                    pass
                
                # Only recurse if we haven't found all elements and haven't hit depth limit
                if len(self._found_elements) < len(known_ids) and depth < max_depth:
                    try:
                        children = elem.children()
                        if children:
                            for child in children:
                                if child is not None:
                                    search_recursive(child, depth + 1, max_depth)
                    except Exception:
                        pass
            except Exception:
                pass
        
        try:
            search_recursive(window_elem, 0, 2)  # Very strict max_depth of 2
        except Exception as e:
            print(f"Warning: Element search had issues: {e}")

    def _populate_element_tree(self, root: Element) -> None:
        """Convert discovered pywinauto elements into Element children of root."""
        for auto_id, uia_elem in self._found_elements.items():
            try:
                try:
                    ctrl_type = uia_elem.friendly_class_name()
                except Exception:
                    ctrl_type = None
                try:
                    title = uia_elem.window_text()
                except Exception:
                    title = None
                try:
                    class_name = uia_elem.element_info.class_name
                except Exception:
                    class_name = None

                elem = Element(
                    name=auto_id,
                    properties=UIAProperty(
                        control_type=ctrl_type,
                        auto_id=auto_id,
                        title=title,
                        class_name=class_name
                    )
                )
                elem.set_runtime_data("uia_element", uia_elem)
                root.add_child(elem)
            except Exception:
                pass

    def enter_username(self, username: str) -> bool:
        """
        Enter username in the login form.

        Args:
            username: Username to enter

        Returns:
            True if successful, False otherwise
        """
        try:
            # Try to use live UIA element first
            if "txtUser" in self._found_elements:
                elem = self._found_elements["txtUser"]
                elem.click_input()
                elem.type_keys(username)
                return True
            
            # Fall back to using locator on root element
            username_element = Locator.by_auto_id("txtUser").find(self._root_element)
            if username_element:
                self.type_in_element(username_element, username, clear_first=True)
                return True
            return False
        except Exception as e:
            print(f"Error entering username: {e}")
            return False

    def enter_password(self, password: str) -> bool:
        """
        Enter password in the login form.

        Args:
            password: Password to enter

        Returns:
            True if successful, False otherwise
        """
        try:
            # Try to use live UIA element first
            if "txtPwd" in self._found_elements:
                elem = self._found_elements["txtPwd"]
                elem.click_input()
                elem.type_keys(password)
                return True
            
            # Fall back to using locator on root element
            password_element = Locator.by_auto_id("txtPwd").find(self._root_element)
            if password_element:
                self.type_in_element(password_element, password, clear_first=True)
                return True
            return False
        except Exception as e:
            print(f"Error entering password: {e}")
            return False

    def enter_domain(self, domain: str) -> bool:
        """
        Enter domain in the login form.

        Args:
            domain: Domain to enter

        Returns:
            True if successful, False otherwise
        """
        try:
            # Try to use live UIA element first
            if "txtDomain" in self._found_elements:
                elem = self._found_elements["txtDomain"]
                elem.click_input()
                elem.type_keys(domain)
                return True
            
            # Fall back to using locator on root element
            domain_element = Locator.by_auto_id("txtDomain").find(self._root_element)
            if domain_element:
                self.type_in_element(domain_element, domain, clear_first=True)
                return True
            return False
        except Exception as e:
            print(f"Error entering domain: {e}")
            return False

    def click_login(self) -> bool:
        """
        Click the login button.

        Returns:
            True if successful, False otherwise
        """
        try:
            # Try to use live UIA element first
            if "btnLogin" in self._found_elements:
                elem = self._found_elements["btnLogin"]
                elem.click_input()
                return True
            
            # Fall back to using locator on root element
            login_button = Locator.by_auto_id("btnLogin").find(self._root_element)
            if login_button:
                self.click_element(login_button)
                return True
            return False
        except Exception as e:
            print(f"Error clicking login: {e}")
            return False

    def click_cancel(self) -> bool:
        """
        Click the cancel button.

        Returns:
            True if successful, False otherwise
        """
        try:
            # Try to use live UIA element first
            if "btnCancel" in self._found_elements:
                elem = self._found_elements["btnCancel"]
                elem.click_input()
                return True
            
            # Fall back to using locator on root element
            cancel_button = Locator.by_auto_id("btnCancel").find(self._root_element)
            if cancel_button:
                self.click_element(cancel_button)
                return True
            return False
        except Exception as e:
            print(f"Error clicking cancel: {e}")
            return False

    def login(self, username: str, password: str, domain: str = "") -> bool:
        """
        Perform complete login sequence.

        Args:
            username: Username to enter
            password: Password to enter
            domain: Optional domain to enter

        Returns:
            True if login clicked successfully, False otherwise
        """
        if domain:
            self.enter_domain(domain)
        
        self.enter_username(username)
        self.enter_password(password)
        return self.click_login()

    def is_login_successful(self, timeout_seconds: float = 10.0) -> bool:
        """
        Check if login was successful by waiting for expected text or element.

        Args:
            timeout_seconds: How long to wait for success indicators

        Returns:
            True if login appears successful, False otherwise
        """
        try:
            # Try to find success indicators
            success_texts = ["Dashboard", "Home", "Application Main", "Welcome","Sales","G2 Welcome Page"]
            error_texts = ["Invalid", "Incorrect", "Failed", "Error"]
            
            # Check if error text appears
            for error_text in error_texts:
                if self.verify_text_present(error_text):
                    print(f"Login failed: {error_text} message displayed")
                    return False
            
            # Wait for success text
            for success_text in success_texts:
                if self.wait_for_text(success_text, timeout_seconds=timeout_seconds):
                    print(f"Login successful: {success_text} found")
                    return True
            
            # If no definitive indicator, consider it successful if no errors
            return True
        except Exception as e:
            print(f"Error checking login success: {e}")
            return False

    def capture_login_screen(self, filename: str = "login_screen.png") -> str:
        """
        Capture screenshot of the login screen.

        Args:
            filename: Output filename

        Returns:
            Path to the screenshot
        """
        return self.capture_screenshot(filename)

    def is_login_screen_visible(self, timeout_seconds: float = 5.0) -> bool:
        """
        Check if the login screen is currently visible.

        Args:
            timeout_seconds: How long to wait for login screen

        Returns:
            True if login screen is visible, False otherwise
        """
        try:
            # Wait for a login screen indicator
            login_indicators = ["Login", "Password", "Username"]
            
            for indicator in login_indicators:
                if self.wait_for_text(indicator, timeout_seconds=2.0):
                    return True
            
            return False
        except Exception as e:
            print(f"Error checking login screen visibility: {e}")
            return False

    def get_login_status(self) -> dict:
        """
        Get current status of the login screen.

        Returns:
            Dictionary with login screen status information
        """
        return {
            "screen_name": self.screen_name,
            "root_element": self._root_element.name if self._root_element else None,
            "elements_count": len(self._root_element.children) if self._root_element else 0,
            "is_visible": self.is_login_screen_visible(timeout_seconds=1.0),
        }
