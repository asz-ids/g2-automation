# Documentation Index

## Complete G2 Desktop Automation Framework Documentation

Welcome to the G2 Desktop Automation Framework documentation. This index helps you navigate all available resources.

---

## 📚 Getting Started

### [QUICK_START.md](QUICK_START.md)
**Duration: 5-10 minutes**
- Installation steps
- First test setup
- Common tasks reference
- Troubleshooting quick fixes
- Key methods reference table

👉 **Start here if you're new to the framework**

---

## 📖 Main Documentation

### [README.md](README.md)
**Project Overview**
- Feature list
- Project structure
- Installation instructions
- Basic usage examples
- Running tests
- Configuration

### [USAGE_GUIDE.md](USAGE_GUIDE.md)
**Complete Usage Guide**
- Feature overview
- Installation with prerequisites
- Core components detailed explanation:
  - Element class
  - Locator system
  - Text tracking
  - Screenshots
  - Keyboard handling
  - Mouse control
  - UIA driver
  - Base screen
- Page object pattern
- Test execution
- Configuration options
- Best practices
- Troubleshooting guide
- Advanced topics

👉 **Read this for comprehensive understanding**

---

## 🔍 Technical References

### [API_REFERENCE.md](API_REFERENCE.md)
**Complete API Documentation**
- Core components API:
  - Element class methods
  - UIAProperty class
  - Locator class
  - LocatorBuilder class
- Handler APIs:
  - TextTracker
  - ScreenshotManager
  - KeyboardHandler
  - MouseHandler
- Driver API (UIADriver)
- Screen API (BaseScreen)
- Enums reference
- Configuration constants
- Pytest fixtures
- Return types and exceptions

👉 **Use this when you need to look up specific methods**

### [ARCHITECTURE.md](ARCHITECTURE.md)
**Framework Architecture**
- Design principles
- Component hierarchy and layers
- Data flow diagrams
- Element hierarchy model
- Locator strategy pattern
- Configuration management
- Error handling strategy
- Caching strategy
- Extension points
- Performance considerations
- Maintenance guidelines
- Future enhancements

👉 **Read this to understand the framework structure**

---

## 💡 Patterns & Examples

### [PATTERNS_AND_EXAMPLES.md](PATTERNS_AND_EXAMPLES.md)
**Common Patterns & Real Examples**
- Page object pattern (basic & advanced)
- Test patterns (basic, parameterized, fixtures)
- Element interaction patterns
- Text verification patterns
- Screenshot patterns
- Wait and synchronization
- Error handling patterns
- Data-driven testing
- Performance testing
- Best practices checklist
- Common gotchas and solutions
- Quick reference guide

👉 **Reference this for code examples and patterns**

---

## 📁 Project Structure

```
e:\G2 Desktop Automation\
│
├── Documentation (You are here)
│   ├── README.md                      # Project overview
│   ├── QUICK_START.md                # 5-minute setup guide
│   ├── USAGE_GUIDE.md                # Comprehensive usage
│   ├── API_REFERENCE.md              # Complete API docs
│   ├── ARCHITECTURE.md               # Design & structure
│   ├── PATTERNS_AND_EXAMPLES.md      # Code examples
│   └── DOCUMENTATION_INDEX.md        # This file
│
├── Core Framework
│   ├── core/                         # Core components
│   │   ├── element.py               # UI element representation
│   │   ├── locator.py               # Element finding strategies
│   │   ├── text_tracker.py          # Text detection & verification
│   │   ├── screenshot_manager.py    # Screenshot capture & compare
│   │   ├── keyboard_handler.py      # Keyboard input
│   │   ├── mouse_handler.py         # Mouse interaction
│   │   └── __init__.py
│   │
│   ├── drivers/                      # Integration drivers
│   │   ├── uia_driver.py            # UI Automation bridge
│   │   └── __init__.py
│   │
│   └── config/                       # Configuration
│       ├── settings.py              # Framework settings
│       └── __init__.py
│
├── Screen Objects
│   ├── screens/                      # Page objects
│   │   ├── base_screen.py           # Base screen class
│   │   ├── login_screen.py          # Example screen
│   │   └── __init__.py
│
├── Tests
│   ├── tests/                        # Test suites
│   │   ├── conftest.py              # Pytest fixtures
│   │   ├── test_login_screen.py     # Example tests
│   │   └── __init__.py
│
└── Configuration
    └── requirements.txt              # Python dependencies
```

---

## 🚀 Quick Navigation

### I want to...

**Get started quickly**
→ [QUICK_START.md](QUICK_START.md)

**Understand the framework**
→ [USAGE_GUIDE.md](USAGE_GUIDE.md)

**Look up a specific method**
→ [API_REFERENCE.md](API_REFERENCE.md)

**See code examples**
→ [PATTERNS_AND_EXAMPLES.md](PATTERNS_AND_EXAMPLES.md)

**Understand the architecture**
→ [ARCHITECTURE.md](ARCHITECTURE.md)

**Set up my development environment**
→ [QUICK_START.md - Step 1](QUICK_START.md#step-1-install-dependencies)

**Create a new screen object**
→ [PATTERNS_AND_EXAMPLES.md - Page Object Pattern](PATTERNS_AND_EXAMPLES.md#page-object-pattern)

**Write a test**
→ [PATTERNS_AND_EXAMPLES.md - Test Patterns](PATTERNS_AND_EXAMPLES.md#test-patterns)

**Find an element**
→ [USAGE_GUIDE.md - Locator System](USAGE_GUIDE.md#2-locator-system-corelocatorpy)

**Interact with keyboard**
→ [USAGE_GUIDE.md - Keyboard Handler](USAGE_GUIDE.md#5-keyboard-handler-corekeyboard_handlerpy)

**Control mouse**
→ [USAGE_GUIDE.md - Mouse Handler](USAGE_GUIDE.md#6-mouse-handler-coremouse_handlerpy)

**Verify text**
→ [USAGE_GUIDE.md - Text Tracking](USAGE_GUIDE.md#3-text-tracking-coretext_trackerpy)

**Take screenshots**
→ [USAGE_GUIDE.md - Screenshot Management](USAGE_GUIDE.md#4-screenshot-management-corescreenshot_managerpy)

**Debug a failing test**
→ [USAGE_GUIDE.md - Troubleshooting](USAGE_GUIDE.md#troubleshooting)

**Configure the framework**
→ [USAGE_GUIDE.md - Configuration](USAGE_GUIDE.md#configuration)

---

## 📋 Key Components Overview

### Core Elements
| Component | File | Purpose |
|-----------|------|---------|
| **Element** | `core/element.py` | Represents UI elements with hierarchy |
| **Locator** | `core/locator.py` | Find elements using various strategies |
| **TextTracker** | `core/text_tracker.py` | Detect and verify text on screen |
| **ScreenshotManager** | `core/screenshot_manager.py` | Capture and compare screenshots |
| **KeyboardHandler** | `core/keyboard_handler.py` | Simulate keyboard input |
| **MouseHandler** | `core/mouse_handler.py` | Simulate mouse interactions |
| **UIADriver** | `drivers/uia_driver.py` | UI Automation element discovery |
| **BaseScreen** | `screens/base_screen.py` | Base class for screen objects |

### Key Classes & Methods

**Finding Elements:**
```python
Locator.by_auto_id("id").find(root)
Locator.by_control_type("Button").find_all(root)
```

**Element Interaction:**
```python
screen.click_element(element)
screen.type_in_element(element, "text")
screen.drag_element(source, target)
```

**Text Operations:**
```python
TextValidator.validate_text_present("text")
tracker.wait_for_text("text", timeout=10)
tracker.find_text("text")
```

**Screenshots:**
```python
screenshots.capture_screenshot("name.png")
screenshots.compare_screenshots("img1", "img2")
```

---

## 🔗 Documentation Reading Order

### For New Users
1. README.md (2 min) - Get context
2. QUICK_START.md (5 min) - Setup & first test
3. PATTERNS_AND_EXAMPLES.md (10 min) - See code examples
4. USAGE_GUIDE.md (30 min) - Deep dive into components

### For Developers
1. ARCHITECTURE.md (15 min) - Understand structure
2. API_REFERENCE.md (20 min) - Know available methods
3. PATTERNS_AND_EXAMPLES.md (15 min) - Review patterns
4. Source code in `core/`, `drivers/`, `screens/`

### For Reference
- API_REFERENCE.md - Always open while coding
- PATTERNS_AND_EXAMPLES.md - Copy-paste code snippets
- USAGE_GUIDE.md - Troubleshooting section

---

## 📚 External Resources

### Dependencies
- **pynput** - Keyboard & mouse control
- **PIL/Pillow** - Image capture & comparison
- **pytesseract** - OCR for text detection
- **pytest** - Test framework
- **pywinauto** - Windows UI automation

### Recommended Reading
- Python Type Hints: https://www.python.org/dev/peps/pep-0484/
- Pytest Documentation: https://docs.pytest.org/
- Page Object Model: https://www.selenium.dev/documentation/en/guidelines_and_recommendations/page_object_models/

---

## ✅ Documentation Checklist

Use this checklist to ensure you have all the information you need:

- [ ] Installed required dependencies (see QUICK_START.md)
- [ ] Understood core components (see USAGE_GUIDE.md)
- [ ] Reviewed API reference (see API_REFERENCE.md)
- [ ] Studied example patterns (see PATTERNS_AND_EXAMPLES.md)
- [ ] Created first screen object (see PATTERNS_AND_EXAMPLES.md - Page Object)
- [ ] Written first test (see PATTERNS_AND_EXAMPLES.md - Test Patterns)
- [ ] Successfully ran tests (see QUICK_START.md)
- [ ] Reviewed best practices (see USAGE_GUIDE.md - Best Practices)
- [ ] Bookmarked API_REFERENCE.md for quick lookup
- [ ] Joined/contacted the team for support

---

## 🆘 Getting Help

### Common Issues
→ See [USAGE_GUIDE.md - Troubleshooting](USAGE_GUIDE.md#troubleshooting)

### Code Examples
→ See [PATTERNS_AND_EXAMPLES.md](PATTERNS_AND_EXAMPLES.md)

### API Questions
→ See [API_REFERENCE.md](API_REFERENCE.md)

### Architecture Questions
→ See [ARCHITECTURE.md](ARCHITECTURE.md)

### Still Need Help?
1. Check relevant documentation section
2. Review similar examples
3. Contact the development team

---

## 📝 Documentation Format

### Code Examples
Code examples use Python syntax highlighting and show real usage:
```python
# Real code you can use
element = Locator.by_auto_id("btnSubmit").find(root)
screen.click_element(element)
```

### File References
File paths are shown relative to project root:
```
core/element.py          # Core framework file
tests/test_login.py      # Test file
screens/login_screen.py  # Screen object file
```

### Important Notes
> **Note:** Important information appears in callout blocks

---

## 🎓 Learning Path

### Beginner
1. Read QUICK_START.md
2. Set up environment
3. Create and run first test
4. Review PATTERNS_AND_EXAMPLES.md

### Intermediate
1. Read USAGE_GUIDE.md thoroughly
2. Create complex screen objects
3. Write data-driven tests
4. Review ARCHITECTURE.md

### Advanced
1. Study ARCHITECTURE.md in depth
2. Create custom locator strategies
3. Extend BaseScreen for special needs
4. Contribute to framework improvements

---

## 📞 Support & Feedback

For questions, issues, or feedback:
- Check the relevant documentation section first
- Review example patterns in PATTERNS_AND_EXAMPLES.md
- Consult API_REFERENCE.md for method details
- Contact the development team if needed

---

## Version Information

- **Framework Version**: 1.0.0
- **Last Updated**: April 2026
- **Python**: 3.8+
- **OS**: Windows

---

## 📄 License

Internal Use Only - G2 Desktop Automation Framework

---

**Happy Automating!** 🚀

For the fastest start, begin with [QUICK_START.md](QUICK_START.md)
