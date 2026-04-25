# screens/work_order_creation_screen.py
"""
G2 Work Order Creation Screen — Phase 1.
Covers: create WO, WO Manager, search, comments, PDF printouts.

UIA Properties Reference (update after running scan_service_work_orders.py):
- Window title pattern: ".*Work Order.*" or ".*Service.*"
- Search field: auto_id="txtWOSearch"  (UPDATE from Task 1 scan)
- New WO button: auto_id="btnNewWO"    (UPDATE from Task 1 scan)
"""
import time
from typing import Optional

from pywinauto import findwindows
from pywinauto.application import Application
from pywinauto.keyboard import send_keys

from screens.base_screen import BaseScreen
from screens.navigator_screen import NavigatorScreen
from core.element import Element, UIAProperty


class WorkOrderCreationScreen(BaseScreen):
    """
    G2 Work Order Creation Screen page object.
    Handles interactions with the Work Order Manager window and WO creation form.
    Supports dual-mode initialization: live UIA discovery or manual element setup.
    """

    WINDOW_TITLE_RE = r".*Work Order.*"

    # Update these with real auto_ids from scan_service_work_orders.py (Task 1)
    ELEMENT_IDS = [
        "txtWOSearch",
        "btnSearch",
        "lstWorkOrders",
        "btnNewWO",
        "txtCustomerNumber",
        "txtUnitNumber",
        "cmbWOType",
        "cmbTechnician",
        "dteDateOpened",
        "txtComments",
        "btnSaveWO",
        "btnPrintCustomer",
        "btnPrintShop",
        "lblWONumber",
    ]

    def __init__(self, discover_from_uia: bool = True):
        super().__init__("WorkOrderCreationScreen")
        self._uia_app = None
        self._uia_window = None
        self._found_elements: dict = {}

        if discover_from_uia:
            self._discover_from_live_uia()
        else:
            self._setup_elements_manual()

    def _discover_from_live_uia(self) -> None:
        try:
            windows = findwindows.find_windows(title_re=self.WINDOW_TITLE_RE)
            if windows:
                self._uia_app = Application(backend='uia').connect(handle=windows[0])
                self._uia_window = self._uia_app.window()
                self._search_for_uia_elements(self._uia_window)
                root = Element(
                    name="WorkOrderForm",
                    properties=UIAProperty(
                        control_type="Window",
                        title="Work Order",
                        auto_id="WorkOrderForm"
                    )
                )
                root.set_runtime_data("uia_element", self._uia_window)
                self.set_root_element(root)
                print(f"[OK] Connected to Work Order window — {len(self._found_elements)} elements found")
            else:
                print("Work Order window not found, using manual setup")
                self._setup_elements_manual()
        except Exception as e:
            print(f"UIA discovery failed: {e}. Using manual setup.")
            self._setup_elements_manual()

    def _search_for_uia_elements(self, window_elem, max_depth: int = 5) -> None:
        def recurse(elem, depth):
            if depth > max_depth:
                return
            try:
                auto_id = elem.automation_id()
                if auto_id and auto_id in self.ELEMENT_IDS and auto_id not in self._found_elements:
                    self._found_elements[auto_id] = elem
            except Exception:
                pass
            if len(self._found_elements) >= len(self.ELEMENT_IDS):
                return
            try:
                for child in elem.children():
                    recurse(child, depth + 1)
            except Exception:
                pass

        recurse(window_elem, 0)

    def _setup_elements_manual(self) -> None:
        root = Element(
            name="WorkOrderForm",
            properties=UIAProperty(control_type="Window", title="Work Order", auto_id="WorkOrderForm")
        )
        for idx, elem_id in enumerate(self.ELEMENT_IDS):
            elem = Element(
                name=elem_id,
                properties=UIAProperty(control_type="Pane", auto_id=elem_id)
            )
            elem.set_runtime_data("center_x", 600)
            elem.set_runtime_data("center_y", 200 + idx * 30)
            root.add_child(elem)
        self.set_root_element(root)

    def _get_elem(self, auto_id: str) -> Optional[object]:
        elem = self._found_elements.get(auto_id)
        if elem is None:
            print(f"Warning: element '{auto_id}' not in discovered set")
        return elem

    def is_wo_manager_loaded(self) -> bool:
        if self._uia_window is not None:
            try:
                self._uia_window.window_text()
                return True
            except Exception:
                pass
        return self.verify_text_present("Work Order")

    def navigate_to_work_orders(self) -> bool:
        """
        Navigate from the G2 Navigator to Service → Work Orders.
        Reconnects UIA discovery to the newly opened WO Manager window.
        """
        navigator = NavigatorScreen()
        if not navigator.click_menu_button("Service"):
            print("[X] Could not click Service menu in Navigator")
            return False
        time.sleep(0.5)
        if not navigator.click_explorer_bar_button("Work Orders"):
            print("[X] Could not click 'Work Orders' explorer bar button")
            return False
        time.sleep(1.5)
        self._discover_from_live_uia()
        return self.is_wo_manager_loaded()

    def click_new_work_order(self) -> bool:
        """Open the blank WO creation form."""
        elem = self._get_elem("btnNewWO")
        if elem is None:
            return False
        elem.click_input()
        time.sleep(0.5)
        return True

    def enter_customer(self, number: str) -> bool:
        """Type customer number into the customer lookup field and wait for resolution."""
        elem = self._get_elem("txtCustomerNumber")
        if elem is None:
            return False
        elem.click_input()
        send_keys('^a')
        send_keys(number)
        time.sleep(0.5)
        return True

    def enter_unit(self, number: str) -> bool:
        """Type unit/stock number into the unit field."""
        elem = self._get_elem("txtUnitNumber")
        if elem is None:
            return False
        elem.click_input()
        send_keys('^a')
        send_keys(number)
        time.sleep(0.3)
        return True

    def select_wo_type(self, type_name: str) -> bool:
        """
        Select WO type from dropdown.
        type_name: "Customer Pay", "Warranty", or "Internal"
        """
        elem = self._get_elem("cmbWOType")
        if elem is None:
            return False
        elem.click_input()
        time.sleep(0.2)
        send_keys(type_name[:3])
        time.sleep(0.2)
        send_keys('{ENTER}')
        return True

    def select_technician(self, name: str) -> bool:
        """Select a technician from the tech dropdown by typing first 3 chars."""
        elem = self._get_elem("cmbTechnician")
        if elem is None:
            return False
        elem.click_input()
        time.sleep(0.2)
        send_keys(name[:3])
        time.sleep(0.2)
        send_keys('{ENTER}')
        return True

    def add_comment(self, text: str) -> bool:
        """Type text into the WO comments field."""
        elem = self._get_elem("txtComments")
        if elem is None:
            return False
        elem.click_input()
        send_keys(text)
        return True

    def save_work_order(self) -> str:
        """
        Click Save. Waits up to 3s for the assigned WO number to appear.
        Returns the WO number string, or "" if save failed.
        """
        elem = self._get_elem("btnSaveWO")
        if elem is None:
            return ""
        elem.click_input()
        for _ in range(30):
            time.sleep(0.1)
            wo_num = self.get_current_wo_number()
            if wo_num:
                return wo_num
        return ""

    def get_current_wo_number(self) -> str:
        """Read the assigned WO number from the label element."""
        elem = self._get_elem("lblWONumber")
        if elem is None:
            return ""
        try:
            text = elem.window_text().strip()
            return text
        except Exception:
            return ""

    def is_wo_saved_successfully(self) -> bool:
        """Returns True if a WO number is assigned (non-empty)."""
        return len(self.get_current_wo_number()) > 0

    def get_wo_status(self) -> str:
        """
        Returns current WO status text by checking screen for known status values.
        Returns "Open", "Closed", or "Unknown".
        """
        if self.verify_text_present("Open"):
            return "Open"
        if self.verify_text_present("Closed"):
            return "Closed"
        return "Unknown"

    def _run_search(self) -> None:
        """Submit the current search by clicking btnSearch or pressing Enter."""
        btn = self._get_elem("btnSearch")
        if btn:
            btn.click_input()
        else:
            send_keys('{ENTER}')
        time.sleep(0.8)

    def search_by_wo_number(self, wo_num: str) -> bool:
        """
        Type wo_num into the search field and submit.
        Returns True if the WO number appears in the results.
        """
        field = self._get_elem("txtWOSearch")
        if field is None:
            return False
        field.click_input()
        send_keys('^a')
        send_keys(wo_num)
        self._run_search()
        return self.verify_text_present(wo_num)

    def search_by_customer(self, name: str) -> list:
        """
        Search by customer name. Returns a list of WO numbers visible in the results grid.
        Returns an empty list if no results or the grid cannot be read.
        """
        field = self._get_elem("txtWOSearch")
        if field is None:
            return []
        field.click_input()
        send_keys('^a')
        send_keys(name)
        self._run_search()
        results = []
        lst = self._get_elem("lstWorkOrders")
        if lst:
            try:
                for item in lst.items():
                    text = item.window_text().strip()
                    if text:
                        results.append(text)
            except Exception:
                pass
        return results

    def clear_search(self) -> None:
        """Clear the search field and reset results."""
        field = self._get_elem("txtWOSearch")
        if field:
            field.click_input()
            send_keys('^a{DELETE}')
            self._run_search()

    def _wait_for_print_window(self, title_re: str, timeout: float = 5.0) -> bool:
        """
        Poll for a new window matching title_re to appear (G2 renders PDFs to a viewer window).
        Returns True if the window appears within timeout seconds.
        """
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                windows = findwindows.find_windows(title_re=title_re)
                if windows:
                    return True
            except Exception:
                pass
            time.sleep(0.3)
        return False

    def print_customer_copy(self) -> bool:
        """
        Click the Print Customer button and verify a print/PDF window appears.
        Window title must contain "Customer", "Print", or "Report".
        """
        elem = self._get_elem("btnPrintCustomer")
        if elem is None:
            return False
        elem.click_input()
        return self._wait_for_print_window(r".*(Customer|Print|Report).*")

    def print_shop_copy(self) -> bool:
        """
        Click the Print Shop button and verify a print/PDF window appears.
        Window title must contain "Shop", "Print", or "Report".
        """
        elem = self._get_elem("btnPrintShop")
        if elem is None:
            return False
        elem.click_input()
        return self._wait_for_print_window(r".*(Shop|Print|Report).*")
