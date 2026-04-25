# G2 Desktop Automation Framework

A comprehensive Python-based test automation framework designed for Desktop applications with support for both **WinForms** and **PICK UI** components.

## Features

- **UIA (UI Automation) Support**: Interact with Windows UI elements using accessibility patterns
- **Text Tracking**: Locate and verify text elements on screen
- **Screenshot Capture**: Capture full screen or element-specific screenshots
- **Keyboard Interaction**: Send keystrokes and keyboard combinations
- **Mouse Control**: Move mouse, click, double-click, right-click, and drag operations
- **Flexible Element Selection**: Support for control types, class names, auto IDs, and selectors
- **Multi-Protocol Support**: Handle both WinForms and PICK UI elements
- **Element Hierarchy Navigation**: Access parents and children of UI elements

## Project Structure

```
├── core/
│   ├── __init__.py
│   ├── element.py              # Element class for UI element representation
│   ├── locator.py              # Locator patterns and matching
│   ├── text_tracker.py         # Text detection and tracking
│   ├── screenshot_manager.py   # Screenshot capture and comparison
│   ├── keyboard_handler.py     # Keyboard input handling
│   └── mouse_handler.py        # Mouse interaction handling
├── drivers/
│   ├── __init__.py
│   └── uia_driver.py           # UIA automation driver
├── screens/
│   ├── __init__.py
│   └── base_screen.py          # Base screen class for page objects
├── tests/
│   ├── __init__.py
│   ├── test_login_screen.py    # Example test for login screen
│   └── conftest.py             # Pytest configuration
├── config/
│   ├── __init__.py
│   └── settings.py             # Configuration settings
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Installation

### Prerequisites
- Python 3.8+
- Windows OS (for UIA support)

### Setup

1. Clone or download the project
2. Install dependencies:
```powershell
pip install -r requirements.txt
```

## Usage

### Basic Example: Login Screen Automation

```python
from screens.login_screen import LoginScreen

# Initialize screen object
login_screen = LoginScreen()

# Enter credentials
login_screen.enter_username("domain\\username")
login_screen.enter_password("password")
login_screen.click_login()

# Verify navigation
assert login_screen.is_login_successful()
```

### Core Methods Available

#### Text Tracking
```python
from core.text_tracker import TextTracker

tracker = TextTracker()
text_found = tracker.find_text("Expected Text", region=(0, 0, 1920, 1080))
```

#### Screenshot Management
```python
from core.screenshot_manager import ScreenshotManager

screenshot_mgr = ScreenshotManager()
screenshot_mgr.capture_screenshot("login_screen.png")
screenshot_mgr.capture_element_screenshot(element, "button.png")
```

#### Keyboard Interaction
```python
from core.keyboard_handler import KeyboardHandler

keyboard = KeyboardHandler()
keyboard.type_text("Hello World")
keyboard.press_key("Enter")
keyboard.key_combination("ctrl", "a")
```

#### Mouse Interaction
```python
from core.mouse_handler import MouseHandler

mouse = MouseHandler()
mouse.move_to(100, 200)
mouse.click()
mouse.double_click()
mouse.right_click()
mouse.drag(100, 200, 300, 400)
```

## UIA Property Format

The framework supports UIA properties in the following format:

```
control_type: Group
class_name: WindowsForms10.Window.8.app.0.392a42d_r11_ad1
auto_id: ultraGroupBox1
selector: control_type="Group",class_name="WindowsForms10.Window.8.app.0.392a42d_r11_ad1",auto_id="ultraGroupBox1"
```

These properties are used to uniquely identify and interact with UI elements.

## Running Tests

```powershell
# Run all tests
pytest

# Run specific test file
pytest tests/test_login_screen.py

# Run with verbose output
pytest -v

# Run with screenshots on failure
pytest --screenshots
```

## Configuration

Edit `config/settings.py` to configure:
- Screenshot directory
- Screenshot format
- Timeout values
- UIA driver settings

## Contributing

When adding new screens, inherit from `BaseScreen` and implement element locators using the provided methods.

## License

Internal Use Only
