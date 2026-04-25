# API Reference - Desktop Automation Framework

## Core Components API

### Element Class

```python
class Element:
    def __init__(name: str, properties: UIAProperty, parent: Optional[Element] = None, 
                 children: Optional[List[Element]] = None)
    
    # Class Methods
    @staticmethod
    def from_uia_dict(data: Dict) -> Element
    
    # Instance Methods
    def add_child(child: Element) -> None
    def get_children_by_control_type(control_type: str) -> List[Element]
    def get_child_by_auto_id(auto_id: str) -> Optional[Element]
    def get_child_by_title(title: str) -> Optional[Element]
    def find_descendant(auto_id: str) -> Optional[Element]
    def get_root() -> Element
    def get_path() -> List[str]
    def set_runtime_data(key: str, value: Any) -> None
    def get_runtime_data(key: str, default: Any = None) -> Any
    def get_selector_string() -> str
```

### UIAProperty Class

```python
@dataclass
class UIAProperty:
    control_type: Optional[str]
    class_name: Optional[str]
    title: Optional[str]
    auto_id: Optional[str]
    rich_text: Optional[str]
    child_count: Optional[int]
    selector: Optional[str]
    
    # Methods
    def to_dict() -> Dict
    def to_selector_string() -> str
```

### Locator Class

```python
class Locator:
    def __init__(strategy: LocatorStrategy, value: str)
    
    # Factory Methods
    @staticmethod
    def by_auto_id(auto_id: str) -> Locator
    @staticmethod
    def by_class_name(class_name: str) -> Locator
    @staticmethod
    def by_control_type(control_type: str) -> Locator
    @staticmethod
    def by_title(title: str) -> Locator
    @staticmethod
    def by_selector(selector: str) -> Locator
    
    # Finding Methods
    def find(root_element: Element) -> Optional[Element]
    def find_all(root_element: Element) -> List[Element]
```

### LocatorBuilder Class

```python
class LocatorBuilder:
    def __init__()
    
    def with_auto_id(auto_id: str) -> LocatorBuilder
    def with_class_name(class_name: str) -> LocatorBuilder
    def with_control_type(control_type: str) -> LocatorBuilder
    def with_title(title: str) -> LocatorBuilder
    
    def build_selector() -> str
    def build_locator() -> Locator
```

### TextTracker Class

```python
class TextTracker:
    def __init__()
    
    def find_text(text: str, region: Optional[Tuple[int,int,int,int]] = None,
                  match_mode: TextMatchMode = TextMatchMode.EXACT,
                  case_sensitive: bool = False) -> Optional[TextLocation]
    
    def find_all_text(text: str, region: Optional[Tuple[int,int,int,int]] = None,
                      match_mode: TextMatchMode = TextMatchMode.EXACT) -> List[TextLocation]
    
    def text_exists(text: str, region: Optional[Tuple[int,int,int,int]] = None,
                    timeout_seconds: float = 5.0) -> bool
    
    def wait_for_text(text: str, timeout_seconds: float = 10.0,
                      region: Optional[Tuple[int,int,int,int]] = None) -> Optional[TextLocation]
    
    def extract_text_from_region(region: Tuple[int,int,int,int]) -> str
    
    def compare_text(text1: str, text2: str,
                    mode: TextMatchMode = TextMatchMode.EXACT) -> bool
    
    def clear_cache() -> None
```

### TextLocation Class

```python
@dataclass
class TextLocation:
    text: str
    x: int
    y: int
    width: int
    height: int
    confidence: float = 1.0
    
    @property
    def center_x() -> int
    
    @property
    def center_y() -> int
    
    def get_center() -> Tuple[int, int]
```

### TextValidator Class

```python
class TextValidator:
    @staticmethod
    def validate_text_present(text: str, 
                             region: Optional[Tuple[int,int,int,int]] = None) -> bool
    
    @staticmethod
    def validate_text_not_present(text: str,
                                 region: Optional[Tuple[int,int,int,int]] = None) -> bool
    
    @staticmethod
    def validate_text_contains(full_text: str, substring: str,
                              case_sensitive: bool = False) -> bool
    
    @staticmethod
    def validate_text_matches_pattern(text: str, pattern: str) -> bool
```

### ScreenshotManager Class

```python
class ScreenshotManager:
    def __init__(screenshots_dir: str = "screenshots")
    
    def capture_screenshot(filename: Optional[str] = None) -> str
    
    def capture_element_screenshot(element: Element,
                                  filename: Optional[str] = None) -> str
    
    def capture_region_screenshot(region: Tuple[int,int,int,int],
                                 filename: Optional[str] = None) -> str
    
    def compare_screenshots(image1_path: str, image2_path: str) -> bool
    
    def compare_screenshots_visual_similarity(image1_path: str, image2_path: str,
                                             threshold: float = 0.95) -> Tuple[bool, float]
    
    def get_screenshot_list() -> list
    
    def delete_screenshot(filename: str) -> bool
    
    def clear_screenshots() -> None
    
    def get_screenshot_path(filename: str) -> str
```

### KeyboardHandler Class

```python
class KeyboardHandler:
    def __init__()
    
    def type_text(text: str, interval: float = 0.05) -> None
    
    def type_text_fast(text: str) -> None
    
    def press_key(key: str) -> None
    
    def press_and_hold(key: str, duration: float = 1.0) -> None
    
    def key_combination(*keys: str) -> None
    
    def key_sequence(keys: List[str], interval: float = 0.2) -> None
    
    def clear_field() -> None
    
    def clear_line() -> None
    
    def send_tab(count: int = 1) -> None
    
    def send_enter() -> None
    
    def send_escape() -> None
    
    def send_backspace(count: int = 1) -> None
    
    def send_delete(count: int = 1) -> None
    
    def copy_to_clipboard() -> None
    
    def paste_from_clipboard() -> None
    
    def cut_to_clipboard() -> None
    
    def select_all() -> None
```

### KeyCode Enum

```python
class KeyCode(Enum):
    BACKSPACE, TAB, CLEAR, ENTER, SHIFT, CTRL, ALT, PAUSE,
    CAPSLOCK, ESCAPE, SPACE, PAGE_UP, PAGE_DOWN, END, HOME,
    LEFT, UP, RIGHT, DOWN, INSERT, DELETE,
    F1-F12
```

### MouseHandler Class

```python
class MouseHandler:
    def __init__()
    
    def move_to(x: int, y: int, duration: float = 0.5) -> None
    
    def move_to_element(element: Element, offset_x: int = 0, offset_y: int = 0) -> None
    
    def click(x: Optional[int] = None, y: Optional[int] = None,
             button: MouseButton = MouseButton.LEFT) -> None
    
    def click_element(element: Element, button: MouseButton = MouseButton.LEFT) -> None
    
    def double_click(x: Optional[int] = None, y: Optional[int] = None) -> None
    
    def double_click_element(element: Element) -> None
    
    def right_click(x: Optional[int] = None, y: Optional[int] = None) -> None
    
    def right_click_element(element: Element) -> None
    
    def drag(start_x: int, start_y: int, end_x: int, end_y: int,
            duration: float = 1.0) -> None
    
    def drag_element_to_element(source_element: Element, target_element: Element,
                               duration: float = 1.0) -> None
    
    def drag_element_by_offset(element: Element, offset_x: int, offset_y: int,
                              duration: float = 1.0) -> None
    
    def get_position() -> Tuple[int, int]
    
    def scroll(x: int, y: int, steps: int, direction: str = "down") -> None
    
    def scroll_element(element: Element, steps: int, direction: str = "down") -> None
```

### MouseButton Enum

```python
class MouseButton(Enum):
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"
```

### UIADriver Class

```python
class UIADriver:
    def __init__()
    
    def set_root_element(element: Element) -> None
    
    def find_element_by_auto_id(auto_id: str) -> Optional[Element]
    
    def find_elements_by_control_type(control_type: str) -> List[Element]
    
    def find_elements_by_class_name(class_name: str) -> List[Element]
    
    def get_element_hierarchy() -> Optional[Element]
    
    def load_hierarchy_from_dict(data: Dict) -> Element
    
    def load_hierarchy_from_json(json_str: str) -> Element
    
    def export_hierarchy_to_dict() -> Optional[Dict]
    
    def export_hierarchy_to_json() -> Optional[str]
    
    def get_element_info(element: Element) -> Dict
    
    def clear_cache() -> None
    
    def refresh_hierarchy() -> None
```

### BaseScreen Class

```python
class BaseScreen:
    def __init__(screen_name: str)
    
    def set_root_element(element: Element) -> None
    
    def register_element(name: str, locator: Locator) -> Element
    
    def get_element(name: str) -> Optional[Element]
    
    def find_element(locator: Locator) -> Optional[Element]
    
    def find_elements(locator: Locator) -> list
    
    def capture_screenshot(filename: Optional[str] = None) -> str
    
    def verify_text_present(text: str) -> bool
    
    def verify_text_not_present(text: str) -> bool
    
    def wait_for_text(text: str, timeout_seconds: float = 10.0) -> bool
    
    def click_element(element: Element) -> None
    
    def double_click_element(element: Element) -> None
    
    def right_click_element(element: Element) -> None
    
    def drag_element(source_element: Element, target_element: Element) -> None
    
    def scroll_element(element: Element, steps: int = 3, direction: str = "down") -> None
    
    def type_in_element(element: Element, text: str, clear_first: bool = True) -> None
```

## Enums

### LocatorStrategy
```python
AUTO_ID, CLASS_NAME, CONTROL_TYPE, TITLE, SELECTOR, XPATH_LIKE, PARTIAL_MATCH, CUSTOM
```

### TextMatchMode
```python
EXACT, PARTIAL, REGEX, CASE_INSENSITIVE
```

### ControlType
```python
WINDOW, BUTTON, TEXT, EDIT, PANE, GROUP, CHECKBOX, RADIO, COMBOBOX, LIST, CUSTOM
```

## Configuration Constants

All constants in `config/settings.py`:

```python
PROJECT_ROOT                   # Project root directory
SCREENSHOTS_DIR               # Screenshot output directory
SCREENSHOT_FORMAT            # Image format (png, jpg)
SCREENSHOT_ON_FAILURE        # Auto capture on test failure
DEFAULT_TIMEOUT              # Default timeout in seconds
ELEMENT_FIND_TIMEOUT        # Element finding timeout
TEXT_WAIT_TIMEOUT           # Text detection timeout
KEYBOARD_TYPE_INTERVAL      # Delay between keystrokes
MOUSE_MOVE_DURATION         # Mouse movement duration
MOUSE_CLICK_DELAY           # Delay after click
OCR_ENABLED                 # Enable/disable OCR
OCR_LANGUAGE               # OCR language code
```

## Return Types & Exceptions

### Common Return Types
- `Optional[Element]` - Element or None
- `List[Element]` - List of Elements
- `TextLocation` - Text with coordinates
- `Tuple[bool, float]` - Similarity result (similar, score)
- `str` - File path or text

### Exception Handling

Most methods fail gracefully and return None rather than raising exceptions. For explicit error handling:

```python
try:
    element = locator.find(root)
    if not element:
        print("Element not found")
except Exception as e:
    print(f"Error finding element: {e}")
```

## Type Hints

All methods include type hints for IDE support:

```python
from typing import Optional, List, Tuple, Dict
```

## Pytest Fixtures

Available fixtures in `tests/conftest.py`:

```python
@pytest.fixture
def login_screen() -> LoginScreen

@pytest.fixture
def screenshot_manager() -> ScreenshotManager

@pytest.fixture
def keyboard_handler() -> KeyboardHandler

@pytest.fixture
def mouse_handler() -> MouseHandler

@pytest.fixture
def text_tracker() -> TextTracker

@pytest.fixture(scope="session")
def test_config() -> config.settings
```
