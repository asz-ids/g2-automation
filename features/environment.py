import ctypes
import os
import re
import time
from pywinauto import Desktop, findwindows

_SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'screenshots')


class _State:
    """Mutable state shared across all steps in a scenario.

    context.attribute = value inside a step writes to the step-scope layer,
    which is popped when the step ends.  Mutating an object that lives in the
    scenario-scope layer (set by before_scenario) persists for the whole scenario.
    """
    def __init__(self):
        self.nav_hwnd = None
        self.ar_hwnd = None
        self.payment_hwnd = None
        self.idspay_hwnd = None
        self.unit_inventory_hwnd = None
        self.stock_number = None
        self.customer_edit = None
        self.table = None
        self.existing_ar_handles = set()
        self.step_count = 0


def before_scenario(context, scenario):
    context.s = _State()


def after_step(context, step):
    """Capture a screenshot after every passed or failed step."""
    if step.status.name == 'skipped':
        return

    try:
        from PIL import ImageGrab
    except ImportError:
        return

    def _safe(text):
        return re.sub(r'[^\w-]', '_', text)[:60]

    scenario_dir = os.path.join(_SCREENSHOTS_DIR, _safe(context.scenario.name))
    os.makedirs(scenario_dir, exist_ok=True)

    context.s.step_count += 1
    filename = f"{context.s.step_count:02d}_{_safe(step.name)}__{step.status.name}.png"
    filepath = os.path.join(scenario_dir, filename)

    try:
        img = ImageGrab.grab()
        img.save(filepath)
        print(f"\n  [Screenshot] {filename}")
    except Exception as e:
        print(f"\n  [Screenshot] Capture failed: {e}")


# def after_scenario(context, scenario):
    # """Close any open AccuTerm windows after each scenario."""
    # handles = findwindows.find_windows(title_re=".*AccuTerm.*")
    # for hwnd in handles:
    #     try:
    #         # SendMessageW is synchronous — waits until the window processes WM_CLOSE
    #         ctypes.windll.user32.SendMessageW(hwnd, 0x0010, 0, 0)  # WM_CLOSE
    #         print(f"\n  [Teardown] Closed AccuTerm window (HWND {hwnd})")
    #         time.sleep(0.5)
    #     except Exception as e:
    #         print(f"\n  [Teardown] Failed to close AccuTerm (HWND {hwnd}): {e}")
