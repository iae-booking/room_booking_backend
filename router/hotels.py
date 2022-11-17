from fastapi import APIRouter, Depends
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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/own", response_model=List[schemas.Hotel])
def get_own_hotels(db: Session = Depends(get_db)):
    # todo change 0 to member_id and add HTTPException for not exist user
    hotels = crud.get_own_hotels(db, 0)
    return hotels