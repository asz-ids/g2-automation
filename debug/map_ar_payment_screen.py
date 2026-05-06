"""
Map all UIA elements from the Accounts Receivable Payment window.
Run while the AR Payment window is open in G2.
"""
import sys
sys.path.insert(0, r'E:\G2 Desktop Automation')

from pywinauto import Desktop, findwindows

AR_TITLE_RE = r".*Accounts Receivable.*"

def props(elem):
    """Extract key UIA properties from an element."""
    p = {}
    try: p['control_type'] = elem.element_info.control_type
    except: p['control_type'] = ''
    try: p['auto_id'] = elem.element_info.automation_id
    except: p['auto_id'] = ''
    try: p['title'] = elem.window_text()
    except: p['title'] = ''
    try: p['class_name'] = elem.element_info.class_name
    except: p['class_name'] = ''
    return p


def walk(elem, depth=0, max_depth=12, results=None):
    """Recursively walk the element tree and collect all nodes."""
    if results is None:
        results = []
    if depth > max_depth:
        return results

    try:
        p = props(elem)
        results.append((depth, p))
        try:
            for child in elem.children():
                walk(child, depth + 1, max_depth, results)
        except Exception:
            pass
    except Exception:
        pass

    return results


def main():
    handles = findwindows.find_windows(title_re=AR_TITLE_RE)
    if not handles:
        print("ERROR: Accounts Receivable Payment window not found. Open it in G2 first.")
        return

    hwnd = handles[0]
    print(f"Found AR window: HWND {hwnd}")
    win = Desktop(backend='uia').window(handle=hwnd)

    print("\nUIA Element Tree — Accounts Receivable Payment")
    print("=" * 80)

    results = walk(win)

    for depth, p in results:
        indent = "  " * depth
        ct    = p['control_type'] or '-'
        aid   = f"  auto_id={p['auto_id']!r}"   if p['auto_id']   else ''
        title = f"  title={p['title']!r}"        if p['title']     else ''
        cls   = f"  class={p['class_name']!r}"   if p['class_name'] else ''
        print(f"{indent}[{ct}]{aid}{title}{cls}")

    print(f"\nTotal elements: {len(results)}")

    # Also dump a flat list of all elements with auto_id or title for quick reference
    print("\n--- Elements with auto_id ---")
    for depth, p in results:
        if p['auto_id']:
            print(f"  auto_id={p['auto_id']!r:30s}  control_type={p['control_type']!r:12s}  title={p['title']!r}")

    print("\n--- Named elements (title, no auto_id) ---")
    seen_titles = set()
    for depth, p in results:
        if p['title'] and not p['auto_id'] and p['title'] not in seen_titles:
            seen_titles.add(p['title'])
            print(f"  title={p['title']!r:40s}  control_type={p['control_type']!r}")


if __name__ == "__main__":
    main()
