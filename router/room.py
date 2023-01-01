from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import crud, schemas
from db.database import get_db
from fastapi_pagination import Page, paginate, Params
from typing import List
import datetime
from router.auth import get_current_user_id

router = APIRouter(
    prefix="/room",
    tags=["room"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.RequestResult)
def add_room(room_info: schemas.CreateRoom, db: Session = Depends(get_db), member_id: int = Depends(get_current_user_id)):
    if member_id is False:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        crud.ensure_user_owns_hotel(db, member_id, room_info.hotel_id)
        crud.add_room(db,room_info)
        return {'status': 'success'}
    except:
        return {'status': 'fail'}


@router.put("/", response_model=schemas.RequestResult)
def update_room(room_info: schemas.GetAndUpdateRoom, db: Session = Depends(get_db), member_id: int = Depends(get_current_user_id)):
    if member_id is False:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        crud.ensure_user_owns_room(db, member_id, room_info.id)
        crud.update_room(db, room_info)
        return {'status': 'success'}
    except:
        return {'status': 'fail'}

@router.get("/", response_model=Page[schemas.GetAndUpdateRoom])
def get_room(hotel_id: int, params: Params = Depends(), db: Session = Depends(get_db)):
    return paginate(crud.get_rooms_of_hotel(db, hotel_id), params).dict()

@router.get("/search", response_model=List[schemas.GetAndUpdateRoom])
def search_rooms(*, db: Session = Depends(get_db), place: str, number_of_people: int, start_date: datetime.date, end_date: datetime.date):
    if start_date >= end_date:
        raise HTTPException(status_code=400, detail="Date error")
    rooms = crud.search_rooms(db, place = place, number_of_people = number_of_people, start_date = start_date, end_date = end_date)
    return rooms

@router.post("/order")
def place_order(shopping_cart: list, order_info: schemas.Order, db: Session = Depends(get_db), member_id: int = Depends(get_member_id)):
    if member_id is False:
        raise HTTPException(status_code=404, detail="User not found")
    if order_info.start_date >= order_info.end_date:
        raise HTTPException(status_code=400, detail="Date error")
    try:
        total_price = [0,0]
        for room in shopping_cart:
            if crud.check_rooms(db, order_info.start_date, order_info.end_date, room['room_id']) is False:
                raise HTTPException(status_code=400, detail="Room is booked")
        order_id = crud.place_order(db, order_info, member_id)
        for room in shopping_cart:
            room_price = crud.place_room_order(db, room['room_id'], room['amount'], order_id)
            total_price[0] += room_price[0]
            total_price[1] += room_price[1]
        return total_price
    except:
        return {'status': 'fail'}