"""
Check DPI and coordinate system issues
"""

from pywinauto import findwindows
from pywinauto.application import Application
from ctypes import windll
import time

print("[1] Getting system DPI...")
try:
    # Get DPI from Windows
    hdc = windll.user32.GetDC(0)
    dpi_x = windll.gdi32.GetDeviceCaps(hdc, 88)  # LOGPIXELSX
    dpi_y = windll.gdi32.GetDeviceCaps(hdc, 90)  # LOGPIXELSY
    windll.user32.ReleaseDC(0, hdc)
    
    print(f"    DPI: {dpi_x}x{dpi_y}")
    scale_factor = dpi_x / 96  # 96 is standard DPI
    print(f"    Scale factor: {scale_factor}")
except Exception as e:
    print(f"    Error: {e}")

print(f"\n[2] Getting window DPI awareness...")
try:
    nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
    app = Application(backend='win32').connect(handle=nav_handles[0])
    window = app.top_window()
    nav_hwnd = nav_handles[0]
    
    # Get window DPI
    import ctypes
    GetDpiForWindow = windll.user32.GetDpiForWindow
    dpi = GetDpiForWindow(nav_hwnd)
    print(f"    Navigator window DPI: {dpi}")
    
    # Get window rect
    rect_api = windll.user32.GetWindowRect
    
    class RECT(ctypes.Structure):
        _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), 
                   ("right", ctypes.c_long), ("bottom", ctypes.c_long)]
    
    rect = RECT()
    rect_api(nav_hwnd, ctypes.byref(rect))
    print(f"    Window API rect: ({rect.left}, {rect.top}, {rect.right}, {rect.bottom})")
    
    # Compare with pywinauto
    pywin_rect = window.rectangle()
    print(f"    PyWinAuto rect: ({pywin_rect.left}, {pywin_rect.top}, {pywin_rect.right}, {pywin_rect.bottom})")
    
except Exception as e:
    print(f"    Error: {e}")
    import traceback
    traceback.print_exc()

print(f"\n[3] Checking button coordinates in both systems...")
try:
    nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
    app = Application(backend='win32').connect(handle=nav_handles[0])
    window = app.top_window()
    
    children = window.children()
    for child in children:
        try:
            if child.window_text() == "Sales" and child.is_visible():
                # PyWinAuto rect
                pywin_rect = child.rectangle()
                print(f"    PyWinAuto Sales rect: {pywin_rect}")
                
                # Windows API rect
                import ctypes
                class RECT(ctypes.Structure):
                    _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), 
                               ("right", ctypes.c_long), ("bottom", ctypes.c_long)]
                
                rect = RECT()
                windll.user32.GetWindowRect(child.handle, ctypes.byref(rect))
                print(f"    Windows API Sales rect: ({rect.left}, {rect.top}, {rect.right}, {rect.bottom})")
                
                # Difference
                if rect.left > 0:
                    print(f"    Difference: X={rect.left - pywin_rect.left}, Y={rect.top - pywin_rect.top}")
                
                break
        except:
            pass

except Exception as e:
    print(f"    Error: {e}")
    import traceback
    traceback.print_exc()

print(f"\nAnalysis complete.")
