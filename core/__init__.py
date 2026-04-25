"""
Initialization file for core automation components.
"""

from .element import Element, UIAProperty, ControlType
from .locator import Locator, LocatorStrategy, LocatorBuilder
from .text_tracker import TextTracker, TextLocation, TextMatchMode, TextValidator
from .screenshot_manager import ScreenshotManager
from .keyboard_handler import KeyboardHandler, KeyCode
from .mouse_handler import MouseHandler, MouseButton

__all__ = [
    # Element
    "Element",
    "UIAProperty",
    "ControlType",
    # Locator
    "Locator",
    "LocatorStrategy",
    "LocatorBuilder",
    # Text Tracking
    "TextTracker",
    "TextLocation",
    "TextMatchMode",
    "TextValidator",
    # Screenshots
    "ScreenshotManager",
    # Keyboard
    "KeyboardHandler",
    "KeyCode",
    # Mouse
    "MouseHandler",
    "MouseButton",
]
