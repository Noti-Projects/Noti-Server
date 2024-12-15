import pytest
from fastapi.testclient import TestClient


def test_create_message(client: TestClient):
    """Test creating a new message"""
    message_data = {
        "title": "Test Message",
        "content": "This is a test message",
        "category": "test"
    }
    response = client.post("/api/v1/messages/", json=message_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == message_data["title"]
    assert data["content"] == message_data["content"]
    assert data["category"] == message_data["category"]
    assert "id" in data


def test_get_messages(client: TestClient):
    """Test getting message list"""
    # First create a message
    message_data = {
        "title": "Test Message",
        "content": "This is a test message",
        "category": "test"
    }
    client.post("/api/v1/messages/", json=message_data)

    # Then get messages list
    response = client.get("/api/v1/messages/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert isinstance(data, list)


def test_get_message(client: TestClient):
    """Test getting a single message"""
    # First create a message
    message_data = {
        "title": "Test Message",
        "content": "This is a test message",
        "category": "test"
    }
    create_response = client.post("/api/v1/messages/", json=message_data)
    message_id = create_response.json()["id"]

    # Then get the message
    response = client.get(f"/api/v1/messages/{message_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == message_id
    assert data["title"] == message_data["title"]


def test_update_message(client: TestClient):
    """Test updating a message"""
    # First create a message
    message_data = {
        "title": "Test Message",
        "content": "This is a test message",
        "category": "test"
    }
    create_response = client.post("/api/v1/messages/", json=message_data)
    message_id = create_response.json()["id"]

    # Then update the message
    update_data = {
        "title": "Updated Message",
        "is_read": True
    }
    response = client.patch(f"/api/v1/messages/{message_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["is_read"] == update_data["is_read"]


def test_delete_message(client: TestClient):
    """Test deleting a message"""
    # First create a message
    message_data = {
        "title": "Test Message",
        "content": "This is a test message",
        "category": "test"
    }
    create_response = client.post("/api/v1/messages/", json=message_data)
    message_id = create_response.json()["id"]

    # Then delete the message
    response = client.delete(f"/api/v1/messages/{message_id}")
    assert response.status_code == 200
    assert response.json()["ok"] == True

    # Verify message is deleted
    get_response = client.get(f"/api/v1/messages/{message_id}")
    assert get_response.status_code == 404


def test_get_messages_with_category(client: TestClient):
    """Test getting messages filtered by category"""
    # Create messages with different categories
    categories = ["test1", "test2"]
    for category in categories:
        message_data = {
            "title": f"Test Message {category}",
            "content": f"This is a test message for {category}",
            "category": category
        }
        client.post("/api/v1/messages/", json=message_data)

    # Test filtering by category
    response = client.get("/api/v1/messages/", params={"category": "test1"})
    assert response.status_code == 200
    data = response.json()
    assert all(msg["category"] == "test1" for msg in data)


def test_create_message_invalid_data(client: TestClient):
    """Test creating a message with invalid data"""
    invalid_data = {
        "title": "",  # Empty title
        "content": "Test content",
        "category": "test"
    }
    response = client.post("/api/v1/messages/", json=invalid_data)
    assert response.status_code == 422  # Validation error


def test_update_nonexistent_message(client: TestClient):
    """Test updating a message that doesn't exist"""
    update_data = {
        "title": "Updated Message"
    }
    response = client.patch("/api/v1/messages/999", json=update_data)
    assert response.status_code == 404


def test_get_messages_pagination(client: TestClient):
    """Test message list pagination"""
    # Create multiple messages
    for i in range(5):
        message_data = {
            "title": f"Test Message {i}",
            "content": f"This is test message {i}",
            "category": "test"
        }
        client.post("/api/v1/messages/", json=message_data)

    # Test pagination
    response = client.get("/api/v1/messages/", params={"skip": 2, "limit": 2})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # Should only return 2 messages
