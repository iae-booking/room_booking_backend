from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Sequence, Date, LargeBinary
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from .database import Base


class Hotel(Base):
    __tablename__ = "hotel"

    id = Column(Integer, Sequence('hotel_id_seq'), primary_key=True)
    member_id = Column(Integer)
    hotel_name = Column(String)
    introduction = Column(String)
    attraction = Column(String)
    regulation = Column(String)
    city = Column(String)
    region = Column(String)
    road_and_number = Column(String)
    transportation = Column(String)
    certificate_number = Column(String)
    images= Column(ARRAY(LargeBinary))
    member_id = Column(Integer, ForeignKey("member.member_id"))
    rooms = relationship(
        "Room",
        back_populates="hotel",
        cascade="all, delete",
        passive_deletes=True,
    )


class Member(Base):
    __tablename__ = "member"
    email = Column(String)
    member_id = Column(Integer, primary_key=True)
    password = Column(String)
    name = Column(String)
    gender = Column(Integer)
    phone = Column(String)
    images = Column(LargeBinary)
    member_type = Column(Integer,default=0)


class CreditCard(Base):
    __tablename__ = "credit_cards"

    safety_number = Column(String)
    card_id = Column(String, primary_key=True)
    expire_date = Column(Date)
    member_id = Column(Integer)


class Room(Base):
    __tablename__ = "room"
    id = Column(Integer, Sequence('room_id_seq'), primary_key=True)
    room_name = Column(String)
    quantity = Column(Integer)
    capacity = Column(Integer)
    bed_type= Column(String)
    introduction= Column(String)
    installation= Column(String)
    original_price= Column(Integer)
    price= Column(Integer)
    hotel_id = Column(Integer, ForeignKey("hotel.id", ondelete="cascade"))
    hotel = relationship("Hotel", back_populates="rooms")

class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)
    start_date = Column(Date)
    end_date = Column(Date)
    member_id = Column(Integer, ForeignKey("member.member_id"))
    payment_method = Column(Integer)
    note = Column(String)

class Rating(Base):
    __tablename__ = "rating"
    id = Column(Integer, Sequence('rating_id_seq'), primary_key=True)
    evaluation = Column(Integer)
    comments = Column(String)
    images= Column(ARRAY(LargeBinary))
    order_id = Column(Integer, ForeignKey("order.id"))

class Room_order(Base):
    __tablename__ = "room_order"
    id = Column(Integer, Sequence('room_order_id_seq'), primary_key=True)
    room_id = Column(Integer, ForeignKey("room.id"))
    order_id = Column(Integer, ForeignKey("order.id"))
    fee = Column(Integer)
    amount = Column(Integer)
