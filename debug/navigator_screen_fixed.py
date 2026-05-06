"""
NavigatorScreen - interact with G2 Navigator using WM_LBUTTONDOWN/UP messages
This is a FIXED version that works around the button click issue.
"""

import pywinauto
from pywinauto import Application
import pywinauto.findwindows
import time
import ctypes
from typing import Optional, Dict, List


class NavigatorScreen:
    """Represents the G2 Navigator screen after login"""
    
    def __init__(self):
        """Initialize Navigator connection"""
        self.app = None
        self.navigator = None
        self.children = None
        self._button_cache = {}
        self._panel_cache = {}
    
    def connect(self) -> bool:
        """Connect to the Navigator window"""
        try:
            windows = pywinauto.findwindows.find_windows(title_re='.*Navigator.*')
            if not windows:
                return False
            
            self.app = Application(backend='win32').connect(handle=windows[0])
            self.navigator = self.app.window(handle=windows[0])
            self._refresh_children()
            return True
        except Exception as e:
            print(f"Error connecting to Navigator: {e}")
            return False
    
    def _refresh_children(self):
        """Refresh the children list from Navigator"""
        try:
            self.children = self.navigator.children()
        except:
            pass
    
    def _find_button_by_automation_id(self, automation_id: str) -> Optional[Dict]:
        """Find a button by its automation ID"""
        try:
            for i, child in enumerate(self.children):
                try:
                    auto_id_prop = child.automation_id
                    if callable(auto_id_prop):
                        auto_id = auto_id_prop()
                    else:
                        auto_id = auto_id_prop
                    
                    if auto_id == automation_id:
                        return {
                            'idx': i,
                            'handle': child.handle,
                            'element': child,
                        }
                except:
                    pass
        except:
            pass
        return None
    
    def _click_button_via_message(self, button_handle: int):
        """Click a button by sending WM_LBUTTONDOWN/UP messages"""
        WM_LBUTTONDOWN = 0x0201
        WM_LBUTTONUP = 0x0202
        
        try:
            ctypes.windll.user32.SendMessageW(button_handle, WM_LBUTTONDOWN, 0, 0)
            time.sleep(0.05)
            ctypes.windll.user32.SendMessageW(button_handle, WM_LBUTTONUP, 0, 0)
            time.sleep(0.3)
            return True
        except Exception as e:
            print(f"Error sending click message: {e}")
            return False
    
    def click_menu_button(self, menu_name: str) -> bool:
        """
        Click a menu button (Sales, Service, Accounting, Admin, Parts)
        
        Args:
            menu_name: Name of the menu button to click
        
        Returns:
            True if click was successful
        """
        menu_name_lower = menu_name.lower()
        automation_id = f"btn{menu_name_lower.capitalize()}"
        
        # Find the button
        button_info = self._find_button_by_automation_id(automation_id)
        if not button_info:
            print(f"Error: Button '{automation_id}' not found")
            return False
        
        # Click the button using messages
        self._click_button_via_message(button_info['handle'])
        
        # Wait for response and refresh
        time.sleep(0.5)
        self._refresh_children()
        
        # Verify the content panel changed
        if self._verify_menu_active(menu_name):
            print(f"✓ Successfully clicked {menu_name}")
            return True
        else:
            print(f"✗ {menu_name} button click did not activate menu")
            return False
    
    def _verify_menu_active(self, menu_name: str) -> bool:
        """Verify that a menu's content panel is visible"""
        # Dynamically find the menu's panel
        try:
            for i, child in enumerate(self.children):
                try:
                    texts = child.texts() if hasattr(child, 'texts') else []
                    if texts and texts[0] == menu_name:
                        rect = child.rectangle()
                        width = rect.right - rect.left
                        
                        # Look for large content panels
                        if width > 1000:
                            is_visible = child.is_visible() if hasattr(child, 'is_visible') else False
                            return is_visible
                except:
                    pass
        except:
            pass
        
        return False
    
    def get_active_menu(self) -> Optional[str]:
        """Get the currently active menu"""
        try:
            for i, child in enumerate(self.children):
                try:
                    texts = child.texts() if hasattr(child, 'texts') else []
                    if texts and texts[0] in ['Sales', 'Service', 'Accounting', 'Admin', 'Parts']:
                        rect = child.rectangle()
                        width = rect.right - rect.left
                        
                        # Look for large content panels
                        if width > 1000:
                            is_visible = child.is_visible() if hasattr(child, 'is_visible') else False
                            if is_visible:
                                return texts[0]
                except:
                    pass
        except:
            pass
        
        return None
    
    def is_navigator_present(self) -> bool:
        """Check if Navigator window is present and accessible"""
        try:
            return self.navigator is not None and self.children is not None
        except:
            return False
    
    def get_all_menu_items(self) -> List[str]:
        """Get list of all available menu buttons"""
        menus = []
        for automation_id in ['btnSales', 'btnService', 'btnAccounting', 'btnAdmin', 'btnParts']:
            menu_name = automation_id[3:]  # Remove 'btn' prefix
            if self._find_button_by_automation_id(automation_id):
                menus.append(menu_name)
        return menus
    
    def verify_all_menus(self) -> bool:
        """Verify all menu buttons are accessible"""
        menu_items = self.get_all_menu_items()
        return len(menu_items) == 5  # Should have all 5 menus


if __name__ == '__main__':
    # Test the fixed NavigatorScreen
    print("Testing NavigatorScreen (Fixed)\n")
    
    nav = NavigatorScreen()
    
    if not nav.connect():
        print("ERROR: Could not connect to Navigator")
        exit(1)
    
    print("[1] Navigator connected successfully")
    print(f"[2] Available menus: {nav.get_all_menu_items()}")
    print(f"[3] Active menu: {nav.get_active_menu()}")
    
    print("\n[4] Testing menu clicks...")
    for menu_name in ['Sales', 'Service', 'Accounting', 'Admin', 'Parts']:
        result = nav.click_menu_button(menu_name)
        time.sleep(0.5)
        active = nav.get_active_menu()
        print(f"    Clicked {menu_name}: active is now {active}")
        
        if active != menu_name:
            print(f"    WARNING: Expected {menu_name} but got {active}")
    
    print("\n[5] All tests complete!")
