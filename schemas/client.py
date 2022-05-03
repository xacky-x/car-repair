from typing import List, Optional
from schemas.vehicle import *

from pydantic import BaseModel


class ClientCreate(BaseModel):
    c_name: str
    c_p: str
    discount: Optional[float] = None
    contact: str
    phone: str


class Client(BaseModel):
    c_id: int
    c_name: str
    c_p: str
    discount: Optional[float] = None
    contact: str
    phone: str
    vehicles: List[Vehicle] = []

    class Config:
        orm_mode = True
