"""Tests for the Mergington High School API"""

import pytest
from fastapi.testclient import TestClient


def test_root_redirect(client):
    """Test that root redirects to static index.html"""
    response = client.get("/")
    assert response.status_code == 200  # Follow redirects
    

def test_get_activities(client, reset_activities):
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    
    # Check structure of an activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club


def test_signup_for_activity_success(client, reset_activities):
    """Test successful signup for an activity"""
    response = client.post("/activities/Soccer Team/signup?email=newstudent@mergington.edu")
    assert response.status_code == 200
    
    data = response.json()
    assert data["message"] == "Signed up newstudent@mergington.edu for Soccer Team"
    
    # Verify the student was actually added
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert "newstudent@mergington.edu" in activities_data["Soccer Team"]["participants"]


def test_signup_for_nonexistent_activity(client, reset_activities):
    """Test signup for a non-existent activity"""
    response = client.post("/activities/Nonexistent Club/signup?email=student@mergington.edu")
    assert response.status_code == 404
    
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_signup_duplicate_student(client, reset_activities):
    """Test signup when student is already registered"""
    # First signup
    client.post("/activities/Soccer Team/signup?email=student@mergington.edu")
    
    # Try to signup again
    response = client.post("/activities/Soccer Team/signup?email=student@mergington.edu")
    assert response.status_code == 400
    
    data = response.json()
    assert data["detail"] == "Student already signed up for this activity"


def test_signup_activity_full(client, reset_activities):
    """Test signup when activity is at maximum capacity"""
    # Fill up Math Olympiad (max 10 participants)
    for i in range(10):
        client.post(f"/activities/Math Olympiad/signup?email=student{i}@mergington.edu")
    
    # Try to add one more
    response = client.post("/activities/Math Olympiad/signup?email=extraStudent@mergington.edu")
    assert response.status_code == 400
    
    data = response.json()
    assert data["detail"] == "Activity is full. No more spots available"


def test_signup_invalid_email_domain(client, reset_activities):
    """Test signup with email from wrong domain"""
    response = client.post("/activities/Chess Club/signup?email=student@otherschool.edu")
    assert response.status_code == 400
    
    data = response.json()
    assert data["detail"] == "Only Mergington High School students can sign up"


def test_cancel_activity_signup_success(client, reset_activities):
    """Test successful cancellation of activity signup"""
    # First signup
    client.post("/activities/Drama Club/signup?email=student@mergington.edu")
    
    # Then cancel
    response = client.delete("/activities/Drama Club/cancel?email=student@mergington.edu")
    assert response.status_code == 200
    
    data = response.json()
    assert data["message"] == "Cancelled student@mergington.edu's signup for Drama Club"
    
    # Verify the student was actually removed
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert "student@mergington.edu" not in activities_data["Drama Club"]["participants"]


def test_cancel_nonexistent_activity(client, reset_activities):
    """Test cancellation for a non-existent activity"""
    response = client.delete("/activities/Nonexistent Club/cancel?email=student@mergington.edu")
    assert response.status_code == 404
    
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_cancel_student_not_signed_up(client, reset_activities):
    """Test cancellation when student is not signed up"""
    response = client.delete("/activities/Chess Club/cancel?email=notsignedUp@mergington.edu")
    assert response.status_code == 400
    
    data = response.json()
    assert data["detail"] == "Student is not signed up for this activity"


def test_get_activity_participants_success(client, reset_activities):
    """Test getting participants for an activity"""
    # Add some participants
    client.post("/activities/Art Workshop/signup?email=artist1@mergington.edu")
    client.post("/activities/Art Workshop/signup?email=artist2@mergington.edu")
    
    response = client.get("/activities/Art Workshop/participants")
    assert response.status_code == 200
    
    data = response.json()
    assert data["activity_name"] == "Art Workshop"
    assert "artist1@mergington.edu" in data["participants"]
    assert "artist2@mergington.edu" in data["participants"]
    assert data["total_participants"] == 2
    assert data["available_spots"] == 14  # 16 max - 2 participants


def test_get_participants_nonexistent_activity(client, reset_activities):
    """Test getting participants for a non-existent activity"""
    response = client.get("/activities/Nonexistent Club/participants")
    assert response.status_code == 404
    
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_get_participants_empty_activity(client, reset_activities):
    """Test getting participants for an activity with no participants"""
    response = client.get("/activities/Basketball Club/participants")
    assert response.status_code == 200
    
    data = response.json()
    assert data["activity_name"] == "Basketball Club"
    assert data["participants"] == []
    assert data["total_participants"] == 0
    assert data["available_spots"] == 15


def test_activity_capacity_management(client, reset_activities):
    """Test comprehensive capacity management scenario"""
    activity_name = "Debate Team"  # max 12 participants
    
    # Sign up 11 students
    for i in range(11):
        response = client.post(f"/activities/{activity_name}/signup?email=student{i}@mergington.edu")
        assert response.status_code == 200
    
    # Check available spots
    response = client.get(f"/activities/{activity_name}/participants")
    data = response.json()
    assert data["total_participants"] == 11
    assert data["available_spots"] == 1
    
    # Sign up one more (should succeed)
    response = client.post(f"/activities/{activity_name}/signup?email=laststudent@mergington.edu")
    assert response.status_code == 200
    
    # Try to sign up another (should fail - activity full)
    response = client.post(f"/activities/{activity_name}/signup?email=rejected@mergington.edu")
    assert response.status_code == 400
    assert "Activity is full" in response.json()["detail"]
    
    # Cancel one student
    response = client.delete(f"/activities/{activity_name}/cancel?email=student5@mergington.edu")
    assert response.status_code == 200
    
    # Now should be able to sign up again
    response = client.post(f"/activities/{activity_name}/signup?email=newspot@mergington.edu")
    assert response.status_code == 200