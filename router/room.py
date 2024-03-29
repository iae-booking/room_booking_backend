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

@router.post("/", response_model=schemas.ResponseRequestWithObjectId)
def add_room(room_info: schemas.CreateRoom, db: Session = Depends(get_db), member_id: int = Depends(get_current_user_id)):
    if member_id is False:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        crud.ensure_user_owns_hotel(db, member_id, room_info.hotel_id)
        room_db_item = crud.add_room(db,room_info)
        return {'status': 'success', 'id': room_db_item.id }
    except:
        return {'status': 'fail', 'id': None}


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

@router.get("/search", response_model=List[schemas.GetSearchdata])
def search_rooms(*, db: Session = Depends(get_db), place: str, number_of_people: int, start_date: datetime.date, end_date: datetime.date):
    if start_date >= end_date:
        raise HTTPException(status_code=400, detail="Date error")
    rooms = crud.search_rooms(db, place = place, number_of_people = number_of_people, start_date = start_date, end_date = end_date)
    return rooms


@router.post("/order")
def place_order(shopping_cart: list, order_info: schemas.Order, db: Session = Depends(get_db), member_id: int = Depends(get_current_user_id)):
    if member_id is False:
        raise HTTPException(status_code=404, detail="User not found")
    if order_info.start_date >= order_info.end_date:
        raise HTTPException(status_code=400, detail="Date error")
    try:
        nonzero_room = crud.room_filter(db, shopping_cart)
        if crud.check_rooms(db, order_info.start_date, order_info.end_date, nonzero_room) is False:
            raise HTTPException(status_code=400, detail="Room is booked")
        order_id = crud.place_order(db, order_info, member_id)
        order_result = crud.place_room_order(db, nonzero_room, order_id)
        order_result.update(order_info)
        nonzero_room.append(order_result)
        return nonzero_room
    except:
        return {'status': 'fail'}


@router.delete("/{room_id}", response_model=schemas.RequestResult)
def del_hotel(room_id: int, member_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    if not member_id:
        raise HTTPException(status_code=400, detail="user not found")
    try:
        crud.ensure_user_owns_room(db, member_id, room_id)
        crud.delete_room(db, room_id)
        return {'status': 'success'}
    except:
        return {'status': 'fail'}

@router.get("/get_historical_order", response_model=List[schemas.historical_order])
def get_historical_order(db: Session = Depends(get_db), member_id: int = Depends(get_current_user_id)):
    if not member_id:
        raise HTTPException(status_code=400, detail="user not found")
    orders = crud.get_historical_order(db, member_id)
    return orders
