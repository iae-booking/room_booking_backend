from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db import crud, schemas
from db.database import get_db
from db.schemas import Member, Token, CreditCard, MemberCreditCardAndMemberType, MemberInfo, MemberType
from router.auth import get_current_user_id

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get('/member/{email}')
def get_member_info(
        email: str,
        member_id: int = Depends(get_current_user_id),
        db: Session = Depends(get_db)
    ):
    user = crud.get_user_with_id(db, member_id)
    if(user.member_type != 2):
        raise HTTPException(status_code=401, detail="not admin")
    res = crud.get_user_with_email(db, email)
    if(not res):
        raise HTTPException(status_code=400, detail="no data found")
    return res

@router.delete('/member')
def delete_member(
        email: str,
        member_id: int = Depends(get_current_user_id),
        db: Session = Depends(get_db)
    ):
    user = crud.get_user_with_id(db, member_id)
    if(user.member_type != 2):
        raise HTTPException(status_code=401, detail="not admin")
    try:
        res = crud.delete_user(db, email)
        return res
    except:
        raise HTTPException(status_code=400, detail="no data found or other error")