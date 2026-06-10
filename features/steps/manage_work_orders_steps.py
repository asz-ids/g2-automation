import ctypes
import re
import time

from behave import given, when, then
from pywinauto import Desktop, findwindows

WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP   = 0x0202

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


def _find_service_manager_hwnd():
    """Return the HWND of the Astra G2 - Service Manager window, or None."""
    handles = findwindows.find_windows(title_re=".*Service Manager.*")
    return handles[0] if handles else None


def _find_child_by_auto_id(parent_hwnd, auto_id):
    """
    Walk the Win32 child-window tree to find a window whose automation_id
    matches auto_id. Returns the HWND or None.
    """
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    buf = ctypes.create_unicode_buffer(512)
    found = []

    def _cb(hwnd, _):
        # GetWindowTextW returns the window caption; for WinForms controls the
        # automation_id is the .Name property which may differ.  Fall back to
        # comparing the window class against the known WinForms BUTTON class
        # and the caption to the control title.
        ctypes.windll.user32.GetWindowTextW(hwnd, buf, 512)
        if buf.value.strip() == auto_id:
            found.append(hwnd)
            return False  # stop enumeration
        return True

    ctypes.windll.user32.EnumChildWindows(parent_hwnd, WNDENUMPROC(_cb), 0)
    return found[0] if found else None


def _find_child_by_title(parent_hwnd, title):
    """Find the first child window whose caption matches title (exact)."""
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    buf = ctypes.create_unicode_buffer(512)
    found = []

    def _cb(hwnd, _):
        ctypes.windll.user32.GetWindowTextW(hwnd, buf, 512)
        if buf.value.strip() == title:
            found.append(hwnd)
            return False
        return True

    ctypes.windll.user32.EnumChildWindows(parent_hwnd, WNDENUMPROC(_cb), 0)
    return found[0] if found else None


def _click_hwnd(hwnd):
    """Send WM_LBUTTONDOWN/UP to hwnd — works for elevated WinForms controls."""
    ctypes.windll.user32.SendMessageW(hwnd, WM_LBUTTONDOWN, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.SendMessageW(hwnd, WM_LBUTTONUP, 0, 0)
    time.sleep(0.3)


# ── Given ─────────────────────────────────────────────────────────────────────

@given('the "{window_title}" window is open and visible')
def step_given_window_open(context, window_title):
    """Alias for the Then step — used as a Given in subsequent scenarios."""
    step_window_is_open_and_visible(context, window_title)


# ── Then ──────────────────────────────────────────────────────────────────────

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


@when('I check the "Open WO\'s" filter')
def step_check_open_wos(context):
    """
    Click the 'Open WO's' checkbox (auto_id=chkOpenWo) inside the
    Selection Criteria group on the Manage Work Orders tab.

    UIA path:
      ServiceTaskForm -> tabControlMaster -> WorkOrderManagerControl
        -> tableLayoutPanelLeft -> gbCriteria -> chkOpenWo
    """
    sm_hwnd = context.s.service_manager_hwnd or _find_service_manager_hwnd()
    assert sm_hwnd, "Service Manager window not found"
    _activate(sm_hwnd)

    # Try UIA first — direct lookup by automation_id avoids EnumChildWindows
    # depth limitations on deeply nested WinForms controls.
    uia_win = Desktop(backend="uia").window(handle=sm_hwnd)
    try:
        chk = uia_win.child_window(
            title="Open WO's",
            class_name="WindowsForms10.BUTTON.app.0.392a42d_r8_ad1",
        )
        chk.click_input()
        time.sleep(0.3)
        return
    except Exception:
        pass

    # Fallback: find by window caption in the Win32 hierarchy.
    chk_hwnd = _find_child_by_title(sm_hwnd, "Open WO's")
    assert chk_hwnd, (
        "Could not find the 'Open WO\\'s' checkbox "
        "(class=WindowsForms10.BUTTON.app.0.392a42d_r8_ad1) "
        "inside the Service Manager window"
    )
    _click_hwnd(chk_hwnd)


@when("I apply the work order filter")
def step_click_select_work_orders(context):
    """
    Click the 'Select Work Orders' button to apply the filter and
    load the matching work order list.
    """
    sm_hwnd = context.s.service_manager_hwnd or _find_service_manager_hwnd()
    assert sm_hwnd, "Service Manager window not found"
    _activate(sm_hwnd)

    uia_win = Desktop(backend="uia").window(handle=sm_hwnd)
    try:
        btn = uia_win.child_window(title="Select Work Orders", control_type="Button")
        btn.click_input()
        time.sleep(1)
        return
    except Exception:
        pass

    btn_hwnd = _find_child_by_title(sm_hwnd, "Select Work Orders")
    assert btn_hwnd, (
        "Could not find the 'Select Work Orders' button "
        "inside the Service Manager window"
    )
    _click_hwnd(btn_hwnd)
    time.sleep(1)


@then("the work order list is displayed")
def step_wo_list_displayed(context):
    """
    Verify that at least one row appears in the Work Orders grid after
    applying the filter.  The list control sits inside WorkOrderManagerControl
    — we check that any child with list-row content is present.
    """
    sm_hwnd = context.s.service_manager_hwnd or _find_service_manager_hwnd()
    assert sm_hwnd, "Service Manager window not found"

    uia_win = Desktop(backend="uia").window(handle=sm_hwnd)
    try:
        # The WO grid is typically a DataGridView or ListView.
        # Any DataItem or ListItem child confirms data was loaded.
        rows = uia_win.descendants(control_type="DataItem")
        if not rows:
            rows = uia_win.descendants(control_type="ListItem")
        assert rows, "Work order list appears empty after applying the filter"
        return
    except Exception as exc:
        assert False, f"Could not inspect the work order list: {exc}"
