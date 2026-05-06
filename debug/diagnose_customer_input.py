"""
Opens AR Payment window automatically, then tests all input methods
on the Customer # field and reads back what actually landed.
"""
import sys, ctypes, ctypes.wintypes, time
sys.path.insert(0, r'E:\G2 Desktop Automation')

from pywinauto import Desktop, findwindows
from pywinauto.keyboard import send_keys

WM_SETTEXT       = 0x000C
WM_GETTEXT       = 0x000D
WM_GETTEXTLENGTH = 0x000E
WM_CHAR          = 0x0102
EM_SETSEL        = 0x00B1

TEST_VALUE = '4268'


def get_hwnd(elem):
    try:
        return elem.handle
    except Exception:
        try:
            return elem.element_info.handle
        except Exception:
            return None


def read_edit_text(hwnd):
    length = ctypes.windll.user32.SendMessageW(hwnd, WM_GETTEXTLENGTH, 0, 0)
    if length == 0:
        return ''
    buf = ctypes.create_unicode_buffer(length + 2)
    ctypes.windll.user32.SendMessageW(hwnd, WM_GETTEXT, length + 1, buf)
    return buf.value


def wm_settext(hwnd, text):
    ctypes.windll.user32.SendMessageW(hwnd, WM_SETTEXT, 0, text)


def wm_char_type(hwnd, text):
    for ch in text:
        ctypes.windll.user32.PostMessageW(hwnd, WM_CHAR, ord(ch), 0)
    time.sleep(0.15)


# ── Step 1: ensure AR window is open ─────────────────────────────────────────
print("=" * 60)
print("Step 1: Opening AR Payment window")
print("=" * 60)

existing = set(findwindows.find_windows(title_re=r".*Accounts Receivable.*"))

# Find Navigator
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
if not nav_handles:
    print("ERROR: G2 Navigator not found — launch G2 first")
    sys.exit(1)

nav_hwnd = nav_handles[0]
ctypes.windll.user32.ShowWindow(nav_hwnd, 9)
ctypes.windll.user32.SetForegroundWindow(nav_hwnd)
time.sleep(0.5)

desktop = Desktop(backend='uia')
nav_win = desktop.window(handle=nav_hwnd)

# Click Parts
try:
    nav_win.child_window(auto_id='btnParts', control_type='Button').click_input()
    print("  Clicked Parts")
except Exception as e:
    print(f"  ERROR clicking Parts: {e}"); sys.exit(1)
time.sleep(2)

# Click Take AR Payments
clicked = False
for spec in [{'auto_id': 'btnTakeARPayments'}, {'title': 'Take AR Payments'}]:
    try:
        nav_win.child_window(control_type='Button', **spec).click_input()
        print("  Clicked Take AR Payments")
        clicked = True
        break
    except Exception:
        pass
if not clicked:
    print("  ERROR: Could not click Take AR Payments"); sys.exit(1)

# Wait for new AR window
print("  Waiting for AR window...")
ar_hwnd = None
for i in range(20):
    current = set(findwindows.find_windows(title_re=r".*Accounts Receivable.*"))
    new = current - existing
    if new:
        ar_hwnd = list(new)[0]
        print(f"  AR window opened: HWND {ar_hwnd}")
        break
    time.sleep(1)

if not ar_hwnd:
    all_ar = findwindows.find_windows(title_re=r".*Accounts Receivable.*")
    if all_ar:
        ar_hwnd = all_ar[0]
        print(f"  Using existing AR window: HWND {ar_hwnd}")
    else:
        print("  ERROR: AR window not found"); sys.exit(1)

ctypes.windll.user32.SetForegroundWindow(ar_hwnd)
ctypes.windll.user32.BringWindowToTop(ar_hwnd)
time.sleep(0.5)

# ── Step 2: locate Customer # elements ───────────────────────────────────────
print("\nStep 2: Locating Customer # field")
win = Desktop(backend='uia').window(handle=ar_hwnd)

label_pane  = win.child_window(title="Customer #", control_type="Pane")
label_rect  = label_pane.rectangle()
label_mid_y = (label_rect.top + label_rect.bottom) // 2

customer_pane = None
for elem in win.children(class_name="ATLVPTextBoxClass31U"):
    r = elem.rectangle()
    if abs((r.top + r.bottom) // 2 - label_mid_y) < 15:
        customer_pane = elem
        break

if customer_pane is None:
    print("  ERROR: ATLVPTextBoxClass31U not found"); sys.exit(1)

edit_elems = customer_pane.descendants(class_name='Edit')
if not edit_elems:
    print("  ERROR: no Edit child found inside ATLVPTextBoxClass31U"); sys.exit(1)
edit_elem = edit_elems[0]
edit_hwnd  = get_hwnd(edit_elem)
pane_hwnd  = get_hwnd(customer_pane)

print(f"  ATLVPTextBoxClass31U HWND : {pane_hwnd}")
print(f"  Inner Edit HWND           : {edit_hwnd}")
print(f"  Initial text              : {read_edit_text(edit_hwnd)!r}")

# ── Step 3: test every input method ──────────────────────────────────────────
print("\nStep 3: Testing input methods")

results = {}

def run_method(label, fn):
    wm_settext(edit_hwnd, '')   # clear before each attempt
    time.sleep(0.15)
    fn()
    time.sleep(0.25)
    val = read_edit_text(edit_hwnd)
    ok  = val.strip() == TEST_VALUE
    tag = "OK  " if ok else "FAIL"
    print(f"  [{tag}] Method {label}: read back {val!r}")
    results[label] = ok
    return ok

def m1():
    customer_pane.click_input(); time.sleep(0.2)
    customer_pane.type_keys(TEST_VALUE, with_spaces=True)

def m2():
    customer_pane.click_input(); time.sleep(0.2)
    edit_elem.type_keys(TEST_VALUE, with_spaces=True)

def m3():
    edit_elem.click_input(); time.sleep(0.2)
    edit_elem.type_keys(TEST_VALUE, with_spaces=True)

def m4():
    wm_settext(edit_hwnd, TEST_VALUE)

def m5():
    wm_settext(pane_hwnd, TEST_VALUE)

def m6():
    customer_pane.click_input(); time.sleep(0.2)
    edit_elem.set_edit_text(TEST_VALUE)

def m7():
    customer_pane.click_input(); time.sleep(0.2)
    ctypes.windll.user32.SetFocus(edit_hwnd)
    time.sleep(0.1)
    wm_char_type(edit_hwnd, TEST_VALUE)

def m8():
    customer_pane.click_input(); time.sleep(0.3)
    send_keys(TEST_VALUE)

def m9():
    customer_pane.click_input(); time.sleep(0.2)
    ctypes.windll.user32.SetForegroundWindow(ar_hwnd)
    ctypes.windll.user32.SetFocus(edit_hwnd)
    time.sleep(0.2)
    send_keys(TEST_VALUE)

for label, fn in [
    ("1 type_keys on pane",                  m1),
    ("2 type_keys on Edit child",            m2),
    ("3 click+type_keys on Edit child",      m3),
    ("4 WM_SETTEXT to edit_hwnd",            m4),
    ("5 WM_SETTEXT to pane_hwnd",            m5),
    ("6 set_edit_text on Edit child",        m6),
    ("7 SetFocus+WM_CHAR to edit_hwnd",      m7),
    ("8 click_pane + global send_keys",      m8),
    ("9 SetFocus+SetFg + global send_keys",  m9),
]:
    run_method(label, fn)

# ── Summary ───────────────────────────────────────────────────────────────────
print("\n=== Summary ===")
winners = [k for k, v in results.items() if v]
if winners:
    print(f"Working methods: {winners}")
    print(f"\nUse method: {winners[0]}")
else:
    print("NO method successfully set text in the Edit control.")
    print("The control likely requires a different approach (e.g. WM_COMMAND, COM, or direct HWND focus bypass).")
