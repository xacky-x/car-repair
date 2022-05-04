from sqlalchemy.orm import Session

import models, schemas

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
        print(db_repair.approach_time)
        print(db_repair.completion_time)
        print(type(db_repair.approach_time))
        print(type(db_repair.completion_time))

        db_repair_list.append(db_repair)
        db.add(db_repair)
        db.commit()
        db.refresh(db_repair)
    return db_repair_list


def get_repair_by_type(db: Session, type: str):
    # 根据维修单类型查询
    return db.query(models.Repair).filter(models.Repair.type == type).first()


def get_repair_by_id(db: Session, id: str):
    # 根据维修单id查询对应维修单具体信息
    return db.query(models.Repair).filter(models.Repair.id == id).first()


def update_repair_by_id(db: Session, repair: schemas.RepairCreate, r_id: int):
    # 更新维修单里的数据
    db_repair = models.Repair(
        r_id=r_id,
        r_type=repair.r_type,
        r_class=repair.r_class,
        payment=repair.payment,
        mileage=repair.mileage,
        fuel=repair.fuel,
        approach_time=repair.approach_time,
        failure=repair.failure,
        completion_time=repair.completion_time,
        date=repair.date,
        cost=repair.cost,
        v_id=repair.v_id,
        s_id=repair.s_id
    )

    db.add(db_repair)
    db.commit()
    db.refresh(db_repair)
    return db_repair


def remove_repair_by_id(db: Session, r_id: int):
    # 删除维修单
    db_repair = db.query(models.Client).filter(models.Repair.r_id == r_id).first()
    if db_repair:
        db.delete(db_repair)
    else:
        return False
    db.commit()
    db.flush()
    return True
