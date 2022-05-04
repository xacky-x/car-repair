from sqlalchemy.orm import Session

import models


def get_vehicles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vehicle).offset(skip).limit(limit).all()

def get_vehicles_by_id(db: Session, c_id: int):
    return db.query(models.Vehicle).filter(models.Vehicle.c_id == c_id).all()