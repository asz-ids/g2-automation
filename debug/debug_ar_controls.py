"""Debug: enumerate all controls in the AR Payment window to find Customer # field."""
import ctypes
import ctypes.wintypes
import time
from pywinauto import findwindows

handles = findwindows.find_windows(title_re=".*Accounts Receivable.*")
if not handles:
    handles = findwindows.find_windows(title_re=".*Payment.*")
if not handles:
    handles = findwindows.find_windows(title_re=".*SMC.*")

if not handles:
    print("ERROR: AR Payment window not found — open it first")
    exit(1)

ar_hwnd = handles[0]
print(f"AR window HWND: {ar_hwnd}")

WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
_cls = ctypes.create_unicode_buffer(64)
_txt = ctypes.create_unicode_buffer(256)
_all_controls = []

def _collect(hwnd, _):
    ctypes.windll.user32.GetClassNameW(hwnd, _cls, 64)
    ctypes.windll.user32.GetWindowTextW(hwnd, _txt, 256)
    r = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(r))
    _all_controls.append({
        'hwnd': hwnd,
        'cls': _cls.value,
        'txt': _txt.value,
        'top': r.top,
        'bottom': r.bottom,
        'left': r.left,
        'right': r.right,
    })
    return True

ctypes.windll.user32.EnumChildWindows(ar_hwnd, WNDENUMPROC(_collect), 0)

print(f"\nTotal controls found: {len(_all_controls)}")
print("\n--- All controls ---")
for c in _all_controls:
    mid_y = (c['top'] + c['bottom']) // 2
    print(f"  cls={c['cls']:<20} txt={repr(c['txt']):<40} top={c['top']} mid_y={mid_y} left={c['left']}")

# Find "Customer" labels
print("\n--- Controls containing 'Customer' ---")
for c in _all_controls:
    if 'customer' in c['txt'].lower():
        mid_y = (c['top'] + c['bottom']) // 2
        print(f"  cls={c['cls']:<20} txt={repr(c['txt']):<40} top={c['top']} mid_y={mid_y} left={c['left']}")

# Find all Edit controls
print("\n--- Edit controls ---")
for c in _all_controls:
    if c['cls'] == 'Edit':
        mid_y = (c['top'] + c['bottom']) // 2
        print(f"  txt={repr(c['txt']):<40} top={c['top']} mid_y={mid_y} left={c['left']}")
