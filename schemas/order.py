from pydantic import BaseModel


class OrderCreate(BaseModel):
    r_id: int
    p_id: int
    hour: float
    status:int
    m_id: int


class Order(BaseModel):
    o_id: int
    r_id: int
    p_id: int
    hour: float
    status:int
    m_id: int

    class Config:
        orm_mode = True