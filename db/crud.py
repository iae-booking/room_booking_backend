from sqlalchemy.orm import Session
from sqlalchemy import select, update
from . import models, schemas


def get_user(db: Session, email: str):
    return db.query(models.Member).filter(models.Member.email == email).first()

def creat_account(db: Session, user_info: schemas.Member):
    db_item = models.Member(**user_info.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_member_info(db: Session, user_info: schemas.MemberInfo):
    db_item = db.query(models.Member).filter(models.Member.email == user_info.email).first()
    if not db_item:
        raise ValueError("data not found")
    stmt = (
        update(models.Member)
        .where(models.Member.email.in_([user_info.email]))
        .values(**user_info.dict())
    )
    db.execute(stmt)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_credit_card(db: Session, member_id: int):
    return db.query(models.CreditCard).filter(models.CreditCard.member_id == member_id).all()

def db_add_credit_card(db: Session, credit_card: schemas.CreditCard, member_id: int):
    db_item = models.CreditCard(**credit_card.dict(), member_id = member_id)
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


def ensure_user_owns_order(db: Session, member_id: int, order_id: int):
    result = db.query(models.Order).filter(models.Order.id == order_id).first()
    if (result is None) | (result.member_id != member_id):
        raise
    return


def ensure_no_duplicate_rating(db: Session, order_id: int):
    result = db.query(models.Rating).filter(models.Rating.order_id == order_id).first()
    if result is not None:
        raise
    return


def rate_order(db: Session, rate_info: schemas.Rate):
    db_item = models.Rating(**rate_info.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_rate(db: Session, new_rate: schemas.Rate):
    stmt = (
        select(models.Rating)
        .where(models.Rating.order_id == new_rate.order_id)
    )
    rate_item = db.scalars(stmt).one()
    if (not rate_item) or (new_rate.evaluation > 5) or (new_rate.evaluation < 1):
        raise
    for key in new_rate.__dict__:
        setattr(rate_item, key, eval("new_rate."+key))
    db.commit()
    db.refresh(rate_item)
    return


def get_rate_of_hotel(db: Session, hotel_id: int):
    # todo refactor
    result = db.query(models.Rating).filter(models.Rating.order_id.in_(db.query(models.Order.id)
               .filter(models.Order.room_id.in_(db.query(models.Room.id)
               .filter(models.Room.hotel_id == hotel_id)))))\
               .all()
    return result
