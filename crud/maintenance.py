from sqlalchemy.orm import Session

import models
import schemas


def get_maintenance_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.is_maintenance == "True", models.User.id == id).first()


def get_maintenances(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.is_maintenance == "True").offset(skip).limit(limit).all()


def get_my_order(db: Session, id: int):
    # 获取所有派单
    return db.query(models.Order).filter(models.Order.m_id == id).all()


def update_order_by_oid(db: Session, order: schemas.OrderCreate, o_id: int):
    # 更新派工状态
    db.query(models.Order).filter(models.Order.o_id == o_id).update(order.dict())
    db.commit()
    return


def update_order_by_oid_repair(db: Session, o_id: int):
    # 更新派工状态
    order = db.query(models.Order).filter(models.Order.o_id == o_id).first()
    order.status = 1
    db.commit()
