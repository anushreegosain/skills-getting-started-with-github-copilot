"""
Tests for the root endpoint (GET /)

Tests the redirect behavior when accessing the root path.
"""

import pytest


class TestRoot:
    """Test cases for GET / endpoint"""

    def test_root_redirects_to_index(self, test_client, reset_activities):
        """
        ARRANGE: Root path is requested
        ACT: Make GET request to "/"
        ASSERT: Response redirects to /static/index.html with 307 status
        """
        # ARRANGE
        # (implicit: test_client already initialized)

        # ACT
        response = test_client.get("/", follow_redirects=False)

        # ASSERT
        assert response.status_code == 307
        assert response.headers["location"].endswith("/static/index.html")
