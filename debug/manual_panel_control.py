"""
Manually control panel visibility to simulate button clicks
"""
import pywinauto
from pywinauto import Application
import pywinauto.findwindows
import time
import ctypes

try:
    windows = pywinauto.findwindows.find_windows(title_re='.*Navigator.*')
    app = Application(backend='win32').connect(handle=windows[0])
    nav = app.window(handle=windows[0])
    children = nav.children()
    
    # Panel indices
    panels = {
        'Sales': {'visible': 15, 'button': 17},  # btnSales at 17
        'Service': {'visible': 26, 'button': 19},
        'Accounting': {'visible': 29, 'button': 21},
        'Admin': {'visible': 28, 'button': 23},
        'Parts': {'visible': 27, 'button': 25},
    }
    
    print("[1] Current state...")
    for label, info in panels.items():
        vis_panel = children[info['visible']]
        is_visible = vis_panel.is_visible() if hasattr(vis_panel, 'is_visible') else None
        print(f"    {label:12s} panel[{info['visible']}]: visible={is_visible}")
    
    print("\n[2] Method 1: Try to hide/show via ShowWindow API...")
    
    SW_HIDE = 0
    SW_SHOW = 5
    
    for label in ['Service', 'Admin']:
        print(f"\n    Showing {label} (hiding others)...")
        
        # Hide all panels
        for other_label, other_info in panels.items():
            if other_label != label:
                panel = children[other_info['visible']]
                hwnd = panel.handle if hasattr(panel, 'handle') else None
                if hwnd:
                    ctypes.windll.user32.ShowWindow(hwnd, SW_HIDE)
        
        # Show target panel
        panel = children[panels[label]['visible']]
        hwnd = panel.handle if hasattr(panel, 'handle') else None
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, SW_SHOW)
            ctypes.windll.user32.InvalidateRect(hwnd, None, 1)
        
        time.sleep(0.5)
        
        # Check state
        print(f"    Result:")
        for other_label, other_info in panels.items():
            vis_panel = children[other_info['visible']]
            is_visible = vis_panel.is_visible() if hasattr(vis_panel, 'is_visible') else None
            status = "✓ VISIBLE" if is_visible else "  hidden"
            print(f"      {other_label:12s}: {status}")
    
    print("\n[3] Method 2: Try WM_SHOWWINDOW message...")
    
    WM_SHOWWINDOW = 0x0018
    
    for label in ['Parts']:
        print(f"\n    Showing {label}...")
        
        # Hide all panels except target
        for other_label, other_info in panels.items():
            if other_label != label:
                panel = children[other_info['visible']]
                hwnd = panel.handle if hasattr(panel, 'handle') else None
                if hwnd:
                    # WM_SHOWWINDOW with wParam=0 (SW_HIDE)
                    ctypes.windll.user32.SendMessageW(hwnd, WM_SHOWWINDOW, 0, 0)
        
        # Show target
        panel = children[panels[label]['visible']]
        hwnd = panel.handle if hasattr(panel, 'handle') else None
        if hwnd:
            ctypes.windll.user32.SendMessageW(hwnd, WM_SHOWWINDOW, 1, 0)
        
        time.sleep(0.5)
        
        # Check state
        print(f"    Result:")
        for other_label, other_info in panels.items():
            vis_panel = children[other_info['visible']]
            is_visible = vis_panel.is_visible() if hasattr(vis_panel, 'is_visible') else None
            status = "✓ VISIBLE" if is_visible else "  hidden"
            print(f"      {other_label:12s}: {status}")

except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
