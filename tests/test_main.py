from unittest import TestCase

from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)

user_id = str(uuid.uuid4())

class TestMain(TestCase):
    def test_health(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"message": "The API is LIVE!!"}
