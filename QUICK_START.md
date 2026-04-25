# Quick Start Guide - G2 Desktop Automation Framework

## 5-Minute Setup

### Step 1: Install Dependencies
```powershell
cd "e:\G2 Desktop Automation"
pip install -r requirements.txt
```

### Step 2: Create Your First Screen
```python
# screens/my_screen.py
from screens.base_screen import BaseScreen
from core.element import Element, UIAProperty
from core.locator import Locator

class MyScreen(BaseScreen):
    def __init__(self):
        super().__init__("MyScreen")
        self._setup_elements()
    
    def _setup_elements(self):
        # Create mock root element
        root = Element(
            name="MainWindow",
            properties=UIAProperty(control_type="Window", title="My App")
        )
        self.set_root_element(root)
    
    def do_something(self):
        element = Locator.by_auto_id("btnClick").find(self._root_element)
        if element:
            self.click_element(element)
```

### Step 3: Write Your First Test
```python
# tests/test_my_screen.py
def test_my_first_test(my_screen):
    my_screen.do_something()
    assert True
```

### Step 4: Run Tests
```powershell
pytest tests/ -v
```

## Common Tasks

### Find an Element
```python
from core.locator import Locator

# By auto_id
element = Locator.by_auto_id("btnLogin").find(root)

# By control type
buttons = Locator.by_control_type("Button").find_all(root)

# By title
element = Locator.by_title("Save").find(root)
```

### Click an Element
```python
self.click_element(element)
```

### Type Text
```python
self.type_in_element(element, "Hello World")
```

### Verify Text
```python
assert self.verify_text_present("Success Message")
assert not self.verify_text_not_present("Error Message")
```

### Take Screenshot
```python
path = self.capture_screenshot("my_screenshot.png")
```

### Wait for Element
```python
found = self.wait_for_text("Expected Text", timeout_seconds=10)
```

## UIA Element Structure

Your application's UI looks like this in UIA:

```
Window (Main Application)
├── Group/Pane (Container)
│   ├── Text (Label)
│   ├── Edit (Input Field)
│   └── Button (Action Button)
├── Group/Pane (Another Container)
│   ├── Text (Label)
│   ├── Pane (Custom Control)
│   └── Button
└── Button (Close)
```

## Creating Element Locators

Based on UIA properties from your app:

```python
# Property format:
# control_type="Button",class_name="...",auto_id="btnLogin",title="Login"

# Create element:
login_button = Element(
    name="Login Button",
    properties=UIAProperty(
        control_type="Button",
        auto_id="btnLogin",
        title="Login"
    )
)

# Or load from dictionary:
data = {
    "name": "Login Button",
    "control_type": "Button",
    "auto_id": "btnLogin",
    "title": "Login"
}
element = Element.from_uia_dict(data)
```

## Screen Setup Pattern

```python
from screens.base_screen import BaseScreen
from core.element import Element, UIAProperty
from core.locator import Locator

class LoginScreen(BaseScreen):
    def __init__(self):
        super().__init__("LoginScreen")
        self._setup_elements()
    
    def _setup_elements(self):
        # Create root window element
        root = Element(
            name="LoginForm",
            properties=UIAProperty(
                control_type="Window",
                title="G2 Login",
                auto_id="LoginForm"
            )
        )
        
        # Add child elements
        username = Element("Username", UIAProperty(auto_id="txtUser"))
        password = Element("Password", UIAProperty(auto_id="txtPwd"))
        login_btn = Element("Login", UIAProperty(auto_id="btnLogin"))
        
        root.add_child(username)
        root.add_child(password)
        root.add_child(login_btn)
        
        # Set element positions (mock data)
        for elem in [username, password, login_btn]:
            elem.set_runtime_data("center_x", 400)
            elem.set_runtime_data("center_y", 300)
        
        self.set_root_element(root)
    
    def login(self, username, password):
        user_elem = Locator.by_auto_id("txtUser").find(self._root_element)
        pass_elem = Locator.by_auto_id("txtPwd").find(self._root_element)
        btn_elem = Locator.by_auto_id("btnLogin").find(self._root_element)
        
        self.type_in_element(user_elem, username)
        self.type_in_element(pass_elem, password)
        self.click_element(btn_elem)
```

## Test Template

```python
import pytest
from screens.login_screen import LoginScreen

class TestLoginFlow:
    
    def test_successful_login(self, login_screen):
        """Test successful login with valid credentials."""
        # Arrange
        login_screen.login("domain\\user", "password")
        
        # Act
        # (covered in login method)
        
        # Assert
        assert login_screen.verify_text_present("Dashboard")
    
    def test_invalid_login(self, login_screen):
        """Test login with invalid credentials."""
        login_screen.login("domain\\user", "wrong")
        assert login_screen.verify_text_present("Invalid credentials")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

## Key Methods Reference

| Task | Method | Example |
|------|--------|---------|
| Click | `click_element(element)` | `self.click_element(btn)` |
| Type | `type_in_element(elem, text)` | `self.type_in_element(field, "text")` |
| Find | `Locator.by_auto_id()` | `Locator.by_auto_id("id").find(root)` |
| Verify Text | `verify_text_present(text)` | `assert self.verify_text_present("OK")` |
| Screenshot | `capture_screenshot()` | `self.capture_screenshot("shot.png")` |
| Wait | `wait_for_text(text)` | `self.wait_for_text("Ready", 10)` |
| Keyboard | `keyboard.type_text()` | `self.keyboard.type_text("text")` |
| Mouse | `mouse.click()` | `self.mouse.click(100, 200)` |

## Troubleshooting

**Element not found?**
- Check auto_id spelling
- Verify element exists in hierarchy
- Try `find_all()` to see what's available

**Clicks not working?**
- Add delay: `time.sleep(0.5)`
- Verify coordinates with `mouse.get_position()`
- Ensure window is focused

**Text not typed?**
- Use `type_text_fast()` instead
- Add interval: `keyboard.type_text(text, interval=0.1)`
- Check if field is focused

**OCR not working?**
- Install Tesseract
- Set path in config if needed
- Test with: `TextTracker().find_text("text")`

## Next Steps

1. **Review** `USAGE_GUIDE.md` for detailed documentation
2. **Reference** `API_REFERENCE.md` for all available methods
3. **Create** screen objects for your application
4. **Write** tests using pytest
5. **Run** with `pytest tests/ -v`

## File Structure

```
e:\G2 Desktop Automation\
├── core/                 # Core automation components
│   ├── element.py       # UI element representation
│   ├── locator.py       # Element finding strategies
│   ├── text_tracker.py  # Text detection & verification
│   ├── screenshot_manager.py
│   ├── keyboard_handler.py
│   ├── mouse_handler.py
│   └── __init__.py
├── drivers/             # Integration drivers
│   ├── uia_driver.py   # UI Automation bridge
│   └── __init__.py
├── screens/             # Page objects
│   ├── base_screen.py  # Base screen class
│   ├── login_screen.py # Example screen
│   └── __init__.py
├── config/              # Configuration
│   ├── settings.py
│   └── __init__.py
├── tests/               # Test suites
│   ├── conftest.py     # Pytest fixtures
│   ├── test_login_screen.py
│   └── __init__.py
├── requirements.txt     # Dependencies
├── README.md           # Overview
├── USAGE_GUIDE.md      # Detailed guide
├── API_REFERENCE.md    # Full API
└── QUICK_START.md      # This file
```

## Support

- **Documentation**: See `USAGE_GUIDE.md`
- **API Details**: See `API_REFERENCE.md`
- **Examples**: See `screens/login_screen.py` and `tests/test_login_screen.py`

Happy Automating! 🚀
