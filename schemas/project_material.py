#!/usr/bin/python3.9
# @Time    : 2022/5/5 17:27
# @Author  : Cetacean
# @File    : project_material.py

from datetime import date, datetime
from pydantic import BaseModel
from schemas.material import Material


class PMaterialUpdate(BaseModel):
    num: int


class PMaterial(BaseModel):
    mt_id: int
    p_id: int
    num: int

    class Config:
        orm_mode = True


class PmMaterial(BaseModel):
    pm_material: Material

    class Config:
        orm_mode = True


class Project_PMaterialShow(BaseModel):
    p_id: int
    p_name: str

    class Config:
        orm_mode = True


class PMaterialShow(BaseModel):
    mt_id: int
    p_id: int
    num: int
    pm_material: Material
    pm_project: Project_PMaterialShow

    class Config:
        orm_mode = True