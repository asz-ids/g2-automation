# screens/service_screen.py
"""
G2 Service Screen — navigation hub for the Service module.
Sits between NavigatorScreen and module-specific screens.
"""
import time
from typing import Optional

from pywinauto import Desktop

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

    # ------------------------------------------------------------------
    # Internal — to be implemented in Task 2
    # ------------------------------------------------------------------

    def _navigate_and_discover(self) -> bool:
        """Click btnService then discover the Service explorer bar buttons."""
        clicked = self._navigator.click_menu_button("Service")
        if not clicked:
            print("[X] ServiceScreen: click_menu_button('Service') failed")
            return False
        # Refresh nav_hwnd in case NavigatorScreen reconnected during the click
        self._nav_hwnd = getattr(self._navigator, "_nav_hwnd", None)
        return self._discover_explorer_buttons()

    def _discover_explorer_buttons(self) -> bool:
        """
        Scan Navigator window descendants for Service explorer bar buttons.
        Polls up to 3 s (6 x 0.5 s) for the panel to render after navigation.
        Excludes the five main menu items (Sales, Service, Accounting, Admin, Parts).
        Returns True if at least one button title is cached.
        """
        self._discovered_buttons = []
        nav_hwnd = getattr(self._navigator, "_nav_hwnd", None)
        if not nav_hwnd:
            print("[!] ServiceScreen: nav_hwnd not available — discovery skipped")
            return False

        for attempt in range(6):
            try:
                uia_window = Desktop(backend="uia").window(handle=nav_hwnd)
                buttons = []
                for btn in uia_window.descendants(control_type="Button"):
                    try:
                        title = btn.window_text().strip()
                        if title and title not in NavigatorScreen.EXPECTED_MENU_ITEMS:
                            if title not in buttons:
                                buttons.append(title)
                    except Exception:
                        pass
                if buttons:
                    self._discovered_buttons = buttons
                    print(
                        f"[OK] Service panel found {len(buttons)} buttons: {buttons}"
                    )
                    return True
            except Exception:
                pass
            time.sleep(0.5)

        print("[!] ServiceScreen: no explorer bar buttons found after 3 s")
        return False

    # ------------------------------------------------------------------
    # Public API — to be implemented in Task 3
    # ------------------------------------------------------------------

    def go_to(self, section_name: str) -> bool:
        raise NotImplementedError("Implement in Task 3")

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
        raise NotImplementedError("Implement in Task 3")

    def is_section_available(self, name: str) -> bool:
        raise NotImplementedError("Implement in Task 3")

    def rediscover(self) -> bool:
        """Re-scan the Service panel explorer bar. Returns True if >=1 button found."""
        return self._discover_explorer_buttons()
