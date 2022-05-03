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
