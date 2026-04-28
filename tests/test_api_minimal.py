def test_get_activities_returns_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]


def test_signup_success_adds_participant(client):
    email = "new.student@mergington.edu"
    response = client.post(f"/activities/Chess%20Club/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    activities_response = client.get("/activities")
    chess_participants = activities_response.json()["Chess Club"]["participants"]
    assert email in chess_participants


def test_signup_duplicate_returns_400(client):
    email = "michael@mergington.edu"

    response = client.post(f"/activities/Chess%20Club/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_activity_not_found_returns_404(client):
    response = client.post("/activities/Unknown%20Club/signup?email=someone@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_success_removes_participant(client):
    email = "daniel@mergington.edu"

    response = client.delete(f"/activities/Chess%20Club/participants?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"

    activities_response = client.get("/activities")
    chess_participants = activities_response.json()["Chess Club"]["participants"]
    assert email not in chess_participants


def test_unregister_participant_not_found_returns_404(client):
    response = client.delete(
        "/activities/Chess%20Club/participants?email=not-enrolled@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_activity_not_found_returns_404(client):
    response = client.delete(
        "/activities/Unknown%20Club/participants?email=not-enrolled@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
