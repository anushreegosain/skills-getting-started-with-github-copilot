"""
Tests for the signup endpoint (POST /activities/{activity_name}/signup)

Tests successful signups, validation errors, and edge cases like duplicate signups.
"""

import pytest


class TestSignup:
    """Test cases for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self, test_client, reset_activities):
        """
        ARRANGE: Prepare a new email and valid activity name
        ACT: Make POST request to signup endpoint
        ASSERT: Response status is 200 and participant is added
        """
        # ARRANGE
        email = "john.doe@mergington.edu"
        activity_name = "Chess Club"

        # ACT
        response = test_client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # ASSERT
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_updates_participants_list(self, test_client, reset_activities):
        """
        ARRANGE: Prepare a new email and valid activity name
        ACT: Sign up, then fetch activities to verify participant added
        ASSERT: Participant appears in the activities list
        """
        # ARRANGE
        email = "jane.smith@mergington.edu"
        activity_name = "Programming Class"

        # ACT
        signup_response = test_client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        activities_response = test_client.get("/activities")

        # ASSERT
        assert signup_response.status_code == 200
        activities_data = activities_response.json()
        participants = activities_data[activity_name]["participants"]
        assert email in participants

    def test_signup_activity_not_found(self, test_client, reset_activities):
        """
        ARRANGE: Request signup for a non-existent activity
        ACT: Make POST request with invalid activity name
        ASSERT: Response status is 404 with appropriate error message
        """
        # ARRANGE
        email = "test@mergington.edu"
        invalid_activity = "Non-Existent Activity"

        # ACT
        response = test_client.post(
            f"/activities/{invalid_activity}/signup?email={email}"
        )

        # ASSERT
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_email(self, test_client, reset_activities):
        """
        ARRANGE: Attempt to sign up the same email twice for the same activity
        ACT: First signup succeeds, second signup is attempted
        ASSERT: Second signup returns 400 error with duplicate message
        """
        # ARRANGE
        email = "michael@mergington.edu"  # Already in Chess Club
        activity_name = "Chess Club"

        # ACT
        response = test_client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # ASSERT
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_different_activities(self, test_client, reset_activities):
        """
        ARRANGE: Sign up same email for two different activities
        ACT: Make two POST requests for different activities
        ASSERT: Both succeed and email appears in both activities
        """
        # ARRANGE
        email = "multi.activity@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Basketball Team"

        # ACT
        response1 = test_client.post(
            f"/activities/{activity1}/signup?email={email}"
        )
        response2 = test_client.post(
            f"/activities/{activity2}/signup?email={email}"
        )
        activities_response = test_client.get("/activities")

        # ASSERT
        assert response1.status_code == 200
        assert response2.status_code == 200
        activities_data = activities_response.json()
        assert email in activities_data[activity1]["participants"]
        assert email in activities_data[activity2]["participants"]

    def test_signup_multiple_different_emails(self, test_client, reset_activities):
        """
        ARRANGE: Sign up multiple people for the same activity
        ACT: Make three POST requests with different emails
        ASSERT: All participants appear in the activity
        """
        # ARRANGE
        emails = [
            "user1@mergington.edu",
            "user2@mergington.edu",
            "user3@mergington.edu",
        ]
        activity_name = "Tennis Club"

        # ACT
        for email in emails:
            response = test_client.post(
                f"/activities/{activity_name}/signup?email={email}"
            )
            assert response.status_code == 200

        activities_response = test_client.get("/activities")

        # ASSERT
        activities_data = activities_response.json()
        participants = activities_data[activity_name]["participants"]
        for email in emails:
            assert email in participants
