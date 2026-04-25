# tests/test_work_order_creation.py
import pytest
from screens.work_order_creation_screen import WorkOrderCreationScreen


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
