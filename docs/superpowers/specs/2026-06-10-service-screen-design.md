# ServiceScreen — Design Spec

**Date:** 2026-06-10
**Scope:** New `ServiceScreen` page object — navigation hub for the G2 Service module
**Phase context:** Additive layer between `NavigatorScreen` and module screens (Work Orders, Appointments, etc.)

---

## Overview

`ServiceScreen` sits between `NavigatorScreen` and module-specific screen classes
(`WorkOrderCreationScreen`, future `AppointmentsScreen`, etc.). Its single
responsibility is to click the **Service** menu button on the G2 Navigator, wait for
the Service panel's explorer bar to render, and expose navigation methods into each
Service sub-section.

It does **not** launch or log into G2 — that remains the responsibility of
`ensure_g2_running` in each test file. It does **not** return downstream screen
instances — callers instantiate those themselves.

---

## Architecture

### New files

```
screens/service_screen.py          ← ServiceScreen page object
tests/test_service_navigation.py   ← smoke tests for ServiceScreen
```

### Modified files

```
tests/conftest.py    ← two new fixtures: service_screen, service_screen_unit
```

### Unchanged files

`screens/work_order_creation_screen.py` and all existing tests are **not modified**.
`ServiceScreen` is purely additive.

### Navigation path

```
ensure_g2_running (session fixture)
  → ServiceScreen.__init__
      → NavigatorScreen.click_menu_button("Service")   # clicks btnService
      → ServiceScreen._discover_explorer_buttons()     # scans Service panel
  → test calls service_screen.go_to_work_orders()
      → NavigatorScreen.click_explorer_bar_button("Work Orders")
```

---

## Class: `ServiceScreen`

**File:** `screens/service_screen.py`
**Base:** `BaseScreen`

### Constructor

```python
def __init__(self, navigator: NavigatorScreen = None, auto_navigate: bool = True):
```

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `navigator` | `None` | Accepts an existing connected `NavigatorScreen`. Creates one internally if `None`. |
| `auto_navigate` | `True` | When `True`, clicks `btnService` and runs discovery on init. Set `False` for unit tests. |

**Internal state:**

| Attribute | Type | Purpose |
|-----------|------|---------|
| `_navigator` | `NavigatorScreen` | Navigator instance used for all clicks |
| `_discovered_buttons` | `list[str]` | Explorer bar button titles found after Service click |
| `_nav_hwnd` | `int` | Navigator HWND used by the explorer bar scanner |

---

## Discovery Logic

Runs automatically when `auto_navigate=True`. Steps:

1. **Click Service** — `self._navigator.click_menu_button("Service")`.  
   `click_menu_button` already handles the WM_LBUTTONDOWN/UP + UIA fallback pattern for the `btnService` button (`auto_id="btnService"`, inside `grpService` → `pnlButtons` → `MainForm`).

2. **Poll for panel render** — up to 3 seconds (6 × 0.5 s). Uses  
   `Desktop(backend='uia').window(handle=nav_hwnd)` and scans for `Button`  
   descendants — same UIA approach as `NavigatorScreen.click_explorer_bar_button()`.

3. **Scan and cache** — collects all `Button` control titles found in the Service  
   explorer area, filters out blank titles, stores in `_discovered_buttons`.  
   Prints `[OK] Service panel found N buttons: [...]`.

4. **Failure path** — if no buttons found after 3 s, logs a warning and continues.  
   `go_to()` calls on an empty `_discovered_buttons` still attempt the click (the  
   button may exist even if discovery missed it) and return `False` if the click  
   fails. No exception is raised.

**`rediscover() -> bool`** — public method that re-runs steps 2–3. Returns `True`
if at least one button was found.

---

## Public API

### Generic navigation

```python
def go_to(self, section_name: str) -> bool
```

Delegates to `self._navigator.click_explorer_bar_button(section_name)`.  
Logs a warning if `section_name` is not in `_discovered_buttons` but still
attempts the click.

### Named shortcuts

Thin one-liner wrappers over `go_to()`. Each maps to a Phase 1–4 roadmap item:

```python
def go_to_work_orders(self)       -> bool: return self.go_to("Work Orders")
def go_to_appointments(self)      -> bool: return self.go_to("Appointments")
def go_to_labor_scheduler(self)   -> bool: return self.go_to("Labor Scheduler")
def go_to_flat_rate_manager(self) -> bool: return self.go_to("Flat Rate Manager")
def go_to_doc_manager(self)       -> bool: return self.go_to("Doc Manager")
```

New shortcuts are added as new phases are built — each is a one-liner.

### Introspection

```python
def get_available_sections(self) -> list[str]      # copy of _discovered_buttons
def is_section_available(self, name: str) -> bool  # case-insensitive membership check
def rediscover(self) -> bool                       # re-runs discovery, returns True if ≥1 found
```

---

## Fixtures (`tests/conftest.py`)

### `service_screen` (session-scoped)

```python
@pytest.fixture(scope="session")
def service_screen(ensure_g2_running):
    from screens.service_screen import ServiceScreen
    screen = ServiceScreen(auto_navigate=True)
    yield screen
```

Declares `ensure_g2_running` as a dependency — pytest guarantees G2 is open before
`ServiceScreen` initialises. Mirrors the `live_work_order_screen` fixture pattern.

### `service_screen_unit` (function-scoped)

```python
@pytest.fixture
def service_screen_unit():
    from screens.service_screen import ServiceScreen
    screen = ServiceScreen(auto_navigate=False)
    yield screen
```

No live G2 required — for unit tests only.

---

## Test File: `tests/test_service_navigation.py`

Uses the same `ensure_g2_running` session fixture as `test_work_order_creation.py`
(copy of the G2_EXE / credential block). All functional tests use `@pytest.mark.functional`.

| Test | Type | Assertion |
|------|------|-----------|
| `test_service_screen_import` | unit | `ServiceScreen` importable |
| `test_service_screen_attributes` | unit | `_discovered_buttons` is a list |
| `test_navigate_to_service` | functional | `auto_navigate=True` does not raise |
| `test_discover_explorer_buttons` | functional | `get_available_sections()` returns ≥ 1 item |
| `test_go_to_work_orders` | functional | `go_to_work_orders()` returns `True` |
| `test_go_to_invalid_section` | functional | `go_to("__invalid__")` returns `False`, no exception |
| `test_get_available_sections` | functional | returns a non-empty list |
| `test_rediscover` | functional | `rediscover()` returns `True` |

---

## Error Handling

Mirrors the existing framework conventions:

- Element lookup timeouts use polling loops (max 3 s), not hard `time.sleep()` blocks
- All failures print `[X]` or `[!]` prefixed messages and return `False` — no exceptions propagate to callers
- Screenshots on failure are handled by the existing `ScreenshotManager` (BaseScreen default)

---

## Out of Scope

- Launching or logging into G2 (owned by `ensure_g2_running`)
- Returning downstream screen instances from `go_to_*` methods
- Modifying `WorkOrderCreationScreen` or any existing tests
- Implementing the sub-screens themselves (Appointments, Labor Scheduler, etc.) — those are future phase work
