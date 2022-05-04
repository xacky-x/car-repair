from sqlalchemy.orm import Session

import models


def get_maintenance_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.is_maintenance == "True").filter(models.User.id == id).first()


def get_maintenances(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.is_maintenance == "True").offset(skip).limit(limit).all()
