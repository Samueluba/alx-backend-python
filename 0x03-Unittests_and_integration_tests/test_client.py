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
            #!/usr/bin/env python3
import unittest
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient.has_license."""

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, *args):
        """Test that has_license returns the correct boolean."""
        repo, license_key, expected = args
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


if __name__ == "__main__":
    unittest.main()



#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from client import GithubOrgClient  # make sure client.py is accessible

class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient.has_license."""

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, *args):
        """Test that has_license returns the correct boolean."""
        repo, license_key, expected = args
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


if __name__ == "__main__":
    unittest.main()


            #!/usr/bin/env python3
"""Unit tests for the client.GithubOrgClient class."""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient methods and properties."""

    def _check_org(self, org_name):
        """Helper to test GithubOrgClient.org with a given org."""
        expected = {"org": org_name}
        with patch("client.get_json", return_value=expected) as mock_get:
            client = GithubOrgClient(org_name)
            self.assertEqual(client.org, expected)
            mock_get.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}"
            )

    def test_org_google(self):
        """Test .org for 'google'."""
        self._check_org("google")

    def test_org_abc(self):
        """Test .org for 'abc'."""
        self._check_org("abc")

    def test_public_repos_url(self):
        """Test _public_repos_url returns expected URL."""
        payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
            return_value=payload,
        ):
            client = GithubOrgClient("testorg")
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/testorg/repos",
            )

    def test_public_repos(self):
        """Test public_repos returns the correct repo list."""
        fake_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        fake_url = "https://api.github.com/orgs/testorg/repos"
        with patch("client.get_json", return_value=fake_payload) as mock_json:
            with patch(
                "client.GithubOrgClient._public_repos_url",
                new_callable=PropertyMock,
                return_value=fake_url,
            ) as mock_url:
                client = GithubOrgClient("testorg")
                self.assertEqual(
                    client.public_repos(),
                    ["repo1", "repo2", "repo3"],
                )
                mock_url.assert_called_once()
                mock_json.assert_called_once_with(fake_url)


if __name__ == "__main__":
    unittest.main()


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

#!/usr/bin/env python3
"""
Unit tests for the client.GithubOrgClient class.
"""

from unittest import TestCase
from unittest.mock import patch, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(TestCase):
    """
    Test cases for GithubOrgClient methods and properties.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the payload from get_json
        and that get_json is called once with the expected GitHub URL.
        """
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """
        Test that GithubOrgClient._public_repos_url returns the correct
        URL based on the mocked org property.
        """
        mock_payload = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
            return_value=mock_payload
        ):
            client = GithubOrgClient("testorg")
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/testorg/repos"
            )


if __name__ == "__main__":
    import unittest
    unittest.main()

#!/usr/bin/env python3
"""
Unit tests for the client.GithubOrgClient class.
"""

from unittest import TestCase
from unittest.mock import patch, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(TestCase):
    """
    Test cases for GithubOrgClient methods and properties.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the payload from get_json
        and that get_json is called once with the expected GitHub URL.
        """
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """
        Test that GithubOrgClient._public_repos_url returns the correct
        URL based on the mocked org property.
        """
        mock_payload = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
            return_value=mock_payload
        ):
            client = GithubOrgClient("testorg")
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/testorg/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test that GithubOrgClient.public_repos returns the expected list
        of repository names and that both get_json and the internal
        _public_repos_url property are called once.
        """
        # Fake payload returned by get_json
        fake_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = fake_payload

        # Fake URL returned by _public_repos_url
        fake_url = "https://api.github.com/orgs/testorg/repos"

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
            return_value=fake_url
        ) as mock_url:
            client = GithubOrgClient("testorg")
            result = client.public_repos()

            expected_names = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected_names)

            # Verify calls
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(fake_url)


if __name__ == "__main__":
    import unittest
    unittest.main()

#!/usr/bin/env python3
"""Unit tests for the client.GithubOrgClient class."""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient methods and properties."""

    def _check_org(self, org_name):
        """Helper to test GithubOrgClient.org with a given org."""
        expected = {"org": org_name}
        with patch("client.get_json", return_value=expected) as mock_get:
            client = GithubOrgClient(org_name)
            self.assertEqual(client.org, expected)
            mock_get.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}"
            )

    def test_org_google(self):
        """Test .org for 'google'."""
        self._check_org("google")

    def test_org_abc(self):
        """Test .org for 'abc'."""
        self._check_org("abc")

    def test_public_repos_url(self):
        """Test _public_repos_url returns expected URL."""
        payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
            return_value=payload,
        ):
            client = GithubOrgClient("testorg")
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/testorg/repos",
            )

    def test_public_repos(self):
        """Test public_repos returns the correct repo list."""
        fake_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        fake_url = "https://api.github.com/orgs/testorg/repos"
        with patch("client.get_json", return_value=fake_payload) as mock_json:
            with patch(
                "client.GithubOrgClient._public_repos_url",
                new_callable=PropertyMock,
                return_value=fake_url,
            ) as mock_url:
                client = GithubOrgClient("testorg")
                self.assertEqual(
                    client.public_repos(),
                    ["repo1", "repo2", "repo3"],
                )
                mock_url.assert_called_once()
                mock_json.assert_called_once_with(fake_url)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient.has_license."""

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, *args):
        """Test that has_license returns the correct boolean."""
        repo, license_key, expected = args
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from client import GithubOrgClient
from fixtures import public_repos  # your fixture providing expected repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test that GithubOrgClient.public_repos returns the expected
        list of repo names from the fixture.
        """
        # Arrange
        mock_get_json.return_value = public_repos  # fixture list of repo dicts
        client = GithubOrgClient("google")

        # Act
        result = client.public_repos()

        # Assert
        expected_names = [repo["name"] for repo in public_repos]
        self.assertEqual(result, expected_names)
        mock_get_json.assert_called_once_with(client._public_repos_url)

    @patch("client.get_json")
    def test_public_repos_with_license(self, mock_get_json):
        """
        Test that GithubOrgClient.public_repos returns only repos
        that have the specified license.
        """
        mock_get_json.return_value = public_repos
        client = GithubOrgClient("google")

        # Act
        result = client.public_repos(license="apache-2.0")

        # Assert
        expected_names = [
            repo["name"]
            for repo in public_repos
            if repo.get("license", {}).get("key") == "apache-2.0"
        ]
        self.assertEqual(result, expected_names)
        mock_get_json.assert_called_once_with(client._public_repos_url)


if __name__ == "__main__":
    unittest.main()



