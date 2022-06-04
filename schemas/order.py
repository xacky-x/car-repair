from datetime import datetime, date

from pydantic import BaseModel
from typing import Optional


class OrderCreate(BaseModel):
    r_id: int
    p_id: int
    hour: float
    status: int
    m_id: int


class Maintanence(BaseModel):
    name: str
    m_type: Optional[str] = None

    class Config:
        orm_mode = True


class Project(BaseModel):
    p_name: str

    class Config:
        orm_mode = True


class Repair(BaseModel):
    r_type: str
    r_class: str
    payment: str
    mileage: float
    fuel: float
    approach_time: datetime
    failure: str
    completion_time: date
    date: date
    v_id: int
    s_id: int

    class Config:
        orm_mode = True


class Order(BaseModel):
    o_id: int
    r_id: int
    p_id: int
    hour: float
    status: int
    m_id: int

    class Config:
        orm_mode = True


class OrderShow(Order):
    o_maintenance: Maintanence
    o_project: Project
    o_repair: Repair


class UpdateOrder(BaseModel):
    status: int

    class Config:
        orm_mode = True


