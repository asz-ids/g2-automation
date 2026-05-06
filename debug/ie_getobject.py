"""
Access IE document through WM_HTML_GETOBJECT message
"""

import time
import ctypes
from ctypes import windll, c_long, POINTER, cast
from comtypes import IUnknown, POINTER as COM_POINTER
from comtypes.automation import IDispatch
import warnings
warnings.filterwarnings('ignore')

print("[1] Finding G2 Navigator and IE Server...")
from pywinauto import findwindows
from pywinauto.application import Application

nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
if not nav_handles:
    print("[X] Navigator not found")
    exit(1)

app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()

ie_server = None
for child in window.children():
    if 'Internet Explorer' in child.class_name():
        ie_server = child
        break

if not ie_server:
    print("[X] IE Server not found")
    exit(1)

ie_hwnd = ie_server.handle
print(f"    IE Server HWND: {ie_hwnd}")

print("\n[2] Getting IE document through WM_HTML_GETOBJECT...")
try:
    # Register the message
    WM_HTML_GETOBJECT = windll.user32.RegisterWindowMessageA(b"WM_HTML_GETOBJECT")
    print(f"    WM_HTML_GETOBJECT: {WM_HTML_GETOBJECT}")
    
    # Send the message
    result = c_long()
    msg_result = windll.user32.SendMessageA(
        ie_hwnd,
        WM_HTML_GETOBJECT,
        0,
        ctypes.byref(result)
    )
    
    print(f"    SendMessage result: {msg_result}")
    print(f"    Object pointer: {result.value}")
    
    if not msg_result or not result.value:
        print("[X] Could not get document object")
        print("    Trying alternative method...")
        
        # Try direct window property access
        from pywinauto.uia_element_info import UIAElementInfo
        
        elem_info = ie_server.element_info
        print(f"    Element info: {elem_info}")
        
        exit(1)
    
    print("\n[3] Converting pointer to COM object...")
    
    # Convert the LRESULT to IDispatch
    obj = cast(result.value, COM_POINTER(IDispatch))
    print(f"    ✓ Got IDispatch object")
    
    print("\n[4] Accessing document methods...")
    
    # Get the document body
    try:
        # Call getElementsByTagName("*") to get all elements
        all_elements = obj.getElementsByTagName("*")
        elem_count = all_elements.length
        print(f"    Total HTML elements: {elem_count}")
        
        # Look for clickable elements
        print(f"\n[5] Searching for Sales/Service/Accounting buttons...")
        
        for i in range(elem_count):
            try:
                elem = all_elements.item(i)
                
                # Get element text
                inner_text = ""
                try:
                    inner_text = elem.innerText
                except:
                    pass
                
                # Look for button text
                if any(x in str(inner_text).lower() for x in ['sales', 'service', 'accounting', 'admin', 'parts']):
                    tag = ""
                    try:
                        tag = elem.tagName
                    except:
                        pass
                    
                    print(f"    Found: {inner_text:20} ({tag})")
                    
                    # Try clicking on Sales
                    if 'sales' in str(inner_text).lower():
                        print(f"\n    Clicking Sales button...")
                        try:
                            elem.click()
                            print(f"    ✓ Click executed")
                            time.sleep(3)
                            
                            # Check if screen opened
                            sales_handles = findwindows.find_windows(title_re=".*Sales.*")
                            if sales_handles:
                                print(f"    ✓ SUCCESS! Sales screen opened!")
                            else:
                                print(f"    [X] No Sales screen")
                        except Exception as click_err:
                            print(f"    [X] Click error: {click_err}")
                        break
            except:
                pass
        
    except Exception as e:
        print(f"    [X] Error accessing elements: {e}")
        import traceback
        traceback.print_exc()

except Exception as e:
    print(f"[X] Error: {e}")
    import traceback
    traceback.print_exc()

print("\nTest complete.")
