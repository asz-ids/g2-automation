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

from screens.base_screen import BaseScreen
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
