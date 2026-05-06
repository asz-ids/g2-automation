"""
Access G2 Navigator through COM and interact with HTML elements
"""

import time
import warnings
warnings.filterwarnings('ignore')

try:
    from comtypes.client import GetActiveObject, CreateObject
    import comtypes.gen.MSHTML as MSHTML
    from ctypes import POINTER
except ImportError as e:
    print(f"[X] Import error: {e}")
    print("Installing required packages...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'comtypes'])
    from comtypes.client import GetActiveObject, CreateObject
    import comtypes.gen.MSHTML as MSHTML
    from ctypes import POINTER

print("[1] Trying to get IE COM object...")
try:
    # Try to get the active IE instance
    ie = GetActiveObject("InternetExplorer.Application")
    print(f"    ✓ Found active IE instance")
    print(f"    URL: {ie.LocationURL}")
except Exception as e:
    print(f"    [X] Could not get IE object: {e}")
    print(f"    This might be embedded in G2 process, not standalone IE")
    
    # Try alternative: use win32api to find and interact with the window
    from pywinauto import findwindows
    from pywinauto.application import Application
    
    print("\n[2] Accessing IE through G2 Navigator window...")
    nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
    if not nav_handles:
        print("[X] Navigator not found")
        exit(1)
    
    app = Application(backend='win32').connect(handle=nav_handles[0])
    window = app.top_window()
    
    # Find IE server child
    ie_server = None
    for child in window.children():
        if 'Internet Explorer' in child.class_name():
            ie_server = child
            break
    
    if not ie_server:
        print("[X] IE Server not found")
        exit(1)
    
    print(f"    Found IE Server window")
    ie_hwnd = ie_server.handle
    print(f"    IE HWND: {ie_hwnd}")
    
    # Try to get document via window handle
    print("\n[3] Attempting to access IE document via COM...")
    try:
        # Create IE object and try to find the document
        from comtypes import IUnknown
        from comtypes.automation import IDispatch
        
        # Try ObjectFromLresult if available
        from comtypes.client import GetBestInterface
        import ctypes
        
        # Get the document from the window handle
        WM_HTML_GETOBJECT = ctypes.windll.user32.RegisterWindowMessageA(b"WM_HTML_GETOBJECT")
        print(f"    WM_HTML_GETOBJECT: {WM_HTML_GETOBJECT}")
        
        # Send message to get the object
        result = ctypes.c_long()
        msg_result = ctypes.windll.user32.SendMessageA(
            ie_hwnd,
            WM_HTML_GETOBJECT,
            0,
            ctypes.byref(result)
        )
        
        print(f"    Message result: {msg_result}")
        print(f"    Object result: {result.value}")
        
        if msg_result and result.value:
            # Convert LRESULT to COM object
            from comtypes import POINTER, cast
            from comtypes.automation import IDispatch
            
            # The result should be a pointer to the document object
            doc = cast(result.value, POINTER(IDispatch))
            print(f"    ✓ Got document object!")
            
            # Now we can interact with the document
            print("\n[4] Accessing HTML elements...")
            
            # Get all elements
            all_elements = doc.getElementsByTagName("*")
            print(f"    Total elements: {all_elements.length}")
            
            # Look for elements with "Sales", "Service" etc
            for i in range(all_elements.length):
                elem = all_elements.item(i)
                try:
                    text = elem.innerText if hasattr(elem, 'innerText') else ""
                    tag = elem.tagName if hasattr(elem, 'tagName') else ""
                    
                    if any(x in text.lower() for x in ['sales', 'service', 'accounting', 'admin', 'parts']):
                        print(f"    [{i}] Found: {text:20} ({tag})")
                        
                        # Try clicking
                        if text.lower() == 'sales':
                            print(f"        Clicking Sales...")
                            elem.click()
                            print(f"        ✓ Clicked")
                            time.sleep(3)
                            break
                except:
                    pass
        else:
            print("[X] Could not get document object from window")
            
    except Exception as e:
        print(f"[X] Error: {e}")
        import traceback
        traceback.print_exc()

print("\nTest complete.")
