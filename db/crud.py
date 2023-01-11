from sqlalchemy.orm import Session
from sqlalchemy import select, update, and_, or_, not_
from . import models, schemas
import datetime
from datetime import date


def get_user_with_email(db: Session, email: str):
    return db.query(models.Member).filter(models.Member.email == email).first()

def get_user_with_id(db: Session, member_id: int):
    return db.query(models.Member).filter(models.Member.member_id == member_id).first()

def get_all_users(db: Session):
    return db.query(models.Member).filter(models.Member.member_type != 2).all()

def get_user_with_name(db: Session, name: str):
    return db.query(models.Member).filter(models.Member.name == name).first()

def delete_user(db: Session, email:str):
    db_item = db.query(models.Member).filter(models.Member.email == email).first()
    db.delete(db_item)
    db.commit()
    return db_item

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

def delete_room(db: Session, room_id: int):
    db_item = db.query(models.Room).filter(models.Room.id == room_id).first()
    db.delete(db_item)
    db.commit()
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
    result = []
    room_id = []
    room_amount = []
    for id, amount in db.query(models.Room.id, models.Room.quantity).filter(
            and_(
                (models.Room.hotel_id.in_(db.query(models.Hotel.id).filter(
                    or_(
                        (models.Hotel.city.like("%" + place + "%")),
                        (models.Hotel.region.like("%" + place + "%")))))),
                (models.Room.capacity == number_of_people))):
        room_id.append(id)
        room_amount.append(amount)
    for id in range(len(room_id)):
        for amount in db.query(models.Room_order.amount).filter(
            and_(
                models.Room_order.room_id == room_id[id],
                models.Order.id == models.Room_order.order_id,
                or_(
                    and_(
                        end_date > models.Order.start_date,
                        models.Order.start_date >= start_date),
                    and_(
                        end_date >= models.Order.end_date,
                        models.Order.end_date > start_date)
                )
            )):
            room_amount[id] -= amount
    for id in range(len(room_id)):
        if room_amount[id] == 0:
            del(room_id[id])
            del(room_amount[id])
    hotel_ids = []
    for num in range(len(room_id)):
        for hotel_id, member_id, hotel_name, hotel_image, hotel_city, hotel_region, hotel_road_and_number, hotel_introduction, room_name, room_price in \
            db.query(models.Hotel.id, models.Member.member_id, models.Hotel.hotel_name, models.Hotel.images, models.Hotel.city,
                     models.Hotel.region, models.Hotel.road_and_number, models.Hotel.introduction, models.Room.room_name, models.Room.price)\
                    .filter(
                and_(
                    models.Hotel.id == models.Room.hotel_id,
                    models.Room.id == room_id[num])):
            if hotel_id not in hotel_ids:
                hotel_ids.append(hotel_id)
                result.append({"hotel_id": hotel_id, "member_id": member_id, "hotel_name": hotel_name, "hotel_image": hotel_image,
                               "hotel_location": hotel_city + hotel_region + hotel_road_and_number, "hotel_introduction": hotel_introduction,
                               "room_name": room_name,"room_price": room_price, "left": room_amount[num]})
            break
    return result

def place_order(db: Session, order_info: schemas.Order, member_id: int):
    db_item = models.Order(**order_info.dict(), member_id=member_id)
    db.add(db_item)
    db.commit()
    order_id = db_item.id
    db.refresh(db_item)
    return order_id

def place_room_order(db: Session, room_list: list, order_id: int):
    total_price = {'save': 0,'price': 0}
    for room in room_list:
        for price, original_price in db.query(models.Room.price, models.Room.original_price).filter(models.Room.id == room['room_id']):
            db_item = models.Room_order(room_id=room['room_id'], amount=room['amount'], order_id=order_id, fee=(price * room['amount']))
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            total_price['save'] += (original_price - price) * room['amount']
            total_price['price'] += price * room['amount']
            break
    return total_price

def check_rooms(db: Session, start_date: datetime.date, end_date: datetime.date, room_list: list):
    for room in room_list:
        room_amount = db.query(models.Room.quantity).filter(models.Room.id == room["room_id"]).first()["quantity"]
        for amount in db.query(models.Room_order.amount).filter(
            and_(
                models.Room_order.room_id == room["room_id"],
                models.Order.id == models.Room_order.order_id,
                or_(
                    and_(
                        end_date > models.Order.start_date,
                        models.Order.start_date >= start_date),
                    and_(
                        end_date >= models.Order.end_date,
                        models.Order.end_date > start_date)
                )
            )
        ):
            room_amount -= amount["amount"]
        if room_amount < room["amount"]:
            return False
    return True

def get_coupon_with_id(db: Session, member_id: int):
    return db.query(models.Coupon).filter(models.Coupon.member_id == member_id).all()

def create_coupon(db:Session, coupon: schemas.CouponInfo, member_id: int):
    db_item = models.Coupon(**coupon.dict(), member_id=member_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_used_coupon_for_order(db:Session, order_id: int):
    return db.query(models.Used_Coupon).filter(models.Used_Coupon.order_id == order_id).first()

def use_coupon(db: Session, order_id: int, coupon_id: int, usage_date: date):
    db_item = models.Used_Coupon(order_id=order_id, coupon_id=coupon_id, usage_date=usage_date)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_historical_order(db: Session, member_id: int):
    order_list = []
    for order_id, start_date, end_date in db.query(models.Order.id, models.Order.start_date, models.Order.end_date).filter(models.Order.member_id == member_id):
        room_list = ''
        total_price = 0
        hotel = []
        for hotel_name, hotel_image, hotel_city, hotel_region, hotel_road_and_number, room_name, amount, price in \
                db.query(models.Hotel.hotel_name, models.Hotel.images, models.Hotel.city, models.Hotel.region, models.Hotel.road_and_number, models.Room.room_name, models.Room_order.amount, models.Room_order.fee)\
            .filter(
            (and_(
                (models.Room_order.order_id == order_id),
                (models.Room.id == models.Room_order.room_id),
                (models.Hotel.id == models.Room.hotel_id)))):
            hotel = [str(hotel_name), str(hotel_city + hotel_region + hotel_road_and_number), hotel_image]
            room_list += str(room_name) + str(amount) + '間'
            total_price += price
        order_list.append({"hotel_name": hotel[0], "hotel_addr": hotel[1], "hotel_image": hotel[2], "rooms": room_list, "price": total_price, "date": (str(start_date) + "-" + str(end_date))})
    return order_list

def room_filter(db: Session, shopping_cart: list):
    rooms = []
    for room in shopping_cart:
        if room["amount"] > 0:
            rooms.append(room)
    return rooms