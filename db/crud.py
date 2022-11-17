from sqlalchemy.orm import Session
from . import models


def get_own_hotels(db: Session, member_id: int):
    return db.query(models.Hotel).filter(models.Hotel.member_id == member_id).all()
