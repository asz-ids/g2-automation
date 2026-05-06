"""
Test script to determine what happens when Credit button is clicked
"""
import time
import logging
import ctypes
from pywinauto import findwindows
from pywinauto import Application

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('credit_button_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Find the Take Payment window
try:
    pay_windows = findwindows.find_windows(title_re=".*Take Payment.*")
    if not pay_windows:
        print("ERROR: Take Payment window not found")
        logger.error("Take Payment window not found")
        exit(1)
    
    pay_hwnd = pay_windows[0]
    logger.info(f"Found Take Payment window: {pay_hwnd}")
    print(f"Take Payment window handle: {pay_hwnd}")
    
    # Connect via UIA
    app = Application(backend='uia')
    app.connect(handle=pay_hwnd)
    window = app.window(handle=pay_hwnd)
    
    # List all windows BEFORE clicking
    all_before = findwindows.find_windows()
    logger.info(f"Windows BEFORE Credit button click: {len(all_before)}")
    
    # Find and enumerate all buttons
    buttons = window.descendants(control_type='Button')
    logger.info(f"Found {len(buttons)} buttons in window")
    
    for i, btn in enumerate(buttons):
        try:
            auto_id = btn.automation_id if hasattr(btn, 'automation_id') else 'N/A'
            btn_text = btn.window_text() if hasattr(btn, 'window_text') else 'N/A'
            logger.info(f"  Button {i}: auto_id='{auto_id}', text='{btn_text}'")
            print(f"  Button {i}: auto_id='{auto_id}', text='{btn_text}'")
        except:
            pass
    
    # Find Credit button
    credit_btn = None
    for btn in buttons:
        try:
            if btn.automation_id == 'btnCredit':
                credit_btn = btn
                break
        except:
            pass
    
    if credit_btn is None:
        print("ERROR: btnCredit not found")
        logger.error("btnCredit not found")
        exit(1)
    
    print("\n" + "="*70)
    print("CLICKING CREDIT BUTTON...")
    print("="*70)
    logger.info("About to click Credit button")
    
    # Click the button
    credit_btn.click()
    logger.info("Credit button clicked")
    print("Credit button clicked - waiting for response...")
    
    # Wait 3 seconds and check windows
    time.sleep(3)
    
    all_after = findwindows.find_windows()
    logger.info(f"Windows AFTER Credit button click: {len(all_after)}")
    print(f"\nTotal windows after click: {len(all_after)}")
    
    # Find NEW windows
    new_windows = set(all_after) - set(all_before)
    logger.info(f"NEW windows created: {len(new_windows)}")
    print(f"NEW windows: {len(new_windows)}")
    
    # List new windows
    for h in new_windows:
        try:
            length = ctypes.windll.user32.GetWindowTextLengthW(h)
            title = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(h, title, length + 1)
            window_title = title.value
            logger.info(f"  NEW: {window_title}")
            print(f"  NEW WINDOW: {window_title}")
        except:
            pass
    
    # Check the current Take Payment window state
    print("\n" + "="*70)
    print("TAKE PAYMENT WINDOW STATUS AFTER CREDIT CLICK:")
    print("="*70)
    
    # List all buttons again to see if any changed
    buttons_after = window.descendants(control_type='Button')
    logger.info(f"Buttons in window after click: {len(buttons_after)}")
    print(f"Total buttons now: {len(buttons_after)}")
    
    # List all text controls (dialogs, labels, etc.)
    print("\nText controls in window:")
    text_ctrls = window.descendants(control_type='Text')
    for tc in text_ctrls[:10]:
        try:
            txt = tc.window_text()
            if txt and len(txt) > 0 and len(txt) < 200:
                logger.info(f"  Text: {txt}")
                print(f"  {txt}")
        except:
            pass
    
    logger.info("Test completed")
    print("\nTest completed - check credit_button_test.log for details")

except Exception as e:
    logger.error(f"Error: {e}", exc_info=True)
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
