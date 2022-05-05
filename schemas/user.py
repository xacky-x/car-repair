from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    phone: str
    password: str
    name: str
    m_type: Optional[str] = None
    m_hour: Optional[float] = None
    is_administrator: bool
    is_maintenance: bool


class SalesmanCreate(BaseModel):
    phone: str
    password: str
    name: str


class MaintenanceCreate(BaseModel):
    phone: str
    password: str
    name: str
    m_type: str
    m_hour: str


class User(BaseModel):
    id: int
    name: str
    phone: str
    m_type: Optional[str] = None
    m_hour: Optional[float] = None
    is_administrator: bool
    is_maintenance: bool

    class Config:
        orm_mode = True
