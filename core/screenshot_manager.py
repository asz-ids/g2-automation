"""
Screenshot management for the automation framework.
Captures, compares, and stores screenshots for testing and debugging.
"""

import os
from datetime import datetime
from typing import Optional, Tuple
from pathlib import Path


class ScreenshotManager:
    """
    Manages screenshot capture, storage, and comparison.
    """

    def __init__(self, screenshots_dir: str = "screenshots"):
        """
        Initialize ScreenshotManager.

        Args:
            screenshots_dir: Directory to store screenshots
        """
        self.screenshots_dir = screenshots_dir
        self._ensure_directory()

    def _ensure_directory(self) -> None:
        """Ensure screenshots directory exists."""
        Path(self.screenshots_dir).mkdir(parents=True, exist_ok=True)

    def capture_screenshot(self, filename: Optional[str] = None) -> str:
        """
        Capture a full-screen screenshot.

        Args:
            filename: Optional filename (uses timestamp if not provided)

        Returns:
            Full path to the saved screenshot
        """
        if not filename:
            filename = self._generate_filename()

        filepath = os.path.join(self.screenshots_dir, filename)
        
        try:
            from PIL import ImageGrab
            screenshot = ImageGrab.grab()
            screenshot.save(filepath)
            print(f"Screenshot saved: {filepath}")
            return filepath
        except ImportError:
            print("PIL (Pillow) not available for screenshots. Install with: pip install pillow")
            return filepath

    def capture_element_screenshot(
        self,
        element,
        filename: Optional[str] = None
    ) -> str:
        """
        Capture a screenshot of a specific element.

        Args:
            element: The element to capture
            filename: Optional filename

        Returns:
            Full path to the saved screenshot
        """
        if not filename:
            filename = f"element_{element.name}_{self._get_timestamp()}.png"

        filepath = os.path.join(self.screenshots_dir, filename)
        
        try:
            from PIL import ImageGrab
            # Get element bounds (this would be from actual element coordinates)
            # For now, using mock bounds
            bounds = self._get_element_bounds(element)
            screenshot = ImageGrab.grab(bbox=bounds)
            screenshot.save(filepath)
            print(f"Element screenshot saved: {filepath}")
            return filepath
        except ImportError:
            print("PIL (Pillow) not available for screenshots.")
            return filepath

    def capture_region_screenshot(
        self,
        region: Tuple[int, int, int, int],
        filename: Optional[str] = None
    ) -> str:
        """
        Capture a screenshot of a specific region.

        Args:
            region: Region tuple (x, y, width, height)
            filename: Optional filename

        Returns:
            Full path to the saved screenshot
        """
        if not filename:
            filename = self._generate_filename(prefix="region_")

        filepath = os.path.join(self.screenshots_dir, filename)
        
        try:
            from PIL import ImageGrab
            x, y, w, h = region
            bbox = (x, y, x + w, y + h)
            screenshot = ImageGrab.grab(bbox=bbox)
            screenshot.save(filepath)
            print(f"Region screenshot saved: {filepath}")
            return filepath
        except ImportError:
            print("PIL (Pillow) not available for screenshots.")
            return filepath

    def compare_screenshots(self, image1_path: str, image2_path: str) -> bool:
        """
        Compare two screenshots for equality.

        Args:
            image1_path: Path to first screenshot
            image2_path: Path to second screenshot

        Returns:
            True if images are identical, False otherwise
        """
        try:
            from PIL import Image
            
            img1 = Image.open(image1_path)
            img2 = Image.open(image2_path)
            
            return img1.tobytes() == img2.tobytes()
        except ImportError:
            print("PIL (Pillow) not available for comparison.")
            return False
        except FileNotFoundError as e:
            print(f"Screenshot file not found: {e}")
            return False

    def compare_screenshots_visual_similarity(
        self,
        image1_path: str,
        image2_path: str,
        threshold: float = 0.95
    ) -> Tuple[bool, float]:
        """
        Compare two screenshots for visual similarity.

        Args:
            image1_path: Path to first screenshot
            image2_path: Path to second screenshot
            threshold: Similarity threshold (0-1)

        Returns:
            Tuple of (similar: bool, similarity_score: float)
        """
        try:
            from PIL import Image, ImageChops
            import math
            
            img1 = Image.open(image1_path)
            img2 = Image.open(image2_path)
            
            if img1.size != img2.size:
                return False, 0.0
            
            diff = ImageChops.difference(img1, img2)
            diff_sum = sum(diff.getdata())
            max_diff = diff.mode_to_bpp["RGB"] * img1.size[0] * img1.size[1] * 255
            
            similarity = 1.0 - (diff_sum / max_diff)
            return similarity >= threshold, similarity
        except Exception as e:
            print(f"Error comparing screenshots: {e}")
            return False, 0.0

    def get_screenshot_list(self) -> list:
        """
        Get list of all screenshots in the directory.

        Returns:
            List of screenshot filenames
        """
        try:
            screenshots = [f for f in os.listdir(self.screenshots_dir) 
                          if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
            return sorted(screenshots)
        except FileNotFoundError:
            return []

    def delete_screenshot(self, filename: str) -> bool:
        """
        Delete a screenshot file.

        Args:
            filename: Name of the screenshot to delete

        Returns:
            True if deleted successfully, False otherwise
        """
        filepath = os.path.join(self.screenshots_dir, filename)
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"Screenshot deleted: {filepath}")
                return True
            return False
        except Exception as e:
            print(f"Error deleting screenshot: {e}")
            return False

    def clear_screenshots(self) -> None:
        """Delete all screenshots in the directory."""
        for filename in self.get_screenshot_list():
            self.delete_screenshot(filename)
        print(f"All screenshots cleared from {self.screenshots_dir}")

    def get_screenshot_path(self, filename: str) -> str:
        """
        Get full path for a screenshot filename.

        Args:
            filename: Screenshot filename

        Returns:
            Full path to the screenshot
        """
        return os.path.join(self.screenshots_dir, filename)

    @staticmethod
    def _generate_filename(prefix: str = "", extension: str = ".png") -> str:
        """
        Generate a timestamped filename for a screenshot.

        Args:
            prefix: Optional prefix for the filename
            extension: File extension (default: .png)

        Returns:
            Generated filename
        """
        timestamp = ScreenshotManager._get_timestamp()
        return f"{prefix}screenshot_{timestamp}{extension}"

    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp for filename."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    @staticmethod
    def _get_element_bounds(element) -> Tuple[int, int, int, int]:
        """
        Get element bounds for screenshot capture.

        Args:
            element: The element to get bounds from

        Returns:
            Bounds tuple (x1, y1, x2, y2)
        """
        # This would be implemented with actual element bounds from UIA
        # For now returning mock bounds
        x = element.get_runtime_data("x", 100)
        y = element.get_runtime_data("y", 100)
        width = element.get_runtime_data("width", 200)
        height = element.get_runtime_data("height", 50)
        
        return (x, y, x + width, y + height)
