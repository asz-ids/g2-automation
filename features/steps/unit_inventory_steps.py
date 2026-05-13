"""
Step definitions for unit_inventory.feature.

Steps reused from ar_payment_steps.py (behave auto-discovers all step files):
  Given G2 is running and the Navigator is open
  When  I navigate to "{menu_item}" from the "{menu_name}" menu
  When  I click "{button_label}"
  Then  the "{window_title}" window opens
"""

import ctypes
import ctypes.wintypes
import random
import time

from behave import given, when, then
from pywinauto import Desktop, findwindows
from pywinauto.keyboard import send_keys


# ── Unit Inventory specific steps ─────────────────────────────────────────────

@when('I enter a new stock number in the "Stock #" field')
def step_enter_stock_number(context):
    s = context.s
    assert s.unit_inventory_hwnd, "Inventory window handle not set"
    win = Desktop(backend='uia').window(handle=s.unit_inventory_hwnd)

    # Random 4-6 digit number, stored for later assertion steps
    stock_num = str(random.randint(1000, 999999))
    s.stock_number = stock_num

    # The Stock # Edit is the first Edit control in this window
    edits = win.descendants(control_type='Edit')
    assert edits, "No Edit controls found in Inventory window"
    edit = edits[0]
    edit.click_input()
    send_keys('^a')
    send_keys(stock_num)
    send_keys('{TAB}')
    print(f"  Entered stock number: {stock_num}")


@when('I click the dropdown next to "{label_text}"')
def step_click_dropdown_next_to(context, label_text):
    s = context.s
    assert s.unit_inventory_hwnd, "Inventory window handle not set"
    win = Desktop(backend='uia').window(handle=s.unit_inventory_hwnd)
    ctypes.windll.user32.SetForegroundWindow(s.unit_inventory_hwnd)
    time.sleep(0.2)

    # Find the label, then locate the dropdown button adjacent to it
    label = win.child_window(title=label_text, class_name='ATLVPStaticClass31U')
    label.wait('exists visible', timeout=5)
    label_rect = label.rectangle()

    # Search the whole window for Button-class controls and pick the one
    # horizontally closest to the right of the label at the same row
    all_buttons = [
        b for b in win.descendants(control_type='Button')
        if b.element_info.class_name == 'Button'
    ]
    print(f"  Standard buttons found: "
          f"{[(str(getattr(b.element_info,'auto_id','')), b.rectangle()) for b in all_buttons]}")

    # Score: prefer buttons on the same row (top aligned) and just to the right
    def _score(b):
        r = b.rectangle()
        row_diff = abs(r.top - label_rect.top)
        col_diff = abs(r.left - label_rect.right)
        return row_diff * 100 + col_diff

    assert all_buttons, f"No standard Button controls found in Inventory window"
    dropdown = min(all_buttons, key=_score)
    print(f"  Chosen dropdown: auto_id={getattr(dropdown.element_info,'auto_id','')} "
          f"rect={dropdown.rectangle()}")
    dropdown.click_input()
    print(f"  Clicked dropdown next to '{label_text}'")


@when('I select "{option}" from the dropdown')
def step_select_from_dropdown(context, option):
    time.sleep(0.4)  # wait for dropdown list to open

    desktop = Desktop(backend='uia')
    selected = False

    # AccuTerm dropdowns appear as a floating popup — search the whole Desktop
    for _ in range(10):
        try:
            item = desktop.window(control_type='List').child_window(
                title=option, control_type='ListItem'
            )
            item.click_input()
            print(f"  Selected '{option}' via UIA ListItem")
            selected = True
            break
        except Exception:
            pass

        # Also try any combo-box popup visible on screen
        try:
            matches = desktop.find_elements(title=option, control_type='ListItem')
            if matches:
                matches[0].click_input()
                print(f"  Selected '{option}' via Desktop find_elements")
                selected = True
                break
        except Exception:
            pass

        time.sleep(0.3)

    if not selected:
        # Fallback: type option text and confirm with Enter
        send_keys(option + '{ENTER}')
        print(f"  Selected '{option}' via keyboard fallback")

    send_keys('{TAB}')


@when('I click "{button}" in the "{dialog_title}" dialog')
def step_click_in_dialog(context, button, dialog_title):
    hwnd = None
    for _ in range(15):
        h = findwindows.find_windows(title_re=f".*{dialog_title}.*")
        if h:
            hwnd = h[0]
            break
        time.sleep(1)
    assert hwnd, f'"{dialog_title}" dialog did not appear within 15s'

    ctypes.windll.user32.SetForegroundWindow(hwnd)
    time.sleep(0.2)

    win = Desktop(backend='uia').window(handle=hwnd)
    btn = win.child_window(title=button, control_type='Button')
    btn.click_input()
    print(f"  Clicked '{button}' in '{dialog_title}' dialog")

@when('I search for unit "{unit_number}"')
def step_search_unit(context, unit_number):
    s = context.s
    win = Desktop(backend='uia').window(handle=s.unit_inventory_hwnd)
    search_field = win.child_window(control_type='Edit')
    search_field.click_input()
    send_keys('^a')
    send_keys(unit_number)
    send_keys('{ENTER}')
    time.sleep(1)


@then('the unit "{unit_number}" appears in the results')
def step_unit_in_results(context, unit_number):
    s = context.s
    win = Desktop(backend='uia').window(handle=s.unit_inventory_hwnd)
    for _ in range(10):
        try:
            win.child_window(title_re=f'.*{unit_number}.*')
            print(f'  Unit {unit_number} found in results')
            return
        except Exception:
            time.sleep(1)
    raise AssertionError(f'Unit "{unit_number}" not found in results after 10s')


@when('I open unit "{unit_number}"')
def step_open_unit(context, unit_number):
    s = context.s
    win = Desktop(backend='uia').window(handle=s.unit_inventory_hwnd)
    row = win.child_window(title_re=f'.*{unit_number}.*')
    row.double_click_input()
    time.sleep(1)


@then('the unit detail window opens')
def step_unit_detail_opens(context):
    hwnd = None
    for _ in range(15):
        h = findwindows.find_windows(title_re=r'.*Unit.*')
        candidates = [x for x in h
                      if x != getattr(context.s, 'unit_inventory_hwnd', None)]
        if candidates:
            hwnd = candidates[0]
            break
        time.sleep(1)
    assert hwnd, 'Unit detail window did not open within 15s'
    context.s.unit_detail_hwnd = hwnd
    ctypes.windll.user32.SetForegroundWindow(hwnd)
