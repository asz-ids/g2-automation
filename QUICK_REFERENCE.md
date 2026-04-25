# G2 Automation - Quick Reference Card

## 🚀 Get Started (Copy & Paste)

### 1. Basic Login Test
```python
from screens.login_screen import LoginScreen
import time

login = LoginScreen()

# Check screen is visible
if login.is_login_screen_visible():
    # Login
    login.login(
        username="DOMAIN\\user",
        password="password",
        domain="DOMAIN"
    )
    
    # Wait for auth
    time.sleep(3)
    
    # Verify success
    if login.is_login_successful():
        print("✓ Login successful!")
    else:
        print("✗ Login failed")
else:
    print("✗ Login screen not found")
```

### 2. Quick Troubleshoot
```powershell
# Check if diagnostic works
python g2_diagnostic.py

# Review findings
cat g2_element_map.json
cat g2_hierarchy.json
```

### 3. Run Full Example
```powershell
# Edit with your credentials first
notepad g2_login_example.py

# Then run
python g2_login_example.py
```

---

## 📋 Method Cheat Sheet

### Entry Methods
```python
login.enter_username("user")      # Type username
login.enter_password("pass")      # Type password  
login.enter_domain("DOMAIN")      # Type domain
login.click_login()               # Click login button
login.click_cancel()              # Click cancel
```

### Verification Methods
```python
login.is_login_screen_visible()   # Screen exists?
login.is_login_successful()       # Logged in?
login.get_login_status()          # Status dict
login.verify_text_present("error") # Text exists?
```

### Screenshot Methods
```python
login.capture_login_screen("img.png")  # Save screenshot
```

### Combined Login
```python
login.login(
    username="DOMAIN\\user",
    password="pass123",
    domain="DOMAIN"
)
```

---

## 🔧 Common Patterns

### Pattern 1: Simple Login
```python
login = LoginScreen()
login.login("DOMAIN\\user", "password")
assert login.is_login_successful()
```

### Pattern 2: With Error Checking
```python
if not login.is_login_screen_visible():
    print("Screen not found!")
    exit(1)

success = login.login("DOMAIN\\user", "pass")
if not success:
    login.capture_login_screen("error.png")
    print("Login failed - check error.png")
```

### Pattern 3: With Delays
```python
login.login("DOMAIN\\user", "pass")
time.sleep(2)  # Wait for auth
assert login.is_login_successful(timeout_seconds=10)
```

### Pattern 4: Test Invalid Credentials
```python
login = LoginScreen()
login.login("DOMAIN\\baduser", "wrongpass")
time.sleep(1)
assert not login.is_login_successful(timeout_seconds=5)
```

### Pattern 5: pytest Test
```python
def test_g2_login():
    login = LoginScreen()
    assert login.is_login_screen_visible()
    login.login("DOMAIN\\user", "pass")
    assert login.is_login_successful()
```

---

## ❌ Troubleshooting Quick Fixes

### "Screen not found"
```powershell
# 1. Run diagnostic
python g2_diagnostic.py

# 2. If it finds screen, increase timeout
login.is_login_screen_visible(timeout_seconds=10)

# 3. If still not working, check G2 is actually running
tasklist | findstr G2
```

### "Elements not found or not clickable"
```python
# 1. Run diagnostic to see actual structure
python g2_diagnostic.py

# 2. Check element IDs in g2_element_map.json

# 3. Update login_screen.py if IDs differ

# 4. Try keyboard shortcut instead
login.keyboard.send_tab()
login.keyboard.send_enter()
```

### "Password/username not typed"
```python
# Add delay before typing
time.sleep(0.5)
login.enter_username("user")

# Or click field first
login.click_element(username_field)
time.sleep(0.2)
login.keyboard.type_text("username")
```

### "Login not recognized"
```python
# 1. Increase timeout
login.is_login_successful(timeout_seconds=15)

# 2. Add delay after click
login.click_login()
time.sleep(5)  # Wait longer

# 3. Take screenshot to see result
login.capture_login_screen("result.png")
```

---

## 📂 File Locations

| File | What | Where |
|------|------|-------|
| Example | Simple login demo | `g2_login_example.py` |
| Diagnostic | Debug tool | `g2_diagnostic.py` |
| Guide | Complete docs | `G2_LOGIN_GUIDE.md` |
| Tests | All examples | `tests/test_login_screen.py` |
| Code | Main class | `screens/login_screen.py` |
| API | Full reference | `API_REFERENCE.md` |

---

## 🧪 Test & Verify

### Check Everything Works
```powershell
# Run all tests (should see 14 passed)
python -m pytest tests/ -v

# Run diagnostic
python g2_diagnostic.py

# Run example
python g2_login_example.py
```

### Expected Results
```
✓ 14 tests pass in ~7 seconds
✓ Diagnostic finds G2 window
✓ Example shows login process
✓ Screenshots saved to /screenshots folder
```

---

## 🎯 Common Tasks

### Task: Find out what elements exist in G2
```powershell
python g2_diagnostic.py
# Check g2_hierarchy.json and g2_element_map.json
```

### Task: Login to G2 in a test
```python
def test_login():
    from screens.login_screen import LoginScreen
    login = LoginScreen()
    login.login("DOMAIN\\testuser", "testpass")
    assert login.is_login_successful()
```

### Task: Login and take screenshot
```python
login.login("DOMAIN\\user", "pass")
login.capture_login_screen("after_login.png")
```

### Task: Check if specific text appears
```python
if login.verify_text_present("Welcome"):
    print("Login successful")
```

### Task: Use keyboard instead of click
```python
login.keyboard.send_tab()      # Move to next field
login.keyboard.send_enter()    # Press Enter
login.keyboard.key_combination("alt", "l")  # Alt+L
```

---

## 🔑 Credentials Format

### With Domain
```python
login.login(
    username="DOMAIN\\user",
    password="password",
    domain="DOMAIN"
)
```

### Without Domain
```python
login.login(
    username="user",
    password="password"
)
```

### From Environment
```python
import os
login.login(
    username=os.environ["G2_USER"],
    password=os.environ["G2_PASSWORD"]
)
```

---

## ⏱️ Timeouts & Delays

### Login Success Check
```python
# Default: 10 seconds
login.is_login_successful()

# Custom: 20 seconds
login.is_login_successful(timeout_seconds=20)

# For slow network: 30+ seconds
login.is_login_successful(timeout_seconds=30)
```

### Screen Visibility Check
```python
# Default: 5 seconds
login.is_login_screen_visible()

# Custom: 15 seconds
login.is_login_screen_visible(timeout_seconds=15)
```

### Manual Delay
```python
import time
time.sleep(2)  # Wait 2 seconds
```

---

## 📊 Status Dictionary

```python
status = login.get_login_status()
# Returns:
# {
#     'screen_name': 'G2LoginScreen',
#     'root_element': 'LoginForm',
#     'elements_count': 8,
#     'is_visible': True
# }

print(status['screen_name'])
print(status['is_visible'])
```

---

## 🛠️ Advanced Usage

### Custom Screen Object
```python
from screens.login_screen import LoginScreen

class MyLoginScreen(LoginScreen):
    def remember_me_login(self, user, pwd):
        self.login(user, pwd)
        # Add custom logic
        self.click_remember()
```

### Direct Element Access
```python
# Get element directly
username = login.locator.by_auto_id("txtUser").find(login._root_element)
if username:
    login.click_element(username)
    login.keyboard.type_text("myuser")
```

### With Screenshot Comparison
```python
# Capture initial
login.capture_login_screen("before.png")

# Do login
login.login("user", "pass")

# Capture after
login.capture_login_screen("after.png")

# Compare (if adding visual comparison)
```

---

## 🚨 Debug Mode

### Print Status
```python
status = login.get_login_status()
print(f"Screen visible: {status['is_visible']}")
print(f"Elements found: {status['elements_count']}")
```

### Take Screenshots
```python
login.capture_login_screen("debug1.png")
# Do something
login.capture_login_screen("debug2.png")
```

### Check Element Location
```python
# Use get_login_status to see what's found
# Check g2_element_map.json for details
# Run g2_diagnostic.py for full structure
```

### Enable Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## ✅ Pre-Flight Checklist

Before running:
- [ ] G2 application is running
- [ ] Login screen is visible
- [ ] Not already logged in
- [ ] Python environment activated
- [ ] All packages installed (pytest --version works)
- [ ] Credentials updated in script
- [ ] Network connection active

---

## 📞 Help Commands

```powershell
# Run diagnostic to debug issues
python g2_diagnostic.py

# Check all tests pass
python -m pytest tests/ -v

# Run with more info
python -m pytest tests/ -v -s

# See installed packages
pip list

# Check Python version
python --version
```

---

## 🎓 Learning Resources

1. **Start Here**: `g2_login_example.py` - Copy and modify
2. **Full Guide**: `G2_LOGIN_GUIDE.md` - Read for details
3. **API Reference**: `API_REFERENCE.md` - All methods
4. **Architecture**: `ARCHITECTURE.md` - How it works
5. **Tests**: `tests/test_login_screen.py` - Real examples
6. **Patterns**: `PATTERNS_AND_EXAMPLES.md` - Common patterns

---

## 🏁 Success!

Once you:
1. ✅ Run `g2_login_example.py` successfully
2. ✅ See "Login successful!" message  
3. ✅ Screenshots saved in `/screenshots`

You're ready to:
- 📝 Write your own tests
- 🔗 Extend to other screens
- 🚀 Build full automation suites
- 📊 Integrate with CI/CD

---

**Remember**: Start with `g2_login_example.py` and modify from there!
