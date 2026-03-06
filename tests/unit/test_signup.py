import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_signup_success():
    """Test successful signup for an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Signed up {email} for {activity_name}" in data["message"]
    # Verify participant was added
    get_response = client.get("/activities")
    activities = get_response.json()
    assert email in activities[activity_name]["participants"]

def test_signup_duplicate():
    """Test signup when student is already signed up"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # already signed up

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]

def test_signup_nonexistent_activity():
    """Test signup for non-existent activity"""
    # Arrange
    activity_name = "NonExistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]