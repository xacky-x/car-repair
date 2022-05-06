import random
from sqlalchemy.orm import Session
from typing import List

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


def create_default_project(db: Session):
    # 创建维修项目表
    action_list = ["维修", "更换"]
    item_list = ["车头", "车灯", "车门", "水箱"]
    project_list = [x+y for x in action_list for y in item_list]
    db_project_list = []
    for i in range(len(project_list)):
        db_project = models.Project(
            p_name=project_list[i]
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


# 材料表部分
def create_default_material(db: Session):
    # 随机生成材料表
    mname_list = ['油漆', '火花塞', '节气门体', '发动机', '发动机总成', '油泵', '油嘴', '涨紧轮', '气缸体', '轴瓦', '水泵', '燃油喷射', '密封垫', '凸轮轴', '气门',
                  '曲轴', '连杆总成', '活塞', '皮带', '消声器', '化油器', '油箱', '水箱', '风扇', '油封', '散热器', '滤清器']
    db_material_list = []
    for i in range(len(mname_list)):
        db_material = models.Material(
            mt_name= mname_list[i],
            mt_cost=utils.random_cost()
        )
        db_material_list.append(db_material)
        db.add(db_material)
        db.commit()
        db.refresh(db_material)
    return db_material_list


def create_material(db: Session, material: schemas.MaterialCreate):
    # 创建材料表
    db_material = models.Material(
        mt_name=material.mt_name,
        mt_cost=material.mt_cost
    )
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


def remove_material_by_id(db: Session, mt_id: int):
    # 删除材料表
    db_material = db.query(models.Material).filter(models.Material.mt_id == mt_id).first()
    if db_material:
        db.delete(db_material)
    else:
        return False
    db.commit()
    db.flush()
    return True


def get_material_by_id(db: Session, mt_id: int):
    # 根据id获取材料表
    return db.query(models.Material).filter(models.Material.mt_id == mt_id).first()


def get_material_by_name(db: Session, mt_name: str):
    # 根据名字获取材料表
    return db.query(models.Material).filter(models.Material.mt_name == mt_name).first()


def get_all_material(db: Session, skip: int = 0, limit: int = 100):
    # 获取所有材料单
    count = db.query(models.Material).count()  # 查询数据库现有的数据量
    if limit > count:  # 若希望查询数据超量，则只返回现有的所有数据
        limit = count
    return db.query(models.Material).offset(skip).limit(limit).all()


def update_material_by_id(db: Session, material: schemas.Material, mt_id: int):
    # 更新材料表
    db.query(models.Material).filter(models.Material.mt_id == mt_id).update(material.dict())
    db.commit()
    return


# 项目使用材料表
def create_pmaterial(db: Session, pmaterial: schemas.PMaterial):
    # 创建使用材料表
    db_pmaterial = models.PMaterial(
        mt_id=pmaterial.mt_id,
        p_id=pmaterial.p_id,
        num=pmaterial.num,
    )
    db.add(db_pmaterial)
    db.commit()
    db.refresh(db_pmaterial)
    return db_pmaterial


def create_mul_pmaterial(db: Session, pmaterial: List[schemas.PMaterial]):
    # 创建多条使用材料记录
    db_pmaterial_list = []
    for i_pmaterial in pmaterial:
        db_pmaterial = models.PMaterial(
            mt_id=i_pmaterial.mt_id,
            p_id=i_pmaterial.p_id,
            num=i_pmaterial.num,
        )
        db_pmaterial_list.append(db_pmaterial)
        db.add(db_pmaterial)
        db.commit()
        db.refresh(db_pmaterial)
    return db_pmaterial_list


def remove_pmaterial_by_id(db: Session, mt_id: int, p_id: int):
    # 删除使用材料表
    db_pmaterial = db.query(models.PMaterial).filter(models.PMaterial.mt_id == mt_id,
                                                     models.PMaterial.p_id == p_id).first()
    if db_pmaterial:
        db.delete(db_pmaterial)
    else:
        return False
    db.commit()
    db.flush()
    return True


def get_pmaterial_by_id(db: Session, mt_id: int, p_id: int):
    # 根据id获取使用材料表
    return db.query(models.PMaterial).filter(models.PMaterial.mt_id == mt_id, models.PMaterial.p_id == p_id).first()


def get_all_pmaterial(db: Session, skip: int = 0, limit: int = 100):
    # 获取所有使用材料单
    count = db.query(models.PMaterial).count()  # 查询数据库现有的数据量
    if limit > count:  # 若希望查询数据超量，则只返回现有的所有数据
        limit = count
    return db.query(models.PMaterial).offset(skip).limit(limit).all()


def update_pmaterial_by_id(db: Session, pmaterial: schemas.PMaterialUpdate, mt_id: int, p_id: int):
    # 更新使用材料表
    db.query(models.PMaterial).filter(models.PMaterial.mt_id == mt_id, models.PMaterial.p_id == p_id).update(
        pmaterial.dict())
    db.commit()
    return
