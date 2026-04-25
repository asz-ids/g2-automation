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
