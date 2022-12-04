import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi.testclient import TestClient
from passlib.context import CryptContext
from main import app

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

client = TestClient(app)

headers = {'Content-Type': 'multipart/form-data'}

user = {
    "email": "tttt@example.com",
    "password": "string",
    "name": "string",
    "gender": 0,
    "phone": "string",
    "member_type": 0
}

user_login = {
    "username": "tttt@example.com",
    "password": "string"
}


def hash_password(password):
    return pwd_context.hash(password)


def test_register():
    res = client.post(
        "/auth/register/",
        json=user
    )

    assert res.status_code == 200

    test_login()


def test_login():
    res = client.post(
        "/auth/login/",
        # headers=headers,
        data=user_login
    )
    assert res.status_code == 200