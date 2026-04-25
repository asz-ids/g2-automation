# Framework Architecture

## Overview

This document describes the architecture of the G2 Desktop Automation Framework, designed for testing WinForms and PICK UI applications.

## Design Principles

1. **Abstraction** - Hide complexity of UI automation behind clean interfaces
2. **Flexibility** - Support multiple locator strategies and interaction methods
3. **Maintainability** - Clear separation of concerns and reusable components
4. **Scalability** - Easy to add new screens and test cases
5. **Reliability** - Robust element finding and interaction handling

## Component Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                    Test Layer (Pytest)                      │
│                 (tests/test_*.py, conftest.py)             │
└─────────────────────────────────────────────────────────────┘
                            ↑
┌─────────────────────────────────────────────────────────────┐
│              Screen/Page Object Layer                       │
│           (screens/base_screen.py, *_screen.py)            │
│                                                             │
│  ├─ Encapsulates screen-specific interactions             │
│  ├─ Provides high-level action methods                    │
│  └─ Manages element locators                              │
└─────────────────────────────────────────────────────────────┘
                            ↑
┌─────────────────────────────────────────────────────────────┐
│           Interaction Handler Layer (Core)                  │
│                                                             │
│  ├─ KeyboardHandler     - Keyboard input simulation       │
│  ├─ MouseHandler        - Mouse interactions              │
│  ├─ TextTracker         - Text detection & verification   │
│  ├─ ScreenshotManager   - Screenshot capture & compare    │
│  └─ UIADriver           - UIA element discovery           │
└─────────────────────────────────────────────────────────────┘
                            ↑
┌─────────────────────────────────────────────────────────────┐
│         Element Management Layer (Core)                     │
│                                                             │
│  ├─ Element         - UI element representation           │
│  ├─ UIAProperty     - Element UIA properties              │
│  ├─ Locator         - Element finding strategies          │
│  └─ LocatorBuilder  - Complex locator construction        │
└─────────────────────────────────────────────────────────────┘
                            ↑
┌─────────────────────────────────────────────────────────────┐
│           External Dependencies                            │
│                                                             │
│  ├─ pynput      - Keyboard & mouse control               │
│  ├─ PIL/Pillow  - Screenshot capture & comparison        │
│  ├─ pytesseract - OCR for text detection                 │
│  ├─ pytest      - Test framework                         │
│  └─ pywinauto   - Windows UI automation support          │
└─────────────────────────────────────────────────────────────┘
```

## Layer Descriptions

### Test Layer
- **Responsibility**: Define test cases and test flow
- **Technology**: Pytest
- **Files**: `tests/test_*.py`, `tests/conftest.py`
- **Example**:
```python
def test_login_flow(login_screen):
    login_screen.login("user", "pass")
    assert login_screen.verify_success()
```

### Screen/Page Object Layer
- **Responsibility**: Encapsulate screen interactions and element access
- **Pattern**: Page Object Model (POM)
- **Base Class**: `BaseScreen`
- **Features**:
  - High-level action methods (login, submit, etc.)
  - Element locator registration
  - Text verification helpers
  - Screenshot capture
- **Files**: `screens/base_screen.py`, `screens/*_screen.py`
- **Example**:
```python
class LoginScreen(BaseScreen):
    def login(self, username, password):
        element = Locator.by_auto_id("txtUser").find(self._root_element)
        self.type_in_element(element, username)
```

### Interaction Handler Layer
- **Responsibility**: Provide high-level interaction abstractions
- **Components**:
  - **KeyboardHandler** - Type text, press keys, key combinations
  - **MouseHandler** - Click, drag, scroll, double-click
  - **TextTracker** - Find and verify text with OCR
  - **ScreenshotManager** - Capture and compare screenshots
  - **UIADriver** - Discover and manage UI elements
- **Files**: `core/*_handler.py`, `core/text_tracker.py`, `core/screenshot_manager.py`, `drivers/uia_driver.py`
- **Example**:
```python
keyboard.type_text("Hello")
mouse.click(100, 200)
tracker.find_text("Success")
```

### Element Management Layer
- **Responsibility**: Represent and locate UI elements
- **Components**:
  - **Element** - Represents a UI element with hierarchy
  - **UIAProperty** - Encapsulates UIA properties
  - **Locator** - Implements element finding strategies
  - **LocatorBuilder** - Builds complex locators
- **Files**: `core/element.py`, `core/locator.py`
- **Key Features**:
  - Hierarchical element tree
  - Multiple locator strategies
  - Element caching
  - Property validation
- **Example**:
```python
element = Locator.by_auto_id("btnLogin").find(root)
```

## Data Flow

### Typical Test Execution Flow

```
Test Start
    ↓
Screen Initialization
    ↓ (BaseScreen.__init__)
Set Root Element (UIADriver)
    ↓
Test Action (e.g., login)
    ↓
Find Element (Locator → Element)
    ↓
Interact with Element
    ├─ Mouse/Keyboard → pynput
    ├─ Text Verification → TextTracker → pytesseract
    ├─ Screenshot → ScreenshotManager → PIL
    └─ Element Discovery → UIADriver
    ↓
Assertion/Verification
    ↓
Test End (Cleanup)
```

## Element Hierarchy Model

```
Application Window (Element)
├── Root Element (UIAProperty: control_type="Window")
│   ├── Child 1 (control_type="Group")
│   │   ├── Grandchild 1 (control_type="Text")
│   │   ├── Grandchild 2 (control_type="Edit")
│   │   └── Grandchild 3 (control_type="Button")
│   ├── Child 2 (control_type="Pane")
│   │   └── Grandchild 4 (control_type="Custom")
│   └── Child 3 (control_type="Button")
```

**Navigation Methods:**
- `element.parent` - Access parent
- `element.children` - Access children list
- `element.get_root()` - Get root element
- `element.get_path()` - Get full path
- `element.find_descendant()` - Recursive search

## Locator Strategy Pattern

### Strategy Selection Priority
1. **auto_id** (Most Specific) - Unique identifier
2. **control_type + auto_id** - Control type + ID
3. **title** (Medium) - Element text/title
4. **class_name** (Less Specific) - CSS/WinForms class
5. **selector** (Most Flexible) - Complex selector string

### Locator Usage Examples
```python
# Simple locators
Locator.by_auto_id("btnLogin")
Locator.by_title("Save")
Locator.by_control_type("Button")

# Complex locator
builder = LocatorBuilder()
builder.with_control_type("Edit").with_auto_id("txtUser")
locator = builder.build_locator()
```

## Configuration Management

### Settings Structure
```python
# config/settings.py
PROJECT_ROOT              # Base directory
SCREENSHOTS_DIR          # Output directory
DEFAULT_TIMEOUT          # Timeout values
KEYBOARD_TYPE_INTERVAL   # Interaction delays
OCR_ENABLED             # Feature toggles
LOG_LEVEL               # Logging config
```

### Usage
```python
from config import settings

path = settings.SCREENSHOTS_DIR
timeout = settings.DEFAULT_TIMEOUT
```

## Error Handling Strategy

### Philosophy
- **Graceful Degradation** - Return None instead of raising exceptions
- **Logging** - Print informative messages
- **Fallbacks** - Try alternative approaches

### Pattern
```python
try:
    # Attempt operation
except ImportError:
    # Library not available - provide fallback
    print("Warning: Feature not available")
except Exception as e:
    # Log error but continue
    print(f"Error: {e}")
    return None
```

## Caching Strategy

### Element Caching
```
UIADriver maintains element cache:
├─ auto_id → Element
├─ auto_id → Element
└─ ...

Benefits:
- Fast element lookup
- Reduced tree traversals
- Memory efficient
```

### Text Caching
```
TextTracker maintains text location cache:
├─ "Login" → [TextLocation, TextLocation, ...]
├─ "Submit" → [TextLocation, ...]
└─ ...
```

## Extension Points

### Adding New Screen
```python
# 1. Create new screen class
class MyScreen(BaseScreen):
    def __init__(self):
        super().__init__("MyScreen")
        self._setup_elements()
    
    def _setup_elements(self):
        # Define element hierarchy
        pass
    
    # 2. Add action methods
    def perform_action(self):
        pass
```

### Adding Custom Locator Strategy
```python
# Extend Locator class
@staticmethod
def by_partial_id(partial_id):
    # Custom finding logic
    pass
```

### Adding Custom Interaction
```python
# Add method to BaseScreen or handler
def custom_interaction(self):
    self.keyboard.type_text("...")
    self.mouse.click(...)
```

## Performance Considerations

### Optimization Strategies
1. **Cache Elements** - Reuse element references
2. **Batch Operations** - Group interactions
3. **Parallel Testing** - Run independent tests in parallel
4. **Screenshot Comparison** - Use efficient algorithms

### Timing Considerations
```python
# Keyboard typing
type_interval = 0.05       # Default between chars
type_fast = 0.0            # No delay

# Mouse movement
move_duration = 0.5        # Smooth movement

# Click delays
click_delay = 0.2          # After click

# Waits and timeouts
default_timeout = 10.0     # General timeout
text_timeout = 10.0        # Text detection
```

## Maintenance Guidelines

### Code Organization
- **One screen per file** - Easy to find and modify
- **Clear method names** - Self-documenting
- **Docstrings** - Explain complex logic
- **Type hints** - Enable IDE support

### Testing Best Practices
- **Arrange-Act-Assert** - Clear test structure
- **Descriptive names** - Clear test intent
- **Single responsibility** - One assertion per test
- **Fixtures** - Reusable test setup

### Documentation
- **README.md** - Project overview
- **USAGE_GUIDE.md** - Detailed usage examples
- **API_REFERENCE.md** - Complete API documentation
- **QUICK_START.md** - Getting started guide
- **ARCHITECTURE.md** - This document

## Future Enhancements

### Potential Additions
- [ ] Mobile app automation support
- [ ] Web automation bridge (Selenium)
- [ ] Video recording capability
- [ ] Machine learning for element detection
- [ ] Visual regression testing
- [ ] Performance metrics collection
- [ ] CI/CD integration
- [ ] Test report generation

## Summary

The framework provides a clean, layered architecture that:
- **Separates concerns** - Each layer has specific responsibility
- **Enables reuse** - Common patterns abstracted to base classes
- **Supports testing** - Fixtures and patterns for pytest
- **Provides flexibility** - Multiple strategies for element location
- **Ensures maintainability** - Clear organization and documentation
