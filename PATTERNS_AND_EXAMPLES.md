# Common Patterns & Examples

## Page Object Pattern

### Basic Screen Class

```python
from screens.base_screen import BaseScreen
from core.element import Element, UIAProperty
from core.locator import Locator

class DashboardScreen(BaseScreen):
    """Dashboard screen page object."""
    
    def __init__(self):
        super().__init__("DashboardScreen")
        self._setup_elements()
    
    def _setup_elements(self):
        """Initialize screen element hierarchy."""
        root = Element(
            name="MainWindow",
            properties=UIAProperty(
                control_type="Window",
                title="G2 Dashboard"
            )
        )
        self.set_root_element(root)
    
    # Properties for lazy element access
    @property
    def logout_button(self):
        return Locator.by_auto_id("btnLogout").find(self._root_element)
    
    @property
    def user_name(self):
        return Locator.by_auto_id("lblUser").find(self._root_element)
    
    # Action methods
    def logout(self):
        """Click logout button."""
        self.click_element(self.logout_button)
    
    def get_user_name(self):
        """Get displayed user name."""
        # In real usage, would extract text from element
        return "John Doe"
```

### Advanced Screen with Multiple Sections

```python
class ComplexScreen(BaseScreen):
    """Complex screen with multiple sections."""
    
    def __init__(self):
        super().__init__("ComplexScreen")
        self._setup_elements()
    
    def _setup_elements(self):
        root = Element("Root", UIAProperty(control_type="Window"))
        
        # Setup header section
        header = Element("Header", UIAProperty(control_type="Pane", auto_id="pnlHeader"))
        
        # Setup navigation
        nav_menu = Element("Navigation", UIAProperty(control_type="Group", auto_id="navMenu"))
        nav_home = Element("Home", UIAProperty(control_type="Button", auto_id="btnHome"))
        nav_settings = Element("Settings", UIAProperty(control_type="Button", auto_id="btnSettings"))
        
        nav_menu.add_child(nav_home)
        nav_menu.add_child(nav_settings)
        header.add_child(nav_menu)
        
        # Setup content area
        content = Element("Content", UIAProperty(control_type="Pane", auto_id="pnlContent"))
        
        # Setup footer
        footer = Element("Footer", UIAProperty(control_type="Pane", auto_id="pnlFooter"))
        
        root.add_child(header)
        root.add_child(content)
        root.add_child(footer)
        
        self.set_root_element(root)
    
    def navigate_to_home(self):
        """Navigate to home section."""
        home_btn = Locator.by_auto_id("btnHome").find(self._root_element)
        self.click_element(home_btn)
    
    def navigate_to_settings(self):
        """Navigate to settings section."""
        settings_btn = Locator.by_auto_id("btnSettings").find(self._root_element)
        self.click_element(settings_btn)
```

## Test Patterns

### Basic Test Case

```python
import pytest
from screens.login_screen import LoginScreen

class TestLogin:
    """Test login functionality."""
    
    def test_successful_login(self, login_screen):
        """Test successful login with valid credentials."""
        # Arrange - Setup
        username = "domain\\testuser"
        password = "validpass123"
        
        # Act - Perform action
        login_screen.enter_username(username)
        login_screen.enter_password(password)
        login_screen.click_login()
        
        # Assert - Verify result
        assert login_screen.verify_text_present("Dashboard")
    
    def test_invalid_credentials(self, login_screen):
        """Test login with invalid credentials."""
        login_screen.enter_username("domain\\user")
        login_screen.enter_password("wrongpass")
        login_screen.click_login()
        
        assert login_screen.verify_text_present("Invalid credentials")
    
    def test_empty_username(self, login_screen):
        """Test login with empty username."""
        login_screen.enter_password("password")
        login_screen.click_login()
        
        assert login_screen.verify_text_present("Username required")
```

### Parameterized Tests

```python
import pytest

class TestLoginVariations:
    """Test login with various inputs."""
    
    @pytest.mark.parametrize("username,password,expected", [
        ("domain\\user1", "pass123", "Dashboard"),
        ("domain\\user2", "pass456", "Dashboard"),
        ("invalid", "invalid", "Invalid credentials"),
    ])
    def test_login_variations(self, login_screen, username, password, expected):
        """Test login with different credentials."""
        login_screen.enter_username(username)
        login_screen.enter_password(password)
        login_screen.click_login()
        
        assert login_screen.verify_text_present(expected)
```

### Fixtures with Setup/Teardown

```python
import pytest

@pytest.fixture
def logged_in_user(login_screen):
    """Fixture: User logged into application."""
    # Setup
    login_screen.enter_username("domain\\testuser")
    login_screen.enter_password("password")
    login_screen.click_login()
    
    yield login_screen  # Test runs here
    
    # Teardown
    login_screen.logout()

class TestLoggedInUser:
    """Tests requiring logged-in user."""
    
    def test_view_profile(self, logged_in_user):
        """Test viewing user profile."""
        logged_in_user.click_profile()
        assert logged_in_user.verify_text_present("User Profile")
```

## Element Interaction Patterns

### Finding Elements

```python
from core.locator import Locator, LocatorBuilder

# Single locators
element = Locator.by_auto_id("txtUsername").find(root)
element = Locator.by_title("Save").find(root)
element = Locator.by_control_type("Button").find(root)

# Multiple results
buttons = Locator.by_control_type("Button").find_all(root)
edits = Locator.by_class_name("WindowsForms10.EDIT").find_all(root)

# Complex locator
builder = LocatorBuilder()
builder.with_control_type("Edit")
builder.with_class_name("WindowsForms10.EDIT.app.0")
complex_element = builder.build_locator().find(root)
```

### Interacting with Elements

```python
# Clicking
mouse.click_element(element)
mouse.double_click_element(element)
mouse.right_click_element(element)

# Typing
keyboard.type_text("Hello World")
keyboard.type_text_fast("FastInput")

# Combining actions
screen.type_in_element(username_field, "user")
screen.type_in_element(password_field, "pass")
screen.click_element(login_button)

# Advanced keyboard
keyboard.clear_field()  # Select all and delete
keyboard.key_combination("ctrl", "a")
keyboard.key_combination("ctrl", "c")

# Mouse operations
mouse.drag(100, 100, 200, 200)
mouse.drag_element_to_element(source, target)
mouse.scroll_element(element, steps=5, direction="down")
```

## Text Verification Patterns

### Basic Text Verification

```python
# Verify text present
assert screen.verify_text_present("Success")
assert screen.verify_text_not_present("Error")

# Wait for text
if screen.wait_for_text("Loading complete", timeout_seconds=5):
    print("Content loaded")

# Find text location
from core.text_tracker import TextTracker
tracker = TextTracker()
location = tracker.find_text("Expected Text")
if location:
    print(f"Text at: {location.get_center()}")
```

### Text Matching Modes

```python
from core.text_tracker import TextTracker, TextMatchMode

tracker = TextTracker()

# Exact match
tracker.find_text("Login", match_mode=TextMatchMode.EXACT)

# Partial match (substring)
tracker.find_text("Success", match_mode=TextMatchMode.PARTIAL)

# Case insensitive
tracker.find_text("SUBMIT", match_mode=TextMatchMode.CASE_INSENSITIVE)

# Regex pattern
tracker.find_text(r"Error \d+", match_mode=TextMatchMode.REGEX)
```

## Screenshot Patterns

### Basic Screenshots

```python
from core.screenshot_manager import ScreenshotManager

screenshots = ScreenshotManager()

# Capture full screen
path = screenshots.capture_screenshot("full_screen.png")

# Capture element
path = screenshots.capture_element_screenshot(element, "element.png")

# Capture region (x, y, width, height)
path = screenshots.capture_region_screenshot((100, 100, 300, 200), "region.png")
```

### Screenshot Comparison

```python
# Exact comparison
are_equal = screenshots.compare_screenshots("baseline.png", "current.png")

# Visual similarity
similar, score = screenshots.compare_screenshots_visual_similarity(
    "baseline.png", "current.png",
    threshold=0.95
)

if not similar:
    print(f"Images differ: {score*100:.2f}% similar")
```

### Screenshot on Failure Pattern

```python
class TestWithScreenshots:
    """Tests that capture screenshots on failure."""
    
    def test_complex_flow(self, login_screen):
        """Test with screenshots on failure."""
        try:
            login_screen.login("user", "pass")
            login_screen.navigate_to_page()
            assert login_screen.verify_element_visible("ImportantElement")
        except AssertionError:
            login_screen.capture_screenshot("failure_screenshot.png")
            raise
```

## Wait and Synchronization Patterns

### Explicit Waits

```python
# Wait for text to appear
if tracker.wait_for_text("Data loaded", timeout_seconds=10):
    print("Data is ready")
else:
    print("Data loading timed out")

# Custom wait with condition
import time

def wait_for_condition(condition_func, timeout=10):
    """Wait for condition to be true."""
    start = time.time()
    while (time.time() - start) < timeout:
        if condition_func():
            return True
        time.sleep(0.5)
    return False

# Usage
if wait_for_condition(lambda: screen.verify_text_present("Ready")):
    print("Component is ready")
```

### Polling Pattern

```python
import time

def wait_for_element(locator, root, timeout=10, poll_interval=0.5):
    """Wait for element to appear."""
    start_time = time.time()
    
    while (time.time() - start_time) < timeout:
        element = locator.find(root)
        if element:
            return element
        time.sleep(poll_interval)
    
    return None

# Usage
element = wait_for_element(
    Locator.by_auto_id("btnSubmit"),
    root_element,
    timeout=10
)
```

## Error Handling Patterns

### Graceful Failure Handling

```python
def safe_click(element):
    """Click element with error handling."""
    try:
        if element:
            click_element(element)
            return True
    except Exception as e:
        print(f"Click failed: {e}")
    return False

# Usage
if not safe_click(element):
    print("Could not click element, trying alternative approach")
```

### Retry Pattern

```python
def retry_action(func, max_attempts=3, delay=1):
    """Retry action multiple times."""
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            if attempt < max_attempts - 1:
                print(f"Attempt {attempt+1} failed: {e}")
                time.sleep(delay)
            else:
                raise

# Usage
retry_action(lambda: screen.click_element(button), max_attempts=3)
```

## Data-Driven Testing Pattern

```python
import pytest

# Test data
LOGIN_USERS = [
    {"username": "user1", "password": "pass1", "role": "Admin"},
    {"username": "user2", "password": "pass2", "role": "User"},
    {"username": "user3", "password": "pass3", "role": "Guest"},
]

class TestDataDriven:
    """Data-driven tests."""
    
    @pytest.mark.parametrize("user", LOGIN_USERS)
    def test_login_as_user(self, login_screen, user):
        """Test login for different user roles."""
        login_screen.login(user["username"], user["password"])
        assert login_screen.verify_user_role(user["role"])
```

## Performance Testing Pattern

```python
import time

class TestPerformance:
    """Performance-related tests."""
    
    def test_login_performance(self, login_screen):
        """Test that login completes within acceptable time."""
        start = time.time()
        
        login_screen.login("user", "pass")
        
        duration = time.time() - start
        assert duration < 5.0, f"Login took {duration:.2f}s (expected < 5s)"
```

## Best Practices Summary

### DO ✓
- Use page objects for screen interactions
- Employ explicit waits instead of sleep
- Capture screenshots on failures
- Use descriptive test names
- Follow Arrange-Act-Assert pattern
- Cache element references
- Use type hints
- Document complex logic

### DON'T ✗
- Use implicit waits with sleep()
- Hardcode coordinates
- Test multiple things in one test
- Ignore exceptions silently
- Mix UI and business logic
- Create fragile selectors
- Write tests without clear intent
- Skip documentation

## Common Gotchas

### Issue: Element Not Found
```python
# ❌ Wrong - Element might not exist yet
element = Locator.by_auto_id("btnSubmit").find(root)
click_element(element)

# ✓ Correct - Wait for element
element = wait_for_element(Locator.by_auto_id("btnSubmit"), root)
if element:
    click_element(element)
```

### Issue: Text Input Not Working
```python
# ❌ Wrong - Field might not be in focus
keyboard.type_text("data")

# ✓ Correct - Click first to focus
click_element(input_field)
keyboard.type_text("data")
```

### Issue: Coordinates Change
```python
# ❌ Wrong - Hardcoded coordinates fail with resolution changes
mouse.click(100, 200)

# ✓ Correct - Use element-based positioning
mouse.click_element(element)
```

## Quick Reference

```python
# Element operations
element.add_child(child)
element.get_children_by_control_type("Button")
element.find_descendant("auto_id")

# Finding
Locator.by_auto_id("id").find(root)
Locator.by_control_type("Button").find_all(root)

# Keyboard
keyboard.type_text("text")
keyboard.key_combination("ctrl", "a")
keyboard.send_enter()

# Mouse
mouse.click_element(element)
mouse.drag(100, 100, 200, 200)
mouse.scroll_element(element, steps=5)

# Text
TextValidator.validate_text_present("Text")
tracker.wait_for_text("Loading", timeout=10)
tracker.find_text("Search Term")

# Screenshot
screenshots.capture_screenshot("name.png")
screenshots.compare_screenshots("img1.png", "img2.png")
```
