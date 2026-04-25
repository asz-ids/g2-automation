"""
Base Screen class for creating page objects in the automation framework.
Provides common functionality for screen interaction.
"""

from typing import Optional
from core.element import Element, UIAProperty
from core.locator import Locator, LocatorBuilder
from core.keyboard_handler import KeyboardHandler
from core.mouse_handler import MouseHandler
from core.screenshot_manager import ScreenshotManager
from core.text_tracker import TextTracker, TextValidator
from drivers.uia_driver import UIADriver


class BaseScreen:
    """
    Base class for screen objects (page objects in testing terms).
    Provides common functionality for interacting with screens.
    """

    def __init__(self, screen_name: str):
        """
        Initialize BaseScreen.

        Args:
            screen_name: Name of the screen
        """
        self.screen_name = screen_name
        self._root_element: Optional[Element] = None
        self._elements: dict = {}
        
        # Initialize handlers
        self.keyboard = KeyboardHandler()
        self.mouse = MouseHandler()
        self.screenshots = ScreenshotManager()
        self.text_tracker = TextTracker()
        self.uia_driver = UIADriver()

    def set_root_element(self, element: Element) -> None:
        """
        Set the root element for this screen.

        Args:
            element: Root element representing the screen
        """
        self._root_element = element
        self.uia_driver.set_root_element(element)

    def register_element(self, name: str, locator: Locator) -> Element:
        """
        Register an element with a locator.

        Args:
            name: Display name for the element
            locator: Locator to find the element

        Returns:
            The found Element
        """
        if not self._root_element:
            raise RuntimeError("Root element not set. Call set_root_element() first.")
        
        element = locator.find(self._root_element)
        if element:
            self._elements[name] = element
            return element
        else:
            raise ValueError(f"Could not find element: {name}")

    def get_element(self, name: str) -> Optional[Element]:
        """
        Get a registered element by name.

        Args:
            name: Name of the element

        Returns:
            Element or None if not found
        """
        return self._elements.get(name)

    def find_element(self, locator: Locator) -> Optional[Element]:
        """
        Find an element using a locator.

        Args:
            locator: Locator to use for finding

        Returns:
            Element or None if not found
        """
        if not self._root_element:
            return None
        return locator.find(self._root_element)

    def find_elements(self, locator: Locator) -> list:
        """
        Find all elements matching a locator.

        Args:
            locator: Locator to use for finding

        Returns:
            List of found elements
        """
        if not self._root_element:
            return []
        return locator.find_all(self._root_element)

    def capture_screenshot(self, filename: Optional[str] = None) -> str:
        """
        Capture a screenshot of the current screen.

        Args:
            filename: Optional custom filename

        Returns:
            Path to the saved screenshot
        """
        if not filename:
            filename = f"{self.screen_name}_{self.screenshots._get_timestamp()}.png"
        
        return self.screenshots.capture_screenshot(filename)

    def verify_text_present(self, text: str) -> bool:
        """
        Verify that text is present on the screen.

        Args:
            text: Text to verify

        Returns:
            True if text is present, False otherwise
        """
        return TextValidator.validate_text_present(text)

    def verify_text_not_present(self, text: str) -> bool:
        """
        Verify that text is NOT present on the screen.

        Args:
            text: Text to verify is absent

        Returns:
            True if text is not present, False otherwise
        """
        return TextValidator.validate_text_not_present(text)

    def wait_for_text(self, text: str, timeout_seconds: float = 10.0) -> bool:
        """
        Wait for text to appear on the screen.

        Args:
            text: Text to wait for
            timeout_seconds: Maximum time to wait

        Returns:
            True if text appeared, False if timeout
        """
        return self.text_tracker.wait_for_text(text, timeout_seconds) is not None

    def click_element(self, element: Element) -> None:
        """
        Click on an element.

        Args:
            element: Element to click
        """
        self.mouse.click_element(element)

    def double_click_element(self, element: Element) -> None:
        """
        Double-click on an element.

        Args:
            element: Element to double-click
        """
        self.mouse.double_click_element(element)

    def right_click_element(self, element: Element) -> None:
        """
        Right-click on an element.

        Args:
            element: Element to right-click
        """
        self.mouse.right_click_element(element)

    def drag_element(self, source_element: Element, target_element: Element) -> None:
        """
        Drag one element to another.

        Args:
            source_element: Element to drag from
            target_element: Element to drag to
        """
        self.mouse.drag_element_to_element(source_element, target_element)

    def scroll_element(self, element: Element, steps: int = 3, direction: str = "down") -> None:
        """
        Scroll on an element.

        Args:
            element: Element to scroll on
            steps: Number of scroll steps
            direction: "up" or "down"
        """
        self.mouse.scroll_element(element, steps, direction)

    def type_in_element(self, element: Element, text: str, clear_first: bool = True) -> None:
        """
        Type text in an element.

        Args:
            element: Element to type in
            text: Text to type
            clear_first: Whether to clear the field first
        """
        try:
            self.click_element(element)
        except Exception as e:
            # In mock mode or if click fails, just proceed with typing
            print(f"Note: Could not click element ({e}), proceeding with typing anyway")
        
        if clear_first:
            try:
                self.keyboard.clear_field()
            except:
                # Use Tab/Shift+Tab as fallback
                self.keyboard.send_tab()
        
        self.keyboard.type_text(text)

    def __repr__(self) -> str:
        return f"Screen({self.screen_name})"

    def __str__(self) -> str:
        return self.screen_name
