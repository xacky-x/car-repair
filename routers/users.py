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

@router.post("/create_project", response_model=schemas.Project)
async def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    """创建项目表"""
    db_project = crud.get_project_by_name(db, p_name=project.p_name)
    if db_project:
        raise HTTPException(status_code=400, detail="维修项目已存在")
    return crud.create_project(db=db, project=project)


@router.get("/get_all_projects", response_model=List[schemas.ProjectShow])
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


# 材料表接口部分
@router.post("/create_material", response_model=schemas.Material)
async def create_material(material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    """创建新材料"""
    db_material = crud.get_material_by_name(db, mt_name=material.mt_name)
    if db_material:
        raise HTTPException(status_code=400, detail="该材料已录入")
    return crud.create_material(db=db, material=material)


@router.delete("/del_material_by_id/{mt_id}", response_model=schemas.Material)
async def delete_material(mt_id: int, db: Session = Depends(dependencies.get_db)):
    """删除材料"""
    res = crud.remove_material_by_id(db, mt_id=mt_id)
    if res is False:
        raise HTTPException(status_code=404, detail="该材料不存在")


@router.get("/get_all_material", response_model=List[schemas.Material])
async def get_all_material(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    """获取所有材料"""
    return crud.get_all_material(db=db, skip=skip, limit=limit)


@router.get("/get_material_by_id", response_model=schemas.Material)
async def get_material_by_id(mt_id: int, db: Session = Depends(dependencies.get_db)):
    """根据id获取材料"""
    return crud.get_material_by_id(db, mt_id=mt_id)


@router.put("/update_material_by_id/{mt_id}", response_model=schemas.Material)
async def update_material_by_id(mt_id: int, material: schemas.MaterialCreate,
                                db: Session = Depends(dependencies.get_db)):
    """更新材料"""
    updated_material = crud.update_material_by_id(db, material=material, mt_id=mt_id)
    return updated_material


# 使用材料表接口
@router.post("/create_pmaterial", response_model=schemas.PMaterial)
async def create_pmaterial(pmaterial: schemas.PMaterial, db: Session = Depends(get_db)):
    """创建新使用材料记录"""
    db_pmaterial = crud.get_pmaterial_by_id(db, mt_id=pmaterial.mt_id, p_id=pmaterial.p_id)
    if db_pmaterial:
        raise HTTPException(status_code=400, detail="该使用记录已录入")
    return crud.create_pmaterial(db=db, pmaterial=pmaterial)


@router.post("/create_mul_pmaterial", response_model=List[schemas.PMaterial])
async def create_mul_pmaterial(pmaterial: List[schemas.PMaterial], db: Session = Depends(get_db)):
    """创建多条新使用材料记录"""
    for i_pmaterial in pmaterial:
        db_pmaterial = crud.get_pmaterial_by_id(db, mt_id=i_pmaterial.mt_id, p_id=i_pmaterial.p_id)
        if db_pmaterial:
            raise HTTPException(status_code=400, detail="该材料已录入")
    return crud.create_mul_pmaterial(db=db, pmaterial=pmaterial)


@router.delete("/del_pmaterial_by_id/{mt_id}/{p_id}", response_model=schemas.PMaterial)
async def delete_pmaterial(mt_id: int, p_id: int, db: Session = Depends(dependencies.get_db)):
    """删除材料"""
    res = crud.remove_pmaterial_by_id(db, mt_id=mt_id, p_id=p_id)
    if res is False:
        raise HTTPException(status_code=404, detail="该材料不存在")


@router.get("/get_all_pmaterial", response_model=List[schemas.PMaterial])
async def get_all_pmaterial(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    """获取所有维修项目"""
    return crud.get_all_pmaterial(db=db, skip=skip, limit=limit)


@router.get("/get_pmaterial_by_id", response_model=schemas.PMaterial)
async def get_pmaterial_by_id(mt_id: int, p_id: int, db: Session = Depends(dependencies.get_db)):
    """根据pid 和 mtid 获取维修项目"""
    return crud.get_pmaterial_by_id(db, mt_id=mt_id, p_id=p_id)


@router.get("/get_pmaterial_by_mtid/{mt_id}", response_model=List[schemas.PMaterial])
async def get_pmatertial_by_mtid(mt_id: int, db: Session = Depends(dependencies.get_db)):
    """ 根据mtid获取所有维修项目"""
    return crud.get_pmatertial_by_mtid(db, mt_id=mt_id)


@router.put("/update_pmaterial_by_id/{mt_id}", response_model=schemas.PMaterial)
async def update_pmaterial_by_id(mt_id: int, p_id: int, pmaterial: schemas.PMaterialUpdate,
                                 db: Session = Depends(dependencies.get_db)):
    """更新维修项目"""
    updated_pmaterial = crud.update_pmaterial_by_id(db, pmaterial=pmaterial, mt_id=mt_id, p_id=p_id)
    return updated_pmaterial
