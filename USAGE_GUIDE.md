# Desktop Automation Framework - Complete Guide

## Overview

This is a professional-grade Desktop Automation Framework designed specifically for testing applications with mixed UI technologies (WinForms and PICK UI). The framework provides a complete abstraction layer for UI automation with support for:

- **Text tracking and detection** using OCR
- **Screenshot capture and comparison**
- **Keyboard input** handling
- **Mouse interaction** (click, drag, scroll)
- **UIA element discovery** and navigation
- **Page Object Model** pattern support

## Quick Start

### Installation

1. **Clone/Download the project**

2. **Install Python dependencies:**
```powershell
pip install -r requirements.txt
```

3. **Configure Tesseract (for OCR):**
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Install with default settings
   - Tesseract will be auto-detected or configure the path in `config/settings.py`

### First Test Run

```python
from screens.login_screen import LoginScreen

# Create screen instance
login = LoginScreen()

# Interact with elements
login.enter_username("domain\\user")
login.enter_password("password")
login.click_login()

# Verify results
assert login.verify_text_present("Dashboard")
```

## Core Components

### 1. **Element Class** (`core/element.py`)

Represents a UI element with UIA properties.

```python
from core.element import Element, UIAProperty

# Create an element
element = Element(
    name="Login Button",
    properties=UIAProperty(
        control_type="Button",
        auto_id="btnLogin",
        title="Login"
    )
)
```

**Key Methods:**
- `add_child()` - Add child element
- `get_children_by_control_type()` - Find children by type
- `get_child_by_auto_id()` - Find child by ID
- `find_descendant()` - Recursive search
- `get_path()` - Get element hierarchy path

### 2. **Locator System** (`core/locator.py`)

Flexible element location strategies.

```python
from core.locator import Locator, LocatorBuilder

# By auto_id
locator = Locator.by_auto_id("btnLogin")

# By multiple conditions
builder = LocatorBuilder()
locator = (builder
    .with_control_type("Edit")
    .with_auto_id("txtUser")
    .build_locator()
)

# Find element
element = locator.find(root_element)

# Find all matching
elements = locator.find_all(root_element)
```

**Locator Strategies:**
- `AUTO_ID` - Find by auto_id
- `CLASS_NAME` - Find by class name
- `CONTROL_TYPE` - Find by UI control type
- `TITLE` - Find by element title
- `SELECTOR` - Find by UIA selector string

### 3. **Text Tracking** (`core/text_tracker.py`)

Locate and verify text on screen.

```python
from core.text_tracker import TextTracker, TextValidator

tracker = TextTracker()

# Find text
text_location = tracker.find_text("Login Failed")
if text_location:
    print(f"Text found at: {text_location.get_center()}")

# Wait for text
if tracker.wait_for_text("Dashboard", timeout_seconds=10):
    print("Dashboard appeared!")

# Validate text
assert TextValidator.validate_text_present("Error Message")
```

**Text Matching Modes:**
- `EXACT` - Exact match
- `PARTIAL` - Substring match
- `REGEX` - Regular expression
- `CASE_INSENSITIVE` - Ignore case

### 4. **Screenshot Management** (`core/screenshot_manager.py`)

Capture and compare screenshots.

```python
from core.screenshot_manager import ScreenshotManager

screenshots = ScreenshotManager("./screenshots")

# Capture full screen
path = screenshots.capture_screenshot("login_screen.png")

# Capture element
path = screenshots.capture_element_screenshot(element, "button.png")

# Capture region
region = (100, 100, 300, 200)  # x, y, width, height
path = screenshots.capture_region_screenshot(region)

# Compare screenshots
are_equal = screenshots.compare_screenshots("img1.png", "img2.png")

# Visual similarity
similar, score = screenshots.compare_screenshots_visual_similarity(
    "img1.png", "img2.png", threshold=0.95
)
```

### 5. **Keyboard Handler** (`core/keyboard_handler.py`)

Simulate keyboard input.

```python
from core.keyboard_handler import KeyboardHandler

keyboard = KeyboardHandler()

# Type text
keyboard.type_text("Hello World")
keyboard.type_text_fast("FastTyping")

# Press keys
keyboard.press_key("enter")
keyboard.press_key("escape")

# Key combinations
keyboard.key_combination("ctrl", "a")      # Ctrl+A
keyboard.key_combination("ctrl", "c")      # Ctrl+C
keyboard.key_combination("alt", "tab")     # Alt+Tab

# Key sequences
keyboard.key_sequence(["up", "up", "down", "enter"])

# Common operations
keyboard.clear_field()      # Ctrl+A then Delete
keyboard.send_tab(count=3)  # Send Tab 3 times
keyboard.send_enter()
keyboard.send_escape()
keyboard.copy_to_clipboard()    # Ctrl+C
keyboard.paste_from_clipboard() # Ctrl+V
keyboard.select_all()           # Ctrl+A
```

### 6. **Mouse Handler** (`core/mouse_handler.py`)

Control mouse interactions.

```python
from core.mouse_handler import MouseHandler, MouseButton

mouse = MouseHandler()

# Basic movements and clicks
mouse.move_to(100, 200)
mouse.click(100, 200)
mouse.double_click(100, 200)
mouse.right_click(100, 200)

# Element-based interactions
mouse.click_element(element)
mouse.double_click_element(element)
mouse.right_click_element(element)

# Dragging
mouse.drag(100, 100, 300, 300, duration=1.0)
mouse.drag_element_to_element(source_element, target_element)
mouse.drag_element_by_offset(element, offset_x=50, offset_y=100)

# Scrolling
mouse.scroll(x=500, y=400, steps=5, direction="down")
mouse.scroll_element(element, steps=3, direction="up")

# Get position
x, y = mouse.get_position()
```

### 7. **UIA Driver** (`drivers/uia_driver.py`)

Manage UI element hierarchy and discovery.

```python
from drivers.uia_driver import UIADriver

driver = UIADriver()

# Set root element
driver.set_root_element(root_element)

# Find elements
element = driver.find_element_by_auto_id("txtUser")
buttons = driver.find_elements_by_control_type("Button")
textboxes = driver.find_elements_by_class_name("WindowsForms10.EDIT")

# Export/Import hierarchy
json_str = driver.export_hierarchy_to_json()
driver.load_hierarchy_from_json(json_str)

# Get element info
info = driver.get_element_info(element)
```

### 8. **Base Screen** (`screens/base_screen.py`)

Page object pattern implementation.

```python
from screens.base_screen import BaseScreen
from core.locator import Locator

class MyScreen(BaseScreen):
    def __init__(self):
        super().__init__("MyScreen")
    
    def enter_text(self, field_id, text):
        element = Locator.by_auto_id(field_id).find(self._root_element)
        self.type_in_element(element, text)
    
    def click_button(self, button_id):
        element = Locator.by_auto_id(button_id).find(self._root_element)
        self.click_element(element)
```

## Working with UIA Properties

### Understanding UIA Properties

```
control_type: Button               # Type of UI control
class_name: WindowsForms10.BUTTON  # CSS/WinForms class
title: Login                       # Visible text/title
auto_id: btnLogin                  # Unique identifier
rich_text: Login                   # Rich text content
selector: control_type="Button"... # Complete selector
```

### Creating Elements from UIA Data

```python
from core.element import Element, UIAProperty

# From properties
uia_props = UIAProperty(
    control_type="Button",
    class_name="WindowsForms10.Window.8.app.0.392a42d_r11_ad1",
    title="Login",
    auto_id="btnLogin"
)

element = Element(name="Login Button", properties=uia_props)

# From dictionary
data = {
    "name": "Cancel Button",
    "control_type": "Button",
    "auto_id": "btnCancel",
    "title": "Cancel"
}
element = Element.from_uia_dict(data)
```

## Page Object Pattern Example

```python
from screens.base_screen import BaseScreen
from core.locator import Locator

class LoginScreen(BaseScreen):
    """Login screen page object."""
    
    def __init__(self):
        super().__init__("LoginScreen")
    
    @property
    def username_field(self):
        return Locator.by_auto_id("txtUser").find(self._root_element)
    
    @property
    def password_field(self):
        return Locator.by_auto_id("txtPwd").find(self._root_element)
    
    @property
    def login_button(self):
        return Locator.by_auto_id("btnLogin").find(self._root_element)
    
    def login(self, username, password):
        self.type_in_element(self.username_field, username)
        self.type_in_element(self.password_field, password)
        self.click_element(self.login_button)
```

## Running Tests

### With Pytest

```powershell
# Run all tests
pytest

# Run specific file
pytest tests/test_login_screen.py

# Run specific test
pytest tests/test_login_screen.py::TestLoginScreen::test_login_flow

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Show print statements
pytest -s

# Parallel execution
pytest -n auto
```

### Test Markers

```python
@pytest.mark.smoke
def test_login(): ...

@pytest.mark.regression
def test_full_workflow(): ...

@pytest.mark.functional
def test_ui_elements(): ...

@pytest.mark.sanity
def test_basic_navigation(): ...

# Run only smoke tests
pytest -m smoke

# Run all except regression
pytest -m "not regression"
```

## Configuration

Edit `config/settings.py` to customize:

```python
# Screenshot settings
SCREENSHOT_ON_FAILURE = True
SCREENSHOT_FORMAT = "png"

# Timeouts
DEFAULT_TIMEOUT = 10.0
TEXT_WAIT_TIMEOUT = 10.0

# Keyboard/Mouse
KEYBOARD_TYPE_INTERVAL = 0.05
MOUSE_CLICK_DELAY = 0.2

# OCR
OCR_ENABLED = True
OCR_LANGUAGE = "eng"
```

## Best Practices

1. **Use Page Objects** - Encapsulate element locators in page object classes
2. **Explicit Waits** - Use `wait_for_text()` instead of `time.sleep()`
3. **Element Caching** - Cache element references to avoid repeated searches
4. **Clear Assertions** - Use descriptive assertions with meaningful messages
5. **Screenshot Evidence** - Capture screenshots on test failures
6. **Locator Strategy** - Prefer `auto_id` > `control_type` > `class_name`
7. **Element Hierarchy** - Understand parent-child relationships for reliable selection

## Troubleshooting

### OCR Not Working
- Install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
- Update path in config if needed
- Test with: `TextTracker().find_text("Some Text")`

### Element Not Found
- Verify element exists in hierarchy
- Check UIA properties (auto_id, control_type)
- Use alternative locator strategy
- Try broader search with control_type

### Keyboard Input Not Registering
- Ensure application window is in focus
- Add delays between keystrokes
- Try `type_text_fast()` instead of `type_text()`

### Mouse Clicks Missing
- Verify element coordinates
- Add delay after click
- Check if element is clickable (not overlapped)

## Advanced Topics

### Custom Element Finder
```python
def find_by_partial_id(root, partial_id):
    results = []
    def search(element):
        if element.properties.auto_id and partial_id in element.properties.auto_id:
            results.append(element)
        for child in element.children:
            search(child)
    search(root)
    return results
```

### Element Wait with Condition
```python
def wait_for_element_enabled(locator, timeout=10):
    import time
    start = time.time()
    while (time.time() - start) < timeout:
        element = locator.find(root)
        if element and element.get_runtime_data("enabled", True):
            return element
        time.sleep(0.5)
    return None
```

### Screenshot Comparison Pipeline
```python
baseline = screenshots.capture_screenshot("baseline.png")
current = screenshots.capture_screenshot("current.png")
similar, score = screenshots.compare_screenshots_visual_similarity(
    baseline, current, threshold=0.95
)
if not similar:
    print(f"UI changed: {score*100:.2f}% similar")
```

## Architecture

```
Core Components
├── Element Management (element.py, locator.py)
├── Text Recognition (text_tracker.py)
├── Visual Capture (screenshot_manager.py)
├── Input Simulation (keyboard_handler.py, mouse_handler.py)
├── Driver/Bridge (uia_driver.py)
└── Page Objects (base_screen.py)

Test Layer
└── Screen-specific implementations
    └── Test suites using fixtures
```

## Support & Issues

For issues or feature requests, refer to the project documentation or contact the development team.

## License

Internal Use Only - G2 Desktop Automation Framework
