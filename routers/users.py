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

@router.get("/get_all_projects", response_model=List[schemas.Project])
async def get_all_projects(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    """获取所有维修项目"""
    projects = crud.get_projects(db, skip=skip, limit=limit)
    return projects

@router.put("/update_project_by_id/{p_id}", response_model=schemas.Project)
async def update_project_by_id(p_id: int, project: schemas.ProjectCreate, db: Session = Depends(dependencies.get_db)):
    """更新维修项目"""
    updated_project = crud.update_project_by_id(db, project=project, p_id=p_id)
    return updated_project

@router.delete("/del_project_by_id/{p_id}", response_model=schemas.Project)
async def delete_project(p_id: int, db: Session = Depends(dependencies.get_db)):
    """删除维修项目"""
    res = crud.remove_project_by_id(db, p_id=p_id)
    if res is False:
        raise HTTPException(status_code=404, detail="维修项目不存在")