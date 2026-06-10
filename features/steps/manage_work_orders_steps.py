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
    # Poll up to 8 s — the Service Manager window may take time to render.
    # Use title_re (contains) instead of exact title to handle minor variations.
    import re
    pattern = re.escape(window_title)
    handles = []
    for _ in range(16):
        handles = findwindows.find_windows(title_re=f".*{pattern}.*")
        if handles:
            break
        time.sleep(0.5)

    if not handles:
        # Diagnostic: show all top-level window titles to help pinpoint the real name.
        all_titles = [
            t for t in (
                Desktop(backend="win32").window(handle=h).window_text()
                for h in findwindows.find_windows()
            )
            if t.strip()
        ]
        assert False, (
            f'Window matching "{window_title}" was not found after 8 s.\n'
            f'Visible windows: {all_titles}'
        )

    hwnd = handles[0]
    _activate(hwnd)
    win = Desktop(backend="win32").window(handle=hwnd)
    assert win.is_visible(), f'Window "{window_title}" exists but is not visible'
    context.s.service_manager_hwnd = hwnd
