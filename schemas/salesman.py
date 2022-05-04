#!/usr/bin/python3.9
# @Time    : 2022/5/4 14:19
# @Author  : Cetacean
# @File    : salesman.py
from typing import List, Optional

from pydantic import BaseModel


class RepairBase(BaseModel):
    r_type: str
    r_class: str
    payment: str
    mileage: float
    fuel: float
    failure: str
    completion_time: str
    date: str
    cost: float


class RepairCreate(RepairBase):
    pass


class Repair(RepairBase):
    s_id: int
    v_id: int
    r_id: int
