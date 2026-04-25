"""
Pytest configuration and fixtures for the automation framework.
"""

try:
    import pytest
except ImportError:
    pytest = None

import subprocess
import time
from screens.login_screen import LoginScreen


G2_EXECUTABLE = r"C:\IDSASTRA\APPS\G2\G2CLIENT\IDS.G2.AppOne.exe"


@pytest.fixture(scope="session", autouse=True)
def open_g2_application():
    """Fixture that opens the G2 application at the start of test session."""
    try:
        print("\n[Setup] Opening G2 application...")
        subprocess.Popen(G2_EXECUTABLE)
        time.sleep(5)  # Wait for application to start and load
        print("[Setup] G2 application opened successfully")
    except Exception as e:
        print(f"[Setup] Warning: Could not open G2 application: {e}")
    
    yield
    
    # Cleanup - application stays running (user can close it manually)
    print("\n[Teardown] Test session complete. G2 application remains running.")


@pytest.fixture
def login_screen():
    """Fixture providing a LoginScreen instance."""
    screen = LoginScreen()
    yield screen
    # Cleanup after test
    screen.screenshots.clear_cache() if hasattr(screen.screenshots, 'clear_cache') else None


@pytest.fixture
def work_order_screen():
    """Fixture providing WorkOrderCreationScreen in manual mode (no live G2 required for unit tests)."""
    from screens.work_order_creation_screen import WorkOrderCreationScreen
    screen = WorkOrderCreationScreen(discover_from_uia=False)
    yield screen


@pytest.fixture
def live_work_order_screen():
    """Fixture providing WorkOrderCreationScreen connected to live G2 (requires G2 open at WO Manager)."""
    from screens.work_order_creation_screen import WorkOrderCreationScreen
    screen = WorkOrderCreationScreen(discover_from_uia=True)
    yield screen


@pytest.fixture(scope="session")
def test_config():
    """Fixture providing test configuration."""
    from config import settings
    return settings


@pytest.fixture
def screenshot_manager():
    """Fixture providing ScreenshotManager."""
    from core.screenshot_manager import ScreenshotManager
    return ScreenshotManager()


@pytest.fixture
def keyboard_handler():
    """Fixture providing KeyboardHandler."""
    from core.keyboard_handler import KeyboardHandler
    return KeyboardHandler()


@pytest.fixture
def mouse_handler():
    """Fixture providing MouseHandler."""
    from core.mouse_handler import MouseHandler
    return MouseHandler()


@pytest.fixture
def text_tracker():
    """Fixture providing TextTracker."""
    from core.text_tracker import TextTracker
    return TextTracker()


def pytest_configure(config):
    """Configure pytest with custom markers."""
    if pytest is None:
        return
    config.addinivalue_line(
        "markers", "smoke: mark test as a smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as a regression test"
    )
    config.addinivalue_line(
        "markers", "functional: mark test as a functional test"
    )
    config.addinivalue_line(
        "markers", "sanity: mark test as a sanity check"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test items during collection."""
    if pytest is None:
        return
    for item in items:
        if "login" in item.nodeid:
            item.add_marker(pytest.mark.functional)
