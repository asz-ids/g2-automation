# How to Run the Navigator Button Tests

## Prerequisites
1. **G2 Application**: Must be running and logged in to the Navigator screen
2. **32-bit Python Environment**: Tests should use 32-bit Python (`.venv32`)
3. **pytest installed**: Part of the dependencies

## Method 1: Run with pytest (Recommended)

### Run all tests in the file:
```bash
cd "e:\G2 Desktop Automation"
.\.venv32\Scripts\python.exe -m pytest tests/test_navigator_buttons.py -v
```

### Run a specific test:
```bash
.\.venv32\Scripts\python.exe -m pytest tests/test_navigator_buttons.py::TestNavigatorButtonInteraction::test_click_parts_button -v
```

### Run with detailed output:
```bash
.\.venv32\Scripts\python.exe -m pytest tests/test_navigator_buttons.py -v -s
```

### Run with short traceback:
```bash
.\.venv32\Scripts\python.exe -m pytest tests/test_navigator_buttons.py -v --tb=short
```

## Method 2: Run directly with Python

```bash
cd "e:\G2 Desktop Automation"
.\.venv32\Scripts\python.exe -m pytest tests/test_navigator_buttons.py
```

## Method 3: Run from PowerShell

```powershell
cd "e:\G2 Desktop Automation"
& ".\.venv32\Scripts\python.exe" -m pytest tests/test_navigator_buttons.py -v
```

## What the Tests Do

1. **test_navigator_present** - Verifies Navigator window is open
2. **test_find_all_menu_buttons** - Finds all 5 menu buttons
3. **test_verify_all_menus_present** - Checks all menus are accessible
4. **test_find_parts_button** - Finds the Parts button specifically
5. **test_click_parts_button** - Clicks Parts and verifies it becomes active
6. **test_click_sales_button** - Clicks Sales and verifies it becomes active
7. **test_click_service_button** - Clicks Service and verifies it becomes active
8. **test_click_accounting_button** - Clicks Accounting and verifies it becomes active
9. **test_click_admin_button** - Clicks Admin and verifies it becomes active
10. **test_all_navigator_buttons_clickable** - Tests all 5 buttons in sequence
11. **test_get_active_menu** - Verifies getting current active menu

## Expected Output

```
tests/test_navigator_buttons.py::TestNavigatorButtonInteraction::test_navigator_present PASSED
tests/test_navigator_buttons.py::TestNavigatorButtonInteraction::test_find_all_menu_buttons PASSED
tests/test_navigator_buttons.py::TestNavigatorButtonInteraction::test_verify_all_menus_present PASSED
tests/test_navigator_buttons.py::TestNavigatorButtonInteraction::test_find_parts_button PASSED
tests/test_navigator_buttons.py::TestNavigatorButtonInteraction::test_click_parts_button PASSED
tests/test_navigator_buttons.py::TestNavigatorButtonInteraction::test_click_sales_button PASSED
tests/test_navigator_buttons.py::TestNavigatorButtonInteraction::test_click_service_button PASSED
tests/test_navigator_buttons.py::TestNavigatorButtonInteraction::test_click_accounting_button PASSED
tests/test_navigator_buttons.py::TestNavigatorButtonInteraction::test_click_admin_button PASSED
tests/test_navigator_buttons.py::TestNavigatorButtonInteraction::test_all_navigator_buttons_clickable PASSED
tests/test_navigator_buttons.py::TestNavigatorButtonInteraction::test_get_active_menu PASSED

============ 11 passed in X.XXs ============
```

## Troubleshooting

### Error: "Navigator window not open"
- Solution: Make sure G2 is running and you're logged into the Navigator screen
- Launch with: `Start-Process "C:\IDSASTRA\APPS\G2\G2CLIENT\IdsG2Client.exe" -ArgumentList "/S", "/v"`

### Error: "No module named 'screens'"
- Solution: Make sure you're running from the `e:\G2 Desktop Automation` directory
- The path insert in the test file should resolve this

### Error: "ModuleNotFoundError: No module named 'pywinauto'"
- Solution: Ensure you're using the 32-bit Python venv:
  - `.\.venv32\Scripts\python.exe -m pytest ...`

### Tests timeout or hang
- Solution: Make sure G2 Navigator is responsive and not blocked
- Check that the window is visible and not minimized

## Quick Start

**Fastest way to run all tests:**
```powershell
cd "e:\G2 Desktop Automation"
& ".\.venv32\Scripts\python.exe" -m pytest tests/test_navigator_buttons.py -v
```

Then verify all 11 tests pass with green checkmarks ✓
