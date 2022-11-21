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


@router.post("/create", response_model=schemas.Hotel)
def create_hotel(hotel_info: schemas.Hotel, db: Session = Depends(get_db), member_id: int = Depends(get_member_id)):
    if member_id is False:
        raise HTTPException(status_code=404, detail="User not found")
    hotels = crud.create_hotel(db,hotel_info, member_id)
    return hotels
