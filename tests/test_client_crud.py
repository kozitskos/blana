import pytest
from fastapi.testclient import TestClient
from main import app
# from app.mocks import (
#     get_mock_db,
#     get_mock_current_user,
#     mock_create_user,
#     mock_get_note_by_id,
#     mock_create_feedback,
#     mock_create_summary,
# )
# from app.deps import get_current_user, get_db
# from app.routers import notes, feedback, summaries

# # Override dependencies
# app.dependency_overrides[get_db] = get_mock_db
# app.dependency_overrides[get_current_user] = get_mock_current_user
# notes.crud.create_user_note = mock_create_user
# notes.crud.get_note_by_id = mock_get_note_by_id
# feedback.crud.create_feedback = mock_create_feedback
# summaries.crud.create_summary = mock_create_summary

client = TestClient(app)

def test_create_note_and_feedback_and_summary():
    # Get JWT token
    response = client.post("/auth/token", data={"username": "jhonedoe", "password": "jhonedoe"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    print(token)
    headers = {"Authorization": f"Bearer {token}"}

    # Create a note
    note_data = {"title": "Test Note", "content": "This is a test note."}
    response = client.post("/notes/", json=note_data, headers=headers)
    assert response.status_code == 200
    note = response.json()
    print(note)
    note_id = note["id"]
    print(note_id)

    # Leave feedback for the note
    feedback_data = {"comment": "Great note!", "rating": 5}
    response = client.post(f"/feedback/{note_id}/feedback/", json=feedback_data, headers=headers)
    assert response.status_code == 200
    feedback = response.json()
    print(feedback)
    assert feedback["comment"] == "Great note!"
    assert feedback["rating"] == 5

    # Create a summary for the note
    summary_data = {"content": "This is a summary of the test note."}
    response = client.post(f"/summary/{note_id}/summary/", json=summary_data, headers=headers)
    assert response.status_code == 200
    summary = response.json()
    print(summary)
    assert summary["content"] == "This is a summary of the test note."


test_create_note_and_feedback_and_summary()
