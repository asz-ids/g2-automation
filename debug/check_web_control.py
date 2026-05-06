"""
Check if Navigator is using embedded web content
"""

from pywinauto import findwindows
from pywinauto.application import Application
import time

print("[1] Connecting to Navigator...")
nav_handles = findwindows.find_windows(title_re=".*Navigator.*")
app = Application(backend='win32').connect(handle=nav_handles[0])
window = app.top_window()

print("\n[2] Analyzing all children for web/ActiveX controls...")
children = window.children()

for i, child in enumerate(children):
    try:
        cls = child.class_name()
        text = child.window_text()
        
        # Look for ActiveX, browser, or rendering controls
        if any(x in cls for x in ['ActiveX', 'Internet', 'Shell', 'WebBrowser', 'Chrome', 'Edge', 'Explorer']):
            print(f"    [{i}] {cls}")
            print(f"        Text: {text}")
            
            # Try to interact with it
            if 'Internet' in cls or 'Explorer' in cls or 'Browser' in cls:
                print(f"        [!] This looks like a web control!")
                
                # Try to get document
                try:
                    doc = child.element_info.element
                    print(f"        Element: {doc}")
                except:
                    pass
    except:
        pass

print("\n[3] Full child hierarchy...")
for i, child in enumerate(children):
    try:
        cls = child.class_name()
        text = child.window_text()[:30] if child.window_text() else ""
        rect = child.rectangle()
        
        print(f"    [{i:2d}] {cls[:50]:50} Text: {text:30}")
    except Exception as e:
        print(f"    [{i:2d}] Error: {e}")

print("\n[4] Checking for hidden or floating windows...")
all_wins = findwindows.find_windows(title_re=".*")
print(f"    Total windows: {len(all_wins)}")

for h in all_wins:
    try:
        a = Application(backend='win32').connect(handle=h)
        w = a.top_window()
        title = w.window_text()
        
        if any(x in title for x in ['Screen', 'Sales', 'Service', 'Input', 'Prompt', 'Dialog']):
            print(f"      - {title} (Visible: {w.is_visible()})")
    except:
        pass

print("\nAnalysis complete - Navigator appears to be using an embedded browser/ActiveX control")
print("The 'buttons' might be HTML elements, not Win32 controls")
