import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    # Prevent the test client from following the redirect so we can
    # assert the original 307 response and Location header.
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307  # Temporary redirect
    assert response.headers.get("location") == "/static/index.html"

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0
    
    # Check structure of an activity
    activity = next(iter(activities.values()))
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)

@pytest.mark.parametrize("activity_name", ["Chess Club", "Programming Class"])
def test_signup_success(activity_name):
    test_email = "test_student@mergington.edu"
    response = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {test_email} for {activity_name}"
    
    # Verify participant was added
    activities = client.get("/activities").json()
    assert test_email in activities[activity_name]["participants"]

def test_signup_nonexistent_activity():
    response = client.post("/activities/NonexistentClub/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_signup_duplicate():
    activity_name = "Chess Club"
    test_email = "duplicate_test@mergington.edu"
    
    # First signup
    response = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert response.status_code == 200
    
    # Duplicate signup
    response = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_unregister_participant():
    activity_name = "Chess Club"
    test_email = "unregister_test@mergington.edu"
    
    # First signup the participant
    client.post(f"/activities/{activity_name}/signup?email={test_email}")
    
    # Now unregister
    response = client.delete(f"/activities/{activity_name}/participant/{test_email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {test_email} from {activity_name}"
    
    # Verify participant was removed
    activities = client.get("/activities").json()
    assert test_email not in activities[activity_name]["participants"]

def test_unregister_nonexistent_activity():
    response = client.delete("/activities/NonexistentClub/participant/test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_nonexistent_participant():
    response = client.delete("/activities/Chess Club/participant/nonexistent@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"