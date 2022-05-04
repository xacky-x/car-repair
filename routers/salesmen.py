from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from typing import List
from datetime import timedelta

import crud, schemas, utils, dependencies

router = APIRouter(
    prefix="/salesmen",
    tags=["salesmen"],
    dependencies=[Depends(dependencies.verify_salesman)]
)


@router.get("/get_me", response_model=schemas.User)
async def get_me(token: str = Depends(utils.oauth2_scheme), db: Session = Depends(dependencies.get_db)):
    """获取当前业务员个人信息"""
    sub = dependencies.verify_token(token)
    phone = sub.split(',')[0]
    db = crud.get_user_by_phone(db, phone=phone)
    if db is None:
        raise HTTPException(status_code=404, detail="业务员信息不存在")
    return db


@router.get("/get_all", response_model=List[schemas.Client])
async def get_clients(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    """获取所有顾客信息"""
    clients = crud.get_clients(db, skip=skip, limit=limit)
    return clients


@router.get("/get_by_phone/{phone}", response_model=schemas.Client)
async def get_client(phone: str, db: Session = Depends(dependencies.get_db)):
    """根据手机号获取顾客信息"""
    db_client = crud.get_client_by_phone(db, phone=phone)
    if db_client is None:
        raise HTTPException(status_code=404, detail="顾客不存在")
    return db_client


@router.post("/create_client", response_model=schemas.Client)
async def create_client(client: schemas.ClientCreate, db: Session = Depends(dependencies.get_db)):
    """创建顾客信息"""
    db_client = crud.get_client_by_phone(db, phone=client.phone)
    if db_client:
        raise HTTPException(status_code=400, detail="顾客已注册")
    return crud.create_client(db=db, client=client)


@router.post("/create_vehicle/{c_id}/", response_model=schemas.Vehicle)
async def create_client_vehicle(c_id: int, vehicle: schemas.VehicleCreate, db: Session = Depends(dependencies.get_db)):
    """新增客户车辆信息"""
    db_vehicle = crud.get_vehicles_by_id(db, c_id=c_id)
    if db_vehicle:
        raise HTTPException(status_code=400, detail="车辆已存在")
    return crud.create_client_vehicle(db=db, vehicle=vehicle, c_id=c_id)


@router.delete("/del_by_id/{c_id}", response_model=schemas.Client)
async def delete_client(c_id: int, db: Session = Depends(dependencies.get_db)):
    """删除客户信息"""
    res = crud.remove_client_by_id(db, c_id=c_id)
    if res is False:
        raise HTTPException(status_code=404, detail="顾客不存在")


@router.get("/get_all_repair", response_model=List[schemas.Repair])
async def get_all_repair(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    all_repair = crud.get_all_repair(db, skip=skip, limit=limit)
    print(all_repair)
    return all_repair


