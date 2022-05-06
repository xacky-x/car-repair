from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from datetime import timedelta

from dependencies import get_db
import crud, schemas, utils

router = APIRouter(
    prefix="/login",
    tags=["login"]
)


@router.post("", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """登录"""
    user = crud.authenticate_user(db, phone=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    sub = user.phone + "," + str(user.is_administrator) + "," + str(user.is_maintenance)
    access_token = utils.create_access_token(
        data={"sub": sub}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "is_administrator": user.is_administrator,
            "is_maintenance": user.is_maintenance}
