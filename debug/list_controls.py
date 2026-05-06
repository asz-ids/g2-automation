"""
Debug: List all controls in the AR Payments window
"""
import sys
sys.path.insert(0, r'e:\G2 Desktop Automation')

from pywinauto import Application, findwindows

# Find window
handles = findwindows.find_windows(title_re=".*Accounts Receivable.*")
if not handles:
    handles = findwindows.find_windows(title_re=".*Payment.*")

ar_hwnd = handles[0]
print(f"Window: {ar_hwnd}\n")

app_uia = Application(backend='uia').connect(handle=ar_hwnd)
window_uia = app_uia.window(handle=ar_hwnd)

print("All control types in window:")
print("-" * 70)

control_types = {}
for elem in window_uia.descendants():
    try:
        elem_type = elem.control_type if hasattr(elem, 'control_type') else "Unknown"
        elem_text = elem.window_text() if hasattr(elem, 'window_text') else ""
        
        if elem_type not in control_types:
            control_types[elem_type] = []
        
        if elem_text:
            control_types[elem_type].append(elem_text[:50])
    except:
        pass

for ctype in sorted(control_types.keys()):
    print(f"\n{ctype}:")
    for text in control_types[ctype][:10]:
        print(f"  - {text}")
    if len(control_types[ctype]) > 10:
        print(f"  ... and {len(control_types[ctype]) - 10} more")
