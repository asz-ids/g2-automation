import ctypes
import time

from behave import when, then
from pywinauto import Desktop, findwindows

SERVICE_MANAGER_TITLE = "Astra G2 - Service Manager"
SERVICE_MANAGER_AUTO_ID = "ServiceTaskForm"


def _activate(hwnd):
    ctypes.windll.user32.ShowWindow(hwnd, 9)   # SW_RESTORE
    ctypes.windll.user32.SetForegroundWindow(hwnd)
    time.sleep(0.3)


@when('I navigate to "Work Orders" from the Service menu')
def step_navigate_to_work_orders(context):
    from screens.navigator_screen import NavigatorScreen
    nav = NavigatorScreen()
    assert nav.is_navigator_present(), "Navigator window not found"
    clicked = nav.click_menu_button("Service")
    assert clicked, "Failed to click the Service menu button"
    clicked = nav.click_explorer_bar_button("Work Orders")
    assert clicked, "Failed to click the Work Orders explorer bar button"
    context.s.service_manager_hwnd = None
    time.sleep(1)


@then('the "{window_title}" window is open and visible')
def step_window_is_open_and_visible(context, window_title):
    handles = findwindows.find_windows(title=window_title)
    assert handles, f'Window "{window_title}" was not found'
    hwnd = handles[0]
    _activate(hwnd)
    win = Desktop(backend="win32").window(handle=hwnd)
    assert win.is_visible(), f'Window "{window_title}" exists but is not visible'
    context.s.service_manager_hwnd = hwnd
