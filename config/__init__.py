"""
Initialization file for configuration.
"""

from .settings import *

__all__ = [
    "PROJECT_ROOT",
    "SCREENSHOTS_DIR",
    "LOGS_DIR",
    "REPORTS_DIR",
    "SCREENSHOT_FORMAT",
    "SCREENSHOT_QUALITY",
    "SCREENSHOT_ON_FAILURE",
    "DEFAULT_TIMEOUT",
    "ELEMENT_FIND_TIMEOUT",
    "TEXT_WAIT_TIMEOUT",
    "UIA_TIMEOUT",
    "KEYBOARD_TYPE_INTERVAL",
    "MOUSE_MOVE_DURATION",
    "MOUSE_CLICK_DELAY",
    "OCR_ENABLED",
    "OCR_LANGUAGE",
    "OCR_CONFIDENCE_THRESHOLD",
    "LOG_LEVEL",
    "LOG_FORMAT",
    "LOG_FILE",
]
