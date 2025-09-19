#!/usr/bin/env python3
"""
Unit test for the utils.memoize decorator.
"""

import unittest
from unittest.mock import patch


def memoize(method):
    """
    Simple memoize decorator.
    Caches the result of a method for each instance.
    """
    attr_name = "_memo_" + method.__name__

    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return property(wrapper)


class TestClass:
    """
    Class to test memoization behavior.
    """

    def a_method(self):
        """Return a constant value."""
        return 42

    @memoize
    def a_property(self):
        """Return value of a_method, memoized."""
        return self.a_method()


class TestMemoize(unittest.TestCase):
    """
    Test case for the memoize decorator.
    """

    def test_memoize(self):
        """
        Ensure that a_property calls a_method only once even
        when accessed multiple times.
        """
        with patch.object(TestClass, "a_method",
                          return_value=42) as mock:
            obj = TestClass()
            first = obj.a_property
            second = obj.a_property
            self.assertEqual(first, 42)
            self.assertEqual(second, 42)
            mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
