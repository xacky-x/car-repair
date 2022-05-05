import random
from sqlalchemy.orm import Session

import models, schemas, utils


def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_administrator(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.is_administrator == "True").offset(skip).limit(limit).all()


def get_salesman_and_maintenance(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.is_administrator == "False").offset(skip).limit(limit).all()


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
        is_administrator=user.is_administrator,
        is_maintenance=user.is_maintenance
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_salesman(db: Session, user: schemas.SalesmanCreate):
    hashed_password = utils.get_password_hash(user.password)
    db_user = models.User(
        phone=user.phone,
        password=hashed_password,
        name=user.name,
        is_administrator=False,
        is_maintenance=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_maintenance(db: Session, user: schemas.MaintenanceCreate):
    hashed_password = utils.get_password_hash(user.password)
    db_user = models.User(
        phone=user.phone,
        password=hashed_password,
        name=user.name,
        m_type=user.m_type,
        m_hour=user.m_hour,
        is_administrator=False,
        is_maintenance=True
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


def create_default_user(db: Session):
    db_user = models.User(
        phone="1",
        password=utils.get_password_hash("1"),
        name="管理员",
        is_administrator=True,
        is_maintenance=False
    )
    db.add(db_user)
    db_user = models.User(
        phone="2",
        password=utils.get_password_hash("2"),
        name="业务员",
        is_administrator=False,
        is_maintenance=False
    )
    db.add(db_user)
    db_user = models.User(
        phone="3",
        password=utils.get_password_hash("3"),
        name="维修员",
        m_type="机修",
        m_hour="50",
        is_administrator=False,
        is_maintenance=True
    )
    db.add(db_user)
    db.commit()


def remove_user_by_id(db: Session, id: int):
    # 删除用户
    db_user = get_user_by_id(db, id=id)
    db.delete(db_user)
    db.commit()
    return db_user


def update_user(db: Session, id: int, name: str):
    db_user = get_user_by_id(db, id=id)
    db_user.name = name
    db.commit()
    return db_user


def authenticate_user(db: Session, phone: str, password: str):
    user = get_user_by_phone(db, phone)
    if not user:
        return False
    if not utils.verify_password(password, user.password):
        return False
    return user

def create_project(db: Session, num: int):
    #创建维修项目表
    db_project_list = []
    for i in range(num):
        db_project = models.Project(
            p_name=utils.random_pname()
        )
        db_project_list.append(db_project)
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
    return db_project_list

def remove_project_by_id(db: Session, p_id: int):
    # 删除维修项目表
    db_project = db.query(models.Project).filter(models.Project.p_id == p_id).first()
    if db_project:
        db.delete(db_project)
    else:
        return False
    db.commit()
    db.flush()
    return True

def get_project_by_id(db: Session, p_id: int):
    # 根据id获取维修项目表
    return db.query(models.Project).filter(models.Project.p_id == p_id).first()

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    # 获取所有维修项目
    return db.query(models.Project).offset(skip).limit(limit).all()

def update_project_by_id(db: Session, project: schemas.Project, p_id: int):
    # 更新维修项目
    db.query(models.Project).filter(models.Project.p_id == p_id).update(project.dict())
    db.commit()
    return