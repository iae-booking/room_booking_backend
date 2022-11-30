import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi.testclient import TestClient
from passlib.context import CryptContext
from main import app

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

client = TestClient(app)


user = {
        "username": "nary",
        "password": "nary"
    }


def hash_password(password):
    return pwd_context.hash(password)


def test_register():
    res = client.post(
        "/auth/register/",
        data=user
    )

    assert res.status_code == 200

    test_login()


def test_login():
    res = client.post(
        "/auth/login/",
        data=user
    )
    assert res.status_code == 200