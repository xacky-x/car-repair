from sqlalchemy.orm import Session
from fastapi import Depends

import models, schemas, utils

import random


def get_client_by_id(db: Session, c_id: int):
    return db.query(models.Client).filter(models.Client.c_id == c_id).first()


def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Client).offset(skip).limit(limit).all()


def get_client_by_phone(db: Session, phone: str):
    return db.query(models.Client).filter(models.Client.phone == phone).first()


def create_client(db: Session, client: schemas.ClientCreate):
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def create_random_client(db: Session, num: int):
    db_client_list = []
    for i in range(num):
        name = utils.random_name()
        if random.choice(range(2)) > 0:
            c_name = utils.random_company()
            c_p = '单位'
        else:
            c_name = name
            c_p = '个人'
        db_client = models.Client(
            c_password=utils.get_password_hash("123"),
            c_name=c_name,
            c_p=c_p,
            discount=utils.random_discount(),
            contact=name,
            phone=utils.random_phone()
        )
        db_client_list.append(db_client)
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
    return db_client_list


def authenticate_client(db: Session, phone: str, password: str):
    client = get_client_by_phone(db, phone)
    if not client:
        return False
    if not utils.verify_password(password, client.c_password):
        return False
    return client


def create_client_vehicle(db: Session, vehicle: schemas.VehicleCreate, c_id: int, token: str = Depends(utils.oauth2_scheme)):
    db_vehicle = models.Vehicle(
        license=vehicle.license,
        v_type=vehicle.v_type,
        colour=vehicle.colour,
        v_class=vehicle.v_class,
        c_id=c_id
    )
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle
