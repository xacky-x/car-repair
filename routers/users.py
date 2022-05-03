from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from typing import List
from datetime import timedelta

from dependencies import get_db
import crud, schemas, utils, dependencies

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(dependencies.verify_administrator)]
)


@router.get("/get_all_salesmen", response_model=List[schemas.User])
async def get_all_salesmen(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    salesmen = crud.get_salesmen(db, skip=skip, limit=limit)
    return salesmen
