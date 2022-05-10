from typing import List

from pydantic import BaseModel
from schemas.project_material import PmMaterial


class ProjectCreate(BaseModel):
    p_name: str


class Project(BaseModel):
    p_id: int
    p_name: str

    class Config:
        orm_mode = True


class ProjectShow(BaseModel):
    p_id: int
    p_name: str
    p_pm: List[PmMaterial] = []

    class Config:
        orm_mode = True
