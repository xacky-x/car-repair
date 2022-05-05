from pydantic import BaseModel


class ProjectCreate(BaseModel):
    p_name:str


class Project(BaseModel):
    p_id: int
    p_name:str

    class Config:
        orm_mode = True