from pydantic import BaseModel


class VehicleCreate(BaseModel):
    license: str
    v_type: str
    colour: str
    v_class: str


class Vehicle(BaseModel):
    v_id: int
    license: str
    v_type: str
    colour: str
    v_class: str
    c_id: int

    class Config:
        orm_mode = True
