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
    return db.query(models.Repair).order_by(models.Repair.r_id).offset(skip).limit(limit).all()


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
    db_repair = models.Repair(**repair.dict())
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


def create_order(db: Session, order: schemas.OrderCreate):
    # 创建派工单
    db_order = models.Order(
        r_id=order.r_id,
        p_id=order.p_id,
        hour=order.hour,
        status=order.status,
        m_id=order.m_id
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def remove_order_by_id(db: Session, o_id: int):
    # 删除派工单
    db_order = db.query(models.Order).filter(models.Order.o_id == o_id).first()
    if db_order:
        db.delete(db_order)
    else:
        return False
    db.commit()
    db.flush()
    return True


def get_order_by_rid(db: Session, r_id: int):
    # 根据维修单获取派单信息
    return db.query(models.Order).filter(models.Order.r_id == r_id).all()


def get_m_hour(db: Session, m_id: int):
    # 获取维修员的单价
    return db.query(models.User).filter(models.User.id == m_id).first()


def update_cost(db: Session, r_id: int, cost: float):
    db_repair = get_repair_by_id(db, id=r_id)
    db_repair.cost = cost
    db.commit()
    return


def get_project_by_pid(db: Session, p_id: int):
    # 根据pid获取项目信息
    return db.query(models.Project).filter(models.Project.p_id == p_id).first()
