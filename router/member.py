from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from db import crud, schemas
from db.database import SessionLocal
from db.schemas import Member, Token, TokenData, CreditCard, MemberCreditCard, MemberInfo
from auth_info import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/member",
    tags=["member"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
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


@router.post("/credit_card")   # add card to login member
def add_credit_card(
        credit_card: CreditCard, 
        current_user: Member = Depends(get_current_user), 
        db: Session = Depends(get_db)
    ):
    res = crud.db_add_credit_card(db, credit_card, current_user.member_id)
    if res:
        return 200
    return "create error"


@router.get('/info', response_model=MemberCreditCard)   # show info of login member
def get_member_info(
        current_user: Member = Depends(get_current_user), 
        db: Session = Depends(get_db)
    ):
    res = crud.get_user(db, current_user.email)
    res_credit_cards = crud.get_credit_card(db, current_user.member_id)
    memberCreditCard = MemberCreditCard(**res.__dict__, credit_cards=res_credit_cards)
    # res_dict['credit_cards'] = res_credit_cards
    return memberCreditCard

@router.put('/info')
def update_member_info(member: MemberInfo, db: Session = Depends(get_db), current_user: Member = Depends(get_current_user)):
    res = crud.update_member_info(db, member)
    return res
