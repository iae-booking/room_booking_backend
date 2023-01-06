from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import crud, schemas
from db.database import get_db
from typing import List
from fastapi_pagination import Page, paginate, Params
from router.auth import get_current_user_id

router = APIRouter(
    prefix="/hotels",
    tags=["hotels"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/own", response_model=List[schemas.HotelForGetUpdate])
def get_own_hotels(db: Session = Depends(get_db), member_id: int = Depends(get_current_user_id)):
    if member_id is False:
        raise HTTPException(status_code=404, detail="User not found")
    hotels = crud.get_own_hotels(db, member_id)
    return hotels


@router.post("/", response_model=schemas.RequestResult)
def create_hotel(hotel_info: schemas.Hotel, db: Session = Depends(get_db), member_id: int = Depends(get_current_user_id)):
    if member_id is False:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        crud.create_hotel(db, hotel_info, member_id)
        return {'status': 'success'}
    except Exception as e:
        return {'status': e}


@router.put("/")
def update_hotel(hotel_info: schemas.HotelForGetUpdate, db: Session = Depends(get_db), member_id: int = Depends(get_current_user_id)):
    if not member_id:
        raise HTTPException(status_code=400, detail="user not found")
    if not crud.check_member_owes_hotel(db, member_id, hotel_info.id):
        raise HTTPException(status_code=400, detail="hotel not found or member doesn't owe the hotel")
    res = crud.update_hotel(db, hotel_info)
    if res:
        return "success"
    raise HTTPException(status_code=400, detail="error")

@router.get('/{hotel_id}')
def get_one_hotel(hotel_id: int, db: Session = Depends(get_db)):
    res = crud.get_one_hotel(db, hotel_id)
    if not res:
        raise HTTPException(status_code=400, detail="hotel not found")
    return res

@router.delete("/{hotel_id}")
def del_hotel(hotel_id: int, member_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    if not member_id:
        raise HTTPException(status_code=400, detail="user not found")
    if not crud.check_member_owes_hotel(db, member_id, hotel_id):
        raise HTTPException(status_code=400, detail="hotel not found or member doesn't owe the hotel")
    res = crud.delete_hotel(db, hotel_id)
    if(res):
        return "success"
    raise HTTPException(status_code=400, detail="error")


@router.post("/rates", response_model=schemas.RequestResult)
def rate_hotel(rate_info: schemas.Rate, db: Session = Depends(get_db), member_id: int = Depends(get_current_user_id)):
    if member_id is False:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        crud.ensure_user_owns_order(db, member_id, rate_info.order_id)
        crud.ensure_no_duplicate_rating(db, rate_info.order_id)
        crud.rate_order(db, rate_info)
        return {'status': 'success'}
    except:
        return {'status': 'fail'}


@router.put("/rates", response_model=schemas.RequestResult)
def rate_hotel(rate_info: schemas.Rate, db: Session = Depends(get_db), member_id: int = Depends(get_current_user_id)):
    if member_id is False:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        crud.ensure_user_owns_order(db, member_id, rate_info.order_id)
        crud.update_rate(db, rate_info)
        return {'status': 'success'}
    except:
        return {'status': 'fail'}



@router.get("/rates", response_model=Page[schemas.Rate])
def rate_hotel(hotel_id: int, params: Params = Depends(), db: Session = Depends(get_db)):
    return paginate(crud.get_rate_of_hotel(db, hotel_id), params)
