#!/usr/bin/env python3
"""
Unit test for the utils.memoize decorator.

This test ensures that a memoized property only calls its underlying
method once, even if accessed multiple times.
"""
import unittest
from unittest.mock import patch
from utils import memoize  # ensure utils.py provides memoize


class TestMemoize(unittest.TestCase):
    """Tests for the utils.memoize decorator."""

    def test_memoize(self):
        """
        Verify that when calling a_property twice, the correct result is
        returned and a_method is only called once.
        """

        class TestClass:
            """
            Helper class for testing memoization.

            Defines a_method returning 42 and a_property decorated with
            @memoize to ensure caching behavior is correct.
            """

            def a_method(self):
                """Return a constant integer."""
                return 42

            @memoize
            def a_property(self):
                """Return the value of a_method, memoized."""
                return self.a_method()

        
        # Patch a_method so we can count how many times it is invoked
        with patch.object(TestClass, "a_method",
                          return_value=42) as mock_method:
            obj = TestClass()

            first = obj.a_property    # First call triggers a_method
            second = obj.a_property   # Second call uses cached value

            self.assertEqual(first, 42)
            self.assertEqual(second, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
