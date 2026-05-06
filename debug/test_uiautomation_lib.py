"""
Use Python UIAutomation library for proper coordinate handling
"""

try:
    import uiautomation as auto
    print("[OK] UIAutomation library available")
except ImportError:
    print("[X] UIAutomation not installed, installing...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'uiautomation'])
    import uiautomation as auto
    print("[OK] UIAutomation installed")

import time

print("\n[1] Finding Navigator window with UIAutomation...")
try:
    navigator = auto.WindowControl(searchDepth=1, Name='G2 Navigator')
    if not navigator.Exists(0):
        print("[X] Navigator not found")
        exit(1)
    print(f"    ✓ Found: {navigator.Name}")
except Exception as e:
    print(f"[X] Error: {e}")
    exit(1)

print("\n[2] Searching for Sales button...")
try:
    # Get all controls in navigator and find Sales
    children = navigator.GetChildren()
    print(f"    Navigator has {len(children)} children")
    
    sales_button = None
    for child in children:
        try:
            if hasattr(child, 'Name') and child.Name == 'Sales':
                sales_button = child
                break
        except:
            pass
    
    if not sales_button:
        print("[X] Sales button not found, listing children...")
        
        for i, child in enumerate(children[:30]):
            try:
                name = child.Name if hasattr(child, 'Name') else "No name"
                ctype = child.ControlType if hasattr(child, 'ControlType') else "Unknown"
                print(f"    [{i}] {name[:30]:30} | {ctype}")
            except:
                pass
    else:
        print(f"    ✓ Found Sales button")
        
        print(f"\n[3] Clicking Sales button...")
        try:
            # Get the button's clickable center
            rect = sales_button.BoundingRectangle
            print(f"        Position: {rect}")
            
            sales_button.Click()
            print(f"        ✓ Clicked")
            time.sleep(3)
            
            # Check for result
            print(f"\n[4] Checking for Sales screen...")
            try:
                sales_screen = auto.WindowControl(searchDepth=1, Name='Sales')
                if sales_screen.Exists(0):
                    print(f"        ✓ SUCCESS! Sales screen opened!")
                else:
                    print(f"        [X] No Sales screen yet")
            except Exception as e2:
                print(f"        Could not find Sales screen: {e2}")
                
        except Exception as e:
            print(f"        [X] Click error: {e}")

except Exception as e:
    print(f"[X] Error: {e}")
    import traceback
    traceback.print_exc()

print("\nTest complete.")
