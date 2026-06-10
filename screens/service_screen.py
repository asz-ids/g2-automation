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
        raise NotImplementedError("Implement in Task 2")

    def _discover_explorer_buttons(self) -> bool:
        raise NotImplementedError("Implement in Task 2")

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
        raise NotImplementedError("Implement in Task 2")
