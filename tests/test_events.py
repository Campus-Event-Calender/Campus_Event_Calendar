def test_list_events(client):
    response = client.get("/api/events")
    assert response.status_code == 200
    assert len(response.get_json()) >= 5

def test_create_event(client):
    response = client.post("/api/events", json={
        "title":"Test Event","start_time":"2026-12-01T10:00:00",
        "end_time":"2026-12-01T11:00:00","capacity":50
    })
    assert response.status_code == 201
    assert response.get_json()["title"] == "Test Event"

def test_get_missing_event(client):
    response = client.get("/api/events/99999")
    assert response.status_code == 404

def test_update_event(client):
    response = client.put("/api/events/1", json={
        "title": "Updated Event",
        "description": "Updated details",
        "category": "Workshop",
        "venue": "New Venue",
        "start_time": "2026-12-01T10:00:00",
        "end_time": "2026-12-01T12:00:00",
        "capacity": 20,
    })
    assert response.status_code == 200
    event = response.get_json()
    assert event["title"] == "Updated Event"
    assert event["venue"] == "New Venue"
    assert event["capacity"] == 20

def test_update_event_rejects_end_before_start(client):
    response = client.put("/api/events/1", json={
        "start_time": "2026-12-01T12:00:00",
        "end_time": "2026-12-01T11:00:00",
    })
    assert response.status_code == 400
    assert "later" in response.get_json()["error"]

def test_update_event_requires_title_start_and_end(client):
    for payload in ({"title": " "}, {"start_time": ""}, {"end_time": ""}):
        response = client.put("/api/events/1", json=payload)
        assert response.status_code == 400

def test_update_event_rejects_capacity_below_rsvps(client):
    response = client.put("/api/events/1", json={"capacity": 1})
    assert response.status_code == 400
    assert "RSVPs" in response.get_json()["error"]

def test_update_event_rejects_non_integer_capacity(client):
    response = client.put("/api/events/1", json={"capacity": 2.5})
    assert response.status_code == 400
    assert "positive integer" in response.get_json()["error"]

def test_update_missing_event(client):
    response = client.put("/api/events/99999", json={"title": "Missing"})
    assert response.status_code == 404

def test_delete_event(client):
    response = client.delete("/api/events/1")
    assert response.status_code == 200
    assert client.get("/api/events/1").status_code == 404
    assert client.get("/api/reports/events/1/attendees").get_json() == []

def test_delete_missing_event(client):
    response = client.delete("/api/events/99999")
    assert response.status_code == 404
