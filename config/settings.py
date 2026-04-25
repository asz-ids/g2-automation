"""
Configuration settings for the automation framework.
"""

import os
from pathlib import Path

# Base directories
PROJECT_ROOT = Path(__file__).parent.parent
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
LOGS_DIR = PROJECT_ROOT / "logs"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Screenshot settings
SCREENSHOT_FORMAT = "png"
SCREENSHOT_QUALITY = 95
SCREENSHOT_ON_FAILURE = True

# Timeout settings (in seconds)
DEFAULT_TIMEOUT = 10.0
ELEMENT_FIND_TIMEOUT = 5.0
TEXT_WAIT_TIMEOUT = 10.0

# UIA settings
UIA_TIMEOUT = 5.0
UIA_TREE_SCOPE = "Descendants"  # Descendants, Children, Element, or Subtree

# Keyboard settings
KEYBOARD_TYPE_INTERVAL = 0.05  # Seconds between keystrokes
KEYBOARD_KEY_INTERVAL = 0.1    # Seconds between key presses

# Mouse settings
MOUSE_MOVE_DURATION = 0.5     # Seconds for mouse movement
MOUSE_CLICK_DELAY = 0.2        # Seconds after click

# OCR settings
OCR_ENABLED = True
OCR_LANGUAGE = "eng"
OCR_CONFIDENCE_THRESHOLD = 0.7

# Logging settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = LOGS_DIR / "automation.log"

# Test execution settings
HEADLESS_MODE = False
RECORD_EXECUTION = False
VIDEO_OUTPUT_DIR = PROJECT_ROOT / "videos"

# Element recognition settings
ELEMENT_HIGHLIGHT_ON_INTERACTION = False
HIGHLIGHT_COLOR = (0, 255, 0)  # RGB
HIGHLIGHT_THICKNESS = 2

# Performance settings
CACHE_ELEMENTS = True
MAX_CACHE_SIZE = 1000
PARALLEL_TEST_EXECUTION = False
MAX_PARALLEL_TESTS = 4

# Create necessary directories
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
