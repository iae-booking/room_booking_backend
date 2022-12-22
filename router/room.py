from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import crud, schemas
from db.database import get_db

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
def add_room(room_info: schemas.Room, db: Session = Depends(get_db), member_id: int = Depends(get_member_id)):
    if member_id is False:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        crud.ensure_user_owns_hotel(db, member_id, room_info.hotel_id)
        crud.add_room(db,room_info)
        return {'status': 'success'}
    except:
        return {'status': 'fail'}