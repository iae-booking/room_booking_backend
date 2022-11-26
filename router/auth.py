from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from db import crud, schemas
from db.database import SessionLocal
from db.schemas import User, Token, TokenData
from auth_info import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


fake_user_db = {
    "nary": {
        "email": "nary@mail.com",
        "password": "$2b$12$ltlzMGdm63UrNfp76bbk8.Fuj.d8ajw/4Z3P9uIahrromZHqFpWb.",
    },
}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def auth_user(db, email: str, password: str):
    users = crud.get_user(db, email)
    if len(users) < 1:
        return False
    user = users[0]
    print(user.password)
    if not verify_password(password, user.password):
        return False
    return user


# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return User(**user_dict)


def verify_password(passward, hashed_password):
    return pwd_context.verify(passward, hashed_password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, token_data.username) # get_user(fake_user_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def hash_password(password):
    return pwd_context.hash(password)


@router.post("/register")
def register(user_info: schemas.User, db: Session = Depends(get_db)):
    # check if username exist
    result = crud.get_user(db, user_info.dict()["email"])
    if(len(result) != 0):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="email already exist",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_info.password = hash_password(user_info.password)
    member = crud.creat_account(db, user_info)
    return member


@router.post("/login", response_model=Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/info')
def get_hashed_password(password: str):
    hashed_password = hash_password(password)
    return hashed_password


@router.get('/user')
def read_user(current_user: User = Depends(get_current_user)):
    return current_user