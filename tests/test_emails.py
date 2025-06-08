import pytest
import time
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.email import EmailCreate

# Ждём, пока PostgreSQL и Mailpit будут готовы
@pytest.fixture(scope="session", autouse=True)
def wait_for_services():
    # Ждём 10 секунд для инициализации контейнеров
    time.sleep(10)
    yield

client = TestClient(app)

def test_send_email():
    response = client.post("/emails/send", json={
        "recipient": "test@example.com",
        "subject": "Test",
        "body": "Hello from test"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["recipient"] == "test@example.com"

def test_get_emails():
    response = client.get("/emails?direction=sent")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_get_statistics():
    start_date = "2025-06-01T00:00:00"
    end_date = "2025-06-07T23:59:59"
    response = client.get(f"/emails/statistics?start_date={start_date}&end_date={end_date}")
    assert response.status_code == 200
    assert "sent" in response.json()
    assert "received" in response.json()