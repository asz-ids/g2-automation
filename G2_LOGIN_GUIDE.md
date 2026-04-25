# Using the G2 Login Screen Automation

## Overview

The `LoginScreen` class has been updated to work with the real G2 Login application. It includes:

- **UIA Property Support** - Matches the actual G2 Login window structure
- **Element Discovery** - Can detect elements from the running application
- **Real User Interaction** - Simulates actual keyboard and mouse input
- **Status Verification** - Checks if login succeeded

---

## Quick Start

### 1. Start the G2 Application

First, open the actual G2 Login application on your machine.

### 2. Create Login Script

```python
from screens.login_screen import LoginScreen
import time

# Create login screen instance
login = LoginScreen()

# Check if login screen is visible
if login.is_login_screen_visible():
    print("✓ G2 Login screen found")
    
    # Perform login
    login.login(
        username="domain\\myusername",
        password="mypassword",
        domain="DOMAIN"
    )
    
    # Wait for login to complete
    time.sleep(3)
    
    # Check if successful
    if login.is_login_successful(timeout_seconds=10):
        print("✓ Login successful!")
    else:
        print("✗ Login may have failed")
        login.capture_login_screen("login_failure.png")
else:
    print("✗ G2 Login screen not found")
```

### 3. Run the Script

```powershell
python -m pytest login_automation.py -v -s
```

---

## Methods Available

### Login Interaction

#### `login(username, password, domain="")`
Performs complete login sequence.

```python
login.login(
    username="domain\\user",
    password="pass123",
    domain="DOMAIN"
)
```

#### `enter_username(username)`
Enters only username.

```python
login.enter_username("domain\\user")
```

#### `enter_password(password)`
Enters only password.

```python
login.enter_password("password123")
```

#### `enter_domain(domain)`
Enters domain name.

```python
login.enter_domain("MYDOMAIN")
```

#### `click_login()`
Clicks the login button.

```python
success = login.click_login()
```

#### `click_cancel()`
Clicks the cancel button.

```python
login.click_cancel()
```

### Status Checking

#### `is_login_successful(timeout_seconds=10.0)`
Checks if login succeeded by looking for success indicators.

```python
if login.is_login_successful(timeout_seconds=10):
    print("Login worked!")
```

#### `is_login_screen_visible(timeout_seconds=5.0)`
Checks if the login screen is currently visible.

```python
if login.is_login_screen_visible():
    print("Login screen is open")
```

#### `get_login_status()`
Gets comprehensive status information.

```python
status = login.get_login_status()
print(status)
# Output: {
#     'screen_name': 'G2LoginScreen',
#     'root_element': 'LoginForm',
#     'elements_count': 8,
#     'is_visible': True
# }
```

### Screenshots

#### `capture_login_screen(filename="login_screen.png")`
Captures screenshot of the login screen.

```python
path = login.capture_login_screen("current_login.png")
```

---

## Complete Example Test

```python
import pytest
from screens.login_screen import LoginScreen
import time

class TestG2Login:
    """Test G2 login functionality with real application."""
    
    def test_successful_login(self):
        """Test successful login with valid credentials."""
        login = LoginScreen()
        
        # Verify login screen is visible
        assert login.is_login_screen_visible(), "Login screen not found"
        
        # Capture before login
        login.capture_login_screen("before_login.png")
        
        # Perform login
        success = login.login(
            username="domain\\testuser",
            password="testpass",
            domain="DOMAIN"
        )
        assert success, "Login button click failed"
        
        # Wait and verify
        time.sleep(2)
        assert login.is_login_successful(timeout_seconds=10), \
            "Login did not complete successfully"
        
        # Capture after login
        login.capture_login_screen("after_login.png")
    
    def test_invalid_credentials(self):
        """Test login with invalid credentials."""
        login = LoginScreen()
        
        assert login.is_login_screen_visible()
        
        # Try login with bad credentials
        login.login(
            username="domain\\baduser",
            password="wrongpass"
        )
        
        # Should see error
        assert not login.is_login_successful(timeout_seconds=5), \
            "Login should have failed with bad credentials"
        
        # Verify error message
        assert login.verify_text_present("Invalid") or \
               login.verify_text_present("Incorrect"), \
            "Expected error message not shown"
    
    def test_cancel_login(self):
        """Test canceling login."""
        login = LoginScreen()
        
        assert login.is_login_screen_visible()
        
        # Enter credentials but don't submit
        login.enter_username("domain\\user")
        
        # Click cancel
        login.click_cancel()
        
        # Should stay on login screen
        time.sleep(1)
        assert login.is_login_screen_visible()
```

---

## Element Structure (UIA Properties)

The login screen is structured as:

```
Window (title="G2 Login", auto_id="LoginForm")
├── Pane (title="Desktop 1")
│   └── Group (auto_id="ultraGroupBox1")
│       ├── Text (title="Domain", auto_id="lblDomain")
│       ├── Pane (auto_id="txtDomain")
│       ├── Text (title="User ID", auto_id="ultraLabel1")
│       ├── Pane (auto_id="txtUser")
│       ├── Text (title="Password", auto_id="ultraLabel2")
│       ├── Pane (auto_id="txtPwd")
│       ├── Button (title="Login", auto_id="btnLogin")
│       └── Button (title="Cancel", auto_id="btnCancel")
```

---

## Important Notes

### Application Must Be Running

The framework needs the G2 application to be running:

```powershell
# Start G2 application first
# Then run your automation

python -m pytest test_g2_login.py -v -s
```

### Element Discovery

If the element structure differs from expectations, you can:

1. **Use Inspect.exe** (Windows)
   - Run `inspect.exe` to see actual UIA properties
   - Compare with expected structure
   - Update element definitions if needed

2. **Enable Live Discovery**
   ```python
   login = LoginScreen(discover_from_uia=True)
   ```

### Timing Considerations

Add appropriate delays for network operations:

```python
login.login(username="user", password="pass")
time.sleep(2)  # Wait for authentication
assert login.is_login_successful(timeout_seconds=10)
```

---

## Troubleshooting

### "Login screen not found"

**Problem**: `is_login_screen_visible()` returns False

**Solutions**:
1. Ensure G2 is running and login window is visible
2. Check window title is exactly "G2 Login"
3. Verify UIA properties using Inspect.exe
4. Increase timeout: `is_login_screen_visible(timeout_seconds=10)`

### "Elements not found"

**Problem**: Cannot locate text fields or buttons

**Solutions**:
1. Verify auto_ids match your G2 version
2. Use Inspect.exe to find correct IDs
3. Update element definitions in `_setup_elements_manual()`
4. Try element finding by title instead of auto_id

### "Keys not typed"

**Problem**: Username/password not appearing in fields

**Solutions**:
1. Verify application has focus
2. Add delay before typing: `time.sleep(0.5)`
3. Use keyboard handler directly for control: `login.keyboard.type_text()`
4. Check if field requires special activation

### "Login button not responding"

**Problem**: Click doesn't submit login

**Solutions**:
1. Verify button location hasn't changed
2. Add delay before checking result: `time.sleep(2)`
3. Try double-clicking: `login.mouse.double_click_element(button)`
4. Use keyboard shortcut: `login.keyboard.send_enter()`

---

## Advanced Usage

### Custom Element Discovery

If your G2 version has different element IDs:

```python
class CustomLoginScreen(LoginScreen):
    def _setup_elements_manual(self):
        # Override with your custom element structure
        root = Element(
            name="LoginForm",
            properties=UIAProperty(
                control_type="Window",
                title="G2 Login",
                auto_id="MyCustomID"  # Your custom ID
            )
        )
        # ... add your custom elements
```

### Extending Functionality

Add custom methods for your specific needs:

```python
class G2LoginScreen(LoginScreen):
    def remember_me(self):
        """Click remember me checkbox if present."""
        remember = Locator.by_auto_id("chkRemember").find(self._root_element)
        if remember:
            self.click_element(remember)
    
    def reset_password(self):
        """Click forgot password link."""
        reset = Locator.by_title("Forgot Password").find(self._root_element)
        if reset:
            self.click_element(reset)
```

---

## Running Real Tests

Create a test file `test_g2_real_login.py`:

```python
import pytest
from screens.login_screen import LoginScreen

@pytest.fixture
def login_screen():
    return LoginScreen()

def test_app_loads(login_screen):
    """Test that G2 login screen loads."""
    assert login_screen.is_login_screen_visible()

def test_login_with_valid_credentials(login_screen):
    """Test login with real credentials."""
    # Update with your test credentials
    login_screen.login(
        username="DOMAIN\\testuser",
        password="testpass123"
    )
    assert login_screen.is_login_successful()
```

Run with:

```powershell
python -m pytest test_g2_real_login.py -v -s
```

---

## Best Practices

1. **Always check screen visibility first**
   ```python
   if login.is_login_screen_visible():
       login.login(...)
   ```

2. **Capture screenshots for debugging**
   ```python
   try:
       login.login(...)
   except Exception as e:
       login.capture_login_screen("error.png")
       raise
   ```

3. **Use appropriate timeouts**
   ```python
   login.is_login_successful(timeout_seconds=15)  # For slow networks
   ```

4. **Handle authentication delays**
   ```python
   login.login(...)
   time.sleep(3)  # Wait for auth backend
   assert login.is_login_successful()
   ```

5. **Store credentials securely**
   ```python
   import os
   username = os.environ.get("TEST_USER")
   password = os.environ.get("TEST_PASS")
   login.login(username, password)
   ```

---

## Summary

The G2 Login Screen automation is now ready to:

✅ Interact with the real G2 Login application  
✅ Enter username, password, and domain  
✅ Click login and cancel buttons  
✅ Verify login success or failure  
✅ Capture screenshots for debugging  
✅ Handle various error conditions  

**Get started**: Run your G2 application and execute tests!
