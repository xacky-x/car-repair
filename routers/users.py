from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from typing import List
from datetime import timedelta

from dependencies import get_db
import crud, schemas, utils, dependencies

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(dependencies.verify_administrator)]
)


@router.get("/get_all_administrators", response_model=List[schemas.User])
async def get_all_administrators(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    administrators = crud.get_administrator(db, skip=skip, limit=limit)
    return administrators


@router.get("/get_all_salesmen", response_model=List[schemas.User])
async def get_all_salesmen(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    salesmen = crud.get_salesmen(db, skip=skip, limit=limit)
    return salesmen


@router.get("/get_all_maintenances", response_model=List[schemas.User])
async def get_all_maintenances(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    maintenances = crud.get_maintenances(db, skip=skip, limit=limit)
    return maintenances


@router.get("/get_all_salesmen_and_maintenances", response_model=List[schemas.User])
async def get_all_salesmen_and_maintenances(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    salesmen_and_maintenances = crud.get_salesman_and_maintenance(db, skip=skip, limit=limit)
    return salesmen_and_maintenances


@router.get("/get_all_users", response_model=List[schemas.User])
async def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.post("/create_project", response_model=List[schemas.Project])
async def create_project(num: int, db: Session = Depends(dependencies.get_db)):
    """随机创建维修项目表"""
    return crud.create_project(db=db, num=num)
