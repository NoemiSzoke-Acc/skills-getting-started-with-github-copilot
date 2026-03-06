import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_signup_then_remove_workflow():
    """Test full workflow: signup then remove participant"""
    # Arrange
    activity_name = "Programming Class"
    email = "newstudent@mergington.edu"

    # Act: Signup
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    # Verify signed up
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]

    # Act: Remove
    remove_response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert remove_response.status_code == 200

    # Assert: Verify removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]

def test_multiple_participants_workflow():
    """Test signing up multiple participants"""
    # Arrange
    activity_name = "Gym Class"
    emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]

    # Act: Signup multiple
    for email in emails:
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 200

    # Assert: All signed up
    activities_response = client.get("/activities")
    activities = activities_response.json()
    participants = activities[activity_name]["participants"]
    for email in emails:
        assert email in participants

def test_state_persistence_workflow():
    """Test that state persists across multiple requests"""
    # Arrange
    activity_name = "Basketball Team"
    email = "persistent@mergington.edu"

    # Act: Signup
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act: Fetch again
    response = client.get("/activities")
    activities = response.json()

    # Assert: Still signed up
    assert email in activities[activity_name]["participants"]