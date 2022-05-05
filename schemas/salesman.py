#!/usr/bin/python3.9
# @Time    : 2022/5/4 14:19
# @Author  : Cetacean
# @File    : salesman.py
from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel


class RepairCreate(BaseModel):
    r_type: str
    r_class: str
    payment: str
    mileage: float
    fuel: float
    approach_time: datetime
    failure: str
    completion_time: date
    date: date
    cost: float
    v_id: int
    s_id: int


class RepairUpdate(BaseModel):
    r_type: Optional[str]
    r_class: Optional[str]
    payment: Optional[str]
    mileage: Optional[float]
    fuel: Optional[float]
    approach_time: Optional[datetime]
    failure: Optional[str]
    completion_time: Optional[date]
    date: Optional[date]
    cost: Optional[float]
    v_id: Optional[int]
    s_id: Optional[int]


class Repair(BaseModel):
    r_id: int
    r_type: str
    r_class: str
    payment: str
    mileage: float
    fuel: float
    approach_time: datetime
    failure: str
    completion_time: date
    date: date
    cost: float
    v_id: int
    s_id: int

    class Config:
        orm_mode = True
