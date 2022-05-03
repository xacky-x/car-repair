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
        raise HTTPException(status_code=404, detail="Client not found")
    return db


@router.post("/create_client", response_model=schemas.Client)
async def create_client(client: schemas.ClientCreate, db: Session = Depends(dependencies.get_db)):
    """创建顾客信息"""
    db_client = crud.get_client_by_phone(db, phone=client.phone)
    if db_client:
        raise HTTPException(status_code=400, detail="顾客已注册")
    return crud.create_client(db=db, client=client)


