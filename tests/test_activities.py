"""
Tests for the activities listing endpoint (GET /activities)

Tests the retrieval of all available activities with proper structure and data.
"""

import pytest


class TestGetActivities:
    """Test cases for GET /activities endpoint"""

    def test_get_activities_success(self, test_client, reset_activities):
        """
        ARRANGE: Request all activities
        ACT: Make GET request to /activities
        ASSERT: Response status is 200 with all activities returned
        """
        # ARRANGE
        # (implicit: test_client already initialized, activities reset)

        # ACT
        response = test_client.get("/activities")

        # ASSERT
        assert response.status_code == 200
        activities_data = response.json()
        assert isinstance(activities_data, dict)
        assert len(activities_data) > 0

    def test_get_activities_contains_chess_club(self, test_client, reset_activities):
        """
        ARRANGE: Request all activities
        ACT: Make GET request to /activities
        ASSERT: Response contains Chess Club with expected structure
        """
        # ARRANGE
        expected_activity = "Chess Club"

        # ACT
        response = test_client.get("/activities")
        activities_data = response.json()

        # ASSERT
        assert expected_activity in activities_data
        chess_club = activities_data[expected_activity]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club

    def test_get_activities_participants_structure(self, test_client, reset_activities):
        """
        ARRANGE: Request all activities
        ACT: Make GET request to /activities
        ASSERT: Participants field is a list with expected initial members
        """
        # ARRANGE
        # (implicit: Chess Club has michael and daniel as initial participants)

        # ACT
        response = test_client.get("/activities")
        activities_data = response.json()
        chess_club = activities_data["Chess Club"]

        # ASSERT
        assert isinstance(chess_club["participants"], list)
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]
        assert len(chess_club["participants"]) == 2

    def test_get_activities_all_activities_present(self, test_client, reset_activities):
        """
        ARRANGE: Request all activities
        ACT: Make GET request to /activities
        ASSERT: All 9 activities are returned
        """
        # ARRANGE
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Club",
            "Music Band",
            "Debate Club",
            "Science Club",
        ]

        # ACT
        response = test_client.get("/activities")
        activities_data = response.json()

        # ASSERT
        assert len(activities_data) == 9
        for activity_name in expected_activities:
            assert activity_name in activities_data
