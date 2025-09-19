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
    unittest.main


#!/usr/bin/env python3
"""
Unit test for a simple memoize decorator.

This script includes:
    • A memoize decorator
    • A helper class using the decorator
    • A unittest verifying correct memoization
"""
import unittest
from unittest.mock import patch


def memoize(method):
    """
    Cache the result of a method the first time it is called on
    an instance and return the cached value on subsequent calls.
    """
    attr_name = "_memo_" + method.__name__

    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return property(wrapper)


class HelperTestClass:
    """
    Helper class to test memoization.

    a_method returns 42.
    a_property is decorated with @memoize to ensure it calls
    a_method only once.
    """

    def a_method(self):
        """Return a constant integer."""
        return 42

    @memoize
    def a_property(self):
        """Return the value of a_method, memoized."""
        return self.a_method()


class TestMemoize(unittest.TestCase):
    """Unit test for the memoize decorator."""

    def test_memoize(self):
        """
        Verify that a_property returns the correct value and
        a_method is called only once even when accessed twice.
        """
        with patch.object(HelperTestClass, "a_method", return_value=42) as mock:
            obj = HelperTestClass()
            first_call = obj.a_property
            second_call = obj.a_property
            self.assertEqual(first_call, 42)
            self.assertEqual(second_call, 42)
            mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()

