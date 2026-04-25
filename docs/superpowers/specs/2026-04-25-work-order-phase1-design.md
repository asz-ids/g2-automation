# Work Order Automation — Phase 1 Design

**Date:** 2026-04-25  
**Scope:** Phase 1 of 4 — Work Order Creation & Search  
**Source:** [GA Comprehensive Testing Doc](https://ids-cloud.atlassian.net/wiki/spaces/QA/pages/2252668929)

---

## Overview

This spec covers Phase 1 of automating the G2 Service → Work Orders module. The goal is to produce a `WorkOrderCreationScreen` class that enables automated QA regression tests for the GA checklist items listed below, following the same Page Object Model pattern used by `LoginScreen` and `NavigatorScreen`.

**GA checklist items covered by Phase 1:**
- Create a Work Order (WO)
- Confirm WO Manager is working correctly
- Confirm WO PDF printouts (Customer/Shop)
- Add comments on a WO
- Search WO/Estimate by multiple fields

---

## Phasing (full picture)

| Phase | Screen Class | GA Features |
|-------|-------------|-------------|
| **1 (this spec)** | `WorkOrderCreationScreen` | Create WO, WO Manager, search, comments, PDF print |
| 2 | `WorkOrderLineItemsScreen` | Add/modify/remove Parts, Labor, Sublet, Extras; Canned Jobs; Flat Rate |
| 3 | `WorkOrderPaymentScreen` | Take payment, IDSPAY, transfer jobs |
| 4 | `WorkOrderSchedulerScreen` | Appointments, drag/drop mechanic, clock in/out, Doc Manager, Flat Rate Manager |

---

## Architecture

### Navigation Path

```
Login
  → NavigatorScreen.click_menu("Service")
  → NavigatorScreen.click_explorer_bar_button("Work Orders")
  → WorkOrderCreationScreen
```

### New Files

```
screens/work_order_creation_screen.py   ← screen object
tests/test_work_order_creation.py       ← pytest regression tests
```

### Class Structure

```python
class WorkOrderCreationScreen(BaseScreen):
    def __init__(self, discover_from_uia: bool = True):
        super().__init__("WorkOrderCreationScreen")
        if discover_from_uia:
            self._discover_from_live_uia()
        else:
            self._setup_elements_manual()
```

Follows the same dual-mode init as `LoginScreen`: live UIA discovery for real runs, manual fallback for offline/unit testing.

---

## Elements & Locators

Actual `auto_id` values will be confirmed via a live UIA scan of the Service → Work Orders window during implementation (same approach as `g2_diagnostic.py` and the existing scan scripts). The names below are the expected identifiers based on G2 WinForms naming conventions.

| Element Name | Control Type | Expected auto_id | Purpose |
|---|---|---|---|
| `txtWOSearch` | Edit | `txtWOSearch` | WO number / customer search input |
| `btnSearch` | Button | `btnSearch` | Triggers WO search |
| `lstWorkOrders` | List | `lstWorkOrders` | Search results grid |
| `btnNewWO` | Button | `btnNewWO` | Opens blank WO form |
| `txtCustomerNumber` | Edit | `txtCustomerNumber` | Customer lookup field |
| `txtUnitNumber` | Edit | `txtUnitNumber` | Unit/stock number field |
| `cmbWOType` | ComboBox | `cmbWOType` | WO type selector (Customer Pay, Warranty, Internal) |
| `cmbTechnician` | ComboBox | `cmbTechnician` | Assigned technician selector |
| `dteDateOpened` | Pane | `dteDateOpened` | Date opened (defaults to today) |
| `txtComments` | Edit | `txtComments` | WO comments field |
| `btnSaveWO` | Button | `btnSaveWO` | Saves the WO |
| `btnPrintCustomer` | Button | `btnPrintCustomer` | Prints customer copy PDF |
| `btnPrintShop` | Button | `btnPrintShop` | Prints shop copy PDF |
| `lblWONumber` | Text | `lblWONumber` | Displays assigned WO# after save |

**Locator strategy priority:** `auto_id` first → `control_type + title` fallback → `class_name` last resort. Custom controls use `WM_LBUTTONDOWN/UP` messages (same pattern as `NavigatorScreen`).

---

## Methods

### Navigation & State

```python
def navigate_to_work_orders() -> bool
    # Clicks Service menu then Work Orders in the explorer bar
    # Returns True when WO Manager grid is confirmed visible

def is_wo_manager_loaded() -> bool
    # Verifies the WO Manager results grid is present on screen
```

### Creating a Work Order

```python
def click_new_work_order()
    # Opens blank WO form via btnNewWO

def enter_customer(number: str)
    # Types customer number into txtCustomerNumber
    # Waits for customer lookup/autocomplete to resolve

def enter_unit(number: str)
    # Types unit/stock number into txtUnitNumber

def select_wo_type(type_name: str)
    # Selects from cmbWOType dropdown (e.g. "Customer Pay", "Warranty", "Internal")

def select_technician(name: str)
    # Selects technician from cmbTechnician dropdown

def add_comment(text: str)
    # Types into txtComments field

def save_work_order() -> str
    # Clicks btnSaveWO, waits for lblWONumber to populate
    # Returns the assigned WO number string
```

### Search

```python
def search_by_wo_number(wo_num: str) -> bool
    # Types WO number into txtWOSearch, clicks btnSearch
    # Returns True if exactly one result appears in lstWorkOrders

def search_by_customer(name: str) -> list[str]
    # Searches by customer name, returns list of matching WO numbers

def clear_search()
    # Clears the search field and resets the results grid
```

### Print

```python
def print_customer_copy()
    # Clicks btnPrintCustomer, waits for print dialog or PDF viewer

def print_shop_copy()
    # Clicks btnPrintShop, waits for print dialog or PDF viewer
```

### Verification

```python
def get_current_wo_number() -> str
    # Reads text from lblWONumber

def is_wo_saved_successfully() -> bool
    # Returns True if lblWONumber is non-empty after save

def get_wo_status() -> str
    # Returns current WO status text (Open, Closed, etc.)
```

---

## Test Plan (`tests/test_work_order_creation.py`)

One test per GA checklist row. All tests share a session-scoped `logged_in_navigator` fixture that handles login and navigates to the Navigator screen.

| Test | GA Feature |
|------|-----------|
| `test_create_work_order` | Create a Work Order |
| `test_wo_manager_loads` | Confirm WO Manager is working correctly |
| `test_search_by_wo_number` | Search WO by WO number |
| `test_search_by_customer_name` | Search WO by customer name |
| `test_add_comment_to_wo` | Add comments on a WO |
| `test_print_customer_copy` | WO PDF printout — customer copy |
| `test_print_shop_copy` | WO PDF printout — shop copy |

---

## Error Handling

- All element lookups use `find_element()` with `DEFAULT_TIMEOUT` (10s) before raising
- Customer/unit lookup fields will use `wait_for_text()` to confirm the autocomplete resolves before proceeding
- Print actions wait for a print dialog or PDF window to appear (verified via `wait_for_text` or window title check)
- Screenshots captured automatically on test failure via existing `ScreenshotManager`

---

## Out of Scope (Phase 1)

The following GA Service items are deferred to later phases:
- Add/modify/remove Parts, Labor, Sublet, Extras (Phase 2)
- Canned Jobs, Flat Rate lookup (Phase 2)
- Take payment on WO, IDSPAY (Phase 3)
- Appointments/Scheduler, clock in/out, Doc Manager (Phase 4)
- Security: cannot edit old WO (not automatable via desktop UI)
- Estimates, Convert Estimate to WO (flagged N in GA doc)
