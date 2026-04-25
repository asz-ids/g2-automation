"""
Locator patterns and element matching logic for the automation framework.
Supports multiple locator strategies for identifying UI elements.
"""

from typing import Dict, List, Optional, Callable
from enum import Enum
from .element import Element, UIAProperty


class LocatorStrategy(Enum):
    """Enumeration of locator strategies."""
    AUTO_ID = "auto_id"
    CLASS_NAME = "class_name"
    CONTROL_TYPE = "control_type"
    TITLE = "title"
    SELECTOR = "selector"
    XPATH_LIKE = "xpath"
    PARTIAL_MATCH = "partial"
    CUSTOM = "custom"


class Locator:
    """
    Base class for element locators.
    Provides flexible element identification strategies.
    """

    def __init__(self, strategy: LocatorStrategy, value: str):
        """
        Initialize a Locator.

        Args:
            strategy: The locator strategy to use
            value: The value to match against
        """
        self.strategy = strategy
        self.value = value

    @staticmethod
    def by_auto_id(auto_id: str) -> 'Locator':
        """Create a locator using auto_id."""
        return Locator(LocatorStrategy.AUTO_ID, auto_id)

    @staticmethod
    def by_class_name(class_name: str) -> 'Locator':
        """Create a locator using class_name."""
        return Locator(LocatorStrategy.CLASS_NAME, class_name)

    @staticmethod
    def by_control_type(control_type: str) -> 'Locator':
        """Create a locator using control_type."""
        return Locator(LocatorStrategy.CONTROL_TYPE, control_type)

    @staticmethod
    def by_title(title: str) -> 'Locator':
        """Create a locator using title."""
        return Locator(LocatorStrategy.TITLE, title)

    @staticmethod
    def by_selector(selector: str) -> 'Locator':
        """Create a locator using a full UIA selector string."""
        return Locator(LocatorStrategy.SELECTOR, selector)

    def find(self, root_element: Element) -> Optional[Element]:
        """
        Find an element using this locator.

        Args:
            root_element: The root element to search from

        Returns:
            The found Element or None
        """
        if self.strategy == LocatorStrategy.AUTO_ID:
            return root_element.find_descendant(self.value)
        
        elif self.strategy == LocatorStrategy.TITLE:
            return self._find_by_title(root_element, self.value)
        
        elif self.strategy == LocatorStrategy.CONTROL_TYPE:
            return self._find_by_control_type(root_element, self.value)
        
        elif self.strategy == LocatorStrategy.CLASS_NAME:
            return self._find_by_class_name(root_element, self.value)
        
        elif self.strategy == LocatorStrategy.SELECTOR:
            return self._find_by_selector(root_element, self.value)
        
        return None

    def find_all(self, root_element: Element) -> List[Element]:
        """
        Find all elements matching this locator.

        Args:
            root_element: The root element to search from

        Returns:
            List of found Elements
        """
        results = []
        
        if self.strategy == LocatorStrategy.TITLE:
            self._find_all_by_title(root_element, self.value, results)
        elif self.strategy == LocatorStrategy.CONTROL_TYPE:
            self._find_all_by_control_type(root_element, self.value, results)
        elif self.strategy == LocatorStrategy.CLASS_NAME:
            self._find_all_by_class_name(root_element, self.value, results)
        
        return results

    @staticmethod
    def _find_by_title(element: Element, title: str) -> Optional[Element]:
        """Recursively find element by title."""
        if element.properties.title == title:
            return element
        
        for child in element.children:
            result = Locator._find_by_title(child, title)
            if result:
                return result
        return None

    @staticmethod
    def _find_by_control_type(element: Element, control_type: str) -> Optional[Element]:
        """Recursively find element by control_type."""
        if element.properties.control_type == control_type:
            return element
        
        for child in element.children:
            result = Locator._find_by_control_type(child, control_type)
            if result:
                return result
        return None

    @staticmethod
    def _find_by_class_name(element: Element, class_name: str) -> Optional[Element]:
        """Recursively find element by class_name."""
        if element.properties.class_name == class_name:
            return element
        
        for child in element.children:
            result = Locator._find_by_class_name(child, class_name)
            if result:
                return result
        return None

    @staticmethod
    def _find_by_selector(element: Element, selector: str) -> Optional[Element]:
        """Find element matching a selector string."""
        # Parse selector and match properties
        conditions = Locator._parse_selector(selector)
        if Locator._matches_conditions(element, conditions):
            return element
        
        for child in element.children:
            result = Locator._find_by_selector(child, selector)
            if result:
                return result
        return None

    @staticmethod
    def _find_all_by_title(element: Element, title: str, results: List) -> None:
        """Recursively find all elements by title."""
        if element.properties.title == title:
            results.append(element)
        
        for child in element.children:
            Locator._find_all_by_title(child, title, results)

    @staticmethod
    def _find_all_by_control_type(element: Element, control_type: str, results: List) -> None:
        """Recursively find all elements by control_type."""
        if element.properties.control_type == control_type:
            results.append(element)
        
        for child in element.children:
            Locator._find_all_by_control_type(child, control_type, results)

    @staticmethod
    def _find_all_by_class_name(element: Element, class_name: str, results: List) -> None:
        """Recursively find all elements by class_name."""
        if element.properties.class_name == class_name:
            results.append(element)
        
        for child in element.children:
            Locator._find_all_by_class_name(child, class_name, results)

    @staticmethod
    def _parse_selector(selector: str) -> Dict[str, str]:
        """Parse a selector string into key-value pairs."""
        conditions = {}
        # Format: control_type="Window",class_name="...",auto_id="..."
        parts = selector.split(",")
        for part in parts:
            part = part.strip()
            if "=" in part:
                key, value = part.split("=", 1)
                conditions[key.strip()] = value.strip().strip('"')
        return conditions

    @staticmethod
    def _matches_conditions(element: Element, conditions: Dict[str, str]) -> bool:
        """Check if element matches all conditions."""
        for key, value in conditions.items():
            element_value = getattr(element.properties, key, None)
            if element_value != value:
                return False
        return True

    def __repr__(self) -> str:
        return f"Locator({self.strategy.value}, {self.value})"


class LocatorBuilder:
    """
    Builder class for creating complex locators with multiple conditions.
    """

    def __init__(self):
        """Initialize the LocatorBuilder."""
        self.conditions = {}

    def with_auto_id(self, auto_id: str) -> 'LocatorBuilder':
        """Add auto_id condition."""
        self.conditions["auto_id"] = auto_id
        return self

    def with_class_name(self, class_name: str) -> 'LocatorBuilder':
        """Add class_name condition."""
        self.conditions["class_name"] = class_name
        return self

    def with_control_type(self, control_type: str) -> 'LocatorBuilder':
        """Add control_type condition."""
        self.conditions["control_type"] = control_type
        return self

    def with_title(self, title: str) -> 'LocatorBuilder':
        """Add title condition."""
        self.conditions["title"] = title
        return self

    def build_selector(self) -> str:
        """Build a selector string from conditions."""
        selector_parts = [f'{k}="{v}"' for k, v in self.conditions.items()]
        return ",".join(selector_parts)

    def build_locator(self) -> Locator:
        """Build a Locator from conditions."""
        selector = self.build_selector()
        return Locator.by_selector(selector)

    def __repr__(self) -> str:
        return f"LocatorBuilder({self.conditions})"
