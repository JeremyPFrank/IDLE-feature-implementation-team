import os
import sys

# Add only the idlelib directory to Python path
idlelib_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../idlelib'))
if idlelib_dir not in sys.path:
    sys.path.insert(0, idlelib_dir)

import unittest
from unittest.mock import Mock, patch
from tkinter import StringVar, Text, Tk

from manualdebug import ManualDebug


class ManualDebugTest(unittest.TestCase):
    """Test the ManualDebug class."""

    @classmethod
    def setUpClass(cls):
        """Create the Tk root for all tests."""
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls):
        """Close the Tk root."""
        cls.root.destroy()
        del cls.root

    def setUp(self):
        """Set up test environment."""
        self.parent = self.root
        self.dialog = ManualDebug(self.parent, _utest=True)

    def tearDown(self):
        """Clean up after each test."""
        if hasattr(self, 'dialog'):
            self.dialog.destroy()
            del self.dialog

    def test_init(self):
        """Test initialization of dialog."""
        self.assertEqual(self.dialog.parent, self.parent)
        self.assertTrue(hasattr(self.dialog, 'frame'))
        self.assertTrue(hasattr(self.dialog, 'output_text'))
        self.assertTrue(hasattr(self.dialog, 'line_entry'))
        self.assertTrue(hasattr(self.dialog, 'line_var'))
        self.assertTrue(hasattr(self.dialog, 'buttons'))

    def test_check_line(self):
        """Test line number validation."""
        # Mock the parent's index method
        self.parent.index = Mock(return_value="5.0")

        # Valid line numbers
        self.assertTrue(self.dialog.check_line('1'))
        self.assertTrue(self.dialog.check_line('5'))

        # Invalid line numbers
        self.assertFalse(self.dialog.check_line('0'))  # Too low
        self.assertFalse(self.dialog.check_line('6'))  # Too high
        self.assertFalse(self.dialog.check_line('abc'))  # Not a number
        self.assertFalse(self.dialog.check_line('-1'))  # Negative

    def test_apply(self):
        """Test applying print statements."""
        # Mock the parent's index method
        self.parent.index = Mock(return_value="5.0")

        # Test single valid line
        self.dialog.line_var.set('1')
        self.dialog.apply()
        
        # Test multiple valid lines
        self.dialog.line_var.set('2,3')
        self.dialog.apply()
        
        # Test invalid line
        self.dialog.line_var.set('10')
        self.dialog.apply()

    def test_cancel(self):
        """Test removing print statements."""
        # Mock the parent's index method
        self.parent.index = Mock(return_value="5.0")

        # Test removing single statement
        self.dialog.line_var.set('1')
        self.dialog.cancel()
        
        # Test removing multiple statements
        self.dialog.line_var.set('2,3')
        self.dialog.cancel()
        
        # Test removing non-existent statement
        self.dialog.line_var.set('4')
        self.dialog.cancel()

    def test_output_message(self):
        """Test showing messages in output text."""
        test_message = "Test message"
        self.dialog.output_message(test_message)
        # Verify the message appears in the output text
        self.dialog.output_text.get("1.0", "end-1c").strip()

    def test_destroy(self):
        """Test dialog destruction."""
        self.dialog.destroy()
        # Just verify it can be called without errors


if __name__ == '__main__':
    unittest.main(verbosity=2)