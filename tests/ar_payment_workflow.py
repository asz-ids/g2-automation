"""
Complete workflow: Enter customer 4268, Tab, wait for table, click Pay checkbox, click Accept Payment
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from screens.navigator_screen import NavigatorScreen
from pywinauto import Desktop, findwindows
from pywinauto.keyboard import send_keys
import time
import ctypes
import ctypes.wintypes
import subprocess
import logging
import re

# Setup logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('workflow_errors.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

print("=" * 70)
print("Complete AR Payment Workflow")
print("=" * 70)

G2_EXE = r"C:\IDSASTRA\APPS\G2\G2CLIENT\IdsG2Client.exe"

# Step 0: Launch G2 (skip if Navigator is already open)
print("\n[0] Checking if G2 is already running...")
import os
_already_running = bool(findwindows.find_windows(title_re=".*Navigator.*"))
login_hwnd = None

if _already_running:
    print("  G2 Navigator already open — skipping launch and login")
else:
    print("  Launching G2 application...")
    result = ctypes.windll.shell32.ShellExecuteW(
        None,       # hwnd
        "open",     # verb
        G2_EXE,     # file
        None,       # parameters
        os.path.dirname(G2_EXE),  # working directory
        1           # SW_SHOWNORMAL
    )
    if result <= 32:
        print(f"  ERROR: ShellExecute failed with code {result} — aborting")
        exit(1)
    print(f"  Launched: {G2_EXE}")

    print("  Waiting for G2 Login window (up to 30s)...")
    for i in range(30):
        handles = findwindows.find_windows(title="G2 Login")
        if handles:
            login_hwnd = handles[0]
            print(f"  G2 Login window found after {i}s")
            break
        print(f"  Waiting... ({i}s)   ", end="\r")
        time.sleep(1)

    if not login_hwnd:
        print("\n  ERROR: G2 Login window did not appear after 30s — aborting")
        exit(1)

    ctypes.windll.user32.ShowWindow(login_hwnd, 9)       # SW_RESTORE
    ctypes.windll.user32.SetForegroundWindow(login_hwnd)
    ctypes.windll.user32.BringWindowToTop(login_hwnd)
    time.sleep(0.5)
if not _already_running:
    print("  OK - G2 Login window activated")

# Steps 0b-0d: Login (skipped if G2 already running)
if not _already_running:
    # Step 0b: Enter username
    print("\n[0b] Entering username 'aqadir.ids'...")
    try:
        login_win = Desktop(backend='uia').window(handle=login_hwnd)
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
        print(f"  ERROR: Could not enter username: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

    # Step 0c: Enter password
    print("\n[0c] Entering password...")
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
        print(f"  ERROR: Could not enter password: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

    # Step 0d: Click Login button
    print("\n[0d] Clicking Login button...")
    try:
        login_btn = login_win.child_window(auto_id="btnLogin", control_type="Button")
        login_btn.wait('exists enabled visible', timeout=10)
        login_btn.click_input()
        print("  OK - Clicked Login")
        time.sleep(3)
    except Exception as e:
        print(f"  ERROR: Could not click Login: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

# Step 1: Navigate to Take AR Payments
print("\n[1] Navigate to Take AR Payments...")

# Poll for Navigator window — login can take 10-30s to fully load
print("  Waiting for G2 Navigator window (up to 60s)...")
nav_hwnd = None
for i in range(60):
    handles = findwindows.find_windows(title_re=".*Navigator.*")
    if handles:
        nav_hwnd = handles[0]
        print(f"  Navigator window found after {i}s")
        break
    print(f"  Waiting... ({i}s)   ", end="\r")
    time.sleep(1)

if not nav_hwnd:
    print("\n  ERROR: G2 Navigator window not found after 60s — aborting")
    exit(1)

ctypes.windll.user32.ShowWindow(nav_hwnd, 9)        # SW_RESTORE — un-minimise if needed
ctypes.windll.user32.SetForegroundWindow(nav_hwnd)
ctypes.windll.user32.BringWindowToTop(nav_hwnd)
time.sleep(0.5)
print("  Navigator window activated")

# Click the Parts button by auto_id (title is empty — text search won't work)
desktop = Desktop(backend='uia')
nav_win_uia = desktop.window(handle=nav_hwnd)

try:
    parts_btn_uia = nav_win_uia.child_window(auto_id='btnParts', control_type='Button')
    parts_btn_uia.click_input()
    print("  [OK] Clicked Parts menu (auto_id=btnParts)")
except Exception as e:
    print(f"  [!] Could not click Parts button: {e}")

time.sleep(2)  # give panel time to expand

# Record existing AR windows before clicking — we want the NEW one G2 opens
existing_ar_handles = set(findwindows.find_windows(title_re=".*Accounts Receivable.*"))

# Click Take AR Payments by auto_id
ar_clicked = False
try:
    ar_btn_uia = nav_win_uia.child_window(auto_id='btnTakeARPayments', control_type='Button')
    ar_btn_uia.click_input()
    print("  [OK] Clicked Take AR Payments (auto_id=btnTakeARPayments)")
    ar_clicked = True
except Exception:
    pass

if not ar_clicked:
    # Fallback: search by title text (in case auto_id differs)
    try:
        ar_btn_uia = nav_win_uia.child_window(title='Take AR Payments', control_type='Button')
        ar_btn_uia.click_input()
        print("  [OK] Clicked Take AR Payments (title match)")
        ar_clicked = True
    except Exception as e:
        print(f"  [!] Take AR Payments button not found: {e}")

# Step 2: Find the correct AR Payment window
# Strategy: prefer a NEW window (not in existing_ar_handles), fall back to foreground window
print("\n[2] Waiting for AR Payment window (up to 20s)...")
ar_hwnd = None
AR_TITLE_RE = ".*Accounts Receivable.*"

for i in range(20):
    current_ar = set(findwindows.find_windows(title_re=AR_TITLE_RE))
    new_ar = current_ar - existing_ar_handles
    if new_ar:
        ar_hwnd = list(new_ar)[0]
        print(f"  New AR window found after {i}s: HWND {ar_hwnd}")
        break

    # Fallback: use the foreground window if it's an AR window
    fg = ctypes.windll.user32.GetForegroundWindow()
    if fg in current_ar:
        ar_hwnd = fg
        print(f"  Foreground AR window found after {i}s: HWND {ar_hwnd}")
        break

    print(f"  Waiting... ({i}s)   ", end="\r")
    time.sleep(1)

if not ar_hwnd:
    # Last resort: use any existing AR window (G2 may reuse the existing one)
    handles = findwindows.find_windows(title_re=AR_TITLE_RE)
    if handles:
        ar_hwnd = handles[0]
        print(f"  Using existing AR window: HWND {ar_hwnd}")
    else:
        print("  ERROR: Could not find AR Payment window")
        exit(1)

# Bring it to front
ctypes.windll.user32.ShowWindow(ar_hwnd, 9)
ctypes.windll.user32.SetForegroundWindow(ar_hwnd)
ctypes.windll.user32.BringWindowToTop(ar_hwnd)
time.sleep(0.5)
print(f"  OK - Using AR window HWND {ar_hwnd}")

# Step 3: Enter customer number 4268
# Must click the inner Edit child (not the parent Pane) before type_keys —
# clicking the Pane does not transfer focus to the Edit, so keystrokes land elsewhere.
print("\n[3] Entering customer number 4268...")

ar_win_uia = Desktop(backend='uia').window(handle=ar_hwnd)

# Strategy: find the Customer # label then take its immediately preceding sibling
# in win.children() — that sibling is always the ATLVPTextBoxClass31U input container.
# Y-proximity alone fails because Customer # and Payment Date sit on the same row.
customer_edit = None
try:
    all_children = list(ar_win_uia.children())
    label_idx = None
    for i, child in enumerate(all_children):
        try:
            if child.window_text() == 'Customer #':
                label_idx = i
                break
        except Exception:
            pass

    if label_idx is None:
        raise RuntimeError("'Customer #' label not found in window children")

    # Walk backwards from the label to find the closest ATLVPTextBoxClass31U sibling
    customer_pane = None
    for j in range(label_idx - 1, max(label_idx - 5, -1), -1):
        try:
            cls = all_children[j].element_info.class_name
            if 'TextBox' in cls:
                customer_pane = all_children[j]
                break
        except Exception:
            pass

    if customer_pane is None:
        raise RuntimeError("No TextBox sibling found before 'Customer #' label")

    edits = customer_pane.descendants(class_name='Edit')
    if not edits:
        raise RuntimeError("No Edit child inside Customer # TextBox pane")
    customer_edit = edits[0]

except Exception as e:
    print(f"  ERROR locating Customer # Edit: {e}")
    exit(1)

ctypes.windll.user32.SetForegroundWindow(ar_hwnd)
ctypes.windll.user32.BringWindowToTop(ar_hwnd)
time.sleep(3)   # let VB6 controls fully initialise before any keyboard input
r = customer_edit.rectangle()
print(f"  Customer # Edit rect: {r}")
customer_edit.click_input()
time.sleep(0.5)
customer_edit.type_keys('4268', with_spaces=True)

# Verify text was actually entered
WM_GETTEXT       = 0x000D
WM_GETTEXTLENGTH = 0x000E
edit_hwnd = customer_edit.handle
buf_len = ctypes.windll.user32.SendMessageW(edit_hwnd, WM_GETTEXTLENGTH, 0, 0)
buf = ctypes.create_unicode_buffer(buf_len + 2)
ctypes.windll.user32.SendMessageW(edit_hwnd, WM_GETTEXT, buf_len + 1, buf)
actual = buf.value.strip()
if actual != '4268':
    print(f"  ERROR: Customer # field contains {actual!r}, expected '4268'")
    exit(1)
print(f"  [OK] Customer # = {actual!r}")

# Step 4: Press Tab to trigger customer lookup
print("\n[4] Pressing Tab to trigger lookup...")
customer_edit.type_keys('{TAB}')
time.sleep(0.5)

# Step 5: Wait for table to load then verify Balance is positive
print("\n[5] Waiting for table to load...")
ar_win = Desktop(backend='uia').window(handle=ar_hwnd)

# Poll until the VSFlexGrid8N table is visible — use class_name to avoid
# ambiguity from the 11 generic Table elements inside the AR window.
table = None
for i in range(30):
    try:
        tbl = ar_win.child_window(class_name='VSFlexGrid8N')
        tbl.wait('exists visible', timeout=1)
        table = tbl
        print(f"\n  Table loaded after {i}s")
        break
    except Exception:
        print(f"  Waiting for table... ({i}s)   ", end="\r")
        time.sleep(1)

if not table:
    print("\n  ERROR: Table did not load after 30s — aborting")
    exit(1)

# Verify table has at least one data row
data_rows = table.children(control_type="Custom")
if not data_rows:
    print("  ERROR: Table loaded but has no invoice rows — customer may have no open invoices")
    exit(1)
print(f"  [OK] Table has {len(data_rows)} invoice row(s)")

# Click Balance header to sort
print("  Clicking Balance column header to sort...")
try:
    balance_header = next(
        h for h in table.children(control_type="Header")
        if h.window_text().strip() == "Balance"
    )
    time.sleep(1)
    balance_header.click_input()
    print("  OK - Clicked Balance header")
    time.sleep(2)
    balance_header.click_input()
    print("  OK - 2nd click Balance header (sort descending)")
    time.sleep(1)
except Exception as e:
    print(f"  WARNING: Could not click Balance header: {e}")

# Tab after sorting to move focus back into the grid
send_keys('{TAB}')
time.sleep(0.5)
print("  Pressed Tab after sort")

send_keys('{SPACE}')
time.sleep(0.5)
print("  Pressed SPACE after Tab to select first invoice")

send_keys('{TAB}')  
time.sleep(2.5)
print("  Pressed Tab again to move to Pay Amount column")

send_keys('{SPACE}')
time.sleep(1.5)
print("To Edit Pay Amount")

send_keys('^a')
time.sleep(0.5)
print("CTRL A Select ALL in Pay Amount")

send_keys("100{TAB}")
time.sleep(0.5)
print("Entered 100 in Pay Amount and pressed TAB")

send_keys('%a')
time.sleep(1.5)
print("Pressed Alt+A")

send_keys('{SPACE}')
time.sleep(0.5)
print("Pressed SPACE to click Accept Payment button")


# Step 7: Wait for Take Payment window (may also appear as "Take Credit Card Payment")
print("\n[7] Waiting for Take Payment window...")
payment_hwnd = None
TAKE_PAY_RE = r".*Take Payment.*|.*Take Credit Card.*|.*Credit Card Payment.*"
for i in range(30):
    handles = findwindows.find_windows(title_re=TAKE_PAY_RE)
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
    payment_window = Desktop(backend='uia').window(handle=payment_hwnd)

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

logger.info("Credit button click attempt completed - moving to next step")


print("\n[8] Waiting for IDSPay window to load (up to 30 seconds)...")
logger.info("Step 8: Waiting for IDSPay window to open")
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
    logger.warning("IDSPay window not found after %ds", IDSPAY_TIMEOUT)
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

    Desktop(backend='uia').window(handle=hwnd).click_input(coords=(rel_x, rel_y))
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
            ids_win = Desktop(backend='uia').window(handle=hwnd)
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
