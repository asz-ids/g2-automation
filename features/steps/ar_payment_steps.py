import ctypes
import ctypes.wintypes
import os
import time

from behave import given, when, then
from pywinauto import Desktop, findwindows
from pywinauto.keyboard import send_keys

G2_EXE = r"C:\IDSASTRA\APPS\G2\G2CLIENT\IdsG2Client.exe"
WM_GETTEXT = 0x000D
WM_GETTEXTLENGTH = 0x000E


# ── Background ────────────────────────────────────────────────────────────────

@given("G2 is running and the Navigator is open")
def step_g2_running(context):
    s = context.s
    handles = findwindows.find_windows(title_re=".*Navigator.*")
    if handles:
        s.nav_hwnd = handles[0]
        print("  Navigator already open — skipping launch and login")
        _activate(s.nav_hwnd)
        return

    result = ctypes.windll.shell32.ShellExecuteW(
        None, "open", G2_EXE, None, os.path.dirname(G2_EXE), 1
    )
    assert result > 32, f"ShellExecute failed with code {result}"

    login_hwnd = None
    for _ in range(30):
        h = findwindows.find_windows(title="G2 Login")
        if h:
            login_hwnd = h[0]        
            break
        time.sleep(1)
    assert login_hwnd, "G2 Login window did not appear within 30s"
    _activate(login_hwnd)

    login_win = Desktop(backend='uia').window(handle=login_hwnd)

    user_field = login_win.child_window(auto_id="txtUser", control_type="Pane") \
                           .child_window(control_type="Custom")
    user_field.click_input()
    send_keys('^a')
    send_keys('aqadir.ids')
    time.sleep(0.3)

    pwd_field = login_win.child_window(auto_id="txtPwd", control_type="Pane") \
                          .child_window(control_type="Custom")
    pwd_field.click_input()
    send_keys('^a')
    send_keys('Aqadir2801')
    time.sleep(0.3)

    login_win.child_window(auto_id="btnLogin", control_type="Button").click_input()

    for _ in range(60):
        h = findwindows.find_windows(title_re=".*Navigator.*")
        if h:
            s.nav_hwnd = h[0]
            break
        time.sleep(1)
    assert s.nav_hwnd, "Navigator window did not appear after login"
    _activate(s.nav_hwnd)


# ── Navigation ────────────────────────────────────────────────────────────────

# Maps top-level menu names to their Navigator button auto_ids
_MENU_AUTO_ID = {
    "Parts":   "btnParts",
    "Sales":   "btnSales",
    "Service": "btnService",
    "Admin":   "btnAdmin",
}

# Maps sub-menu item names to their Navigator button auto_ids
_ITEM_AUTO_ID = {
    "Take AR Payments": "btnTakeARPayments",
    "Unit Inventory":   "btnUnitInventory",
    "Maintain Units":   "btnMaintainUnits",
}


class _POINT(ctypes.Structure):
    _fields_ = [('x', ctypes.c_long), ('y', ctypes.c_long)]

BM_CLICK            = 0x00F5
WM_LBUTTONDOWN      = 0x0201
WM_LBUTTONUP        = 0x0202
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP   = 0x0004


def _nav_click(nav_win, label):
    """
    Click a Navigator button by trying progressively lower-level mechanisms.

    Buttons with a known auto_id work via click_input().
    Buttons without auto_id (e.g. Maintain Units inside UltraExplorerBar) have a
    real WinForms HWND but no title — we fall through several strategies:
      A) UIA InvokePattern  — bypasses UIPI, most reliable for accessibility
      B) BM_CLICK (sync)    — standard Win32 button message via SendMessageW
      C) WM_LBUTTONDOWN/UP  — raw mouse messages via SendMessageW (sync)
      D) Hardware mouse_event — SetCursorPos + mouse_event LEFTDOWN/LEFTUP
    """
    # 1. Try known auto_id
    auto_id = _ITEM_AUTO_ID.get(label)
    if auto_id:
        try:
            nav_win.child_window(auto_id=auto_id, control_type='Button').click_input()
            print(f"  [OK] Clicked '{label}' via auto_id={auto_id!r}")
            return
        except Exception:
            pass

    # 2. Find UIA element and get screen centre
    btn = nav_win.child_window(title=label, control_type='Button')
    btn.wait('exists visible', timeout=5)
    rect = btn.rectangle()
    cx   = (rect.left + rect.right)  // 2
    cy   = (rect.top  + rect.bottom) // 2

    # Bring Navigator to foreground before any click attempt
    ctypes.windll.user32.SetForegroundWindow(nav_win.handle)
    time.sleep(0.15)

    # A. UIA InvokePattern — crosses UIPI elevation boundary via COM accessibility
    try:
        btn.invoke()
        print(f"  [OK] Invoked '{label}' via UIA InvokePattern")
        return
    except Exception as e:
        print(f"  [--] invoke() failed for '{label}': {e}")

    # B. BM_CLICK via SendMessageW — synchronous, triggers WinForms Click event
    btn_hwnd = ctypes.windll.user32.WindowFromPoint(_POINT(cx, cy))
    print(f"  HWND at ({cx},{cy}): {btn_hwnd}")
    if btn_hwnd:
        ret = ctypes.windll.user32.SendMessageW(btn_hwnd, BM_CLICK, 0, 0)
        print(f"  [OK] SendMessageW(BM_CLICK) → {ret} for '{label}'")
        return

    # C. WM_LBUTTONDOWN/UP via SendMessageW (sync) with client coords
    if btn_hwnd:
        pt = _POINT(cx, cy)
        ctypes.windll.user32.ScreenToClient(btn_hwnd, ctypes.byref(pt))
        lparam = (pt.y << 16) | (pt.x & 0xFFFF)
        ctypes.windll.user32.SendMessageW(btn_hwnd, WM_LBUTTONDOWN, 1, lparam)
        time.sleep(0.05)
        ctypes.windll.user32.SendMessageW(btn_hwnd, WM_LBUTTONUP,   0, lparam)
        print(f"  [OK] SendMessageW(WM_LBUTTONDOWN/UP) to HWND {btn_hwnd} for '{label}'")
        return

    # D. Hardware mouse_event — last resort, bypasses window messages entirely
    ctypes.windll.user32.SetCursorPos(cx, cy)
    time.sleep(0.05)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP,   0, 0, 0, 0)
    print(f"  [OK] Hardware mouse_event click at ({cx},{cy}) for '{label}'")


@when('I navigate to "{menu_item}" from the "{menu_name}" menu')
def step_navigate(context, menu_item, menu_name):
    s = context.s
    nav_win = Desktop(backend='uia').window(handle=s.nav_hwnd)

    # Click the top-level menu — try toolbar auto_id first, fall back to explorer bar
    menu_auto_id = _MENU_AUTO_ID.get(menu_name)
    if menu_auto_id:
        try:
            nav_win.child_window(auto_id=menu_auto_id, control_type='Button').click_input()
        except Exception:
            _nav_click(nav_win, menu_name)
    else:
        _nav_click(nav_win, menu_name)
    time.sleep(2)

    # Snapshot existing AR windows (needed by the AR payment workflow)
    s.existing_ar_handles = set(
        findwindows.find_windows(title_re=".*Accounts Receivable.*")
    )

    # Click the sub-menu item via explorer bar
    _nav_click(nav_win, menu_item)


# ── Window assertions ─────────────────────────────────────────────────────────

@then('the "{window_title}" window opens')
def step_window_opens(context, window_title):
    s = context.s
    hwnd = None

    if window_title == "Accounts Receivable":
        for _ in range(20):
            current = set(findwindows.find_windows(title_re=".*Accounts Receivable.*"))
            new = current - s.existing_ar_handles
            if new:
                hwnd = list(new)[0]
                break
            fg = ctypes.windll.user32.GetForegroundWindow()
            if fg in current:
                hwnd = fg
                break
            time.sleep(1)
        if not hwnd:
            all_ar = findwindows.find_windows(title_re=".*Accounts Receivable.*")
            hwnd = all_ar[0] if all_ar else None
        assert hwnd, "Accounts Receivable window did not open"
        s.ar_hwnd = hwnd

    elif window_title == "Take Payment":
        for _ in range(30):
            h = findwindows.find_windows(
                title_re=r".*Take Payment.*|.*Take Credit Card.*|.*Credit Card Payment.*"
            )
            if h:
                hwnd = h[0]
                break
            time.sleep(1)
        assert hwnd, "Take Payment window did not open within 30s"
        s.payment_hwnd = hwnd

    elif window_title == "IDSPay":
        hwnd = _wait_for_idspay(timeout=30)
        assert hwnd, "IDSPay window did not appear within 30s"
        s.idspay_hwnd = hwnd

    elif window_title == "Maintain Units":
        for _ in range(30):
            h = findwindows.find_windows(title_re=r".*Maintain Units.*")
            if h:
                hwnd = h[0]
                break
            time.sleep(1)
        assert hwnd, "Maintain Units window did not open within 30s"
        s.unit_inventory_hwnd = hwnd

    elif "Inventory" in window_title and "Sunset Marine" in window_title:
        for _ in range(30):
            h = findwindows.find_windows(title_re=r".*Inventory.*Sunset Marine.*")
            if h:
                hwnd = h[0]
                break
            time.sleep(1)
        assert hwnd, f'"{window_title}" window did not open within 30s'
        s.unit_inventory_hwnd = hwnd

    else:
        for _ in range(30):
            h = findwindows.find_windows(title_re=f".*{window_title}.*")
            if h:
                hwnd = h[0]
                break
            time.sleep(1)
        assert hwnd, f'"{window_title}" window did not open within 30s'
        # Store on state so subsequent steps can reference any window by name
        setattr(s, f"{window_title.lower().replace(' ', '_')}_hwnd", hwnd)

    _activate(hwnd)


# ── Customer entry ────────────────────────────────────────────────────────────

@when('I enter customer number "{customer_no}"')
def step_enter_customer(context, customer_no):
    s = context.s
    ar_win = Desktop(backend='uia').window(handle=s.ar_hwnd)
    all_children = list(ar_win.children())

    label_idx = next(
        (i for i, c in enumerate(all_children) if _safe_text(c) == 'Customer #'),
        None
    )
    assert label_idx is not None, "'Customer #' label not found in AR window children"

    customer_pane = None
    for j in range(label_idx - 1, max(label_idx - 5, -1), -1):
        try:
            if 'TextBox' in all_children[j].element_info.class_name:
                customer_pane = all_children[j]
                break
        except Exception:
            pass
    assert customer_pane, "No TextBox pane found before 'Customer #' label"

    edits = customer_pane.descendants(class_name='Edit')
    assert edits, "No Edit control found inside Customer # pane"
    s.customer_edit = edits[0]

    _activate(s.ar_hwnd)
    time.sleep(3)

    s.customer_edit.click_input()
    time.sleep(0.5)
    s.customer_edit.type_keys(customer_no, with_spaces=True)

    edit_hwnd = s.customer_edit.handle
    buf_len = ctypes.windll.user32.SendMessageW(edit_hwnd, WM_GETTEXTLENGTH, 0, 0)
    buf = ctypes.create_unicode_buffer(buf_len + 2)
    ctypes.windll.user32.SendMessageW(edit_hwnd, WM_GETTEXT, buf_len + 1, buf)
    actual = buf.value.strip()
    assert actual == customer_no, \
        f"Customer # field contains {actual!r}, expected {customer_no!r}"

    s.customer_edit.type_keys('{TAB}')
    time.sleep(0.5)


# ── Invoice table ─────────────────────────────────────────────────────────────

@then("the invoice table loads")
def step_table_loads(context):
    s = context.s
    ar_win = Desktop(backend='uia').window(handle=s.ar_hwnd)
    for _ in range(30):
        try:
            tbl = ar_win.child_window(class_name='VSFlexGrid8N')
            tbl.wait('exists visible', timeout=1)
            s.table = tbl
            break
        except Exception:
            time.sleep(1)
    assert s.table, "Invoice table (VSFlexGrid8N) did not load within 30s"

    rows = s.table.children(control_type="Custom")
    assert rows, "Invoice table loaded but has no rows — customer may have no open invoices"
    print(f"  Table loaded with {len(rows)} row(s)")


@when('I sort the invoice table by "{column}" descending')
def step_sort_table(context, column):
    s = context.s
    assert s.table is not None, "Invoice table not loaded — did 'the invoice table loads' step pass?"
    try:
        header = next(
            h for h in s.table.children(control_type="Header")
            if h.window_text().strip() == column
        )
    except StopIteration:
        raise AssertionError(f'Column header "{column}" not found in invoice table')

    time.sleep(1)
    header.click_input()
    time.sleep(2)
    header.click_input()
    time.sleep(1)


# ── Invoice selection and payment entry ───────────────────────────────────────

@when("I select the first invoice")
def step_select_first_invoice(context):
    send_keys('{TAB}')
    time.sleep(0.5)
    send_keys('{SPACE}')
    time.sleep(0.5)


@when('I set the pay amount to "{amount}"')
def step_set_pay_amount(context, amount):
    send_keys('{TAB}')
    time.sleep(2.5)
    send_keys('{SPACE}')
    time.sleep(1.5)
    send_keys('^a')
    time.sleep(0.5)
    send_keys(f'{amount}{{TAB}}')
    time.sleep(0.5)


@when("I accept the payment")
def step_accept_payment(context):
    send_keys('%a')
    time.sleep(1.5)
    send_keys('{SPACE}')
    time.sleep(0.5)


# ── Payment method ────────────────────────────────────────────────────────────

@when('I choose "{method}" as the payment method')
def step_choose_payment_method(context, method):
    s = context.s
    payment_win = Desktop(backend='uia').window(handle=s.payment_hwnd)
    btn = None
    for spec in [
        {"auto_id": f"btn{method}", "control_type": "Button"},
        {"title": method,           "control_type": "Button"},
        {"title_re": f".*{method}.*", "control_type": "Button"},
    ]:
        try:
            candidate = payment_win.child_window(**spec)
            candidate.wait('exists enabled visible', timeout=2)
            btn = candidate
            break
        except Exception:
            pass
    assert btn, f'"{method}" button not found in Take Payment window'
    btn.click_input()
    time.sleep(0.5)


# ── IDSPay ────────────────────────────────────────────────────────────────────

@when('I click the "{tab_name}" tab')
def step_click_tab(context, tab_name):
    s = context.s
    tab_coords = {"SAVED CARDS": (0.58, 0.16)}
    x_pct, y_pct = tab_coords.get(tab_name, (0.5, 0.5))

    assert s.idspay_hwnd, "IDSPay window handle not set — did 'the IDSPay window opens' step run?"

    print("\n  Waiting 40s for IDSPay web content to render...")
    for i in range(40, 0, -1):
        print(f"  {i}s remaining   ", end="\r")
        time.sleep(1)
    print()

    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(s.idspay_hwnd, ctypes.byref(rect))
    w, h = rect.right - rect.left, rect.bottom - rect.top
    Desktop(backend='uia').window(handle=s.idspay_hwnd).click_input(
        coords=(int(w * x_pct), int(h * y_pct))
    )
    time.sleep(5)


@when('I click "{button_label}"')
def step_click_label(context, button_label):
    s = context.s

    if button_label == "PROCESS PAYMENT":
        assert s.idspay_hwnd, "IDSPay window handle not set"
        btn = _find_process_payment_btn(s.idspay_hwnd, timeout=15)
        if btn:
            btn.click_input()
            print("  Clicked PROCESS PAYMENT via UIA")
        else:
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(s.idspay_hwnd, ctypes.byref(rect))
            w, h = rect.right - rect.left, rect.bottom - rect.top
            Desktop(backend='uia').window(handle=s.idspay_hwnd).click_input(
                coords=(int(w * 0.50), int(h * 0.82))
            )
            print("  Clicked PROCESS PAYMENT via coordinate fallback")
        return

    # Generic Navigator button — same strategy as Take AR Payments in ar_payment_workflow.py
    nav_win = Desktop(backend='uia').window(handle=s.nav_hwnd)
    _nav_click(nav_win, button_label)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _find_by_title(root_info, title, timeout=5):
    """
    Walk the full UIA element tree under root_info and return the first element
    whose name matches title (case-sensitive). No control_type filter so it works
    for Infragistics tree items that may not map cleanly to 'Button'.
    """
    import time as _time
    deadline = _time.time() + timeout

    def _walk(info):
        try:
            if info.name == title:
                return info
            for child in info.children():
                result = _walk(child)
                if result:
                    return result
        except Exception:
            pass
        return None

    while _time.time() < deadline:
        result = _walk(root_info)
        if result:
            return result
        _time.sleep(0.5)
    return None


def _activate(hwnd):
    ctypes.windll.user32.ShowWindow(hwnd, 9)
    ctypes.windll.user32.SetForegroundWindow(hwnd)
    ctypes.windll.user32.BringWindowToTop(hwnd)
    time.sleep(0.3)


def _safe_text(elem):
    try:
        return elem.window_text()
    except Exception:
        return ''


def _wait_for_idspay(timeout=60):
    for _ in range(timeout):
        h = findwindows.find_windows(title="IDSPay")
        if h:
            return h[0]
        time.sleep(1)
    return None


def _find_process_payment_btn(hwnd, timeout=15):
    for _ in range(timeout):
        try:
            ids_win = Desktop(backend='uia').window(handle=hwnd)
            btn = (ids_win
                   .child_window(auto_id="PerseusPayControl")
                   .child_window(auto_id="webViewBrowser")
                   .child_window(title_re="PROCESS PAYMENT.*", control_type="Button"))
            btn.wait('exists enabled visible', timeout=1)
            return btn
        except Exception:
            time.sleep(1)
    return None
