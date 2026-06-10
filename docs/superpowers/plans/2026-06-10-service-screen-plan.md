# ServiceScreen Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create `ServiceScreen` — a page-object hub that clicks the Service menu button, auto-discovers the explorer bar buttons, and exposes `go_to(section)` + named shortcuts for navigating to Work Orders, Appointments, etc.

**Architecture:** `ServiceScreen(BaseScreen)` sits between `NavigatorScreen` and module screens. On init it calls `NavigatorScreen.click_menu_button("Service")`, polls the Navigator window for explorer bar buttons (up to 3 s), and caches their titles. All navigation delegates back to `NavigatorScreen.click_explorer_bar_button()`. Existing files are untouched except `conftest.py` (two new fixtures added).

**Tech Stack:** Python 3, pywinauto (UIA backend), pytest, ctypes — same as the rest of the framework.

---

## File Map

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `screens/service_screen.py` | `ServiceScreen` page object |
| Create | `tests/test_service_navigation.py` | Unit + functional tests |
| Modify | `tests/conftest.py` | Add `ensure_g2_running`, `service_screen`, `service_screen_unit` fixtures |

---

## Task 1: Write all tests + create `ServiceScreen` skeleton

Get to TDD "red then green" for unit tests. Functional tests will remain red until Tasks 2–3.

**Files:**
- Create: `tests/test_service_navigation.py`
- Create: `screens/service_screen.py`
- Modify: `tests/conftest.py`

---

- [ ] **Step 1.1 — Create the full test file (all tests, all failing)**

Create `tests/test_service_navigation.py`:

```python
# tests/test_service_navigation.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import time
import ctypes
import pytest
from pywinauto import findwindows
from pywinauto.keyboard import send_keys

G2_EXE = r"C:\IDSASTRA\APPS\G2\G2CLIENT\IdsG2Client.exe"
G2_USERNAME = "aqadir.ids"
G2_PASSWORD = "Aqadir2801"
NAV_PATTERN = r".*Navigator.*"


def _navigator_open():
    return bool(findwindows.find_windows(title_re=NAV_PATTERN))


@pytest.fixture(scope="session", autouse=True)
def ensure_g2_running():
    """Launch G2 and log in if the Navigator is not already open."""
    if _navigator_open():
        print("\n  G2 Navigator already open — skipping launch/login")
        return

    if not findwindows.find_windows(title="G2 Login"):
        print("\n  Launching G2...")
        result = ctypes.windll.shell32.ShellExecuteW(
            None, "open", G2_EXE, None, os.path.dirname(G2_EXE), 1
        )
        if result <= 32:
            pytest.fail(f"ShellExecute failed (code {result}) — cannot launch G2")

    login_hwnd = None
    for i in range(30):
        handles = findwindows.find_windows(title="G2 Login")
        if handles:
            login_hwnd = handles[0]
            print(f"\n  G2 Login window found after {i}s")
            break
        time.sleep(1)
    if not login_hwnd:
        pytest.fail("G2 Login window did not appear after 30s")

    ctypes.windll.user32.ShowWindow(login_hwnd, 9)
    ctypes.windll.user32.SetForegroundWindow(login_hwnd)
    time.sleep(0.5)

    try:
        ctypes.windll.user32.SetForegroundWindow(login_hwnd)
        time.sleep(0.5)
        send_keys(f'{G2_USERNAME}{{TAB}}{G2_PASSWORD}{{ENTER}}')
        print("  Credentials submitted — waiting for Navigator...")
    except Exception as e:
        pytest.fail(f"Could not submit login credentials: {e}")

    for i in range(60):
        if _navigator_open():
            print(f"  Navigator appeared after {i}s")
            return
        time.sleep(1)
    pytest.fail("G2 Navigator did not appear within 60s after login")


# ---------------------------------------------------------------------------
# Unit tests — no live G2 required (auto_navigate=False)
# ---------------------------------------------------------------------------

def test_service_screen_import(service_screen_unit):
    from screens.service_screen import ServiceScreen
    assert ServiceScreen is not None


def test_service_screen_attributes(service_screen_unit):
    assert isinstance(service_screen_unit._discovered_buttons, list)


# ---------------------------------------------------------------------------
# Functional tests — require live G2 (use service_screen fixture)
# ---------------------------------------------------------------------------

@pytest.mark.functional
def test_navigate_to_service(service_screen):
    assert service_screen is not None


@pytest.mark.functional
def test_discover_explorer_buttons(service_screen):
    sections = service_screen.get_available_sections()
    assert len(sections) >= 1, f"Expected at least 1 explorer button, got: {sections}"


@pytest.mark.functional
def test_go_to_work_orders(service_screen):
    result = service_screen.go_to_work_orders()
    assert result is True, "go_to_work_orders() should return True"


@pytest.mark.functional
def test_go_to_invalid_section(service_screen):
    result = service_screen.go_to("__invalid_section__")
    assert result is False, "go_to() with unknown section should return False"


@pytest.mark.functional
def test_get_available_sections(service_screen):
    sections = service_screen.get_available_sections()
    assert isinstance(sections, list)
    assert len(sections) > 0, "get_available_sections() must return a non-empty list"


@pytest.mark.functional
def test_rediscover(service_screen):
    result = service_screen.rediscover()
    assert result is True, "rediscover() should return True when ≥1 button found"
```

---

- [ ] **Step 1.2 — Run tests to confirm import error (expected red)**

```
cd "E:\G2 Desktop Automation"
pytest tests/test_service_navigation.py -v 2>&1 | head -20
```

Expected: `ImportError: cannot import name 'ServiceScreen'` or `ModuleNotFoundError`.

---

- [ ] **Step 1.3 — Create `screens/service_screen.py` skeleton**

Create `screens/service_screen.py`:

```python
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
```

---

- [ ] **Step 1.4 — Add fixtures to `tests/conftest.py`**

Open `tests/conftest.py`. Add these three fixtures after the existing `open_g2_application` fixture:

```python
@pytest.fixture(scope="session")
def service_screen():
    """Session fixture — clicks Service and returns a ready ServiceScreen.
    Requires G2 to be running; the autouse ensure_g2_running fixture in
    test_service_navigation.py guarantees this before any test in that file."""
    from screens.service_screen import ServiceScreen
    screen = ServiceScreen(auto_navigate=True)
    yield screen


@pytest.fixture
def service_screen_unit():
    """Unit-test fixture — no live G2 required."""
    from screens.service_screen import ServiceScreen
    screen = ServiceScreen(auto_navigate=False)
    yield screen
```

Note: `service_screen` has no explicit `ensure_g2_running` dependency because conftest.py fixtures cannot depend on fixtures defined in individual test files. The `autouse=True` `ensure_g2_running` in `test_service_navigation.py` is session-scoped and fires before any test in that file, so G2 is guaranteed to be running by the time `service_screen` is first requested. Existing test files are unaffected.

---

- [ ] **Step 1.5 — Run unit tests to confirm green**

```
cd "E:\G2 Desktop Automation"
pytest tests/test_service_navigation.py::test_service_screen_import tests/test_service_navigation.py::test_service_screen_attributes -v
```

Expected output:
```
PASSED tests/test_service_navigation.py::test_service_screen_import
PASSED tests/test_service_navigation.py::test_service_screen_attributes
2 passed
```

---

- [ ] **Step 1.6 — Commit**

```
git add screens/service_screen.py tests/test_service_navigation.py tests/conftest.py
git commit -m "feat: scaffold ServiceScreen skeleton + unit tests + conftest fixtures"
```

---

## Task 2: Implement `_navigate_and_discover` + `_discover_explorer_buttons` + `rediscover`

**Files:**
- Modify: `screens/service_screen.py`

---

- [ ] **Step 2.1 — Run the two discovery functional tests to confirm red**

```
cd "E:\G2 Desktop Automation"
pytest tests/test_service_navigation.py::test_navigate_to_service tests/test_service_navigation.py::test_discover_explorer_buttons -v
```

Expected: both FAIL with `NotImplementedError`.

---

- [ ] **Step 2.2 — Replace the three stub methods with full implementations**

In `screens/service_screen.py`, replace the three `raise NotImplementedError` stubs with:

```python
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
    Polls up to 3 s (6 × 0.5 s) for the panel to render after navigation.
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

def rediscover(self) -> bool:
    """Re-scan the Service panel explorer bar. Returns True if ≥1 button found."""
    return self._discover_explorer_buttons()
```

---

- [ ] **Step 2.3 — Run discovery tests to confirm green**

```
cd "E:\G2 Desktop Automation"
pytest tests/test_service_navigation.py::test_navigate_to_service tests/test_service_navigation.py::test_discover_explorer_buttons tests/test_service_navigation.py::test_rediscover -v
```

Expected: all three PASS. (Requires live G2 open.)

---

- [ ] **Step 2.4 — Commit**

```
git add screens/service_screen.py
git commit -m "feat: implement ServiceScreen discovery — click Service + scan explorer bar"
```

---

## Task 3: Implement `go_to()` + introspection methods

**Files:**
- Modify: `screens/service_screen.py`

---

- [ ] **Step 3.1 — Run remaining functional tests to confirm red**

```
cd "E:\G2 Desktop Automation"
pytest tests/test_service_navigation.py::test_go_to_work_orders tests/test_service_navigation.py::test_go_to_invalid_section tests/test_service_navigation.py::test_get_available_sections -v
```

Expected: all FAIL with `NotImplementedError`.

---

- [ ] **Step 3.2 — Replace the three stub methods with full implementations**

In `screens/service_screen.py`, replace the three remaining `raise NotImplementedError` stubs:

```python
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
    if section_name not in self._discovered_buttons:
        print(
            f"[!] ServiceScreen: '{section_name}' not in discovered buttons "
            f"{self._discovered_buttons} — attempting anyway"
        )
    return self._navigator.click_explorer_bar_button(section_name)

def get_available_sections(self) -> list:
    """Return a copy of the discovered explorer bar button titles."""
    return list(self._discovered_buttons)

def is_section_available(self, name: str) -> bool:
    """Case-insensitive check whether a section was found during discovery."""
    name_lower = name.lower()
    return any(b.lower() == name_lower for b in self._discovered_buttons)
```

---

- [ ] **Step 3.3 — Run all tests (unit + functional)**

```
cd "E:\G2 Desktop Automation"
pytest tests/test_service_navigation.py -v
```

Expected:
```
PASSED test_service_screen_import
PASSED test_service_screen_attributes
PASSED test_navigate_to_service
PASSED test_discover_explorer_buttons
PASSED test_go_to_work_orders
PASSED test_go_to_invalid_section
PASSED test_get_available_sections
PASSED test_rediscover
8 passed
```

---

- [ ] **Step 3.4 — Commit**

```
git add screens/service_screen.py
git commit -m "feat: implement ServiceScreen go_to() and introspection methods"
```

---

## Task 4: Validate no regressions in existing tests

**Files:** None modified.

---

- [ ] **Step 4.1 — Run the full test suite**

```
cd "E:\G2 Desktop Automation"
pytest tests/ -v --tb=short 2>&1 | tail -30
```

Expected: all existing tests in `test_work_order_creation.py`, `test_login_screen.py`, `test_navigator_buttons.py`, etc. still PASS. The new `test_service_navigation.py` tests PASS.

---

- [ ] **Step 4.2 — Run work order tests to confirm ServiceScreen didn't break navigation**

```
cd "E:\G2 Desktop Automation"
pytest tests/test_work_order_creation.py -v -m functional
```

Expected: all functional work order tests PASS (they use `NavigatorScreen` directly, not `ServiceScreen` — no change).

---

- [ ] **Step 4.3 — Final commit**

```
git add .
git commit -m "feat: ServiceScreen complete — navigation hub for G2 Service module

Implements ServiceScreen page object:
- Clicks btnService on Navigator, auto-discovers explorer bar buttons
- go_to(section) + named shortcuts (work_orders, appointments, etc.)
- get_available_sections(), is_section_available(), rediscover()
- service_screen and service_screen_unit conftest fixtures
- 8 tests (2 unit, 6 functional) all passing"
```
