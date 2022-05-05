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
    count = db.query(models.Repair).count()  # 查询数据库现有的数据量
    if limit > count:  # 若希望查询数据超量，则只返回现有的所有数据
        limit = count
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


def create_repair(db: Session, repair: schemas.RepairCreate):
    # 创建维修单
    db_repair = models.Repair(
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
        s_id=repair.s_id,
        v_id=repair.v_id
    )
    db.add(db_repair)
    db.commit()
    db.refresh(db_repair)
    return db_repair


def get_repair_by_type(db: Session, type: str):
    # 根据维修单类型查询
    return db.query(models.Repair).filter(models.Repair.r_type == type).all()


def get_repair_by_id(db: Session, id: int):
    # 根据维修单id查询对应维修单具体信息
    return db.query(models.Repair).filter(models.Repair.r_id == id).first()


def get_repair_by_cv(db: Session, s_id: int, v_id: int):
    # 根据用户id和车辆id获取对应维修单,没有写接口（先留着，不用可以删除）
    return db.query(models.Repair).filter(models.Repair.s_id == s_id, models.Repair.v_id == v_id).first()


def update_repair_by_id(db: Session, repair: schemas.RepairCreate, r_id: int):
    # 更新维修单
    db.query(models.Repair).filter(models.Repair.r_id == r_id).update(repair.dict())
    db.commit()
    return


def remove_repair_by_id(db: Session, r_id: int):
    # 删除维修单
    db_repair = db.query(models.Repair).filter(models.Repair.r_id == r_id).first()
    if db_repair:
        db.delete(db_repair)
    else:
        return False
    db.commit()
    db.flush()
    return True
