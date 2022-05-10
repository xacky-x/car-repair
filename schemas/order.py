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
