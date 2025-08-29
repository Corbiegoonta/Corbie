from fastapi.testclient import TestClient
from main import app
import requests


client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

test_health_endpoint()

# def get_health_status():
#     response = requests.get("http://localhost:8000/health")
#     return response.json()

# print(get_health_status())