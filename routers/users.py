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
async def get_all_salesmen_and_maintenances(skip: int = 0, limit: int = 100,
                                            db: Session = Depends(dependencies.get_db)):
    salesmen_and_maintenances = crud.get_salesman_and_maintenance(db, skip=skip, limit=limit)
    return salesmen_and_maintenances


@router.get("/get_all_users", response_model=List[schemas.User])
async def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/create_salesman", response_model=schemas.User)
async def create_salesman(user: schemas.SalesmanCreate, db: Session = Depends(get_db)):
    """创建业务员"""
    db_salesman = crud.get_user_by_phone(db, phone=user.phone)
    if db_salesman:
        raise HTTPException(status_code=400, detail="业务员已注册")
    return crud.create_salesman(db=db, user=user)


@router.post("/create_maintenance", response_model=schemas.User)
async def create_maintenance(user: schemas.MaintenanceCreate, db: Session = Depends(get_db)):
    """创建维修员"""
    db_maintenance = crud.get_user_by_phone(db, phone=user.phone)
    if db_maintenance:
        raise HTTPException(status_code=400, detail="维修员已注册")
    return crud.create_maintenance(db=db, user=user)


@router.delete("/delete", response_model=schemas.User)
async def delete_user(id: int, db: Session = Depends(get_db)):
    """删除用户"""
    db_user = crud.get_user_by_id(db, id=id)
    if not db_user:
        raise HTTPException(status_code=400, detail="用户不存在")
    return crud.remove_user_by_id(db=db, id=id)


# @router.put("/update", response_model=schemas.User)
# async def update_user(id: int, name: str, db: Session = Depends(get_db)):
#     """更新用户"""
#     db_user = crud.get_user_by_id(db, id=id)
#     if not db_user:
#         raise HTTPException(status_code=400, detail="用户不存在")
#     return crud.update_user(db=db, id=id, name=name)

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