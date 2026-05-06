# tests/test_work_order_creation.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import time
import ctypes
import pytest
from pywinauto import findwindows
from pywinauto.keyboard import send_keys
from screens.work_order_creation_screen import WorkOrderCreationScreen

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

    # Launch if no login window is visible yet
    if not findwindows.find_windows(title="G2 Login"):
        print("\n  Launching G2...")
        result = ctypes.windll.shell32.ShellExecuteW(
            None, "open", G2_EXE, None, os.path.dirname(G2_EXE), 1
        )
        if result <= 32:
            pytest.fail(f"ShellExecute failed (code {result}) — cannot launch G2")

    # Wait for login window
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

    # Enter credentials using keyboard input — avoids COM/UIA which can crash inside pytest
    try:
        ctypes.windll.user32.SetForegroundWindow(login_hwnd)
        time.sleep(0.5)
        send_keys(f'{G2_USERNAME}{{TAB}}{G2_PASSWORD}{{ENTER}}')
        print("  Credentials submitted — waiting for Navigator...")
    except Exception as e:
        pytest.fail(f"Could not submit login credentials: {e}")

    # Wait for Navigator to appear after login
    for i in range(60):
        if _navigator_open():
            print(f"  Navigator appeared after {i}s")
            return
        time.sleep(1)
    pytest.fail("G2 Navigator did not appear within 60s after login")


def test_import():
    assert WorkOrderCreationScreen is not None


@pytest.mark.functional
def test_navigate_to_work_orders(live_work_order_screen):
    """GA: Confirm WO Manager is working correctly — navigation succeeds."""
    result = live_work_order_screen.navigate_to_work_orders()
    assert result is True, "navigate_to_work_orders() should return True when WO Manager loads"


@pytest.mark.functional
def test_wo_manager_is_loaded(live_work_order_screen):
    """GA: Confirm WO Manager is working correctly — manager grid visible."""
    live_work_order_screen.navigate_to_work_orders()
    assert live_work_order_screen.is_wo_manager_loaded(), "WO Manager should be visible after navigation"


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
