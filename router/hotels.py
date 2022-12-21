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

@router.post("/add_room", response_model=schemas.RequestResult)
def add_room(room_info: schemas.Room, db: Session = Depends(get_db), member_id: int = Depends(get_member_id)):
    if member_id is False:
        raise HTTPException(status_code=404, detail="User not found")
    if crud.check_hotel_id(db, member_id, room_info.hotel_id):
        try:
            crud.add_room(db,room_info)
            return {'status': 'success'}
        except:
            return {'status': 'fail'}
    else:
        raise HTTPException(status_code=404, detail="Hotel not found")