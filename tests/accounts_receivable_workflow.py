"""
Workflow: Launch G2 → Login → Navigator → Accounting → Accounts Receivable
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from pywinauto import Application, findwindows
from pywinauto.keyboard import send_keys
import time
import ctypes
import ctypes.wintypes
import subprocess
import logging

# Setup logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('workflow_errors.log'),
        logging.StreamHandler()
    ]
)

print("=" * 70)
print("Accounts Receivable Workflow")
print("=" * 70)

G2_EXE = r"C:\IDSASTRA\APPS\G2\G2CLIENT\IdsG2Client.exe"

# # ── Step 1: Launch G2 ────────────────────────────────────────────────────────
print("\n[1] Launching G2 application...")
import os
result = ctypes.windll.shell32.ShellExecuteW(
    None, "open", G2_EXE, None, os.path.dirname(G2_EXE), 1
)
if result <= 32:
    print(f"  ERROR: ShellExecute failed with code {result} — aborting")
    exit(1)
print(f"  Launched: {G2_EXE}")

# ── Step 2: Wait for G2 Login window ─────────────────────────────────────────
print("\n[2] Waiting for G2 Login window (up to 30s)...")
login_hwnd = None
for i in range(30):
    handles = findwindows.find_windows(title="G2 Login")
    if handles:
        login_hwnd = handles[0]
        print(f"  Found after {i}s")
        break
    print(f"  Waiting... ({i}s)   ", end="\r")
    time.sleep(1)

if not login_hwnd:
    print("\n  ERROR: G2 Login window did not appear after 30s — aborting")
    exit(1)

ctypes.windll.user32.ShowWindow(login_hwnd, 9)
ctypes.windll.user32.SetForegroundWindow(login_hwnd)
ctypes.windll.user32.BringWindowToTop(login_hwnd)
time.sleep(0.5)
print("  OK - G2 Login window activated")

app_login = Application(backend='uia').connect(handle=login_hwnd)
login_win = app_login.window(handle=login_hwnd)

# ── Step 3: Enter username ────────────────────────────────────────────────────
print("\n[3] Entering username 'aqadir.ids'...")
try:
    txt_user_pane = login_win.child_window(auto_id="txtUser", control_type="Pane")
    txt_user_pane.wait('exists visible', timeout=10)
    user_field = txt_user_pane.child_window(control_type="Custom")
    user_field.click_input()
    time.sleep(0.2)
    send_keys('^a')
    time.sleep(0.1)
    send_keys('aqadir.ids')
    print("  OK - Entered username")
    time.sleep(0.3)
except Exception as e:
    print(f"  ERROR: {e}")
    import traceback; traceback.print_exc()
    exit(1)

# ── Step 4: Enter password ────────────────────────────────────────────────────
print("\n[4] Entering password...")
try:
    txt_pwd_pane = login_win.child_window(auto_id="txtPwd", control_type="Pane")
    txt_pwd_pane.wait('exists visible', timeout=10)
    pwd_field = txt_pwd_pane.child_window(control_type="Custom")
    pwd_field.click_input()
    time.sleep(0.2)
    send_keys('^a')
    time.sleep(0.1)
    send_keys('Aqadir2801')
    print("  OK - Entered password")
    time.sleep(0.3)
except Exception as e:
    print(f"  ERROR: {e}")
    import traceback; traceback.print_exc()
    exit(1)

# ── Step 5: Click Login ───────────────────────────────────────────────────────
print("\n[5] Clicking Login button...")
try:
    login_btn = login_win.child_window(auto_id="btnLogin", control_type="Button")
    login_btn.wait('exists enabled visible', timeout=10)
    login_btn.click_input()
    print("  OK - Clicked Login")
except Exception as e:
    print(f"  ERROR: {e}")
    import traceback; traceback.print_exc()
    exit(1)

# ── Step 6: Wait for G2 Navigator ────────────────────────────────────────────
print("\n[6] Waiting for G2 Navigator window (up to 60s)...")
nav_hwnd = None
for i in range(60):
    handles = findwindows.find_windows(title_re=".*Navigator.*")
    if handles:
        nav_hwnd = handles[0]
        print(f"  Found after {i}s")
        break
    print(f"  Waiting... ({i}s)   ", end="\r")
    time.sleep(1)

if not nav_hwnd:
    print("\n  ERROR: G2 Navigator not found after 60s — aborting")
    exit(1)

ctypes.windll.user32.ShowWindow(nav_hwnd, 3)        # SW_MAXIMIZE
ctypes.windll.user32.SetForegroundWindow(nav_hwnd)
ctypes.windll.user32.BringWindowToTop(nav_hwnd)
time.sleep(0.5)
print("  OK - G2 Navigator activated")

app_nav = Application(backend='uia').connect(handle=nav_hwnd)
nav_win = app_nav.window(handle=nav_hwnd)

# ── Step 7: Click Accounting ──────────────────────────────────────────────────
print("\n[7] Clicking Accounting button...")
try:
    accounting_btn = nav_win.child_window(auto_id="btnAccounting", control_type="Button")
    accounting_btn.wait('exists enabled visible', timeout=10)
    accounting_btn.click_input()
    print("  OK - Clicked Accounting")
    time.sleep(1)
except Exception as e:
    print(f"  ERROR: {e}")
    import traceback; traceback.print_exc()
    exit(1)

# ── Step 8: Click Accounts Receivable ────────────────────────────────────────
print("\n[8] Clicking Accounts Receivable...")
try:
    ar_btn = nav_win.child_window(title="Accounts Receivable", control_type="Button")
    ar_btn.wait('exists enabled visible', timeout=10)
    ar_btn.click_input()
    print("  OK - Clicked Accounts Receivable")
    time.sleep(1)
except Exception as e:
    print(f"  ERROR: {e}")
    import traceback; traceback.print_exc()
    exit(1)

# ── Step 9: Click Take Customer Deposits ─────────────────────────────────────
print("\n[9] Clicking Take Customer Deposits...")
try:
    deposits_btn = nav_win.child_window(title="Take Customer Deposits", control_type="Button")
    deposits_btn.wait('exists enabled visible', timeout=10)
    deposits_btn.click_input()
    print("  OK - Clicked Take Customer Deposits")
    time.sleep(1)
except Exception as e:
    print(f"  ERROR: {e}")
    import traceback; traceback.print_exc()
    exit(1)

# ── Step 10: Wait for Customer Deposits window ───────────────────────────────
print("\n[10] Waiting for Customer Deposits window (up to 30s)...")
deposits_hwnd = None
for i in range(30):
    handles = findwindows.find_windows(title_re=".*Customer Deposits.*")
    if handles:
        deposits_hwnd = handles[0]
        print(f"  Found after {i}s")
        break
    print(f"  Waiting... ({i}s)   ", end="\r")
    time.sleep(1)

if not deposits_hwnd:
    print("\n  ERROR: Customer Deposits window not found after 30s — aborting")
    exit(1)

ctypes.windll.user32.ShowWindow(deposits_hwnd, 9)
ctypes.windll.user32.SetForegroundWindow(deposits_hwnd)
ctypes.windll.user32.BringWindowToTop(deposits_hwnd)
time.sleep(0.5)
print("  OK - Customer Deposits window activated")

# Wait for window content to fully load by polling for an Edit field inside it
print("  Waiting for window content to load...")
app_dep = Application(backend='uia').connect(handle=deposits_hwnd)
dep_win = app_dep.window(handle=deposits_hwnd)
for i in range(30):
    try:
        edits = dep_win.descendants(control_type="Edit", class_name="Edit")
        if edits:
            print(f"  Content ready after {i}s ({len(edits)} Edit field(s) found)")
            break
    except Exception:
        pass
    print(f"  Waiting for content... ({i}s)   ", end="\r")
    time.sleep(1)
else:
    print("\n  ERROR: Window content did not load after 30s — aborting")
    exit(1)

# ── Step 11: Enter 4268 and press Tab ────────────────────────────────────────
print("\n[11] Entering customer number 4268...")
try:
    send_keys('4268')
    time.sleep(0.2)
    send_keys('{TAB}')
    print("  OK - Entered 4268 and pressed Tab")
    time.sleep(1)
except Exception as e:
    print(f"  ERROR: {e}")
    import traceback; traceback.print_exc()
    exit(1)

# ── Step 12: Click asCommandCtlClassU button ─────────────────────────────────
print("\n[12] Clicking command button (asCommandCtlClassU)...")
try:
    app_dep = Application(backend='uia').connect(handle=deposits_hwnd)
    dep_win = app_dep.window(handle=deposits_hwnd)

    all_btns = dep_win.descendants(class_name="asCommandCtlClassU", control_type="Pane")
    if not all_btns:
        raise Exception("No asCommandCtlClassU buttons found")
    print(f"  Found {len(all_btns)} button(s) — clicking first")
    all_btns[0].click_input()
    print("  OK - Clicked command button")
    time.sleep(1)
except Exception as e:
    print(f"  ERROR: {e}")
    import traceback; traceback.print_exc()
    exit(1)

# ── Step 13: Enter random description ────────────────────────────────────────
print("\n[13] Entering description...")
try:
    import random, string
    description = "Deposit-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    print(f"  Generated description: {description}")

    all_edits = dep_win.descendants(control_type="Edit", class_name="Edit")
    print(f"  Found {len(all_edits)} Edit field(s)")

    # Find the "Description" label and pick the Edit nearest to its right
    target_edit = None
    try:
        desc_label = dep_win.child_window(title="Description:", control_type="Pane")
        lbl_rect = desc_label.rectangle()
        print(f"  Description label rect: {lbl_rect}")
        lbl_cy = (lbl_rect.top + lbl_rect.bottom) / 2

        best_dist = float('inf')
        for ed in all_edits:
            r = ed.rectangle()
            v_diff = abs((r.top + r.bottom) / 2 - lbl_cy)
            h_dist = r.left - lbl_rect.right
            if v_diff < 20 and h_dist >= 0 and h_dist < best_dist:
                best_dist = h_dist
                target_edit = ed
        if target_edit:
            print(f"  Found Description field at {target_edit.rectangle()}")
    except Exception as e:
        print(f"  Label search failed: {e}")

    if not target_edit:
        # Fallback: pick the Edit with the greatest width (Description is the widest)
        target_edit = max(all_edits, key=lambda e: e.rectangle().width())
        print(f"  Using widest Edit field: {target_edit.rectangle()}")

    target_edit.click_input()
    time.sleep(0.2)
    send_keys('^a')
    time.sleep(0.1)
    send_keys(description)
    print(f"  OK - Entered description: {description}")
    time.sleep(0.3)
except Exception as e:
    print(f"  ERROR: {e}")
    import traceback; traceback.print_exc()
    exit(1)

# ── Step 14: Enter random amount ─────────────────────────────────────────────
print("\n[14] Entering random amount...")
try:
    amount = str(random.randint(100, 9999))
    print(f"  Generated amount: {amount}")

    # Find the "Amount:" label and pick the Edit nearest to its right
    target_edit = None
    try:
        amount_label = dep_win.child_window(title="Amount:", control_type="Pane")
        lbl_rect = amount_label.rectangle()
        print(f"  Amount label rect: {lbl_rect}")
        lbl_cy = (lbl_rect.top + lbl_rect.bottom) / 2

        all_edits = dep_win.descendants(control_type="Edit", class_name="Edit")
        best_dist = float('inf')
        for ed in all_edits:
            r = ed.rectangle()
            v_diff = abs((r.top + r.bottom) / 2 - lbl_cy)
            h_dist = r.left - lbl_rect.right
            if v_diff < 20 and h_dist >= 0 and h_dist < best_dist:
                best_dist = h_dist
                target_edit = ed
        if target_edit:
            print(f"  Found Amount field at {target_edit.rectangle()}")
    except Exception as e:
        print(f"  Label search failed: {e}")

    if not target_edit:
        print("  ERROR: Could not find Amount field — aborting")
        exit(1)

    target_edit.click_input()
    time.sleep(0.2)
    send_keys('^a')
    time.sleep(0.1)
    send_keys(amount)
    print(f"  OK - Entered amount: {amount}")
    time.sleep(0.3)
except Exception as e:
    print(f"  ERROR: {e}")
    import traceback; traceback.print_exc()
    exit(1)

# ── Step 15: Click Save ───────────────────────────────────────────────────────
print("\n[15] Clicking Save button...")
try:
    # Navigate directly through the known parent (auto_id="262145") to avoid
    # a slow full-tree search that can time out on large windows
    toolbar_container = dep_win.child_window(auto_id="262145", control_type="Text")
    toolbar = toolbar_container.child_window(control_type="ToolBar")
    save_btn = toolbar.child_window(title="Save", control_type="Button")
    save_btn.click_input()
    print("  OK - Clicked Save")
    time.sleep(1)
except Exception as e:
    print(f"  ERROR: {e}")
    import traceback; traceback.print_exc()
    exit(1)


    # Step 7: Click Credit button in Take Payment window
print("\n[7] Waiting for Take Payment window...")
payment_hwnd = None
for i in range(30):
    handles = findwindows.find_windows(title_re=".*Take Payment.*")
    if handles:
        payment_hwnd = handles[0]
        print(f"  Found Take Payment window after {i}s")
        break
    print(f"  Waiting... ({i}s)   ", end="\r")
    time.sleep(1)

if not payment_hwnd:
    print("\n  ERROR: Take Payment window not found after 30s — aborting")
    exit(1)

try:
    app_uia = Application(backend='uia').connect(handle=payment_hwnd)
    payment_window = app_uia.window(handle=payment_hwnd)

    credit_btn = None
    for spec in [
        {"auto_id": "btnCredit", "control_type": "Button"},
        {"title": "Credit", "control_type": "Button"},
        {"title_re": ".*[Cc]redit.*", "control_type": "Button"},
    ]:
        try:
            btn = payment_window.child_window(**spec)
            btn.wait('exists enabled visible', timeout=2)
            credit_btn = btn
            print(f"  Found Credit button via {spec}")
            break
        except Exception:
            pass

    if not credit_btn:
        print("  ERROR: Credit button not found — aborting")
        exit(1)

    credit_btn.click_input()
    print("  OK - Clicked Credit button")
    time.sleep(0.5)

except Exception as e:
    print(f"  ERROR: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
    logger.error(f"Error in Credit button click: {e}", exc_info=True)

# logger.info("Credit button click attempt completed - moving to next step")


print("\n[8] Waiting for IDSPay window to load (up to 30 seconds)...")
# logger.info("Step 8: Waiting for IDSPay window to open")
idspay_window = None

IDSPAY_TIMEOUT = 30   # seconds to keep polling
IDSPAY_POLL    = 1    # seconds between each check

def _get_window_title(hwnd):
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
    buf = ctypes.create_unicode_buffer(length + 1)
    ctypes.windll.user32.GetWindowTextW(hwnd, buf, length + 1)
    return buf.value

def _is_idspay(title):
    return (
        any(kw in title for kw in ['IdsG2', 'IDSPay', 'Card', 'Pay', 'Payment'])
        and not any(skip in title for skip in ['Take Payment', 'Accounts Receivable', 'Navigator'])
    )

elapsed = 0
while elapsed < IDSPAY_TIMEOUT:
    for hwnd in findwindows.find_windows(title_re=r".*[Pp]ay.*") + \
                findwindows.find_windows(title_re=r".*[Cc]ard.*"):
        try:
            title = _get_window_title(hwnd)
            if _is_idspay(title):
                idspay_window = hwnd
                break
        except Exception:
            pass
    if idspay_window:
        break
    print(f"  Waiting... ({elapsed}s elapsed)", end="\r")
    time.sleep(IDSPAY_POLL)
    elapsed += IDSPAY_POLL

if not idspay_window:
    # logger.warning("IDSPay window not found after %ds", IDSPAY_TIMEOUT)
    print(f"\n  WARNING: IDSPay window not found after {IDSPAY_TIMEOUT}s")
else:
    print(f"\n  IDSPay window detected after ~{elapsed}s.")

from pywinauto import Desktop

def _click_by_title(title_re, control_type, timeout=60, description="element"):
    """
    Poll Desktop UIA tree until an element matching title_re + control_type appears,
    then click it. Returns True on success.
    """
    print(f"  Waiting for {description} to appear (up to {timeout}s)...")
    for i in range(timeout):
        try:
            d = Desktop(backend='uia')
            el = d.window(title_re=title_re, control_type=control_type)
            el.wait('exists enabled visible', timeout=1)
            el.click_input()
            print(f"  Found and clicked after {i}s")
            return True
        except Exception:
            print(f"  Waiting... ({i}s)   ", end="\r")
            time.sleep(1)
    print(f"\n  WARNING: {description} not found after {timeout}s")
    return False

def _coord_click(hwnd, x_pct, y_pct, label=""):
    """Click at (x_pct, y_pct) relative to hwnd's bounding rect."""
    import ctypes.wintypes
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
    win_w = rect.right - rect.left
    win_h = rect.bottom - rect.top

    rel_x = int(win_w * x_pct)
    rel_y = int(win_h * y_pct)
    print(f"  Coordinate click {label} at rel ({rel_x}, {rel_y}) — window {rect.left},{rect.top} {win_w}x{win_h}")

    # Use pywinauto click_input with relative coords — handles DPI correctly
    app = Application(backend='uia').connect(handle=hwnd)
    win = app.window(handle=hwnd)
    win.click_input(coords=(rel_x, rel_y))
    print(f"  OK - Coordinate click sent")

def _wait_for_idspay_hwnd(timeout=60):
    """Poll until a window with title 'IDSPay' appears, up to timeout seconds."""
    print(f"  Waiting for IDSPay window (up to {timeout}s)...")
    for i in range(timeout):
        handles = findwindows.find_windows(title="IDSPay")
        if handles:
            hwnd = handles[0]
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
            print(f"  Found after {i}s — rect: {rect.left},{rect.top} size {rect.right-rect.left}x{rect.bottom-rect.top}")
            return hwnd
        print(f"  Waiting... ({i}s)   ", end="\r")
        time.sleep(1)
    print(f"\n  WARNING: IDSPay window not found after {timeout}s")
    return None

def _find_process_payment_btn(hwnd, timeout=15):
    """
    Navigate the UIA tree through the known WebView2 hierarchy to find
    the PROCESS PAYMENT button, polling until it appears.
    Returns the element or None.
    """
    print(f"  Searching for PROCESS PAYMENT button (up to {timeout}s)...")
    for i in range(timeout):
        try:
            app = Application(backend='uia').connect(handle=hwnd)
            ids_win = app.window(handle=hwnd)
            # Navigate step-by-step through the known auto_id hierarchy
            perseus = ids_win.child_window(auto_id="PerseusPayControl")
            webview = perseus.child_window(auto_id="webViewBrowser")
            btn = webview.child_window(title_re="PROCESS PAYMENT.*", control_type="Button")
            btn.wait('exists enabled visible', timeout=1)
            print(f"  Found PROCESS PAYMENT button after {i}s")
            return btn
        except Exception:
            print(f"  Searching... ({i}s)   ", end="\r")
            time.sleep(1)
    print(f"\n  Button not found via UIA after {timeout}s")
    return None

# Step 9: Click SAVED CARDS tab
print("\n[9] Clicking SAVED CARDS tab in IDSPay...")
idspay_hwnd = _wait_for_idspay_hwnd(timeout=60)
if idspay_hwnd:
    # Window appears early but web content takes 30-40s to fully render
    CONTENT_LOAD_WAIT = 40
    for i in range(CONTENT_LOAD_WAIT, 0, -1):
        print(f"  Waiting for web content to load... {i}s remaining   ", end="\r")
        time.sleep(1)
    print(f"\n  Web content wait done — clicking SAVED CARDS tab")
    _coord_click(idspay_hwnd, 0.58, 0.16, "SAVED CARDS tab")

    # Wait for SAVED CARDS content to render before proceeding
    print("  Waiting 5s for SAVED CARDS content to render...")
    time.sleep(5)
else:
    print("  Skipping - IDSPay window not found")

# Step 10: Click PROCESS PAYMENT button
print("\n[10] Clicking PROCESS PAYMENT button...")
idspay_hwnd = _wait_for_idspay_hwnd(timeout=10)
if idspay_hwnd:
    btn = _find_process_payment_btn(idspay_hwnd, timeout=15)
    if btn:
        btn.click_input()
        print("  OK - Clicked PROCESS PAYMENT")
    else:
        print("  Falling back to coordinate click...")
        _coord_click(idspay_hwnd, 0.50, 0.82, "PROCESS PAYMENT button")
else:
    print("  Skipping - IDSPay window not found")


# ── Step 11: Wait for payment to complete (IDSPay window closes) ─────────────
print("\n[11] Waiting for payment to complete (IDSPay window to close, up to 60s)...")
for i in range(60):
    handles = findwindows.find_windows(title="IDSPay")
    if not handles:
        print(f"  Payment completed after ~{i}s — IDSPay window closed")
        break
    print(f"  Processing... ({i}s)   ", end="\r")
    time.sleep(1)
else:
    print("\n  ERROR: IDSPay window did not close after 60s — aborting")
    exit(1)

time.sleep(1)

# ── Step 12: Click Row 0 hyperlink in dgvCurrentPayments grid ────────────────
print("\n[12] Clicking Row 0 in payment results grid (dgvCurrentPayments)...")
try:
    payment_handles = findwindows.find_windows(title_re=".*Take Payment.*")
    if not payment_handles:
        print("  ERROR: Take Payment window not found — aborting")
        exit(1)

    app_tp = Application(backend='uia').connect(handle=payment_handles[0])
    tp_win = app_tp.window(handle=payment_handles[0])

    # Bring window to foreground
    ctypes.windll.user32.ShowWindow(payment_handles[0], 9)
    ctypes.windll.user32.SetForegroundWindow(payment_handles[0])
    time.sleep(0.3)

    # Find the payments grid table
    dgv = tp_win.child_window(auto_id="dgvCurrentPayments", control_type="Table")
    dgv.wait('exists visible', timeout=10)

    # Find the Row 0 hyperlink inside the grid
    row0 = dgv.child_window(title=" Row 0", control_type="Hyperlink")
    row0.wait('exists enabled visible', timeout=10)
    row0.click_input()
    print("  OK - Clicked Row 0 in dgvCurrentPayments")
    time.sleep(1)

except Exception as e:
    print(f"  ERROR: {e}")
    import traceback; traceback.print_exc()
    exit(1)

# ── Step 13: Click Yes in Reverse Payment dialog ──────────────────────────────
print("\n[13] Waiting for Reverse Payment dialog and clicking Yes...")
reverse_hwnd = None
for i in range(30):
    handles = findwindows.find_windows(title_re=".*Reverse Payment.*")
    if handles:
        reverse_hwnd = handles[0]
        print(f"  Found Reverse Payment dialog after {i}s")
        break
    print(f"  Waiting... ({i}s)   ", end="\r")
    time.sleep(1)

if not reverse_hwnd:
    print("\n  ERROR: Reverse Payment dialog not found after 30s — aborting")
    exit(1)

try:
    ctypes.windll.user32.SetForegroundWindow(reverse_hwnd)
    ctypes.windll.user32.BringWindowToTop(reverse_hwnd)
    time.sleep(0.3)

    app_rev = Application(backend='uia').connect(handle=reverse_hwnd)
    rev_win = app_rev.window(handle=reverse_hwnd)

    yes_btn = rev_win.child_window(auto_id="6", control_type="Button", title="Yes")
    yes_btn.wait('exists enabled visible', timeout=10)
    yes_btn.click_input()
    print("  OK - Clicked Yes in Reverse Payment dialog")
    time.sleep(1)

except Exception as e:
    print(f"  ERROR: {e}")
    import traceback; traceback.print_exc()
    exit(1)


print("\n" + "=" * 70)
print("Workflow complete")
print("=" * 70)
