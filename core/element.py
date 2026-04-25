"""
Core Element class for representing UI elements in the automation framework.
Handles both WinForms and PICK UI elements with UIA properties.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ControlType(Enum):
    """Enumeration of common UI control types."""
    WINDOW = "Window"
    BUTTON = "Button"
    TEXT = "Text"
    EDIT = "Edit"
    PANE = "Pane"
    GROUP = "Group"
    CHECKBOX = "CheckBox"
    RADIO = "RadioButton"
    COMBOBOX = "ComboBox"
    LIST = "List"
    CUSTOM = "Custom"


@dataclass
class UIAProperty:
    """Represents a UIA property for element identification."""
    control_type: Optional[str] = None
    class_name: Optional[str] = None
    title: Optional[str] = None
    auto_id: Optional[str] = None
    rich_text: Optional[str] = None
    child_count: Optional[int] = None
    selector: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert properties to dictionary, excluding None values."""
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def to_selector_string(self) -> str:
        """Generate a UIA selector string from properties."""
        if self.selector:
            return self.selector
        
        conditions = []
        if self.control_type:
            conditions.append(f'control_type="{self.control_type}"')
        if self.class_name:
            conditions.append(f'class_name="{self.class_name}"')
        if self.auto_id:
            conditions.append(f'auto_id="{self.auto_id}"')
        if self.title:
            conditions.append(f'title="{self.title}"')
        
        return ",".join(conditions) if conditions else ""


class Element:
    """
    Represents a UI element in the automation framework.
    Supports hierarchical navigation and UIA property management.
    """

    def __init__(
        self,
        name: str,
        properties: UIAProperty,
        parent: Optional['Element'] = None,
        children: Optional[List['Element']] = None
    ):
        """
        Initialize an Element.

        Args:
            name: Display name for the element
            properties: UIA properties for element identification
            parent: Parent element in the hierarchy
            children: List of child elements
        """
        self.name = name
        self.properties = properties
        self.parent = parent
        self.children = children or []
        self._runtime_data = {}

    @staticmethod
    def from_uia_dict(data: Dict) -> 'Element':
        """
        Create an Element from a UIA properties dictionary.

        Args:
            data: Dictionary containing UIA properties

        Returns:
            Element: Newly created Element instance
        """
        uia_prop = UIAProperty(
            control_type=data.get("control_type"),
            class_name=data.get("class_name"),
            title=data.get("title"),
            auto_id=data.get("auto_id"),
            rich_text=data.get("rich_text"),
            child_count=data.get("child_count"),
            selector=data.get("selector")
        )
        return Element(
            name=data.get("name", data.get("auto_id", "Unknown")),
            properties=uia_prop
        )

    def add_child(self, child: 'Element') -> None:
        """Add a child element."""
        child.parent = self
        self.children.append(child)

    def get_children_by_control_type(self, control_type: str) -> List['Element']:
        """Get all children matching a specific control type."""
        return [c for c in self.children if c.properties.control_type == control_type]

    def get_child_by_auto_id(self, auto_id: str) -> Optional['Element']:
        """Get a child element by auto_id."""
        for child in self.children:
            if child.properties.auto_id == auto_id:
                return child
        return None

    def get_child_by_title(self, title: str) -> Optional['Element']:
        """Get a child element by title."""
        for child in self.children:
            if child.properties.title == title:
                return child
        return None

    def find_descendant(self, auto_id: str) -> Optional['Element']:
        """Find a descendant element by auto_id (recursive search)."""
        if self.properties.auto_id == auto_id:
            return self
        
        for child in self.children:
            result = child.find_descendant(auto_id)
            if result:
                return result
        return None

    def get_root(self) -> 'Element':
        """Get the root element of the hierarchy."""
        current = self
        while current.parent:
            current = current.parent
        return current

    def get_path(self) -> List[str]:
        """Get the path to this element from root."""
        path = [self.name]
        current = self.parent
        while current:
            path.insert(0, current.name)
            current = current.parent
        return path

    def set_runtime_data(self, key: str, value) -> None:
        """Store runtime data on the element."""
        self._runtime_data[key] = value

    def get_runtime_data(self, key: str, default=None):
        """Retrieve runtime data from the element."""
        return self._runtime_data.get(key, default)

    def get_selector_string(self) -> str:
        """Get the UIA selector string for this element."""
        return self.properties.to_selector_string()

    def __repr__(self) -> str:
        """String representation of the element."""
        props = self.properties.to_dict()
        return f"Element(name={self.name}, properties={props}, children={len(self.children)})"

    def __str__(self) -> str:
        """User-friendly string representation."""
        return f"{self.name} ({self.properties.control_type})"
