"""
Test script to discover G2 Login form elements using pywinauto
"""

from pywinauto import findwindows
from pywinauto.application import Application
import ctypes

def get_window_title(hwnd):
    """Helper function to get window title"""
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    length = GetWindowTextLength(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    GetWindowText(hwnd, buff, length + 1)
    return buff.value

def main():
    print("="*60)
    print("G2 LOGIN FORM STRUCTURE DISCOVERY")
    print("="*60)
    
    try:
        # Find G2 Login window
        print("\n[1] Finding G2 Login window...")
        windows = findwindows.find_windows(title_re=".*G2 Login.*")
        
        if not windows:
            print("    [X] G2 Login window not found!")
            return False
        
        g2_window_handle = windows[0]
        print(f"    [OK] Found G2 Login window (handle: {g2_window_handle})")
        print(f"    Title: {get_window_title(g2_window_handle)}")
        
        # Connect to the window
        print("\n[2] Connecting to window...")
        app = Application(backend='uia').connect(handle=g2_window_handle)
        print("    [OK] Connected successfully")
        
        # Get the window element
        print("\n[3] Exploring window structure...")
        window = app.window()
        print(f"    Window: {window.name}")
        
        # Look for known elements
        print("\n[4] Finding login form elements...")
        known_ids = ["txtUser", "txtPwd", "txtDomain", "btnLogin", "btnCancel"]
        found_elements = {}
        
        def search_for_elements(elem, depth=0, max_depth=5):
            """Recursively search for elements"""
            if depth > max_depth:
                return
            
            try:
                try:
                    auto_id = elem.automation_id()
                    if auto_id in known_ids and auto_id not in found_elements:
                        found_elements[auto_id] = elem
                        print(f"    [OK] Found element: {auto_id}")
                except:
                    pass
                
                try:
                    for child in elem.children():
                        search_for_elements(child, depth + 1, max_depth)
                except:
                    pass
            except:
                pass
        
        search_for_elements(window)
        print(f"\n    Total elements found: {len(found_elements)}/{len(known_ids)}")
        
        print("\n" + "="*60)
        print("DISCOVERY COMPLETE")
        print("="*60)
        for elem_id in known_ids:
            status = "[OK]" if elem_id in found_elements else "[X]"
            print(f"{status} {elem_id}")
        
        return True
        
    except Exception as e:
        print(f"\n[X] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
