from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Sequence

from .database import Base


class Hotel(Base):
    __tablename__ = "hotel"

    id = Column(Integer, Sequence('hotel_id_seq'), primary_key=True)
    member_id = Column(Integer)
    hotel_name = Column(String)
    regulation = Column(String)
    city = Column(String)
    region = Column(String)
    road_and_number = Column(String)
    certificate_number = Column(String)
    image_path = Column(String)
    member_id = Column(Integer, ForeignKey("member.member_id"))

class Member(Base):
    __tablename__ = "member"
    # todo fill in the rest of this table
    email = Column(String)
    member_id = Column(Integer, primary_key=True)
    password = Column(String)
    name = Column(String)
    gender = Column(Integer)
    phone = Column(String)
    member_type = Column(Integer)
    # credit_cards = Column(String)

class Room(Base):
    __tablename__ = "room"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_name = Column(String)
    quantity = Column(Integer)
    capacity = Column(Integer)
    price = Column(Integer)
    image_path = Column(String)
    hotel_id = Column(Integer, ForeignKey("Hotel.id"))

class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)
    fee = Column(Integer)
    amount = Column(Integer)
    payment_method = Column(Integer)
    end_data = Column(String)
    start_data = Column(String)
    note = Column(String)
    member_id = Column(Integer, ForeignKey("member.member_id"))
    room_id = Column(Integer, ForeignKey("Room.id"))

class Rating(Base):
    __tablename__ = "rating"
    id = Column(Integer, Sequence('rating_id_seq'), primary_key=True)
    evaluation = Column(Integer)
    comments = Column(String)
    image_path = Column(String)
    order_id = Column(Integer, ForeignKey("order.id"))
