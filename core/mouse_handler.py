"""
Mouse interaction handling for the automation framework.
Simulates mouse movements, clicks, and drag operations.
"""

import time
from typing import Tuple, Optional
from enum import Enum


class MouseButton(Enum):
    """Enumeration of mouse buttons."""
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"


class MouseHandler:
    """
    Handles mouse interactions for application automation.
    Supports movement, clicking, double-clicking, and dragging.
    """

    def __init__(self):
        """Initialize MouseHandler."""
        try:
            import pynput.mouse as ms
            self.mouse = ms
            self.controller = ms.Controller()
            self.mouse_available = True
        except ImportError:
            self.mouse_available = False
            print("Warning: pynput not available. Install with: pip install pynput")

    def move_to(self, x: int, y: int, duration: float = 0.5) -> None:
        """
        Move mouse to coordinates.

        Args:
            x: X coordinate
            y: Y coordinate
            duration: Time to move (seconds) - smooth movement
        """
        if not self.mouse_available:
            print(f"Mock move mouse to ({x}, {y})")
            return

        try:
            self.controller.position = (x, y)
            time.sleep(0.1)
        except Exception as e:
            print(f"Error moving mouse: {e}")

    def move_to_element(self, element, offset_x: int = 0, offset_y: int = 0) -> None:
        """
        Move mouse to element center.

        Args:
            element: The element to move to
            offset_x: X offset from center
            offset_y: Y offset from center
        """
        center_x = element.get_runtime_data("center_x", 100)
        center_y = element.get_runtime_data("center_y", 100)
        
        self.move_to(center_x + offset_x, center_y + offset_y)

    def click(self, x: Optional[int] = None, y: Optional[int] = None, button: MouseButton = MouseButton.LEFT) -> None:
        """
        Click at coordinates.

        Args:
            x: X coordinate (uses current position if None)
            y: Y coordinate (uses current position if None)
            button: Mouse button to click
        """
        if not self.mouse_available:
            print(f"Mock click at ({x}, {y})")
            return

        try:
            if x is not None and y is not None:
                self.move_to(x, y)
            
            self.controller.click(button.value)
            time.sleep(0.2)
        except Exception as e:
            print(f"Error clicking: {e}")

    def click_element(self, element, button: MouseButton = MouseButton.LEFT) -> None:
        """
        Click on element center.

        Args:
            element: The element to click
            button: Mouse button to click
        """
        # Handle case where element might be a string or mock
        if isinstance(element, str):
            print(f"Mock click on element: {element}")
            return
        
        try:
            center_x = element.get_runtime_data("center_x", None)
            center_y = element.get_runtime_data("center_y", None)
            
            # If coordinates not available, use defaults for mocking
            if center_x is None or center_y is None:
                print(f"Mock click on element: {element.name if hasattr(element, 'name') else element}")
                return
            
            self.click(center_x, center_y, button)
        except AttributeError as e:
            print(f"Mock click - element missing attributes: {e}")

    def double_click(self, x: Optional[int] = None, y: Optional[int] = None) -> None:
        """
        Double-click at coordinates.

        Args:
            x: X coordinate (uses current position if None)
            y: Y coordinate (uses current position if None)
        """
        if not self.mouse_available:
            print(f"Mock double-click at ({x}, {y})")
            return

        try:
            if x is not None and y is not None:
                self.move_to(x, y)
            
            self.controller.click(MouseButton.LEFT.value, 2)
            time.sleep(0.3)
        except Exception as e:
            print(f"Error double-clicking: {e}")

    def double_click_element(self, element) -> None:
        """
        Double-click on element center.

        Args:
            element: The element to double-click
        """
        center_x = element.get_runtime_data("center_x", 100)
        center_y = element.get_runtime_data("center_y", 100)
        
        self.double_click(center_x, center_y)

    def right_click(self, x: Optional[int] = None, y: Optional[int] = None) -> None:
        """
        Right-click at coordinates.

        Args:
            x: X coordinate (uses current position if None)
            y: Y coordinate (uses current position if None)
        """
        if not self.mouse_available:
            print(f"Mock right-click at ({x}, {y})")
            return

        try:
            if x is not None and y is not None:
                self.move_to(x, y)
            
            self.controller.click(MouseButton.RIGHT.value)
            time.sleep(0.2)
        except Exception as e:
            print(f"Error right-clicking: {e}")

    def right_click_element(self, element) -> None:
        """
        Right-click on element center.

        Args:
            element: The element to right-click
        """
        center_x = element.get_runtime_data("center_x", 100)
        center_y = element.get_runtime_data("center_y", 100)
        
        self.right_click(center_x, center_y)

    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 1.0) -> None:
        """
        Drag from one position to another.

        Args:
            start_x: Starting X coordinate
            start_y: Starting Y coordinate
            end_x: Ending X coordinate
            end_y: Ending Y coordinate
            duration: Duration of drag (seconds)
        """
        if not self.mouse_available:
            print(f"Mock drag from ({start_x}, {start_y}) to ({end_x}, {end_y})")
            return

        try:
            self.move_to(start_x, start_y)
            time.sleep(0.2)
            
            self.controller.press(MouseButton.LEFT.value)
            
            # Calculate steps for smooth drag
            steps = int(duration * 50)  # 50 steps per second
            step_x = (end_x - start_x) / steps
            step_y = (end_y - start_y) / steps
            step_duration = duration / steps
            
            for _ in range(steps):
                current_x = self.controller.position[0] + step_x
                current_y = self.controller.position[1] + step_y
                self.controller.position = (int(current_x), int(current_y))
                time.sleep(step_duration)
            
            self.controller.release(MouseButton.LEFT.value)
            time.sleep(0.2)
        except Exception as e:
            print(f"Error dragging: {e}")

    def drag_element_to_element(self, source_element, target_element, duration: float = 1.0) -> None:
        """
        Drag one element to another.

        Args:
            source_element: Element to drag from
            target_element: Element to drag to
            duration: Duration of drag (seconds)
        """
        source_x = source_element.get_runtime_data("center_x", 100)
        source_y = source_element.get_runtime_data("center_y", 100)
        target_x = target_element.get_runtime_data("center_x", 200)
        target_y = target_element.get_runtime_data("center_y", 200)
        
        self.drag(source_x, source_y, target_x, target_y, duration)

    def drag_element_by_offset(
        self,
        element,
        offset_x: int,
        offset_y: int,
        duration: float = 1.0
    ) -> None:
        """
        Drag element by offset amount.

        Args:
            element: Element to drag
            offset_x: X offset to drag
            offset_y: Y offset to drag
            duration: Duration of drag (seconds)
        """
        start_x = element.get_runtime_data("center_x", 100)
        start_y = element.get_runtime_data("center_y", 100)
        end_x = start_x + offset_x
        end_y = start_y + offset_y
        
        self.drag(start_x, start_y, end_x, end_y, duration)

    def get_position(self) -> Tuple[int, int]:
        """
        Get current mouse position.

        Returns:
            Tuple of (x, y) coordinates
        """
        if not self.mouse_available:
            return (0, 0)

        try:
            return self.controller.position
        except Exception as e:
            print(f"Error getting mouse position: {e}")
            return (0, 0)

    def scroll(self, x: int, y: int, steps: int, direction: str = "down") -> None:
        """
        Scroll at specific coordinates.

        Args:
            x: X coordinate for scroll
            y: Y coordinate for scroll
            steps: Number of scroll steps
            direction: "up" or "down"
        """
        if not self.mouse_available:
            print(f"Mock scroll {direction} {steps} steps at ({x}, {y})")
            return

        try:
            self.move_to(x, y)
            time.sleep(0.2)
            
            scroll_value = steps if direction.lower() == "down" else -steps
            self.controller.scroll(0, scroll_value)
            time.sleep(0.3)
        except Exception as e:
            print(f"Error scrolling: {e}")

    def scroll_element(self, element, steps: int, direction: str = "down") -> None:
        """
        Scroll on element.

        Args:
            element: Element to scroll on
            steps: Number of scroll steps
            direction: "up" or "down"
        """
        center_x = element.get_runtime_data("center_x", 100)
        center_y = element.get_runtime_data("center_y", 100)
        
        self.scroll(center_x, center_y, steps, direction)
