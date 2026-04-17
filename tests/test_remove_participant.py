"""
Tests for the remove participant endpoint (DELETE /activities/{activity_name}/participants)

Tests successful removal, validation errors, and state changes.
"""

import pytest


class TestRemoveParticipant:
    """Test cases for DELETE /activities/{activity_name}/participants endpoint"""

    def test_remove_participant_success(self, test_client, reset_activities):
        """
        ARRANGE: Prepare an existing participant and activity
        ACT: Make DELETE request to remove the participant
        ASSERT: Response status is 200 and participant is removed
        """
        # ARRANGE
        email = "michael@mergington.edu"  # Already in Chess Club
        activity_name = "Chess Club"

        # ACT
        response = test_client.delete(
            f"/activities/{activity_name}/participants?email={email}"
        )

        # ASSERT
        assert response.status_code == 200
        data = response.json()
        assert "Unregistered" in data["message"]
        assert email in data["message"]

    def test_remove_participant_updates_list(self, test_client, reset_activities):
        """
        ARRANGE: Prepare an existing participant in an activity
        ACT: Remove the participant, then fetch activities
        ASSERT: Email no longer appears in the participants list
        """
        # ARRANGE
        email = "emma@mergington.edu"  # In Programming Class
        activity_name = "Programming Class"

        # Verify email is initially present
        activities_before = test_client.get("/activities").json()
        assert email in activities_before[activity_name]["participants"]

        # ACT
        response = test_client.delete(
            f"/activities/{activity_name}/participants?email={email}"
        )

        # ASSERT
        assert response.status_code == 200
        activities_after = test_client.get("/activities").json()
        assert email not in activities_after[activity_name]["participants"]

    def test_remove_participant_activity_not_found(self, test_client, reset_activities):
        """
        ARRANGE: Attempt removal from a non-existent activity
        ACT: Make DELETE request with invalid activity name
        ASSERT: Response status is 404 with appropriate error
        """
        # ARRANGE
        email = "test@mergington.edu"
        invalid_activity = "Non-Existent Activity"

        # ACT
        response = test_client.delete(
            f"/activities/{invalid_activity}/participants?email={email}"
        )

        # ASSERT
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_remove_participant_not_in_activity(self, test_client, reset_activities):
        """
        ARRANGE: Attempt to remove an email not signed up for an activity
        ACT: Make DELETE request for non-existent participant
        ASSERT: Response status is 404 with participant not found message
        """
        # ARRANGE
        email = "nonexistent@mergington.edu"
        activity_name = "Chess Club"

        # ACT
        response = test_client.delete(
            f"/activities/{activity_name}/participants?email={email}"
        )

        # ASSERT
        assert response.status_code == 404
        data = response.json()
        assert "Participant not found" in data["detail"]

    def test_remove_only_participant(self, test_client, reset_activities):
        """
        ARRANGE: Remove the only participant from an activity
        ACT: Make DELETE request to remove the single participant
        ASSERT: Participants list becomes empty
        """
        # ARRANGE
        email = "isabella@mergington.edu"  # Only one in Art Club
        activity_name = "Art Club"

        # Verify she's the only participant
        activities_before = test_client.get("/activities").json()
        assert activities_before[activity_name]["participants"] == [email]

        # ACT
        response = test_client.delete(
            f"/activities/{activity_name}/participants?email={email}"
        )

        # ASSERT
        assert response.status_code == 200
        activities_after = test_client.get("/activities").json()
        assert activities_after[activity_name]["participants"] == []

    def test_remove_one_from_multiple_participants(self, test_client, reset_activities):
        """
        ARRANGE: Remove one participant from activity with multiple
        ACT: Make DELETE request
        ASSERT: Other participants remain, only target is removed
        """
        # ARRANGE
        email_to_remove = "michael@mergington.edu"
        remaining_email = "daniel@mergington.edu"
        activity_name = "Chess Club"

        # Verify both are present
        activities_before = test_client.get("/activities").json()
        assert email_to_remove in activities_before[activity_name]["participants"]
        assert remaining_email in activities_before[activity_name]["participants"]

        # ACT
        response = test_client.delete(
            f"/activities/{activity_name}/participants?email={email_to_remove}"
        )

        # ASSERT
        assert response.status_code == 200
        activities_after = test_client.get("/activities").json()
        assert email_to_remove not in activities_after[activity_name]["participants"]
        assert remaining_email in activities_after[activity_name]["participants"]

    def test_remove_participant_then_readd(self, test_client, reset_activities):
        """
        ARRANGE: Remove a participant, then sign them up again
        ACT: DELETE then POST for the same email and activity
        ASSERT: Both operations succeed and email is readded
        """
        # ARRANGE
        email = "sophia@mergington.edu"  # In Programming Class
        activity_name = "Programming Class"

        # ACT - Remove
        delete_response = test_client.delete(
            f"/activities/{activity_name}/participants?email={email}"
        )

        # ACT - Re-add
        signup_response = test_client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # ASSERT
        assert delete_response.status_code == 200
        assert signup_response.status_code == 200
        activities_final = test_client.get("/activities").json()
        assert email in activities_final[activity_name]["participants"]
