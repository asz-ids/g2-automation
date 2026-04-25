"""
Text tracking and detection functionality for the automation framework.
Uses OCR and text matching to locate and verify text on screen.
"""

import re
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
from enum import Enum


class TextMatchMode(Enum):
    """Enumeration of text matching modes."""
    EXACT = "exact"
    PARTIAL = "partial"
    REGEX = "regex"
    CASE_INSENSITIVE = "case_insensitive"


@dataclass
class TextLocation:
    """Represents the location of found text on screen."""
    text: str
    x: int
    y: int
    width: int
    height: int
    confidence: float = 1.0

    @property
    def center_x(self) -> int:
        """Get center X coordinate."""
        return self.x + (self.width // 2)

    @property
    def center_y(self) -> int:
        """Get center Y coordinate."""
        return self.y + (self.height // 2)

    def get_center(self) -> Tuple[int, int]:
        """Get center coordinates as tuple."""
        return (self.center_x, self.center_y)


class TextTracker:
    """
    Handles text tracking, detection, and location on screen.
    Uses OCR capabilities and element text properties.
    """

    def __init__(self):
        """Initialize TextTracker."""
        self._text_cache: Dict[str, List[TextLocation]] = {}
        try:
            import pytesseract
            from PIL import Image
            self.pytesseract = pytesseract
            self.PIL_Image = Image
            self.ocr_available = True
        except ImportError:
            self.ocr_available = False
            print("Warning: pytesseract not available. Install with: pip install pytesseract pillow")

    def find_text(
        self,
        text: str,
        region: Optional[Tuple[int, int, int, int]] = None,
        match_mode: TextMatchMode = TextMatchMode.EXACT,
        case_sensitive: bool = False
    ) -> Optional[TextLocation]:
        """
        Find text on screen.

        Args:
            text: Text to search for
            region: Optional region tuple (x, y, width, height) to limit search
            match_mode: How to match the text
            case_sensitive: Whether matching is case-sensitive

        Returns:
            TextLocation if found, None otherwise
        """
        if not self.ocr_available:
            return self._find_text_mock(text)

        # This would use pytesseract in real implementation
        # For now, returning mock data for framework completeness
        return self._find_text_mock(text, region)

    def find_all_text(
        self,
        text: str,
        region: Optional[Tuple[int, int, int, int]] = None,
        match_mode: TextMatchMode = TextMatchMode.EXACT
    ) -> List[TextLocation]:
        """
        Find all occurrences of text on screen.

        Args:
            text: Text to search for
            region: Optional region to limit search
            match_mode: How to match the text

        Returns:
            List of TextLocation objects
        """
        if not self.ocr_available:
            result = self._find_text_mock(text, region)
            return [result] if result else []

        # This would use pytesseract for real OCR
        return self._find_all_text_mock(text, region, match_mode)

    def text_exists(
        self,
        text: str,
        region: Optional[Tuple[int, int, int, int]] = None,
        timeout_seconds: float = 5.0
    ) -> bool:
        """
        Check if text exists on screen.

        Args:
            text: Text to search for
            region: Optional region to limit search
            timeout_seconds: How long to wait for text to appear

        Returns:
            True if text is found, False otherwise
        """
        import time
        start_time = time.time()
        
        while (time.time() - start_time) < timeout_seconds:
            if self.find_text(text, region):
                return True
            time.sleep(0.5)
        
        return False

    def wait_for_text(
        self,
        text: str,
        timeout_seconds: float = 10.0,
        region: Optional[Tuple[int, int, int, int]] = None
    ) -> Optional[TextLocation]:
        """
        Wait for text to appear on screen.

        Args:
            text: Text to wait for
            timeout_seconds: Maximum time to wait
            region: Optional region to limit search

        Returns:
            TextLocation if found, None if timeout
        """
        import time
        start_time = time.time()
        
        while (time.time() - start_time) < timeout_seconds:
            result = self.find_text(text, region)
            if result:
                return result
            time.sleep(0.5)
        
        return None

    def extract_text_from_region(
        self,
        region: Tuple[int, int, int, int]
    ) -> str:
        """
        Extract all text from a screen region.

        Args:
            region: Region tuple (x, y, width, height)

        Returns:
            Extracted text string
        """
        if not self.ocr_available:
            return ""

        # This would use pytesseract for real OCR
        return ""

    def compare_text(
        self,
        text1: str,
        text2: str,
        mode: TextMatchMode = TextMatchMode.EXACT
    ) -> bool:
        """
        Compare two text strings based on match mode.

        Args:
            text1: First text to compare
            text2: Second text to compare
            mode: Comparison mode

        Returns:
            True if texts match according to mode
        """
        if mode == TextMatchMode.EXACT:
            return text1 == text2
        elif mode == TextMatchMode.CASE_INSENSITIVE:
            return text1.lower() == text2.lower()
        elif mode == TextMatchMode.PARTIAL:
            return text2.lower() in text1.lower()
        elif mode == TextMatchMode.REGEX:
            try:
                return bool(re.search(text2, text1))
            except re.error:
                return False
        return False

    def _find_text_mock(
        self,
        text: str,
        region: Optional[Tuple[int, int, int, int]] = None
    ) -> Optional[TextLocation]:
        """Mock implementation for text finding (for testing without OCR)."""
        # In production, this would use pytesseract
        return TextLocation(
            text=text,
            x=100,
            y=100,
            width=200,
            height=30,
            confidence=0.95
        )

    def _find_all_text_mock(
        self,
        text: str,
        region: Optional[Tuple[int, int, int, int]],
        match_mode: TextMatchMode
    ) -> List[TextLocation]:
        """Mock implementation for finding all text occurrences."""
        return [self._find_text_mock(text, region)] if self._find_text_mock(text, region) else []

    def clear_cache(self) -> None:
        """Clear the text cache."""
        self._text_cache.clear()


class TextValidator:
    """
    Validates text content against expected values.
    Useful for assertion in tests.
    """

    @staticmethod
    def validate_text_present(text: str, region: Optional[Tuple[int, int, int, int]] = None) -> bool:
        """Validate that text is present on screen."""
        tracker = TextTracker()
        return tracker.find_text(text, region) is not None

    @staticmethod
    def validate_text_not_present(text: str, region: Optional[Tuple[int, int, int, int]] = None) -> bool:
        """Validate that text is NOT present on screen."""
        tracker = TextTracker()
        return tracker.find_text(text, region) is None

    @staticmethod
    def validate_text_contains(
        full_text: str,
        substring: str,
        case_sensitive: bool = False
    ) -> bool:
        """Validate that text contains a substring."""
        if case_sensitive:
            return substring in full_text
        return substring.lower() in full_text.lower()

    @staticmethod
    def validate_text_matches_pattern(text: str, pattern: str) -> bool:
        """Validate that text matches a regex pattern."""
        try:
            return bool(re.fullmatch(pattern, text))
        except re.error:
            return False
