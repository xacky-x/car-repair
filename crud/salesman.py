from sqlalchemy.orm import Session

import models


def get_salesman_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.is_maintenance == "False").filter(models.User.is_administrator == "False").filter(models.User.id == id).first()


def get_salesmen(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.is_maintenance == "False").filter(models.User.is_administrator == "False").offset(skip).limit(limit).all()
