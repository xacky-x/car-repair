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


@router.get("/get_all_clients", response_model=List[schemas.Client])
async def get_all_clients(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    """获取所有顾客信息"""
    clients = crud.get_clients(db, skip=skip, limit=limit)
    return clients


@router.get("/get_client_by_phone/{phone}", response_model=schemas.Client)
async def get_client_by_phone(phone: str, db: Session = Depends(dependencies.get_db)):
    """根据手机号获取顾客信息"""
    db_client = crud.get_client_by_phone(db, phone=phone)
    if db_client is None:
        raise HTTPException(status_code=404, detail="顾客不存在")
    return db_client


@router.get("/get_client_by_id/{id}", response_model=schemas.Client)
async def get_client_by_id(id: int, db: Session = Depends(dependencies.get_db)):
    """根据id获取顾客信息"""
    db_client = crud.get_client_by_id(db, c_id=id)
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
    db_client = crud.get_client_by_id(db, c_id=c_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="顾客不存在")
    return crud.create_client_vehicle(db=db, vehicle=vehicle, c_id=c_id)


@router.delete("/delvehicle/{c_id}/{v_id}", response_model=schemas.Client)
async def delete_vehicle(c_id: int, v_id: int, db: Session = Depends(dependencies.get_db)):
    """删除客户车辆信息"""
    db_client = crud.get_client_by_id(db, c_id=c_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="顾客不存在")
    res = crud.remove_vehicle_by_id(db, v_id=v_id, c_id=c_id)
    if res is False:
        raise HTTPException(status_code=404, detail="车辆不存在")


@router.delete("/del_by_id/{c_id}", response_model=schemas.Client)
async def delete_client(c_id: int, db: Session = Depends(dependencies.get_db)):
    """删除客户信息"""
    res = crud.remove_client_by_id(db, c_id=c_id)
    if res is False:
        raise HTTPException(status_code=404, detail="顾客不存在")


@router.post("/create_repair", response_model=schemas.Repair)
async def create_repair(repair: schemas.RepairCreate, db: Session = Depends(dependencies.get_db)):
    """创建维修单信息"""
    return crud.create_repair(db=db, repair=repair)


@router.get("/get_all_repair", response_model=List[schemas.RepairShow])
async def get_all_repair(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    """获取所有维修单"""
    all_repair = crud.get_all_repair(db, skip=skip, limit=limit)
    return all_repair


@router.get("/get_repair_by_type/{type}", response_model=List[schemas.Repair])
async def get_repair_by_type(type: str, db: Session = Depends(dependencies.get_db)):
    """根据类型获取维修单"""
    db_repair = crud.get_repair_by_type(db, type=type)
    if db_repair is None:
        raise HTTPException(status_code=404, detail="维修单不存在")
    return db_repair


@router.get("/get_repair_by_id/{id}", response_model=schemas.Repair)
async def get_repair_by_id(id: int, db: Session = Depends(dependencies.get_db)):
    """根据id获取维修单"""
    db_repair = crud.get_repair_by_id(db, id=id)
    if db_repair is None:
        raise HTTPException(status_code=404, detail="维修单不存在")
    return db_repair


@router.put("/update_repair_by_id/{r_id}", response_model=schemas.Repair)
async def update_repair_by_id(r_id: int, repair: schemas.RepairCreate, db: Session = Depends(dependencies.get_db)):
    updated_repair = crud.update_repair_by_id(db, repair=repair, r_id=r_id)
    return updated_repair


@router.delete("/del_repair_by_id/{r_id}", response_model=schemas.Repair)
async def delete_repair_by_id(id: int, db: Session = Depends(dependencies.get_db)):
    """删除维修单"""
    db_repair = crud.get_repair_by_id(db, id=id)
    print(db_repair)
    if db_repair is None:
        raise HTTPException(status_code=404, detail="维修单不存在")
    crud.remove_repair_by_id(db, r_id=id)


@router.post("/create_order", response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate, db: Session = Depends(dependencies.get_db)):
    """创建派工单信息"""
    if not crud.get_maintenance_by_id(db, id=order.m_id):
        raise HTTPException(status_code=404, detail="维修人员不存在")
    else:
        return crud.create_order(db=db, order=order)


@router.delete("/del_order_by_id/{o_id}", response_model=schemas.Order)
async def delete_order(o_id: int, db: Session = Depends(dependencies.get_db)):
    """删除派工单"""
    res = crud.remove_order_by_id(db, o_id=o_id)
    if res is False:
        raise HTTPException(status_code=404, detail="派工单不存在")


@router.get("/get_order_by_rid/{r_id}", response_model=List[schemas.OrderShow])
async def get_order_by_rid(r_id: int, db: Session = Depends(dependencies.get_db)):
    """根据维修单id获取派单信息"""
    db_order = crud.get_order_by_rid(db, r_id=r_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="无派单")
    return db_order


@router.put("/update_order_by_oid/{o_id}", response_model=schemas.Order)
async def update_order_by_oid(o_id: int, order: schemas.OrderCreate, db: Session = Depends(dependencies.get_db)):
    """更新派工单"""
    updated_order = crud.update_order_by_oid(db, order=order, o_id=o_id)
    return updated_order


@router.get("/get_all_projects", response_model=List[schemas.ProjectShow])
async def get_all_projects(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    """获取所有维修项目"""
    projects = crud.get_projects(db, skip=skip, limit=limit)
    return projects


@router.get("/get_cost/{r_id}")
async def get_cost(r_id: int, db: Session = Depends(dependencies.get_db)):
    """获取维修费用"""
    order = crud.get_order_by_rid(db, r_id=r_id)
    cost = 0
    if not order:   # 没有订单，返回403
        raise HTTPException(status_code=403, detail="该维修单还未派工！")
    for item in order:
        if item.status == 0:    # 有未完成订单，返回403
            raise HTTPException(status_code=403,detail="该维修任务未完成！")
        elif item.status == 1:  # 订单都完成，返回价格
            maintenance = crud.get_m_hour(db, m_id=item.m_id)
            cost += item.hour * maintenance.m_hour  # 所有工时费用
            pm = crud.get_pmaterial_by_pid(db, p_id=item.p_id)
            for pm_item in pm:
                m = crud.get_material_by_id(db, mt_id=pm_item.mt_id)
                cost += pm_item.num * m.mt_cost
    crud.update_cost(db, r_id, cost)
    return cost


@router.get("/get_project_by_pid/{p_id}", response_model=schemas.Project)
async def get_project_by_pid(p_id: int, db: Session = Depends(dependencies.get_db)):
    """根据pid查询项目信息"""
    db_project = crud.get_project_by_pid(db, p_id=p_id)
    return db_project


@router.get("/get_maintenance_by_id/{m_id}", response_model=schemas.User)
async def get_maintenance_by_id(m_id: int, db: Session = Depends(dependencies.get_db)):
    """根据mid查询维修员信息"""
    return crud.get_maintenance_by_id(db, id=m_id)


@router.get("/get_maintenances/", response_model=List[schemas.User])
async def get_maintenances(db: Session = Depends(dependencies.get_db)):
    """查询所有维修员的信息"""
    return crud.get_maintenances(db)
