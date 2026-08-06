from urllib.parse import quote


def test_get_activities_returns_expected_shape(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert activity_name in payload
    assert "participants" in payload[activity_name]
    assert isinstance(payload[activity_name]["participants"], list)


def test_signup_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "new.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email in participants


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Activity"
    encoded_activity_name = quote(activity_name, safe="")
    email = "new.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email not in participants


def test_unregister_unknown_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "missing.student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found in this activity"}
