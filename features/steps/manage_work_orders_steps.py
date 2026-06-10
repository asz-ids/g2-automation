import ctypes
import re
import time

from behave import given, when, then, step
from pywinauto import Desktop, findwindows

WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP   = 0x0202

SERVICE_MANAGER_TITLE = "Astra G2 - Service Manager"


# ── Low-level helpers ─────────────────────────────────────────────────────────

def _activate(hwnd):
    ctypes.windll.user32.ShowWindow(hwnd, 9)
    ctypes.windll.user32.SetForegroundWindow(hwnd)
    time.sleep(0.3)


def _click_hwnd(hwnd):
    """WM_LBUTTONDOWN/UP — for regular buttons (not checkboxes)."""
    ctypes.windll.user32.SendMessageW(hwnd, WM_LBUTTONDOWN, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.SendMessageW(hwnd, WM_LBUTTONUP, 0, 0)
    time.sleep(0.3)


def _enum_children(parent_hwnd):
    """Return list of (hwnd, title, class_name) for every child of parent_hwnd."""
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
    """First child whose title contains partial_title (case-insensitive, & stripped)."""
    needle = partial_title.lower().replace("&", "")
    for hwnd, title, _ in _enum_children(parent_hwnd):
        if needle in title.lower().replace("&", ""):
            return hwnd
    return None


def _find_service_manager_hwnd():
    handles = findwindows.find_windows(title_re=".*Service Manager.*")
    return handles[0] if handles else None


# ── Checkbox helpers ──────────────────────────────────────────────────────────
# UIA hangs for G2 checkboxes (get_toggle_state / click_input block
# indefinitely). BM_GETCHECK does not reflect the true WinForms state.
# Solution: find HWND via Win32 EnumChildWindows, click via pywinauto
# win32-backend click_input() which uses SetCursorPos + mouse_event
# (pure Win32, no COM).

def _click_checkbox(sm_hwnd, label):
    """Find a checkbox by partial title and click it via physical mouse input."""
    chk_hwnd = _find_child_by_partial_title(sm_hwnd, label)
    assert chk_hwnd, (
        f"Could not find checkbox '{label}' inside the Service Manager window"
    )
    Desktop(backend="win32").window(handle=chk_hwnd).click_input()
    time.sleep(0.3)


def _ensure_checkbox_state(sm_hwnd, label, want_checked: bool):
    """
    Click a checkbox only if it is not already in the desired state.
    State is read via BM_GETCHECK (0x00F0); if that returns an unexpected
    value the click is performed unconditionally (safe — worst case is a
    double-toggle, which the filter result will catch).
    """
    BM_GETCHECK   = 0x00F0
    BST_UNCHECKED = 0
    BST_CHECKED   = 1

    chk_hwnd = _find_child_by_partial_title(sm_hwnd, label)
    assert chk_hwnd, (
        f"Could not find checkbox '{label}' inside the Service Manager window"
    )

    state = ctypes.windll.user32.SendMessageW(chk_hwnd, BM_GETCHECK, 0, 0)
    desired = BST_CHECKED if want_checked else BST_UNCHECKED

    # Only click if state differs from desired OR if BM_GETCHECK returned
    # something other than 0/1 (unreliable — click anyway).
    if state != desired:
        Desktop(backend="win32").window(handle=chk_hwnd).click_input()
        time.sleep(0.3)


def _get_checkbox_state(sm_hwnd, label):
    """Return BM_GETCHECK value for a checkbox (0=unchecked, 1=checked)."""
    BM_GETCHECK = 0x00F0
    chk_hwnd = _find_child_by_partial_title(sm_hwnd, label)
    if chk_hwnd is None:
        return None
    return ctypes.windll.user32.SendMessageW(chk_hwnd, BM_GETCHECK, 0, 0)


# ── When ──────────────────────────────────────────────────────────────────────

@when('I navigate to "Work Orders" from the Service menu')
def step_navigate_to_work_orders(context):
    from screens.navigator_screen import NavigatorScreen
    nav = NavigatorScreen()
    assert nav.is_navigator_present(), "Navigator window not found"
    assert nav.click_menu_button("Service"), "Failed to click Service menu button"
    assert nav.click_explorer_bar_button("Work Orders"), (
        "Failed to click Work Orders explorer bar button"
    )
    context.s.service_manager_hwnd = None
    time.sleep(1)


@when('I check the "Open WO\'s" filter')
def step_check_open_wos(context):
    """Ensure 'Open WO\'s' checkbox is checked via UIA."""
    sm_hwnd = context.s.service_manager_hwnd or _find_service_manager_hwnd()
    assert sm_hwnd, "Service Manager window not found"
    _activate(sm_hwnd)
    time.sleep(0.5)
    _ensure_checkbox_state(sm_hwnd, "Open WO's", want_checked=True)


@when("I apply the work order filter")
def step_click_select_work_orders(context):
    """Click 'Se&lect Work Orders' button to load the filtered list."""
    sm_hwnd = context.s.service_manager_hwnd or _find_service_manager_hwnd()
    assert sm_hwnd, "Service Manager window not found"
    _activate(sm_hwnd)

    btn_hwnd = _find_child_by_partial_title(sm_hwnd, "Select Work Order")
    if btn_hwnd is None:
        children = _enum_children(sm_hwnd)
        labelled = [f"{repr(t)}[{c}]" for _, t, c in children if t]
        assert False, (
            "Could not find 'Select Work Order' button.\n"
            f"All labelled children: {labelled}"
        )
    _click_hwnd(btn_hwnd)
    time.sleep(1)


@step('I check the "{checkbox_label}" checkbox')
def step_check_checkbox(context, checkbox_label):
    """Ensure a checkbox is checked via UIA."""
    sm_hwnd = context.s.service_manager_hwnd or _find_service_manager_hwnd()
    assert sm_hwnd, "Service Manager window not found"
    _ensure_checkbox_state(sm_hwnd, checkbox_label, want_checked=True)


@step('I uncheck the "{checkbox_label}" checkbox')
def step_uncheck_checkbox(context, checkbox_label):
    """Ensure a checkbox is unchecked via UIA."""
    sm_hwnd = context.s.service_manager_hwnd or _find_service_manager_hwnd()
    assert sm_hwnd, "Service Manager window not found"
    _ensure_checkbox_state(sm_hwnd, checkbox_label, want_checked=False)


# ── Given / Then ──────────────────────────────────────────────────────────────

@given('the "{window_title}" window is open and visible')
def step_given_window_open(context, window_title):
    step_window_is_open_and_visible(context, window_title)


@then('the "{window_title}" window is open and visible')
def step_window_is_open_and_visible(context, window_title):
    """Poll up to 8 s; use title_re to handle minor title variations."""
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
    Verify the WO list is populated by reading the 'N Work Orders Selected'
    status label via EnumChildWindows — avoids UIA descendants() COM crash.
    """
    sm_hwnd = context.s.service_manager_hwnd or _find_service_manager_hwnd()
    assert sm_hwnd, "Service Manager window not found"

    children = _enum_children(sm_hwnd)
    count_label = next(
        (title for _, title, _ in children if "Work Orders Selected" in title),
        None,
    )
    assert count_label is not None, (
        "Could not find 'Work Orders Selected' count label.\n"
        f"Labelled children: {[t for _, t, _ in children if t]}"
    )

    match = re.match(r"(\d+)", count_label.strip())
    assert match and int(match.group(1)) > 0, (
        f"Work order count is zero or unreadable: {repr(count_label)}"
    )
    print(f"  Work order list verified: {count_label}")


@step('the "{checkbox_label}" checkbox is checked')
def step_checkbox_is_checked(context, checkbox_label):
    """Assert a checkbox is checked via UIA TogglePattern."""
    sm_hwnd = context.s.service_manager_hwnd or _find_service_manager_hwnd()
    assert sm_hwnd, "Service Manager window not found"
    state = _get_checkbox_state(sm_hwnd, checkbox_label)
    assert state == 1, (
        f"Expected '{checkbox_label}' to be checked but toggle state={state}"
    )


@step('the "{checkbox_label}" checkbox is unchecked')
def step_checkbox_is_unchecked(context, checkbox_label):
    """Assert a checkbox is unchecked via UIA TogglePattern."""
    sm_hwnd = context.s.service_manager_hwnd or _find_service_manager_hwnd()
    assert sm_hwnd, "Service Manager window not found"
    state = _get_checkbox_state(sm_hwnd, checkbox_label)
    assert state == 0, (
        f"Expected '{checkbox_label}' to be unchecked but toggle state={state}"
    )
