#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b'),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), repr(expected_key))

#!/usr/bin/env python3

#!/usr/bin/env python3
"""
Unit tests for utils.get_json.
"""
import unittest
from unittest.mock import patch, Mock
from utils import get_json


class TestGetJson(unittest.TestCase):
    """Tests for utils.get_json."""

    @patch("utils.requests.get")
    def test_get_json_example(self, mock_get):
        """Test get_json with http://example.com."""
        test_url = "http://example.com"
        test_payload = {"payload": True}

        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)
        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)

    @patch("utils.requests.get")
    def test_get_json_holberton(self, mock_get):
        """Test get_json with http://holberton.io."""
        test_url = "http://holberton.io"
        test_payload = {"payload": False}

        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)
        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)


if __name__ == "__main__":
    unittest.main()

"""
Unit tests for utils.get_json
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import get_json


class TestGetJson(unittest.TestCase):
    """
    Tests for the get_json function in utils.py
    """

    @parameterized.expand([
        ("example", "http://example.com", {"payload": True}),
        ("holberton", "http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, name, test_url, test_payload, mock_get):
        """
        Test that utils.get_json returns the expected JSON payload
        and that requests.get is called exactly once with test_url.
        """
        # Configure the mock to return a response whose .json() returns test_payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""
Self-contained module that defines utils.get_json
and tests it using unittest and unittest.mock.
Running this file executes the tests directly.
"""

import unittest
from unittest.mock import patch, Mock
import requests


# ---------- Implementation ----------
def get_json(url: str):
    """
    Fetch JSON data from a URL and return it.

    Args:
        url (str): Target URL.

    Returns:
        dict: JSON payload.
    """
    return requests.get(url).json()


# ---------- Tests ----------
class TestGetJson(unittest.TestCase):
    """Unit tests for the get_json function."""

    @patch("requests.get")
    def test_get_json_example(self, mock_get):
        """Test get_json with http://example.com."""
        test_url = "http://example.com"
        test_payload = {"payload": True}

        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)
        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)

    @patch("requests.get")
    def test_get_json_holberton(self, mock_get):
        """Test get_json with http://holberton.io."""
        test_url = "http://holberton.io"
        test_payload = {"payload": False}

        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)
        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)


# ---------- Entry Point ----------
if __name__ == "__main__":
    unittest.main()
#!/usr/bin/env python3
"""
Self-contained memoization test module.

It defines:
    - A simple utils.memoize decorator
    - A TestClass using the decorator
    - A unittest TestMemoize test case verifying memoization
"""
import unittest
from unittest.mock import patch


# ---------- Implementation (utils) ----------
def memoize(method):
    """
    Decorator that caches the result of a method
    the first time it is called on an instance.
    """
    attr_name = "_memo_" + method.__name__

    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return property(wrapper)


# ---------- Class Under Test ----------
class TestClass:
    def a_method(self):
        return 42

    @memoize
    def a_property(self):
        return self.a_method()


# ---------- Tests ----------
class TestMemoize(unittest.TestCase):
    """Tests for the utils.memoize decorator."""

    def test_memoize(self):
        """
        Verify that calling a_property twice only calls a_method once
        and returns the correct cached result.
        """
        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()

            first_call = obj.a_property
            second_call = obj.a_property

            self.assertEqual(first_call, 42)
            self.assertEqual(second_call, 42)
            mock_method.assert_called_once()


# ---------- Entry Point ----------
if __name__ == "__main__":
    unittest.main()




