from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import crud, schemas
from db.database import SessionLocal
from typing import List

router = APIRouter(
    prefix="/hotels",
    tags=["hotels"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

def get_member_id():
    # todo complete this
    return 1

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/own", response_model=List[schemas.Hotel])
def get_own_hotels(db: Session = Depends(get_db), member_id: int = Depends(get_member_id)):
    if member_id is False:
        raise HTTPException(status_code=404, detail="User not found")
    hotels = crud.get_own_hotels(db, member_id)
    return hotels


@router.post("/create", response_model=schemas.RequestResult)
def create_hotel(hotel_info: schemas.Hotel, db: Session = Depends(get_db), member_id: int = Depends(get_member_id)):
    if member_id is False:
        raise HTTPException(status_code=404, detail="User not found")
    crud.create_hotel(db,hotel_info, member_id)
    return {'status': 'success'}

@router.post("/create", response_model=schemas.Room)
def add_room(room_info: schemas.Room, db: Session = Depends(get_db), member_id: int = Depends(get_member_id), hotel_id: int = 1):
    if member_id is False:
        raise HTTPException(status_code=404, detail="User not found")
    rooms = crud.add_room(db,room_info, hotel_id)
    return rooms

@router.post("/order", response_model=schemas.Order)
def order(order_info: schemas.Order, db: Session = Depends(get_db), member_id: int = Depends(get_member_id), hotel_id: int = 1, room_id: int = 1):
    if member_id is False:
        raise HTTPException(status_code=404, detail="User not found")
    orders = crud.order(db,order_info, hotel_id, room_id, member_id)
    return orders

@router.get("/search", response_model=List[schemas.Hotel])
def Search_hotels(db: Session = Depends(get_db)):
    rooms = crud.create_hotel(db)
    return rooms

@router.post("/rates", response_model=schemas.RequestResult)
def rate_hotel(rate_info: schemas.Rate, db: Session = Depends(get_db), member_id: int = Depends(get_member_id)):
    if member_id is False:
        raise HTTPException(status_code=404, detail="User not found")
    if crud.ensure_user_owns_order(db, member_id, rate_info.order_id) & \
            crud.ensure_no_duplicate_rating(db, rate_info.order_id):
        crud.rate_order(db, rate_info)
        return {'status': 'success'}
    else:
        return {'status': 'fail'}

