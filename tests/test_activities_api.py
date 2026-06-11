import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Fixture providing TestClient for the FastAPI app"""
    return TestClient(app)


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client):
        """
        Arrange: Client is ready
        Act: Make GET request to /activities
        Assert: Response status is 200 and returns activities dict
        """
        # Arrange
        expected_activity_count = len(activities)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        assert len(response.json()) == expected_activity_count

    def test_get_activities_contains_chess_club(self, client):
        """
        Arrange: Known activity exists
        Act: Make GET request to /activities
        Assert: Response includes Chess Club with details
        """
        # Arrange
        expected_activity_name = "Chess Club"

        # Act
        response = client.get("/activities")
        activities_data = response.json()

        # Assert
        assert expected_activity_name in activities_data
        assert "description" in activities_data[expected_activity_name]
        assert "participants" in activities_data[expected_activity_name]


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_for_activity_success(self, client):
        """
        Arrange: Activity exists and student not signed up
        Act: POST signup request with valid activity and email
        Assert: Response is 200 and participant is added
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newemail@mergington.edu"
        initial_count = len(activities[activity_name]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count + 1

    def test_signup_for_activity_not_found(self, client):
        """
        Arrange: Nonexistent activity
        Act: POST signup request with invalid activity name
        Assert: Response is 404 with appropriate error
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "test@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_duplicate_registration_fails(self, client):
        """
        Arrange: Student already signed up for activity
        Act: POST signup request with duplicate email
        Assert: Response is 400 with duplicate signup error
        """
        # Arrange
        activity_name = "Chess Club"
        email = activities[activity_name]["participants"][0]

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_multiple_students_different_activities(self, client):
        """
        Arrange: Two different students and activities ready
        Act: POST signup requests for both students to different activities
        Assert: Both students are added to their respective activities
        """
        # Arrange
        student1_email = "student1@mergington.edu"
        student2_email = "student2@mergington.edu"
        activity1 = "Programming Class"
        activity2 = "Art Club"

        # Act
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": student1_email}
        )
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": student2_email}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert student1_email in activities[activity1]["participants"]
        assert student2_email in activities[activity2]["participants"]


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/signup endpoint"""

    def test_unregister_from_activity_success(self, client):
        """
        Arrange: Student is registered for an activity
        Act: DELETE unregister request with valid activity and email
        Assert: Response is 200 and participant is removed
        """
        # Arrange
        activity_name = "Chess Club"
        email = activities[activity_name]["participants"][0]
        initial_count = len(activities[activity_name]["participants"])

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert email not in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count - 1

    def test_unregister_activity_not_found(self, client):
        """
        Arrange: Nonexistent activity
        Act: DELETE unregister request with invalid activity
        Assert: Response is 404 with activity not found error
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "test@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_participant_not_found(self, client):
        """
        Arrange: Valid activity but student not registered
        Act: DELETE unregister request with email not in participants
        Assert: Response is 404 with participant not found error
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Participant not found"

    def test_unregister_then_signup_again(self, client):
        """
        Arrange: Student registered for activity
        Act: Unregister student, then register again
        Assert: Both operations succeed
        """
        # Arrange
        activity_name = "Programming Class"
        email = "testuser@mergington.edu"

        # Act - First signup
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Act - Unregister
        response2 = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Act - Signup again
        response3 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert email in activities[activity_name]["participants"]
