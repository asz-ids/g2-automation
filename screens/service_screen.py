# screens/service_screen.py
"""
G2 Service Screen — navigation hub for the Service module.
Sits between NavigatorScreen and module-specific screens.
"""
import ctypes
import time
from typing import Optional

from screens.base_screen import BaseScreen
from screens.navigator_screen import NavigatorScreen


class ServiceScreen(BaseScreen):
    """
    Page object for the G2 Service panel.
    Clicks the Service menu button, discovers the explorer bar buttons,
    and exposes go_to() + named shortcuts for each sub-section.
    """

    def __init__(
        self,
        navigator: Optional[NavigatorScreen] = None,
        auto_navigate: bool = True,
    ):
        super().__init__("ServiceScreen")
        self._navigator: NavigatorScreen = (
            navigator if navigator is not None else NavigatorScreen()
        )
        self._discovered_buttons: list = []
        self._nav_hwnd: Optional[int] = getattr(self._navigator, "_nav_hwnd", None)

        if auto_navigate:
            self._navigate_and_discover()

    def _navigate_and_discover(self) -> bool:
        """Click btnService then discover the Service explorer bar buttons."""
        clicked = self._navigator.click_menu_button("Service")
        if not clicked:
            print("[X] ServiceScreen: click_menu_button('Service') failed")
            return False
        return self._discover_explorer_buttons()

    def _discover_explorer_buttons(self) -> bool:
        """
        Scan Navigator window child windows for Service explorer bar button titles.
        Uses Win32 EnumChildWindows to avoid COM/UIA crashes that occur when the
        Navigator's UIA tree changes after sub-screen navigation.
        Polls up to 3 s (6 x 0.5 s) for the panel to render.
        Excludes the five main menu items (Sales, Service, Accounting, Admin, Parts).
        Returns True if at least one button title is cached.
        """
        self._discovered_buttons = []
        nav_hwnd = getattr(self._navigator, "_nav_hwnd", None)
        if not nav_hwnd:
            print("[!] ServiceScreen: nav_hwnd not available — discovery skipped")
            return False

        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

        for attempt in range(6):
            found_titles = []
            buf = ctypes.create_unicode_buffer(512)

            def _cb(hwnd, _, _buf=buf, _titles=found_titles):
                ctypes.windll.user32.GetWindowTextW(hwnd, _buf, 512)
                title = _buf.value.strip()
                if (title
                        and title not in NavigatorScreen.EXPECTED_MENU_ITEMS
                        and title not in _titles):
                    _titles.append(title)
                return True

            try:
                ctypes.windll.user32.EnumChildWindows(nav_hwnd, WNDENUMPROC(_cb), 0)
            except Exception as e:
                if attempt == 5:
                    print(f"[!] ServiceScreen: EnumChildWindows error on final attempt: {e}")

            if found_titles:
                self._discovered_buttons = found_titles
                print(f"[OK] Service panel found {len(found_titles)} buttons: {found_titles}")
                return True

            if attempt < 5:
                time.sleep(0.5)

        print("[!] ServiceScreen: no explorer bar buttons found after 3 s")
        return False

    def go_to(self, section_name: str) -> bool:
        """
        Navigate to a Service sub-section by explorer bar button title.

        Logs a warning if section_name was not found during discovery but still
        attempts the click — the button may exist even if discovery missed it.

        Args:
            section_name: Explorer bar button title e.g. "Work Orders"

        Returns:
            True if the click succeeded, False otherwise
        """
        if not self.is_section_available(section_name):
            print(
                f"[!] ServiceScreen: '{section_name}' not in discovered buttons "
                f"{self._discovered_buttons} — attempting anyway"
            )
        return self._navigator.click_explorer_bar_button(section_name)

    def go_to_work_orders(self) -> bool:
        return self.go_to("Work Orders")

    def go_to_appointments(self) -> bool:
        return self.go_to("Appointments")

    def go_to_labor_scheduler(self) -> bool:
        return self.go_to("Labor Scheduler")

    def go_to_flat_rate_manager(self) -> bool:
        return self.go_to("Flat Rate Manager")

    def go_to_doc_manager(self) -> bool:
        return self.go_to("Doc Manager")

    def get_available_sections(self) -> list:
        """Return a copy of the discovered explorer bar button titles."""
        return list(self._discovered_buttons)

    def is_section_available(self, name: str) -> bool:
        """Case-insensitive check whether a section was found during discovery."""
        name_lower = name.lower()
        return any(b.lower() == name_lower for b in self._discovered_buttons)

    def rediscover(self) -> bool:
        """Re-scan the Service panel explorer bar. Returns True if >=1 button found."""
        return self._discover_explorer_buttons()
