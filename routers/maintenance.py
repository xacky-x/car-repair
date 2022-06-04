from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from typing import List
from datetime import timedelta

import crud, schemas, utils, dependencies

router = APIRouter(
    prefix="/maintenance",
    tags=["maintenance"],
    dependencies=[Depends(dependencies.verify_maintenance)]
)


@router.get("/get_me", response_model=schemas.User)
async def get_me(token: str = Depends(utils.oauth2_scheme), db: Session = Depends(dependencies.get_db)):
    """获取当前维修员个人信息"""
    sub = dependencies.verify_token(token)
    phone = sub.split(',')[0]
    db = crud.get_user_by_phone(db, phone=phone)
    if db is None:
        raise HTTPException(status_code=404, detail="维修员信息不存在")
    return db


@router.get("/get_my_order/{m_id}", response_model=List[schemas.OrderShow])
async def get_my_order(m_id: int, db: Session = Depends(dependencies.get_db)):
    """根据id获取自己的派单信息"""
    db_order_list = crud.get_my_order(db, id=m_id)
    return db_order_list


@router.get("/get_repair_by_id/{id}", response_model=schemas.Repair)
async def get_repair_by_id(id: int, db: Session = Depends(dependencies.get_db)):
    """根据id获取维修单"""
    db_repair = crud.get_repair_by_id(db, id=id)
    if db_repair is None:
        raise HTTPException(status_code=404, detail="维修单不存在")
    return db_repair


@router.put("/update_order_by_oid/{o_id}")
async def update_order_by_oid(o_id: int, db: Session = Depends(dependencies.get_db)):
    """更新派工单"""
    crud.update_order_by_oid_repair(db, o_id=o_id)


@router.get("/get_all_projects", response_model=List[schemas.ProjectShow])
async def get_all_projects(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    """获取所有维修项目"""
    projects = crud.get_projects(db, skip=skip, limit=limit)
    return projects
