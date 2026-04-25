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
