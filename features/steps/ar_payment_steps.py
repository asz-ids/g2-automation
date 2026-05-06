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

@when('I navigate to "{menu_item}" from the Parts menu')
def step_navigate(context, menu_item):
    s = context.s
    nav_win = Desktop(backend='uia').window(handle=s.nav_hwnd)
    nav_win.child_window(auto_id='btnParts', control_type='Button').click_input()
    time.sleep(2)

    s.existing_ar_handles = set(
        findwindows.find_windows(title_re=".*Accounts Receivable.*")
    )

    auto_id_map = {"Take AR Payments": "btnTakeARPayments"}
    auto_id = auto_id_map.get(menu_item)
    clicked = False
    if auto_id:
        try:
            nav_win.child_window(auto_id=auto_id, control_type='Button').click_input()
            clicked = True
        except Exception:
            pass
    if not clicked:
        nav_win.child_window(title=menu_item, control_type='Button').click_input()


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

    else:
        for _ in range(30):
            h = findwindows.find_windows(title_re=f".*{window_title}.*")
            if h:
                hwnd = h[0]
                break
            time.sleep(1)
        assert hwnd, f'"{window_title}" window did not open within 30s'

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
    else:
        raise AssertionError(f'No handler for button "{button_label}"')


# ── Helpers ───────────────────────────────────────────────────────────────────

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
