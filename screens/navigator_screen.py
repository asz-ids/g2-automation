"""
G2 Navigator Screen - Main application after successful login
Verifies that all expected menus and buttons are present.
"""

from typing import List, Dict, Optional
import warnings
from screens.base_screen import BaseScreen
from core.element import Element, UIAProperty
from core.locator import Locator
from pywinauto import findwindows
from pywinauto.application import Application

warnings.filterwarnings('ignore')


class NavigatorScreen(BaseScreen):
    """
    G2 Navigator Screen page object.
    Represents the main application window after successful login.
    """
    
    # Expected menu items and buttons (actual G2 Navigator structure)
    EXPECTED_MENU_ITEMS = [
        "Sales",
        "Service",
        "Accounting",
        "Admin",
        "Parts",
    ]
    
    def __init__(self, discover_from_window=True):
        """Initialize NavigatorScreen."""
        super().__init__("G2NavigatorScreen")
        self._uia_app = None
        self._uia_window = None
        self._win32_app = None
        self._win32_window = None
        self._discovered_menus = set()
        if discover_from_window:
            self._discover_navigator_window()
    
    def _discover_navigator_window(self) -> bool:
        """
        Discover and connect to the G2 Navigator window.
        Uses win32 backend for reliable menu detection.
        
        Returns:
            True if successfully connected, False otherwise
        """
        try:
            # Find G2 Navigator window
            windows = findwindows.find_windows(title_re=".*Navigator.*")
            
            if not windows:
                print("G2 Navigator window not found")
                return False
            
            # Connect with win32 backend for menu detection
            self._win32_app = Application(backend='win32').connect(handle=windows[0])
            self._win32_window = self._win32_app.top_window()
            
            # Also try UIA backend as backup
            try:
                self._uia_app = Application(backend='uia').connect(handle=windows[0])
                self._uia_window = self._uia_app.window()
            except:
                pass
            
            # Cache discovered menus
            self._scan_and_cache_menus()
            
            print(f"[OK] Connected to G2 Navigator window")
            return True
            
        except Exception as e:
            print(f"Error discovering Navigator window: {e}")
            return False
    
    def is_navigator_present(self, timeout_seconds: float = 1.0) -> bool:
        """
        Check if G2 Navigator window is present/visible.
        
        Args:
            timeout_seconds: Timeout in seconds (for compatibility)
            
        Returns:
            True if present, False otherwise
        """
        try:
            if self._win32_window is None:
                return self._discover_navigator_window()
            
            # Check if window still exists
            try:
                _ = self._win32_window.window_text()
                return True
            except:
                # Try to rediscover
                return self._discover_navigator_window()
        except:
            return False
    
    def is_navigator_visible(self, timeout_seconds: float = 5.0) -> bool:
        """
        Check if G2 Navigator window is visible.
        
        Args:
            timeout_seconds: Timeout in seconds
            
        Returns:
            True if visible, False otherwise
        """
        return self.is_navigator_present(timeout_seconds)
    
    def _scan_and_cache_menus(self) -> None:
        """
        Scan the Navigator window and cache all visible menu items.
        Uses win32 backend for reliable detection.
        """
        self._discovered_menus.clear()
        
        if self._win32_window is None:
            return
        
        try:
            children = self._win32_window.children()
            for child in children:
                try:
                    text = child.window_text()
                    if text and len(text.strip()) > 0:
                        self._discovered_menus.add(text)
                except:
                    pass
        except Exception as e:
            print(f"Error scanning menus: {e}")
    
    def verify_menu_item_present(self, menu_title: str) -> bool:
        """
        Verify that a specific menu item or button is present.
        
        Args:
            menu_title: Title of the menu item to find
            
        Returns:
            True if found, False otherwise
        """
        # Check cached menus first
        if menu_title in self._discovered_menus:
            return True
        
        # Try win32 backend scan
        if self._win32_window is None:
            return False
        
        try:
            children = self._win32_window.children()
            for child in children:
                try:
                    text = child.window_text()
                    if text and text == menu_title:
                        return True
                except:
                    pass
        except Exception as e:
            print(f"Error searching for menu item '{menu_title}': {e}")
        
        return False
    
    def verify_all_menus(self) -> Dict[str, bool]:
        """
        Verify that all expected menu items are present.
        
        Returns:
            Dictionary with menu_title -> is_present mapping
        """
        results = {}
        
        for menu_item in self.EXPECTED_MENU_ITEMS:
            is_present = self.verify_menu_item_present(menu_item)
            results[menu_item] = is_present
            status = "[OK]" if is_present else "[X]"
            print(f"{status} {menu_item}")
        
        return results
    
    def get_all_menu_items(self) -> List[str]:
        """
        Get all menu items/buttons currently visible in the navigator.
        
        Returns:
            List of menu item titles
        """
        # Return cached menus
        if self._discovered_menus:
            return sorted(list(self._discovered_menus))
        
        # If cache empty, scan now
        if self._win32_window is None:
            return []
        
        try:
            menu_items = set()
            children = self._win32_window.children()
            for child in children:
                try:
                    text = child.window_text()
                    if text and len(text.strip()) > 0:
                        menu_items.add(text)
                except:
                    pass
            
            return sorted(list(menu_items))
        except Exception as e:
            print(f"Error collecting menu items: {e}")
        
        return []
    
    def get_verification_report(self) -> Dict:
        """
        Get comprehensive verification report.
        
        Returns:
            Dictionary with verification results
        """
        all_menus = self.get_all_menu_items()
        found_expected = sum(1 for menu in self.EXPECTED_MENU_ITEMS if menu in all_menus)
        total_expected = len(self.EXPECTED_MENU_ITEMS)
        
        return {
            'navigator_found': self.is_navigator_present(),
            'menus_found': len(all_menus),
            'expected_found': found_expected,
            'expected_total': total_expected,
            'match_percentage': (found_expected / total_expected * 100) if total_expected > 0 else 0,
            'all_menus': all_menus,
            'missing_menus': [m for m in self.EXPECTED_MENU_ITEMS if m not in all_menus],
        }
    
    def get_status(self) -> Dict:
        """
        Get comprehensive status of the Navigator screen.
        
        Returns:
            Dictionary with screen status information
        """
        return {
            'screen_name': self.screen_name,
            'is_visible': self.is_navigator_visible(timeout_seconds=1),
            'window_object': self._win32_window is not None,
            'app_object': self._win32_app is not None,
            'menus_cached': len(self._discovered_menus),
        }
