#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient.public_repos.
"""
import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient

# ---- Fixtures ----
org_payload = {
    "login": "test-org",
    "repos_url": "https://api.github.com/orgs/test-org/repos",
}
repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "mit"}},
    {"name": "repo3", "license": {"key": "apache-2.0"}},
]
expected_repos = ["repo1", "repo2", "repo3"]
apache2_repos = ["repo1", "repo3"]


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient.public_repos."""

    @patch("client.get_json", return_value=repos_payload)
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns the expected repository names.
        """
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
        ) as mock_repos_url:
            mock_repos_url.return_value = (
                "https://api.github.com/orgs/test-org/repos"
            )

            client = GithubOrgClient("test-org")
            result = client.public_repos()

            self.assertEqual(result, expected_repos)
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test-org/repos"
            )

    @patch("client.get_json", return_value=repos_payload)
    def test_public_repos_with_license(self, mock_get_json):
        """
        Test that public_repos filters repositories by license.
        """
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
        ) as mock_repos_url:
            mock_repos_url.return_value = (
                "https://api.github.com/orgs/test-org/repos"
            )

            client = GithubOrgClient("test-org")
            result = client.public_repos(license="apache-2.0")

            self.assertEqual(result, apache2_repos)
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test-org/repos"
            )


if __name__ == "__main__":
    unittest.main()
#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient.public_repos.
"""
import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient

# ---- Fixtures ----
repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "mit"}},
    {"name": "repo3", "license": {"key": "apache-2.0"}},
]
expected_repos = ["repo1", "repo2", "repo3"]
apache2_repos = ["repo1", "repo3"]


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient.public_repos."""

    @patch("client.get_json", return_value=repos_payload)
    def test_public_repos(self, mock_get_json):
        """public_repos returns all repository names."""
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
        ) as mock_repos_url:
            mock_repos_url.return_value = "https://api.github.com/orgs/test-org/repos"

            client = GithubOrgClient("test-org")
            result = client.public_repos()

            self.assertEqual(result, expected_repos)
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test-org/repos"
            )

    @patch("client.get_json", return_value=repos_payload)
    def test_public_repos_with_license(self, mock_get_json):
        """public_repos filters by license key."""
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
        ) as mock_repos_url:
            mock_repos_url.return_value = "https://api.github.com/orgs/test-org/repos"

            client = GithubOrgClient("test-org")
            result = client.public_repos(license="apache-2.0")

            self.assertEqual(result, apache2_repos)
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test-org/repos"
            )


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""
Unit tests for the client.GithubOrgClient.org property.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Test case for GithubOrgClient.org method.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Ensure that GithubOrgClient.org returns the value
        from get_json and that get_json is called once with
        the expected GitHub API URL.
        """
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )


if __name__ == "__main__":
    unittest.main()
