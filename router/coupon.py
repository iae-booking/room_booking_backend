from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db import crud, schemas
from db.database import get_db
from db.schemas import Member, Token, CreditCard, MemberCreditCardAndMemberType, MemberInfo, MemberType
from router.auth import get_current_user_id
from datetime import date

router = APIRouter(
    prefix="/coupon",
    tags=["coupon"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get('/{member_id}')
def get_coupon_of_member(
        member_id: int,
        _: int = Depends(get_current_user_id),
        db: Session = Depends(get_db)
    ):
    res = crud.get_coupon_with_id(db, member_id)
    if(not res):
        raise HTTPException(status_code=400, detail="no data found")
    return res

@router.post('/')
def create_coupon(
        coupon: schemas.CouponInfo,
        member_id: int = Depends(get_current_user_id),
        db: Session = Depends(get_db)
    ):
    res = crud.create_coupon(db, coupon, member_id)
    if(not res):
        raise HTTPException(status_code=400, detail="no data found")
    return res

'''
@router.get('/order/{order_id}')
def get_coupon_for_order(
        order_id: int,
        _: int = Depends(get_current_user_id),
        db: Session = Depends(get_db)
    ):
    res = crud.get_used_coupon_for_order(db, order_id)
    print(res)
    if(not res):
        raise HTTPException(status_code=400, detail="no data found")
    return res

@router.post('/order')
def use_coupon(
        order_id: int,
        coupon_id: int,
        _: int = Depends(get_current_user_id),
        db: Session = Depends(get_db)
    ):
    res = crud.use_coupon(db, order_id, coupon_id, usage_date=date.today())
    print(res)
    if(not res):
        raise HTTPException(status_code=400, detail="no data found")
    return res
'''