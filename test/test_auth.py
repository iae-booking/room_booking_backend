import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login():
    user = {
        "username": "nary",
        "password": "nary"
    }
    res = client.post(
        "/auth/login/",
        data=user
    )
    assert res.status_code == 200