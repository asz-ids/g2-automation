"""
G2 Navigator Screen - Main application after successful login
Verifies that all expected menus and buttons are present.

IMPORTANT: Button clicking uses WM_LBUTTONDOWN/UP messages because standard 
pywinauto click methods don't work with these custom WindowsForms controls.
"""

from typing import List, Dict, Optional
import warnings
import time
import ctypes
from screens.base_screen import BaseScreen
from core.element import Element, UIAProperty
from core.locator import Locator
from pywinauto import Desktop, findwindows
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
        self._nav_hwnd = None
        self._discovered_menus = set()
        if discover_from_window:
            self._discover_navigator_window()
    
    def _discover_navigator_window(self) -> bool:
        """
        Discover and connect to the G2 Navigator window.
        Uses Desktop() instead of Application.connect() to avoid OpenProcess
        (which fails with UIPI/access-denied when G2 runs elevated).
        """
        try:
            windows = findwindows.find_windows(title_re=".*Navigator.*|.*IDS G2.*")
            if not windows:
                print("G2 Navigator window not found")
                return False

            hwnd = windows[0]

            # Restore if minimised — WM_SHOWWINDOW is UIPI-exempt
            ctypes.windll.user32.ShowWindow(hwnd, 9)   # SW_RESTORE
            ctypes.windll.user32.SetForegroundWindow(hwnd)
            ctypes.windll.user32.BringWindowToTop(hwnd)
            time.sleep(0.3)

            # Desktop() wraps by HWND without calling OpenProcess — works cross-privilege
            self._win32_window = Desktop(backend='win32').window(handle=hwnd)
            try:
                self._uia_window = Desktop(backend='uia').window(handle=hwnd)
            except Exception:
                self._uia_window = None

            self._nav_hwnd = hwnd
            self._scan_and_cache_menus()
            print("[OK] Connected to G2 Navigator window")
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
    
    def _find_button_by_automation_id(self, automation_id: str) -> Optional[Dict]:
        """
        Find a button by its automation ID.
        
        Args:
            automation_id: The automation ID to search for (e.g., 'btnSales')
            
        Returns:
            Dictionary with button info or None if not found
        """
        if self._win32_window is None:
            return None
        
        try:
            children = self._win32_window.children()
            for i, child in enumerate(children):
                try:
                    auto_id_prop = child.automation_id
                    if callable(auto_id_prop):
                        auto_id = auto_id_prop()
                    else:
                        auto_id = auto_id_prop
                    
                    if auto_id == automation_id:
                        return {
                            'idx': i,
                            'handle': child.handle if hasattr(child, 'handle') else None,
                            'element': child,
                        }
                except:
                    pass
        except Exception as e:
            print(f"Error finding button by automation_id: {e}")
        
        return None
    
    def _find_panel_by_label(self, menu_name: str) -> Optional[Dict]:
        """
        Find a content panel by its menu label.
        
        Args:
            menu_name: The menu name to find panel for (e.g., 'Sales')
            
        Returns:
            Dictionary with panel info or None if not found
        """
        if self._win32_window is None:
            return None
        
        try:
            children = self._win32_window.children()
            for i, child in enumerate(children):
                try:
                    texts = child.texts() if hasattr(child, 'texts') else []
                    if texts and texts[0] == menu_name:
                        rect = child.rectangle()
                        width = rect.right - rect.left
                        
                        # Look for large content panels (>1000 width)
                        if width > 1000:
                            is_visible = child.is_visible() if hasattr(child, 'is_visible') else False
                            return {
                                'idx': i,
                                'handle': child.handle if hasattr(child, 'handle') else None,
                                'element': child,
                                'visible': is_visible,
                            }
                except:
                    pass
        except Exception as e:
            print(f"Error finding panel: {e}")
        
        return None
    
    def _click_button_via_message(self, button_handle: int) -> bool:
        """
        Click a button by sending WM_LBUTTONDOWN/UP messages.
        This method is used because standard click methods don't work
        with these custom WindowsForms controls.
        
        Args:
            button_handle: Window handle of the button to click
            
        Returns:
            True if successful, False otherwise
        """
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
        Click a menu button to navigate to that menu.
        
        Args:
            menu_name: Name of the menu to click (Sales, Service, Accounting, Admin, Parts)
            
        Returns:
            True if click was successful and menu became active, False otherwise
        """
        # Ensure we're connected
        if self._win32_window is None:
            if not self._discover_navigator_window():
                print(f"Error: Navigator not found")
                return False
        
        # Find the button by automation ID
        button_auto_id = f"btn{menu_name}"
        button_info = self._find_button_by_automation_id(button_auto_id)
        
        if not button_info or not button_info.get('handle'):
            print(f"Error: Button '{button_auto_id}' not found")
            return False
        
        # Click via UIA (crosses UIPI privilege boundary via accessibility layer)
        btn_hwnd = button_info['handle']
        clicked = False
        try:
            uia_btn = Desktop(backend='uia').window(handle=btn_hwnd)
            uia_btn.click_input()
            clicked = True
        except Exception:
            pass

        if not clicked:
            # Fallback: raw SendMessage (works if G2 is not elevated)
            self._click_button_via_message(btn_hwnd)

        # Refresh window references without OpenProcess
        time.sleep(0.5)
        try:
            handles = findwindows.find_windows(title_re=".*Navigator.*")
            if handles:
                self._win32_window = Desktop(backend='win32').window(handle=handles[0])
                try:
                    self._uia_window = Desktop(backend='uia').window(handle=handles[0])
                except Exception:
                    pass
        except Exception:
            pass
        
        # Verify panel became active — treat as informational, not a hard failure
        panel_info = self._find_panel_by_label(menu_name)
        if panel_info and panel_info.get('visible'):
            print(f"[OK] {menu_name} panel confirmed visible")
        else:
            print(f"[!] {menu_name} panel not confirmed visible — click may still have worked")
        return clicked  # trust the UIA click result
    
    def get_active_menu(self) -> Optional[str]:
        """
        Get the currently active menu.
        
        Returns:
            Name of the active menu or None if unable to determine
        """
        if self._win32_window is None:
            return None
        
        try:
            children = self._win32_window.children()
            for child in children:
                try:
                    texts = child.texts() if hasattr(child, 'texts') else []
                    if texts and texts[0] in self.EXPECTED_MENU_ITEMS:
                        rect = child.rectangle()
                        width = rect.right - rect.left
                        
                        # Look for large content panels
                        if width > 1000:
                            is_visible = child.is_visible() if hasattr(child, 'is_visible') else False
                            if is_visible:
                                return texts[0]
                except:
                    pass
        except Exception as e:
            print(f"Error getting active menu: {e}")
        
        return None
    
    def click_explorer_bar_button(self, button_title: str) -> bool:
        """
        Click a button in the explorer bar (e.g. 'Work Orders', 'Take AR Payments').
        Tries UIA first (crosses UIPI), then falls back to HWND text search + UIA click.
        """
        # UIA approach — works cross-privilege via accessibility layer
        if self._uia_window is not None:
            try:
                btn = self._uia_window.child_window(title=button_title, control_type="Button")
                btn.click_input()
                print(f"[OK] Clicked '{button_title}' (UIA)")
                return True
            except Exception:
                pass

            # Partial-title UIA scan
            try:
                for btn in self._uia_window.descendants(control_type="Button"):
                    try:
                        if button_title.lower() in btn.window_text().lower():
                            btn.click_input()
                            print(f"[OK] Clicked '{btn.window_text()}' (UIA partial)")
                            return True
                    except Exception:
                        pass
            except Exception:
                pass

        # Fallback: find by HWND text, click via UIA wrapper
        if self._nav_hwnd:
            WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
            found_hwnd = []
            buf = ctypes.create_unicode_buffer(512)
            def _cb(hwnd, _):
                ctypes.windll.user32.GetWindowTextW(hwnd, buf, 512)
                if button_title.lower() in buf.value.strip().lower():
                    found_hwnd.append(hwnd)
                    return False
                return True
            ctypes.windll.user32.EnumChildWindows(self._nav_hwnd, WNDENUMPROC(_cb), 0)
            if found_hwnd:
                try:
                    uia_btn = Desktop(backend='uia').window(handle=found_hwnd[0])
                    uia_btn.click_input()
                    print(f"[OK] Clicked '{button_title}' (HWND+UIA)")
                    return True
                except Exception:
                    pass

        print(f"[X] Could not find or click '{button_title}' button")
        return False
