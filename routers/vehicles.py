from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from typing import List

from dependencies import get_db
import crud, schemas

router = APIRouter(
    prefix="/vehicles",
    tags=["vehicles"]
)


@router.get("/get_all", response_model=List[schemas.Vehicle])
async def get_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vehicles = crud.get_vehicles(db, skip=skip, limit=limit)
    return vehicles

@router.post("/create_random", response_model=List[schemas.Vehicle])
async def create_vehicle_random(num: int, db: Session = Depends(get_db)):
    return crud.create_random_vehicle(db=db, num=num)