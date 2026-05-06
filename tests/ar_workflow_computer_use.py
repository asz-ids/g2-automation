"""
Accounts Receivable Workflow — Claude Computer Use Agent
Replicates accounts_receivable_workflow.py using the Claude Computer Use API
instead of pywinauto.

Usage:
    set ANTHROPIC_API_KEY=sk-ant-...
    python ar_workflow_computer_use.py

Credentials default to the QA account used in accounts_receivable_workflow.py.
Override with env vars: IDS_USERNAME, IDS_PASSWORD
"""

import base64
import os
import subprocess
import sys
import time
from io import BytesIO

import anthropic
import mss
import pyautogui
from PIL import Image

# ──────────────────────────────────────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────────────────────────────────────

G2_EXE       = r"C:\IDSASTRA\APPS\G2\G2CLIENT\IdsG2Client.exe"
USERNAME     = os.environ.get("IDS_USERNAME", "aqadir.ids")
PASSWORD     = os.environ.get("IDS_PASSWORD", "Aqadir2801")
API_KEY      = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL        = "claude-opus-4-7"
MAX_STEPS    = 80
CLAUDE_MAX   = 1568   # max long-edge dimension for screenshots

# ──────────────────────────────────────────────────────────────────────────────
# Screenshot / scaling
# ──────────────────────────────────────────────────────────────────────────────

def take_screenshot() -> tuple[str, int, int]:
    with mss.mss() as sct:
        mon = sct.monitors[0]
        raw = sct.grab(mon)
        img = Image.frombytes("RGB", (raw.width, raw.height), raw.rgb)

    aw, ah = img.size
    if max(aw, ah) > CLAUDE_MAX:
        scale = CLAUDE_MAX / max(aw, ah)
        img = img.resize((int(aw * scale), int(ah * scale)), Image.LANCZOS)

    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.standard_b64encode(buf.getvalue()).decode(), aw, ah


def scale_up(x: int, y: int, aw: int, ah: int) -> tuple[int, int]:
    if max(aw, ah) > CLAUDE_MAX:
        s = CLAUDE_MAX / max(aw, ah)
        return int(x / s), int(y / s)
    return x, y


# ──────────────────────────────────────────────────────────────────────────────
# Action executor
# ──────────────────────────────────────────────────────────────────────────────

def execute_action(action: dict, aw: int, ah: int) -> str:
    atype = action.get("action", "")

    if atype == "screenshot":
        return "screenshot"

    if atype in ("left_click", "right_click", "double_click", "mouse_move"):
        cx, cy = action["coordinate"]
        rx, ry = scale_up(cx, cy, aw, ah)
        pyautogui.moveTo(rx, ry, duration=0.15)
        if atype == "left_click":
            pyautogui.click()
        elif atype == "right_click":
            pyautogui.rightClick()
        elif atype == "double_click":
            pyautogui.doubleClick()
        return f"{atype} ({rx},{ry})"

    if atype == "left_click_drag":
        cx, cy = action["coordinate"]
        ex, ey = action.get("end_coordinate", [cx, cy])
        rx, ry = scale_up(cx, cy, aw, ah)
        rex, rey = scale_up(ex, ey, aw, ah)
        pyautogui.moveTo(rx, ry, duration=0.1)
        pyautogui.dragTo(rex, rey, duration=0.3, button="left")
        return f"drag ({rx},{ry})→({rex},{rey})"

    if atype == "type":
        text = action.get("text", "")
        pyautogui.typewrite(text, interval=0.04)
        return f"type {text!r}"

    if atype == "key":
        key = action.get("key", "")
        key_map = {
            "Return": "enter", "Tab": "tab", "Escape": "escape",
            "BackSpace": "backspace", "Delete": "delete",
            "ctrl+a": ["ctrl", "a"], "ctrl+c": ["ctrl", "c"],
            "ctrl+v": ["ctrl", "v"], "ctrl+z": ["ctrl", "z"],
        }
        mapped = key_map.get(key, key)
        if isinstance(mapped, list):
            pyautogui.hotkey(*mapped)
        elif "+" in mapped:
            pyautogui.hotkey(*mapped.split("+"))
        else:
            pyautogui.press(mapped)
        return f"key {key}"

    if atype == "scroll":
        cx, cy = action.get("coordinate", [0, 0])
        rx, ry = scale_up(cx, cy, aw, ah)
        direction = action.get("direction", "down")
        amount = action.get("amount", 3)
        pyautogui.scroll(-amount if direction == "down" else amount, x=rx, y=ry)
        return f"scroll {direction} {amount} at ({rx},{ry})"

    return f"unknown: {atype}"


# ──────────────────────────────────────────────────────────────────────────────
# Agent loop
# ──────────────────────────────────────────────────────────────────────────────

def run_agent(task: str) -> None:
    if not API_KEY:
        sys.exit("ERROR: Set ANTHROPIC_API_KEY environment variable.")

    client = anthropic.Anthropic(api_key=API_KEY)
    img_b64, aw, ah = take_screenshot()

    long_edge = max(aw, ah)
    disp_w = int(aw * CLAUDE_MAX / long_edge) if long_edge > CLAUDE_MAX else aw
    disp_h = int(ah * CLAUDE_MAX / long_edge) if long_edge > CLAUDE_MAX else ah

    tools = [{
        "type": "computer_20251124",
        "name": "computer",
        "display_width_px": disp_w,
        "display_height_px": disp_h,
        "display_number": 1,
    }]

    messages = [{
        "role": "user",
        "content": [
            {"type": "text", "text": task},
            {"type": "image", "source": {
                "type": "base64", "media_type": "image/png", "data": img_b64
            }},
        ],
    }]

    print(f"Screen: {aw}x{ah}  Claude sees: {disp_w}x{disp_h}")
    print("=" * 70)

    for step in range(MAX_STEPS):
        print(f"\n[Step {step + 1}] Querying Claude...")

        response = client.beta.messages.create(
            model=MODEL,
            max_tokens=4096,
            tools=tools,
            messages=messages,
            betas=["computer-use-2025-11-24"],
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            print("\n[DONE] Claude completed the workflow.")
            for b in response.content:
                if hasattr(b, "text") and b.text:
                    print(f"  Claude: {b.text}")
            break

        if response.stop_reason != "tool_use":
            print(f"[STOP] stop_reason={response.stop_reason}")
            break

        tool_results = []
        for block in response.content:
            if hasattr(block, "text") and block.text:
                print(f"  Claude: {block.text}")
            if block.type != "tool_use":
                continue

            action = block.input
            print(f"  → {action.get('action', '?')} {action}")
            result = execute_action(action, aw, ah)
            print(f"    {result}")

            time.sleep(0.7)

            img_b64, aw, ah = take_screenshot()
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": [{
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/png", "data": img_b64},
                }],
            })

        messages.append({"role": "user", "content": tool_results})

    else:
        print(f"\n[LIMIT] Reached max steps ({MAX_STEPS}).")


# ──────────────────────────────────────────────────────────────────────────────
# Workflow task prompt
# ──────────────────────────────────────────────────────────────────────────────

TASK = f"""
You are automating a Windows desktop application called IDS ASTRA G2.
Follow these steps EXACTLY in order. Take a screenshot before each action
to confirm the current state. Be patient — windows can take 30-60 seconds to load.

STEP 1 — LAUNCH
  The G2 Client is launching (or may already be open). Wait for a window
  titled "G2 Login" to appear.

STEP 2 — LOGIN
  In the G2 Login window:
    • Click the Username field and type: {USERNAME}
    • Click the Password field and type: {PASSWORD}
    • Click the Login button.
  Wait up to 60 seconds for a window containing "Navigator" in its title.

STEP 3 — NAVIGATOR → ACCOUNTING
  In the Navigator window:
    • Maximise it if it is not already maximised.
    • Click the button labelled "Accounting".
  Wait for the Accounting sub-menu to appear.

STEP 4 — ACCOUNTS RECEIVABLE
  Click the button labelled "Accounts Receivable".

STEP 5 — TAKE CUSTOMER DEPOSITS
  Click the button labelled "Take Customer Deposits".
  Wait up to 30 seconds for a window with "Customer Deposits" in its title.

STEP 6 — ENTER CUSTOMER NUMBER
  In the Customer Deposits window:
    • Click on the first input field (customer number field).
    • Type: 4268
    • Press Tab.
  Wait 2 seconds for the customer record to load.

STEP 7 — CLICK COMMAND BUTTON
  Find and click the first available command / action button in the
  Customer Deposits window (it may be labelled "New", "Add", or similar).

STEP 8 — DESCRIPTION
  Find the Description field and type a short random description
  (e.g. "Deposit-TEST01").

STEP 9 — AMOUNT
  Find the Amount field and type a random amount between 100 and 9999
  (e.g. 1234).

STEP 10 — SAVE
  Click the Save button (usually in the toolbar at the top of the window).
  Wait 2 seconds.

STEP 11 — TAKE PAYMENT → CREDIT
  A "Take Payment" window will appear. Click the "Credit" button inside it.

STEP 12 — IDSPAY WINDOW
  Wait up to 60 seconds for a window titled "IDSPay" to open.
  The web content inside takes 30-40 seconds to fully render — wait for it.
  Then click the "SAVED CARDS" tab (approximately 58% across, 16% down
  from the top of the IDSPay window).
  Wait 5 seconds for the saved-cards list to appear.

STEP 13 — PROCESS PAYMENT
  Click the "PROCESS PAYMENT" button inside the IDSPay window.
  Wait up to 60 seconds for the IDSPay window to close automatically.

STEP 14 — REVERSE PAYMENT
  Back in the Take Payment window, find the payment grid and click
  the first row (Row 0) which will be a clickable hyperlink.
  A dialog titled "Reverse Payment" will appear — click the "Yes" button.

STEP 15 — DONE
  Confirm the workflow completed successfully and say "Workflow complete".

IMPORTANT NOTES:
  - Always verify each step visually before proceeding.
  - If a dialog or error pops up that is not part of the workflow, dismiss it
    (press Escape or click OK/Cancel) and then continue.
  - Do not skip steps; do not proceed if a required window is not visible.
  - IDSPay contains a WebView2 embedded browser — its content loads slowly.
""".strip()


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    pyautogui.FAILSAFE = True

    print("=" * 70)
    print("Accounts Receivable Workflow — Claude Computer Use Agent")
    print("=" * 70)
    print(f"User: {USERNAME}")
    print(f"Exe:  {G2_EXE}")
    print()

    print("Launching G2 Client...")
    subprocess.Popen([G2_EXE])
    print("Waiting 5 s for application to start...")
    time.sleep(5)

    run_agent(TASK)
