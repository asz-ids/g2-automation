"""
Simple test to find G2 application window using pywinauto
"""

try:
    from pywinauto import findwindows
    from pywinauto.application import Application
    import ctypes
    
    print("Searching for G2 Login window...")
    
    # Find windows with "G2" in title
    windows = findwindows.find_windows(title_re=".*G2.*", class_name_re=".*")
    
    print(f"Found {len(windows)} windows matching 'G2':")
    for i, w in enumerate(windows):
        # Get window title using ctypes
        GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
        GetWindowText = ctypes.windll.user32.GetWindowTextW
        length = GetWindowTextLength(w)
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(w, buff, length + 1)
        title = buff.value
        print(f"  {i+1}. Handle: {w}, Title: {title}")
    
    # Try to connect to first window
    if windows:
        print(f"\nAttempting to connect to first G2 window...")
        app = Application(backend='uia').connect(handle=windows[0])
        print(f"Successfully connected to G2 window")
        print(f"Window element: {app.window()}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
