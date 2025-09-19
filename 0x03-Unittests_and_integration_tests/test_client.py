#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient.public_repos.

These tests validate that:
1. public_repos() returns the expected list of repository names.
2. public_repos(license="apache-2.0") correctly filters repos by license.

All network calls are mocked to use local fixtures so the tests
are deterministic and do not depend on GitHub API availability.
"""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from fixtures import (
    org_payload,
    repos_payload,
    expected_repos,
    apache2_repos,
)


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient.public_repos."""

    @patch("client.get_json", return_value=repos_payload)
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns the expected repository names.

        It verifies that:
        - The method returns the exact list from the fixture.
        - The internal _public_repos_url property is accessed once.
        - get_json is called exactly once with the expected URL.
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

        It checks that passing license="apache-2.0" returns only
        the repositories with that license as defined in the fixture.
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

