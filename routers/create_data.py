from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from datetime import timedelta

from dependencies import get_db
import crud, schemas, utils

router = APIRouter(
    prefix="/creates",
    tags=["creates"]
)


@router.post("/create", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """创建用户"""
    db_user = crud.get_user_by_phone(db, phone=user.phone)
    if db_user:
        raise HTTPException(status_code=400, detail="用户已注册")
    return crud.create_user(db=db, user=user)


@router.post("/create_random_user", response_model=List[schemas.User])
async def create_random_user(num: int, db: Session = Depends(get_db)):
    """随机生成用户"""
    return crud.create_random_user(db=db, num=num)


@router.post("/create_default_user")
async def create_default_user(db: Session = Depends(get_db)):
    """创建默认用户"""
    return crud.create_default_user(db=db)


@router.post("/create_random_vehicle", response_model=List[schemas.Vehicle])
async def create_random_vehicle(num: int, db: Session = Depends(get_db)):
    """随机生成车辆"""
    return crud.create_random_vehicle(db=db, num=num)


@router.post("/create_random_client", response_model=List[schemas.Client])
async def create_random_client(num: int, db: Session = Depends(get_db)):
    """随机生成客户"""
    return crud.create_random_client(db=db, num=num)


@router.post("/create_random_repair", response_model=List[schemas.Repair])
async def create_random_repair(num: int, db: Session = Depends(get_db)):
    """随机创建维修单"""
    return crud.create_random_repair(db=db, num=num)


# 材料表部分


@router.post("/create_default_material", response_model=List[schemas.Material])
async def create_default_material(db: Session = Depends(get_db)):
    """创建默认材料表"""
    return crud.create_default_material(db=db)


@router.post("/create_default_project", response_model=List[schemas.Project])
async def create_default_project(db: Session = Depends(get_db)):
    """创建默认维修项目表"""
    return crud.create_default_project(db=db)
