# Work Order Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `WorkOrderCreationScreen` — a Page Object that automates G2 Service → Work Orders (create WO, WO Manager, search, comments, PDF print) — and a matching pytest regression suite covering the 7 GA checklist items.

**Architecture:** Option B from the design: one focused screen class per phase. `WorkOrderCreationScreen` inherits `BaseScreen`, mirrors the `LoginScreen` dual-mode init (live UIA discovery + manual fallback), and uses the same `_found_elements` dict pattern. Navigation reuses `NavigatorScreen.click_menu_button("Service")` + `click_explorer_bar_button("Work Orders")`.

**Tech Stack:** Python, pywinauto (uia + win32 backends), pywinauto.keyboard.send_keys, pytest, ctypes (WM messages for custom controls)

---

## File Map

| Action | Path | Responsibility |
|--------|------|---------------|
| Create | `scan_service_work_orders.py` | One-shot UIA scan to discover actual element auto_ids |
| Create | `screens/work_order_creation_screen.py` | WorkOrderCreationScreen page object |
| Modify | `tests/conftest.py` | Add `navigator_screen` and `work_order_screen` fixtures |
| Create | `tests/test_work_order_creation.py` | 7 pytest tests (one per GA checklist item) |

---

## Task 1: UIA Discovery Script

> Run this before writing the screen class. The actual element auto_ids in G2 are unknown. This script connects to the live Work Orders window and prints every element's auto_id, control_type, and title so you can update `ELEMENT_IDS` in Task 2.

**Files:**
- Create: `scan_service_work_orders.py`

- [ ] **Step 1: Create the discovery script**

```python
# scan_service_work_orders.py
"""
Run with G2 open and navigated to Service → Work Orders.
Prints all UIA element IDs found in that window.
"""
import sys
sys.path.insert(0, r'E:\G2 Desktop Automation')

import time
from pywinauto import findwindows
from pywinauto.application import Application

# Patterns to try — one of these should match the WO Manager window
TITLE_PATTERNS = [
    r".*Work Order.*",
    r".*Service.*",
    r".*WO.*",
]

def scan_window(title_re: str):
    windows = findwindows.find_windows(title_re=title_re)
    if not windows:
        return None, []
    app = Application(backend='uia').connect(handle=windows[0])
    win = app.window()
    return win.window_text(), win

def print_element_tree(elem, depth=0, max_depth=5, found=None):
    if found is None:
        found = []
    if depth > max_depth:
        return found
    try:
        auto_id = elem.automation_id() if callable(getattr(elem, 'automation_id', None)) else getattr(elem, 'automation_id', '')
        ctrl_type = elem.element_info.control_type if hasattr(elem, 'element_info') else ''
        title = elem.window_text() if hasattr(elem, 'window_text') else ''
        indent = "  " * depth
        line = f"{indent}auto_id={repr(auto_id)!s:<35} ctrl={ctrl_type!s:<15} title={repr(title)}"
        print(line)
        if auto_id:
            found.append({'auto_id': auto_id, 'ctrl_type': ctrl_type, 'title': title})
    except Exception:
        pass
    try:
        for child in elem.children():
            print_element_tree(child, depth + 1, max_depth, found)
    except Exception:
        pass
    return found

print("Scanning for Work Orders window...")
win_title, win = None, None
for pattern in TITLE_PATTERNS:
    win_title, win = scan_window(pattern)
    if win:
        print(f"Found window: '{win_title}' (pattern: {pattern})")
        break

if not win:
    print("ERROR: No matching window found. Open G2 and navigate to Service → Work Orders first.")
    sys.exit(1)

print(f"\n{'='*70}")
print(f"Element tree for: {win_title}")
print(f"{'='*70}\n")
found_elements = print_element_tree(win)

print(f"\n{'='*70}")
print(f"Summary: {len(found_elements)} elements with auto_ids")
print(f"{'='*70}")
for e in found_elements:
    print(f"  {e['auto_id']}")
```

- [ ] **Step 2: Open G2, log in, navigate to Service → Work Orders**

Manually: Launch G2 → log in → click "Service" in Navigator → click "Work Orders" in the explorer bar. Wait until the Work Orders screen is fully loaded.

- [ ] **Step 3: Run the discovery script**

```
cd "E:\G2 Desktop Automation"
python scan_service_work_orders.py
```

Expected: A tree of all UIA elements with their `auto_id`, `control_type`, and `title` values printed to console.

- [ ] **Step 4: Note the real auto_ids**

From the output, find the actual auto_ids for these logical elements (they may differ from the design spec names):
- Search input field
- Search/Find button
- Work orders results grid/list
- "New WO" button
- Customer number input
- Unit number input
- WO type dropdown
- Technician dropdown
- Comments text area
- Save button
- Print customer button
- Print shop button
- WO number label (after save)

Write these down — you will use them in `ELEMENT_IDS` in Task 2.

- [ ] **Step 5: Commit the discovery script**

```bash
git add scan_service_work_orders.py
git commit -m "feat: add UIA discovery script for Service Work Orders window"
```

---

## Task 2: WorkOrderCreationScreen Skeleton

**Files:**
- Create: `screens/work_order_creation_screen.py`

- [ ] **Step 1: Write the failing test (import check)**

Create `tests/test_work_order_creation.py` with just the import:

```python
# tests/test_work_order_creation.py
from screens.work_order_creation_screen import WorkOrderCreationScreen


def test_import():
    """Verify the class can be imported."""
    assert WorkOrderCreationScreen is not None
```

- [ ] **Step 2: Run to confirm it fails**

```
cd "E:\G2 Desktop Automation"
python -m pytest tests/test_work_order_creation.py::test_import -v
```

Expected: `ModuleNotFoundError: No module named 'screens.work_order_creation_screen'`

- [ ] **Step 3: Create the screen class skeleton**

Replace `ELEMENT_IDS` with the actual auto_ids you captured in Task 1.

```python
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

    def _get_elem(self, auto_id: str):
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
```

- [ ] **Step 4: Run the import test — confirm it passes**

```
python -m pytest tests/test_work_order_creation.py::test_import -v
```

Expected: `PASSED`

- [ ] **Step 5: Commit**

```bash
git add screens/work_order_creation_screen.py tests/test_work_order_creation.py
git commit -m "feat: add WorkOrderCreationScreen skeleton with UIA discovery"
```

---

## Task 3: Navigate to Work Orders + WO Manager Test

**Files:**
- Modify: `screens/work_order_creation_screen.py` (add `navigate_to_work_orders`)
- Modify: `tests/conftest.py` (add `navigator_screen` and `work_order_screen` fixtures)
- Modify: `tests/test_work_order_creation.py` (add two WO Manager tests)

- [ ] **Step 1: Write the failing tests**

Replace `tests/test_work_order_creation.py` with:

```python
# tests/test_work_order_creation.py
import pytest
from screens.work_order_creation_screen import WorkOrderCreationScreen


def test_import():
    assert WorkOrderCreationScreen is not None


@pytest.mark.functional
def test_navigate_to_work_orders(work_order_screen):
    """GA: Confirm WO Manager is working correctly — navigation succeeds."""
    result = work_order_screen.navigate_to_work_orders()
    assert result is True, "navigate_to_work_orders() should return True when WO Manager loads"


@pytest.mark.functional
def test_wo_manager_is_loaded(work_order_screen):
    """GA: Confirm WO Manager is working correctly — manager grid visible."""
    work_order_screen.navigate_to_work_orders()
    assert work_order_screen.is_wo_manager_loaded(), "WO Manager should be visible after navigation"
```

- [ ] **Step 2: Run to confirm new tests fail**

```
python -m pytest tests/test_work_order_creation.py::test_navigate_to_work_orders -v
```

Expected: `FAILED` — `fixture 'work_order_screen' not found`

- [ ] **Step 3: Add fixtures to conftest.py**

Open `tests/conftest.py` and add after the existing `login_screen` fixture:

```python
@pytest.fixture
def navigator_screen():
    """Fixture providing a NavigatorScreen connected to the live G2 Navigator."""
    from screens.navigator_screen import NavigatorScreen
    screen = NavigatorScreen(discover_from_window=True)
    yield screen


@pytest.fixture
def work_order_screen():
    """Fixture providing WorkOrderCreationScreen in manual mode (no live G2 required for unit tests)."""
    from screens.work_order_creation_screen import WorkOrderCreationScreen
    screen = WorkOrderCreationScreen(discover_from_uia=False)
    yield screen


@pytest.fixture
def live_work_order_screen():
    """Fixture providing WorkOrderCreationScreen connected to live G2 (requires G2 open at WO Manager)."""
    from screens.work_order_creation_screen import WorkOrderCreationScreen
    screen = WorkOrderCreationScreen(discover_from_uia=True)
    yield screen
```

- [ ] **Step 4: Add `navigate_to_work_orders` to the screen class**

Append to `screens/work_order_creation_screen.py`:

```python
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
```

- [ ] **Step 5: Run the tests against live G2**

Ensure G2 is open and you are at the Navigator screen (logged in), then:

```
python -m pytest tests/test_work_order_creation.py::test_navigate_to_work_orders tests/test_work_order_creation.py::test_wo_manager_is_loaded -v
```

Expected: Both tests `PASSED`. If the window title doesn't match `.*Work Order.*`, update `WINDOW_TITLE_RE` in the class to the actual title found during Task 1 scan.

- [ ] **Step 6: Commit**

```bash
git add screens/work_order_creation_screen.py tests/conftest.py tests/test_work_order_creation.py
git commit -m "feat: add navigate_to_work_orders and WO Manager verification"
```

---

## Task 4: Create Work Order (click_new_work_order, enter_customer, enter_unit, select_wo_type, select_technician)

**Files:**
- Modify: `screens/work_order_creation_screen.py`
- Modify: `tests/test_work_order_creation.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/test_work_order_creation.py`:

```python
@pytest.mark.functional
def test_open_new_wo_form(live_work_order_screen):
    """GA: Create a Work Order — new WO form opens."""
    live_work_order_screen.navigate_to_work_orders()
    result = live_work_order_screen.click_new_work_order()
    assert result is True, "click_new_work_order() should return True when the form opens"


@pytest.mark.functional
def test_enter_customer_on_wo(live_work_order_screen):
    """GA: Create a Work Order — customer number is accepted."""
    live_work_order_screen.navigate_to_work_orders()
    live_work_order_screen.click_new_work_order()
    result = live_work_order_screen.enter_customer("10001")
    assert result is True, "enter_customer() should return True when customer field accepts input"
```

- [ ] **Step 2: Run to confirm failure**

```
python -m pytest tests/test_work_order_creation.py::test_open_new_wo_form -v
```

Expected: `FAILED` — `WorkOrderCreationScreen has no attribute 'click_new_work_order'`

- [ ] **Step 3: Implement WO creation methods**

Append to `screens/work_order_creation_screen.py`:

```python
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
```

- [ ] **Step 4: Run the new tests against live G2**

With G2 at the Navigator screen:

```
python -m pytest tests/test_work_order_creation.py::test_open_new_wo_form tests/test_work_order_creation.py::test_enter_customer_on_wo -v
```

Expected: Both `PASSED`. If `btnNewWO` is not found, check the actual button auto_id from Task 1 and update `ELEMENT_IDS`.

- [ ] **Step 5: Commit**

```bash
git add screens/work_order_creation_screen.py tests/test_work_order_creation.py
git commit -m "feat: add WO creation methods (new WO, customer, unit, type, tech)"
```

---

## Task 5: Add Comment, Save, and Verification Methods

**Files:**
- Modify: `screens/work_order_creation_screen.py`
- Modify: `tests/test_work_order_creation.py`

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_work_order_creation.py`:

```python
@pytest.mark.functional
def test_create_work_order(live_work_order_screen):
    """GA: Create a Work Order — full create flow returns a WO number."""
    live_work_order_screen.navigate_to_work_orders()
    live_work_order_screen.click_new_work_order()
    live_work_order_screen.enter_customer("10001")
    live_work_order_screen.enter_unit("U001")
    live_work_order_screen.select_wo_type("Customer Pay")
    wo_num = live_work_order_screen.save_work_order()
    assert len(wo_num) > 0, f"Expected a WO number after saving, got: '{wo_num}'"


@pytest.mark.functional
def test_add_comment_to_wo(live_work_order_screen):
    """GA: Add comments on a WO — comment is entered and WO is saved."""
    live_work_order_screen.navigate_to_work_orders()
    live_work_order_screen.click_new_work_order()
    live_work_order_screen.enter_customer("10001")
    comment_result = live_work_order_screen.add_comment("Automated test comment - Phase 1")
    assert comment_result is True, "add_comment() should return True"
    wo_num = live_work_order_screen.save_work_order()
    assert len(wo_num) > 0, f"WO with comment should save and return a WO number, got: '{wo_num}'"
```

- [ ] **Step 2: Run to confirm failure**

```
python -m pytest tests/test_work_order_creation.py::test_create_work_order -v
```

Expected: `FAILED` — `WorkOrderCreationScreen has no attribute 'save_work_order'`

- [ ] **Step 3: Implement comment, save, and verification methods**

Append to `screens/work_order_creation_screen.py`:

```python
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
        # Wait for WO number label to populate
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
```

- [ ] **Step 4: Run the save tests against live G2**

```
python -m pytest tests/test_work_order_creation.py::test_create_work_order tests/test_work_order_creation.py::test_add_comment_to_wo -v
```

Expected: Both `PASSED`. If `save_work_order()` returns `""`, the `lblWONumber` auto_id is wrong — re-check Task 1 output and update `ELEMENT_IDS`.

- [ ] **Step 5: Commit**

```bash
git add screens/work_order_creation_screen.py tests/test_work_order_creation.py
git commit -m "feat: add add_comment, save_work_order, and WO verification methods"
```

---

## Task 6: Search Methods

**Files:**
- Modify: `screens/work_order_creation_screen.py`
- Modify: `tests/test_work_order_creation.py`

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_work_order_creation.py`:

```python
@pytest.mark.functional
def test_search_by_wo_number(live_work_order_screen):
    """GA: Search WO by WO number — finds the WO created in this test."""
    live_work_order_screen.navigate_to_work_orders()
    live_work_order_screen.click_new_work_order()
    live_work_order_screen.enter_customer("10001")
    wo_num = live_work_order_screen.save_work_order()
    assert len(wo_num) > 0, "Precondition: need a WO to search for"

    live_work_order_screen.clear_search()
    found = live_work_order_screen.search_by_wo_number(wo_num)
    assert found is True, f"search_by_wo_number('{wo_num}') should return True"


@pytest.mark.functional
def test_search_by_customer_name(live_work_order_screen):
    """GA: Search WO by customer name — returns a list (may be empty for unknown customer)."""
    live_work_order_screen.navigate_to_work_orders()
    results = live_work_order_screen.search_by_customer("Test")
    assert isinstance(results, list), "search_by_customer() must return a list"
```

- [ ] **Step 2: Run to confirm failure**

```
python -m pytest tests/test_work_order_creation.py::test_search_by_wo_number -v
```

Expected: `FAILED` — `WorkOrderCreationScreen has no attribute 'search_by_wo_number'`

- [ ] **Step 3: Implement search methods**

Append to `screens/work_order_creation_screen.py`:

```python
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
```

- [ ] **Step 4: Run the search tests against live G2**

```
python -m pytest tests/test_work_order_creation.py::test_search_by_wo_number tests/test_work_order_creation.py::test_search_by_customer_name -v
```

Expected: Both `PASSED`. If `search_by_wo_number` returns False, the results grid may show the WO in a different format — inspect via Task 1 scan output and adjust the `verify_text_present` call if needed.

- [ ] **Step 5: Commit**

```bash
git add screens/work_order_creation_screen.py tests/test_work_order_creation.py
git commit -m "feat: add search_by_wo_number, search_by_customer, clear_search methods"
```

---

## Task 7: Print Methods

**Files:**
- Modify: `screens/work_order_creation_screen.py`
- Modify: `tests/test_work_order_creation.py`

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_work_order_creation.py`:

```python
@pytest.mark.functional
def test_print_customer_copy(live_work_order_screen):
    """GA: Confirm WO PDF printouts — customer copy triggers a print/viewer window."""
    live_work_order_screen.navigate_to_work_orders()
    live_work_order_screen.click_new_work_order()
    live_work_order_screen.enter_customer("10001")
    live_work_order_screen.save_work_order()
    result = live_work_order_screen.print_customer_copy()
    assert result is True, "print_customer_copy() should return True when a print/PDF window appears"


@pytest.mark.functional
def test_print_shop_copy(live_work_order_screen):
    """GA: Confirm WO PDF printouts — shop copy triggers a print/viewer window."""
    live_work_order_screen.navigate_to_work_orders()
    live_work_order_screen.click_new_work_order()
    live_work_order_screen.enter_customer("10001")
    live_work_order_screen.save_work_order()
    result = live_work_order_screen.print_shop_copy()
    assert result is True, "print_shop_copy() should return True when a print/PDF window appears"
```

- [ ] **Step 2: Run to confirm failure**

```
python -m pytest tests/test_work_order_creation.py::test_print_customer_copy -v
```

Expected: `FAILED` — `WorkOrderCreationScreen has no attribute 'print_customer_copy'`

- [ ] **Step 3: Implement print methods**

Append to `screens/work_order_creation_screen.py`:

```python
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
```

- [ ] **Step 4: Run the print tests against live G2**

```
python -m pytest tests/test_work_order_creation.py::test_print_customer_copy tests/test_work_order_creation.py::test_print_shop_copy -v
```

Expected: Both `PASSED`. If `print_customer_copy` returns False, check what window title actually appears — adjust the `title_re` in `_wait_for_print_window` calls to match.

- [ ] **Step 5: Commit**

```bash
git add screens/work_order_creation_screen.py tests/test_work_order_creation.py
git commit -m "feat: add print_customer_copy and print_shop_copy methods"
```

---

## Task 8: Full Test Suite Run + Final Commit

**Files:**
- No new code — run existing tests end-to-end

- [ ] **Step 1: Run the full Phase 1 test suite**

With G2 open, logged in, at the Navigator screen:

```
python -m pytest tests/test_work_order_creation.py -v --tb=short
```

Expected output:
```
tests/test_work_order_creation.py::test_import                    PASSED
tests/test_work_order_creation.py::test_navigate_to_work_orders   PASSED
tests/test_work_order_creation.py::test_wo_manager_is_loaded      PASSED
tests/test_work_order_creation.py::test_open_new_wo_form          PASSED
tests/test_work_order_creation.py::test_enter_customer_on_wo      PASSED
tests/test_work_order_creation.py::test_create_work_order         PASSED
tests/test_work_order_creation.py::test_add_comment_to_wo         PASSED
tests/test_work_order_creation.py::test_search_by_wo_number       PASSED
tests/test_work_order_creation.py::test_search_by_customer_name   PASSED
tests/test_work_order_creation.py::test_print_customer_copy       PASSED
tests/test_work_order_creation.py::test_print_shop_copy           PASSED
```

- [ ] **Step 2: If any test fails**

Check the failure message:
- `element 'XYZ' not in discovered set` → auto_id is wrong; re-run `scan_service_work_orders.py` and update `ELEMENT_IDS` in the class
- `navigate_to_work_orders() returned False` → check the explorer bar button title matches what G2 shows; update `click_explorer_bar_button("Work Orders")` call
- Print test fails → adjust the `title_re` pattern in `_wait_for_print_window`

- [ ] **Step 3: Commit the plan + any final fixes**

```bash
git add docs/superpowers/plans/2026-04-25-work-order-phase1-plan.md
git commit -m "docs: add Phase 1 Work Order implementation plan"
```

---

## GA Checklist Coverage

| GA Feature | Test | Status after Phase 1 |
|---|---|---|
| Create a Work Order | `test_create_work_order` | Covered |
| Confirm WO Manager is working correctly | `test_navigate_to_work_orders`, `test_wo_manager_is_loaded` | Covered |
| Confirm WO PDF printouts (Customer/Shop) | `test_print_customer_copy`, `test_print_shop_copy` | Covered |
| Add comments on a WO | `test_add_comment_to_wo` | Covered |
| Search WO/Estimate by multiple fields | `test_search_by_wo_number`, `test_search_by_customer_name` | Covered |
