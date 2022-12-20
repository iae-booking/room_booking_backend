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

def check_hotel_id(db: Session, member_id: int):
    return db.query(models.Hotel.id).filter(models.Hotel.member_id == member_id).all()


def add_room(db: Session, room_info: schemas.Room):
    db_item = models.Room(**room_info.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def search_rooms(db: Session, condition: dict):
    res = db.query(models.Room).filter(((models.Hotel.city == condition[0]) or (models.Hotel.region == condition[0])) \
                                       and models.Hotel.capacity == condition[1]).all()
    return res

def place_order(db: Session, order_info: schemas.Order, member_id: int):
    db_item = models.Order(**order_info.dict(), member_id=member_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def ensure_user_owns_order(db: Session, member_id: int, order_id: int):
    result = db.query(models.Order).filter(models.Order.id == order_id).first()
    if result is None:
        return False
    else:
        return result.member_id == member_id


def ensure_no_duplicate_rating(db: Session, order_id: int):
    result = db.query(models.Rating).filter(models.Rating.order_id == order_id).first()
    return result is None


def rate_order(db: Session, rate_info: schemas.Rate):
    db_item = models.Rating(**rate_info.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
