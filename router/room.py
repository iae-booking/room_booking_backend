from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import crud, schemas
from db.database import get_db
from fastapi_pagination import Page, paginate, Params

router = APIRouter(
    prefix="/room",
    tags=["room"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


def get_member_id():
    # todo complete this
    return 1


@router.post("/", response_model=schemas.RequestResult)
def add_room(room_info: schemas.CreateRoom, db: Session = Depends(get_db), member_id: int = Depends(get_member_id)):
    if member_id is False:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        crud.ensure_user_owns_hotel(db, member_id, room_info.hotel_id)
        crud.add_room(db,room_info)
        return {'status': 'success'}
    except:
        return {'status': 'fail'}


@router.put("/", response_model=schemas.RequestResult)
def update_room(room_info: schemas.GetAndUpdateRoom, db: Session = Depends(get_db), member_id: int = Depends(get_member_id)):
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
