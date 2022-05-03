import random
from sqlalchemy.orm import Session

import models, schemas, utils


def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_phone(db: Session, phone: str):
    return db.query(models.User).filter(models.User.phone == phone).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = utils.get_password_hash(user.password)
    db_user = models.User(
        phone=user.phone,
        password=hashed_password,
        name=user.name,
        m_type=user.m_type,
        m_hour=user.m_hour,
        is_maintenance=user.is_maintenance
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_random_user(db: Session, num: int):
    db_user_list = []
    for i in range(num):
        is_administrator = random.choice(range(2))
        is_maintenance = random.choice(range(2))
        if is_administrator > 0:
            db_user = models.User(
                phone=utils.random_phone(),
                password=utils.get_password_hash("123"),
                name=utils.random_name(),
                is_administrator=is_administrator,
                is_maintenance=False
            )
        else:
            if is_maintenance > 0:
                db_user = models.User(
                    phone=utils.random_phone(),
                    password=utils.get_password_hash("123"),
                    name=utils.random_name(),
                    m_type=utils.random_type(),
                    m_hour=utils.random_hour(),
                    is_administrator=False,
                    is_maintenance=is_maintenance
                )
            else:
                db_user = models.User(
                    phone=utils.random_phone(),
                    password=utils.get_password_hash("123"),
                    name=utils.random_name(),
                    is_administrator=False,
                    is_maintenance=is_maintenance
                )
        db_user_list.append(db_user)
        db.add(db_user)
    db.commit()
    return db_user_list


def authenticate_user(db: Session, phone: str, password: str):
    user = get_user_by_phone(db, phone)
    if not user:
        return False
    if not utils.verify_password(password, user.password):
        return False
    return user
