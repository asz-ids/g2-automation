"""
Workflow: Open G2 Navigator, click Accounting, then click Update Payable Invoices
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from pywinauto import Application, findwindows
import time
import ctypes
import ctypes.wintypes
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
logger = logging.getLogger(__name__)

print("=" * 70)
print("Update Payable Invoices Workflow")
print("=" * 70)

# Step 1: Find and activate G2 Navigator window
print("\n[1] Finding and activating G2 Navigator window...")
nav_handles = findwindows.find_windows(title="G2 Navigator")
if not nav_handles:
    nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
if not nav_handles:
    print("  ERROR: G2 Navigator window not found — aborting")
    exit(1)

nav_hwnd = nav_handles[0]
ctypes.windll.user32.ShowWindow(nav_hwnd, 3)        # SW_MAXIMIZE
ctypes.windll.user32.SetForegroundWindow(nav_hwnd)
ctypes.windll.user32.BringWindowToTop(nav_hwnd)
time.sleep(0.5)
print("  OK - G2 Navigator maximized and activated")

# Step 2: Click Accounting button (auto_id="btnAccounting")
print("\n[2] Clicking Accounting button...")
try:
    app_uia = Application(backend='uia').connect(handle=nav_hwnd)
    nav_win = app_uia.window(handle=nav_hwnd)

    accounting_btn = nav_win.child_window(auto_id="btnAccounting", control_type="Button")
    accounting_btn.wait('exists enabled visible', timeout=10)
    accounting_btn.click_input()
    print("  OK - Clicked Accounting button")
    time.sleep(1)
except Exception as e:
    print(f"  ERROR: Could not click Accounting button: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Step 3: Click Accounts Receivable button
print("\n[3] Clicking Accounts Receivable...")
try:
    ar_btn = nav_win.child_window(title="Accounts Receivable", control_type="Button")
    ar_btn.wait('exists enabled visible', timeout=10)
    ar_btn.click_input()
    print("  OK - Clicked Accounts Receivable")
    time.sleep(1)
except Exception as e:
    print(f"  ERROR: Could not click Accounts Receivable: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Step 4: Click Update Receivable Invoices
print("\n[4] Clicking Update Receivable Invoices...")
try:
    update_recv_btn = nav_win.child_window(title="Update Receivable Invoices", control_type="Button")
    update_recv_btn.wait('exists enabled visible', timeout=10)
    update_recv_btn.click_input()
    print("  OK - Clicked Update Receivable Invoices")
except Exception as e:
    print(f"  ERROR: Could not click Update Receivable Invoices: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Step 5: Wait for Enter/Update Receivables window to open
print("\n[5] Waiting for Enter/Update Receivables window...")
recv_hwnd = None
for i in range(30):
    handles = findwindows.find_windows(title_re=".*Enter/Update Receivables.*")
    if handles:
        recv_hwnd = handles[0]
        print(f"  Found after {i}s")
        break
    print(f"  Waiting... ({i}s)   ", end="\r")
    time.sleep(1)

if not recv_hwnd:
    print("\n  ERROR: Enter/Update Receivables window not found after 30s — aborting")
    exit(1)

ctypes.windll.user32.ShowWindow(recv_hwnd, 9)       # SW_RESTORE
ctypes.windll.user32.SetForegroundWindow(recv_hwnd)
ctypes.windll.user32.BringWindowToTop(recv_hwnd)
time.sleep(0.5)
print("  OK - Enter/Update Receivables window activated")

# Step 6: Enter 4268 in the Ship To ID field
# 12 Edit fields share auto_id="65535" so we locate the right one by finding
# the "Ship To ID:" label and picking the Edit nearest to its right edge.
print("\n[6] Entering 4268 in Ship To ID field...")
try:
    app_recv = Application(backend='uia').connect(handle=recv_hwnd)
    recv_win = app_recv.window(handle=recv_hwnd)

    # Get screen rect of the "Ship To ID:" label
    label = recv_win.child_window(title="Ship To ID:", control_type="Pane")
    label.wait('exists visible', timeout=10)
    lbl_rect = label.rectangle()
    print(f"  Ship To ID label rect: {lbl_rect}")

    # Find all Edit fields (descendants, not just direct children)
    all_edits = recv_win.descendants(control_type="Edit")
    print(f"  Found {len(all_edits)} Edit fields total")

    lbl_cy = (lbl_rect.top + lbl_rect.bottom) / 2
    best = None
    best_dist = float('inf')
    for ed in all_edits:
        try:
            r = ed.rectangle()
            v_diff = abs((r.top + r.bottom) / 2 - lbl_cy)
            h_dist = r.left - lbl_rect.right
            print(f"    Edit rect: {r}  v_diff={v_diff:.0f}  h_dist={h_dist:.0f}")
            if v_diff < 30 and h_dist >= -10 and h_dist < best_dist:
                best_dist = h_dist
                best = ed
        except Exception:
            pass

    if not best:
        print("  ERROR: Could not find Edit field next to Ship To ID label — aborting")
        exit(1)

    from pywinauto.keyboard import send_keys
    import win32api, win32con, win32gui
    r = best.rectangle()
    cx = (r.left + r.right) // 2
    cy = (r.top + r.bottom) // 2
    print(f"  Found field at rect: {r} — clicking center ({cx}, {cy})")

    # Ensure the recv window is in the foreground before clicking
    ctypes.windll.user32.SetForegroundWindow(recv_hwnd)
    ctypes.windll.user32.BringWindowToTop(recv_hwnd)
    time.sleep(0.5)

    # Find the HWND under the screen coords
    target_hwnd = win32gui.WindowFromPoint((cx, cy))
    print(f"  HWND at click point: {target_hwnd}")

    # Convert screen coords to CLIENT coords relative to target_hwnd
    pt = ctypes.wintypes.POINT(cx, cy)
    ctypes.windll.user32.ScreenToClient(target_hwnd, ctypes.byref(pt))
    client_x, client_y = pt.x, pt.y
    print(f"  Client coords: ({client_x}, {client_y})")

    WM_LBUTTONDOWN = 0x0201
    WM_LBUTTONUP   = 0x0202
    lparam = (client_y << 16) | (client_x & 0xFFFF)
    win32api.SendMessage(target_hwnd, WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
    time.sleep(0.05)
    win32api.SendMessage(target_hwnd, WM_LBUTTONUP, 0, lparam)
    time.sleep(0.2)
    send_keys('^a')
    time.sleep(0.1)
    send_keys('4268')
    print("  OK - Entered 4268")
    time.sleep(0.5)
except Exception as e:
    print(f"  ERROR: Could not enter customer number: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "=" * 70)
print("Workflow complete")
print("=" * 70)
