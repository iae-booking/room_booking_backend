from sqlalchemy.orm import Session
from sqlalchemy import select, update, and_, or_, not_
from . import models, schemas
import datetime


def get_user(db: Session, email: str):
    return db.query(models.Member).filter(models.Member.email == email).first()

def get_user_with_id(db: Session, member_id: int):
    return db.query(models.Member).filter(models.Member.member_id == member_id).first()

def get_all_users(db: Session):
    return db.query(models.Member).filter(models.Member.member_type != 2).all()

def upgrade_to_seller(db: Session, member_id: int):
    db_item = db.query(models.Member).filter(models.Member.member_id == member_id).first()
    if not db_item:
        raise ValueError("data not found")
    stmt = (
        update(models.Member)
        .where(models.Member.member_id.in_([member_id]))
        .values(**{"member_type": 1})
    )
    db.execute(stmt)
    db.commit()
    db.refresh(db_item)
    return db_item

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

def update_member_type(db: Session, member_type: schemas.MemberType, member_id: int):
    db_item = db.query(models.Member).filter(models.Member.member_id == member_id).first()
    if not db_item:
        raise ValueError("data not found")
    stmt = (
        update(models.Member)
        .where(models.Member.member_id.in_([member_id]))
        .values(**member_type.dict())
    )
    db.execute(stmt)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_credit_cards_by_member(db: Session, member_id: int):
    return db.query(models.CreditCard).filter(models.CreditCard.member_id == member_id).all()

def get_credit_card(db: Session, card_id: str):
    return db.query(models.CreditCard).filter(models.CreditCard.card_id == card_id).first()

def db_add_credit_card(db: Session, credit_card: schemas.CreditCard, member_id: int):
    db_item = models.CreditCard(**credit_card.dict(), member_id = member_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def add_room(db: Session, room_info: schemas.CreateRoom):
    db_item = models.Room(**room_info.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_credit_card(db: Session, credit_card: schemas.CreditCard):
    db_item = db.query(models.CreditCard).filter(models.CreditCard.card_id == credit_card.card_id).first()
    if not db_item:
        raise ValueError("data not found")
    stmt = (
        update(models.CreditCard)
        .where(models.CreditCard.card_id.in_([credit_card.card_id]))
        .values(**credit_card.dict())
    )
    db.execute(stmt)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_own_hotels(db: Session, member_id: int):
    return db.query(models.Hotel).filter(models.Hotel.member_id == member_id).all()


def check_member_owes_hotel(db: Session, member_id: int, hotel_id: int):
    return db.query(models.Hotel).filter(models.Hotel.member_id == member_id, models.Hotel.id == hotel_id).first


def update_hotel(db: Session, hotel_info: schemas.Hotel):
    db_item = db.query(models.Hotel).filter(models.Hotel.id == hotel_info.id).first()
    if not db_item:
        raise ValueError("data not found")
    stmt = (
        update(models.Hotel)
        .where(models.Hotel.id.in_([hotel_info.id]))
        .values(**hotel_info.dict())
    )
    db.execute(stmt)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_one_hotel(db: Session, hotel_id: int):
    return db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()

def delete_hotel(db: Session, hotel_id: int):
    db_item = db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()
    db.delete(db_item)
    db.commit()
    return db_item



def create_hotel(db: Session, hotel_info: schemas.Hotel, member_id: int):
    db_item = models.Hotel(**hotel_info.dict(), member_id=member_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def ensure_user_owns_room(db: Session, member_id: int, room_id: int):
    print(room_id)
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    result = db.query(models.Hotel).filter(models.Hotel.id == room.hotel_id).first()
    if (result is None) | (result.member_id != member_id):
        raise
    return


def ensure_user_owns_hotel(db: Session, member_id: int, hotel_id: int):
    result = db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()
    if (result is None) | (result.member_id != member_id):
        raise
    return


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


def get_rooms_of_hotel(db: Session, hotel_id: int):
    result = db.query(models.Room).filter(models.Room.hotel_id == hotel_id).all()
    return result


def update_room(db: Session, room_info: schemas.GetAndUpdateRoom):
    db_item = db.query(models.Room).filter(models.Room.id == room_info.id).first()
    if not db_item:
        raise ValueError("room not found")
    stmt = (
        update(models.Room)
        .where(models.Room.id.in_([room_info.id]))
        .values(**room_info.dict())
    )
    db.execute(stmt)
    db.commit()
    db.refresh(db_item)
    return

def search_rooms(db: Session, place: str, number_of_people: int, start_date: datetime.date, end_date: datetime.date):
    result = db.query(models.Room).filter(
        and_(
            (models.Room.hotel_id.in_(db.query(models.Hotel.id).filter(
                or_(
                    (models.Hotel.city == place),
                    (models.Hotel.region == place))))),
            (models.Room.capacity == number_of_people),
            (or_(
                (models.Room.id.notin_(db.query(models.Room_order.room_id))),
                (and_(
                    (end_date < models.Order.start_date),
                    (start_date >= models.Order.end_date)))))))\
        .all()
    return result