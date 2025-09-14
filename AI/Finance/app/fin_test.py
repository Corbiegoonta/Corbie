from fastapi.testclient import TestClient
from main import app
import requests


client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test():
    yield range(3)

print(list(test()))
# print(list(test()))
# print("Health endpoint test passed.")

# def get_health_status():
#     response = requests.get("http://localhost:8000/health")
#     return response.json()

# print(get_health_status())