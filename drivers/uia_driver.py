"""
UIA Driver for interacting with Windows UI Automation.
Provides abstraction for UIA element discovery and manipulation.
"""

from typing import List, Optional, Dict
import json
from core.element import Element, UIAProperty


class UIADriver:
    """
    Driver for Windows UI Automation interactions.
    Manages UIA element discovery and provides a bridge to automation actions.
    """

    def __init__(self):
        """Initialize UIADriver."""
        self._root_element: Optional[Element] = None
        self._element_cache: Dict[str, Element] = {}
        self.uia_available = self._check_uia_availability()

    @staticmethod
    def _check_uia_availability() -> bool:
        """Check if UIA dependencies are available."""
        try:
            import pywinauto
            return True
        except ImportError:
            print("Warning: pywinauto not available. Install with: pip install pywinauto")
            return False

    def set_root_element(self, element: Element) -> None:
        """
        Set the root element for the UI hierarchy.

        Args:
            element: Root element of the application
        """
        self._root_element = element
        self._build_cache(element)

    def _build_cache(self, element: Element) -> None:
        """Build a cache of elements for quick lookup."""
        if element.properties.auto_id:
            self._element_cache[element.properties.auto_id] = element
        
        for child in element.children:
            self._build_cache(child)

    def find_element_by_auto_id(self, auto_id: str) -> Optional[Element]:
        """
        Find element by auto_id.

        Args:
            auto_id: The auto_id of the element

        Returns:
            Element if found, None otherwise
        """
        return self._element_cache.get(auto_id)

    def find_elements_by_control_type(self, control_type: str) -> List[Element]:
        """
        Find all elements of a specific control type.

        Args:
            control_type: The control type to search for

        Returns:
            List of matching elements
        """
        results = []
        if self._root_element:
            self._collect_by_control_type(self._root_element, control_type, results)
        return results

    def find_elements_by_class_name(self, class_name: str) -> List[Element]:
        """
        Find all elements with a specific class name.

        Args:
            class_name: The class name to search for

        Returns:
            List of matching elements
        """
        results = []
        if self._root_element:
            self._collect_by_class_name(self._root_element, class_name, results)
        return results

    def get_element_hierarchy(self) -> Optional[Element]:
        """
        Get the root element with full hierarchy.

        Returns:
            Root element with all children
        """
        return self._root_element

    def load_hierarchy_from_dict(self, data: Dict) -> Element:
        """
        Load element hierarchy from dictionary representation.

        Args:
            data: Dictionary containing element hierarchy

        Returns:
            Root element with loaded hierarchy
        """
        element = Element.from_uia_dict(data)
        
        # Load children recursively
        if "children" in data:
            for child_data in data["children"]:
                child_element = self.load_hierarchy_from_dict(child_data)
                element.add_child(child_element)
        
        self.set_root_element(element)
        return element

    def load_hierarchy_from_json(self, json_str: str) -> Element:
        """
        Load element hierarchy from JSON string.

        Args:
            json_str: JSON string containing element hierarchy

        Returns:
            Root element with loaded hierarchy
        """
        data = json.loads(json_str)
        return self.load_hierarchy_from_dict(data)

    def export_hierarchy_to_dict(self) -> Optional[Dict]:
        """
        Export element hierarchy to dictionary.

        Returns:
            Dictionary representation of hierarchy
        """
        if not self._root_element:
            return None
        
        return self._element_to_dict(self._root_element)

    def export_hierarchy_to_json(self) -> Optional[str]:
        """
        Export element hierarchy to JSON string.

        Returns:
            JSON representation of hierarchy
        """
        data = self.export_hierarchy_to_dict()
        if data:
            return json.dumps(data, indent=2)
        return None

    def get_element_info(self, element: Element) -> Dict:
        """
        Get detailed information about an element.

        Args:
            element: Element to get info for

        Returns:
            Dictionary with element information
        """
        return {
            "name": element.name,
            "path": element.get_path(),
            "properties": element.properties.to_dict(),
            "selector": element.get_selector_string(),
            "children_count": len(element.children),
            "has_parent": element.parent is not None
        }

    @staticmethod
    def _collect_by_control_type(
        element: Element,
        control_type: str,
        results: List[Element]
    ) -> None:
        """Recursively collect elements by control type."""
        if element.properties.control_type == control_type:
            results.append(element)
        
        for child in element.children:
            UIADriver._collect_by_control_type(child, control_type, results)

    @staticmethod
    def _collect_by_class_name(
        element: Element,
        class_name: str,
        results: List[Element]
    ) -> None:
        """Recursively collect elements by class name."""
        if element.properties.class_name == class_name:
            results.append(element)
        
        for child in element.children:
            UIADriver._collect_by_class_name(child, class_name, results)

    @staticmethod
    def _element_to_dict(element: Element) -> Dict:
        """Convert element to dictionary representation."""
        data = {
            "name": element.name,
            "properties": element.properties.to_dict(),
        }
        
        if element.children:
            data["children"] = [UIADriver._element_to_dict(child) for child in element.children]
        
        return data

    def clear_cache(self) -> None:
        """Clear the element cache."""
        self._element_cache.clear()

    def refresh_hierarchy(self) -> None:
        """Refresh the element hierarchy and cache."""
        self.clear_cache()
        if self._root_element:
            self._build_cache(self._root_element)
