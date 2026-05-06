"""
Access the Internet Explorer DOM and click HTML buttons
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time
import warnings
warnings.filterwarnings('ignore')

print("[1] Connecting to Navigator...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()

print("\n[2] Finding Internet Explorer server control...")
children = window.children()
ie_server = None

for child in children:
    try:
        if 'Internet Explorer' in child.class_name():
            ie_server = child
            print(f"    Found IE Server")
            break
    except:
        pass

if not ie_server:
    print("[X] IE Server not found")
    exit(1)

print("\n[3] Trying to access IE document object...")
try:
    # Try to get the document through COM
    import win32com.client
    
    # Get the window handle of IE server
    ie_hwnd = ie_server.handle
    print(f"    IE HWND: {ie_hwnd}")
    
    # Try to get Internet Explorer application
    for ie in win32com.client.GetObject("winmgmts:").ExecQuery("select * from win32_process where name='IdsG2Client.exe'"):
        print(f"    Found process: {ie}")
    
except ImportError:
    print("    [X] win32com not available, installing...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'pywin32'])
    print("    Trying again...")
    import win32com.client

except Exception as e:
    print(f"    Error: {e}")

print("\n[4] Trying alternative: Direct browser automation...")
try:
    import comtypes
    from comtypes.client import CreateObject, GetActiveObject
    
    # Try to get IE COM object
    print(f"    Attempting to create IE object...")
    ie = None
    
    try:
        ie = GetActiveObject("InternetExplorer.Application")
        print(f"    [!] Got active IE object")
    except:
        ie = CreateObject("InternetExplorer.Application")
        print(f"    [!] Created new IE object")
    
    if ie:
        print(f"    IE object acquired")
        
        # Enumerate documents
        for i in range(ie.Document.all.length):
            elem = ie.Document.all(i)
            if 'sales' in elem.innerText.lower():
                print(f"        Found element with 'sales': {elem.tagName}")
                
                # Try clicking
                elem.click()
                print(f"        Clicked!")
                time.sleep(2)
                break

except ImportError as e:
    print(f"    [X] comtypes not available: {e}")
except Exception as e:
    print(f"    Error: {e}")
    import traceback
    traceback.print_exc()

print("\nTest complete.")
