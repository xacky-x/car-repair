#!/usr/bin/python3.9
# @Time    : 2022/5/5 17:25
# @Author  : Cetacean
# @File    : material.py.py

from pydantic import BaseModel


class MaterialBase(BaseModel):
    mt_name: str
    mt_cost: float


class MaterialCreate(MaterialBase):
    pass


class Material(MaterialBase):
    mt_id: int

    class Config:
        orm_mode = True
