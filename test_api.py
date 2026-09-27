from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_faqs():
    response = client.get("/api/faqs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_ask():
    response = client.post("/api/ask", json={"question": "What is Python?"})
    assert response.status_code == 200
    assert "answer" in response.json()

def test_add_faq():
    response = client.post("/api/faqs", json={
        "question": "What is HTML?",
        "answer": "HTML is used to structure web pages.",
        "category": "Web"
    })
    assert response.status_code == 200
    assert response.json()["question"] == "What is HTML?"
