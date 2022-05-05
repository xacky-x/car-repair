#!/usr/bin/python3.9
# @Time    : 2022/5/4 14:19
# @Author  : Cetacean
# @File    : repair.py
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
