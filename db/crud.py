from sqlalchemy.orm import Session
from . import models, schemas

def check_hotel_id(db: Session, member_id: int, hotel_id: int):
    own_hotel_id = []
    for id in db.query(models.Hotel.id).filter(models.Hotel.member_id == member_id).all():
        own_hotel_id.append(id['id'])
    if hotel_id in own_hotel_id:
        return True
    else: return False

def add_room(db: Session, room_info: schemas.Room):
    db_item = models.Room(**room_info.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item