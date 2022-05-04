from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from typing import List
from datetime import timedelta

from dependencies import get_db
import crud, schemas, utils

router = APIRouter(
    prefix="/clients",
    tags=["clients"]
)


@router.get("/get_by_id/{c_id}", response_model=schemas.Client)
async def get_client(c_id: int, db: Session = Depends(get_db)):
    db_client = crud.get_client_by_id(db, c_id=c_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client
