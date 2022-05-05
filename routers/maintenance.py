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


@router.get("/get_my_order/{m_id}", response_model=schemas.Order)
async def get_my_order(m_id:int, db: Session = Depends(dependencies.get_db)):
    """根据id获取自己的派单信息"""
    db_order = crud.get_my_order(db, id=m_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="无派单")
    return db_order

@router.put("/update_order_by_oid/{o_id}", response_model=schemas.Order)
async def update_order_by_oid(o_id: int, order: schemas.OrderCreate, db: Session = Depends(dependencies.get_db)):
    """更新派工单"""
    updated_order = crud.update_order_by_oid(db, order=order, o_id=o_id)
    return updated_order

@router.get("/get_all_projects", response_model=List[schemas.Project])
async def get_all_projects(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    """获取所有维修项目"""
    projects = crud.get_projects(db, skip=skip, limit=limit)
    return projects
