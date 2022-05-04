from sqlalchemy.orm import Session

import models

from utils import random_data as rd


def get_salesman_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.is_maintenance == "False").filter(
        models.User.is_administrator == "False").filter(models.User.id == id).first()


def get_salesmen(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.is_maintenance == "False").filter(
        models.User.is_administrator == "False").offset(skip).limit(limit).all()


def get_all_repair(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Repair).offset(skip).limit(limit).all()


def create_random_repair(db: Session, num: int):
    db_repair_list = []
    for i in range(num):
        db_repair = models.Repair(
            r_type=rd.random_r_type(),
            r_class=rd.random_r_class(),
            payment=rd.random_payment(),
            mileage=rd.random_mileage(),
            fuel=rd.random_fuel(),
            approach_time=rd.random_approach_time(),
            failure=rd.random_failure(),
            completion_time=rd.random_completion_time(),
            date=rd.random_date(),
            cost=rd.random_cost(),
            s_id=rd.random_id(),
            v_id=rd.random_id(),
        )
        db_repair_list.append(db_repair)
        db.add(db_repair)
        db.commit()
        db.refresh(db_repair)
    return db_repair_list
