import ctypes
import re
import time

from behave import given, when, then
from pywinauto import Desktop, findwindows

WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP   = 0x0202

SERVICE_MANAGER_TITLE = "Astra G2 - Service Manager"


def _activate(hwnd):
    ctypes.windll.user32.ShowWindow(hwnd, 9)   # SW_RESTORE
    ctypes.windll.user32.SetForegroundWindow(hwnd)
    time.sleep(0.3)


def _click_hwnd(hwnd):
    """Send WM_LBUTTONDOWN/UP to hwnd — works for elevated WinForms controls."""
    ctypes.windll.user32.SendMessageW(hwnd, WM_LBUTTONDOWN, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.SendMessageW(hwnd, WM_LBUTTONUP, 0, 0)
    time.sleep(0.3)


def _enum_children(parent_hwnd):
    """Yield (hwnd, title, class_name) for every child window under parent_hwnd."""
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    buf_t = ctypes.create_unicode_buffer(512)
    buf_c = ctypes.create_unicode_buffer(512)
    results = []

    def _cb(hwnd, _):
        ctypes.windll.user32.GetWindowTextW(hwnd, buf_t, 512)
        ctypes.windll.user32.GetClassNameW(hwnd, buf_c, 512)
        results.append((hwnd, buf_t.value.strip(), buf_c.value.strip()))
        return True

    ctypes.windll.user32.EnumChildWindows(parent_hwnd, WNDENUMPROC(_cb), 0)
    return results


def _find_child_by_partial_title(parent_hwnd, partial_title):
    """Return the HWND of the first child whose title contains partial_title (case-insensitive).
    Strips Win32 keyboard-accelerator ampersands (e.g. 'Se&lect' → 'Select') before comparing."""
    needle = partial_title.lower().replace("&", "")
    for hwnd, title, _ in _enum_children(parent_hwnd):
        if needle in title.lower().replace("&", ""):
            return hwnd
    return None


def _find_service_manager_hwnd():
    """Return the HWND of the Astra G2 - Service Manager window, or None."""
    handles = findwindows.find_windows(title_re=".*Service Manager.*")
    return handles[0] if handles else None


# ── When ──────────────────────────────────────────────────────────────────────

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


@when('I check the "Open WO\'s" filter')
def step_check_open_wos(context):
    """
    Click the 'Open WO's' checkbox inside the Selection Criteria group.
    Uses partial-title Win32 search — avoids UIA descendants crash and
    class-name hash variations across G2 builds.

    UIA path: ServiceTaskForm -> tabControlMaster
      -> WorkOrderManagerControl -> tableLayoutPanelLeft
      -> gbCriteria -> chkOpenWo (title "Open WO's")
    """
    sm_hwnd = context.s.service_manager_hwnd or _find_service_manager_hwnd()
    assert sm_hwnd, "Service Manager window not found"
    _activate(sm_hwnd)
    time.sleep(0.5)  # allow tab content to finish rendering

    chk_hwnd = _find_child_by_partial_title(sm_hwnd, "Open WO")
    if chk_hwnd is None:
        children = _enum_children(sm_hwnd)
        labelled = [f"{repr(t)}[{c}]" for _, t, c in children if t]
        assert False, (
            "Could not find a child containing 'Open WO'.\n"
            f"All labelled children ({len(labelled)}): {labelled}"
        )

    _click_hwnd(chk_hwnd)


@when("I apply the work order filter")
def step_click_select_work_orders(context):
    """
    Click the 'Select Work Orders' button to apply the filter.
    Uses partial-title Win32 search for robustness.
    """
    sm_hwnd = context.s.service_manager_hwnd or _find_service_manager_hwnd()
    assert sm_hwnd, "Service Manager window not found"
    _activate(sm_hwnd)

    btn_hwnd = _find_child_by_partial_title(sm_hwnd, "Select Work Order")
    if btn_hwnd is None:
        children = _enum_children(sm_hwnd)
        labelled = [f"{repr(t)}[{c}]" for _, t, c in children if t]
        assert False, (
            "Could not find a child containing 'Select Work Order'.\n"
            f"All labelled children ({len(labelled)}): {labelled}"
        )

    _click_hwnd(btn_hwnd)
    time.sleep(1)


# ── Given / Then ──────────────────────────────────────────────────────────────

@given('the "{window_title}" window is open and visible')
def step_given_window_open(context, window_title):
    """Alias so subsequent scenarios can use this as a Given."""
    step_window_is_open_and_visible(context, window_title)


@then('the "{window_title}" window is open and visible')
def step_window_is_open_and_visible(context, window_title):
    """Poll up to 8 s for the window; use title_re to handle minor title variations."""
    pattern = re.escape(window_title)
    handles = []
    for _ in range(16):
        handles = findwindows.find_windows(title_re=f".*{pattern}.*")
        if handles:
            break
        time.sleep(0.5)

    if not handles:
        all_titles = [
            Desktop(backend="win32").window(handle=h).window_text()
            for h in findwindows.find_windows()
        ]
        assert False, (
            f'Window matching "{window_title}" not found after 8 s.\n'
            f'Visible windows: {[t for t in all_titles if t.strip()]}'
        )

    hwnd = handles[0]
    _activate(hwnd)
    win = Desktop(backend="win32").window(handle=hwnd)
    assert win.is_visible(), f'Window "{window_title}" found but not visible'
    context.s.service_manager_hwnd = hwnd


@then("the work order list is displayed")
def step_wo_list_displayed(context):
    """
    Verify the WO list is populated after applying the filter.
    Reads the 'N Work Orders Selected' status label via Win32 EnumChildWindows
    — avoids UIA descendants() which causes a fatal COM crash (0x80040155).
    """
    sm_hwnd = context.s.service_manager_hwnd or _find_service_manager_hwnd()
    assert sm_hwnd, "Service Manager window not found"

    # The WO Manager shows a label like "9552 Work Orders Selected (...)"
    # after Select Work Orders is clicked.  Find it among all child titles.
    children = _enum_children(sm_hwnd)
    count_label = next(
        (title for _, title, _ in children if "Work Orders Selected" in title),
        None,
    )
    assert count_label is not None, (
        "Could not find 'Work Orders Selected' count label — "
        "filter may not have been applied.\n"
        f"Labelled children: {[t for _, t, _ in children if t]}"
    )

    # Extract the leading number and confirm it is > 0.
    import re as _re
    match = _re.match(r"(\d+)", count_label.strip())
    assert match and int(match.group(1)) > 0, (
        f"Work order count is zero or unreadable: {repr(count_label)}"
    )
    print(f"  Work order list verified: {count_label}")
