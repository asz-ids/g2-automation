# tests/test_service_navigation.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import time
import ctypes
import pytest
from pywinauto import findwindows
from pywinauto.keyboard import send_keys

G2_EXE = r"C:\IDSASTRA\APPS\G2\G2CLIENT\IdsG2Client.exe"
G2_USERNAME = "aqadir.ids"
G2_PASSWORD = "Aqadir2801"
NAV_PATTERN = r".*Navigator.*"


def _navigator_open():
    return bool(findwindows.find_windows(title_re=NAV_PATTERN))


@pytest.fixture(scope="session", autouse=True)
def ensure_g2_running():
    """Launch G2 and log in if the Navigator is not already open."""
    if _navigator_open():
        print("\n  G2 Navigator already open — skipping launch/login")
        return

    if not findwindows.find_windows(title="G2 Login"):
        print("\n  Launching G2...")
        result = ctypes.windll.shell32.ShellExecuteW(
            None, "open", G2_EXE, None, os.path.dirname(G2_EXE), 1
        )
        if result <= 32:
            pytest.fail(f"ShellExecute failed (code {result}) — cannot launch G2")

    login_hwnd = None
    for i in range(30):
        handles = findwindows.find_windows(title="G2 Login")
        if handles:
            login_hwnd = handles[0]
            print(f"\n  G2 Login window found after {i}s")
            break
        time.sleep(1)
    if not login_hwnd:
        pytest.fail("G2 Login window did not appear after 30s")

    ctypes.windll.user32.ShowWindow(login_hwnd, 9)
    ctypes.windll.user32.SetForegroundWindow(login_hwnd)
    time.sleep(0.5)

    try:
        ctypes.windll.user32.SetForegroundWindow(login_hwnd)
        time.sleep(0.5)
        send_keys(f'{G2_USERNAME}{{TAB}}{G2_PASSWORD}{{ENTER}}')
        print("  Credentials submitted — waiting for Navigator...")
    except Exception as e:
        pytest.fail(f"Could not submit login credentials: {e}")

    for i in range(60):
        if _navigator_open():
            print(f"  Navigator appeared after {i}s")
            return
        time.sleep(1)
    pytest.fail("G2 Navigator did not appear within 60s after login")


# ---------------------------------------------------------------------------
# Unit tests — no live G2 required (auto_navigate=False)
# ---------------------------------------------------------------------------

def test_service_screen_import(service_screen_unit):
    from screens.service_screen import ServiceScreen
    assert ServiceScreen is not None


def test_service_screen_attributes(service_screen_unit):
    assert isinstance(service_screen_unit._discovered_buttons, list)


# ---------------------------------------------------------------------------
# Functional tests — require live G2 (use service_screen fixture)
# ---------------------------------------------------------------------------

@pytest.mark.functional
def test_navigate_to_service(service_screen):
    assert service_screen is not None


@pytest.mark.functional
def test_discover_explorer_buttons(service_screen):
    sections = service_screen.get_available_sections()
    assert len(sections) >= 1, f"Expected at least 1 explorer button, got: {sections}"


@pytest.mark.functional
def test_go_to_work_orders(service_screen):
    result = service_screen.go_to_work_orders()
    assert result is True, "go_to_work_orders() should return True"


@pytest.mark.functional
def test_go_to_invalid_section(service_screen):
    result = service_screen.go_to("__invalid_section__")
    assert result is False, "go_to() with unknown section should return False"


@pytest.mark.functional
def test_get_available_sections(service_screen):
    sections = service_screen.get_available_sections()
    assert isinstance(sections, list)
    assert len(sections) > 0, "get_available_sections() must return a non-empty list"


@pytest.mark.functional
def test_is_section_available(service_screen):
    sections = service_screen.get_available_sections()
    assert len(sections) > 0, "Precondition: need at least one section"
    # Exact match
    assert service_screen.is_section_available(sections[0]) is True
    # Case-insensitive match
    assert service_screen.is_section_available(sections[0].lower()) is True
    # Non-existent section
    assert service_screen.is_section_available("__nonexistent__") is False


@pytest.mark.functional
def test_rediscover(service_screen):
    result = service_screen.rediscover()
    assert result is True, "rediscover() should return True when ≥1 button found"
