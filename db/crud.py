from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, email: str):
    return db.query(models.Member).filter(models.Member.email == email).all()

def creat_account(db: Session, user_info: schemas.User):
    db_item = models.Member(**user_info.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_own_hotels(db: Session, member_id: int):
    return db.query(models.Hotel).filter(models.Hotel.member_id == member_id).all()

def create_hotel(db: Session, hotel_info: schemas.Hotel, member_id: int):
    db_item = models.Hotel(**hotel_info.dict(), member_id=member_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
