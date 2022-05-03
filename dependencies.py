from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt

from database import SessionLocal

import schemas, utils, crud


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_token(token: str = Depends(utils.oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
        sub: str = payload.get("sub")
        if sub is None:
            raise credentials_exception
        return sub
    except JWTError:
        raise credentials_exception


def verify_administrator(sub: str = Depends(verify_token)):
    is_administrator = sub.split(',')[1]
    if is_administrator == 'False':
        raise HTTPException(status_code=401, detail="非管理员权限")


def verify_salesman(sub: str = Depends(verify_token)):
    is_maintenance = sub.split(',')[2]
    if is_maintenance == 'True':
        raise HTTPException(status_code=401, detail="非业务员权限")


def verify_maintenance(sub: str = Depends(verify_token)):
    is_maintenance = sub.split(',')[2]
    if is_maintenance == 'False':
        raise HTTPException(status_code=401, detail="非维修员权限")


if __name__ == '__main__':
    verify_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMzc0ODU1ODg0MixGYWxzZSxGYWxzZSIsImV4cCI6MTY1MTU0NTM5NH0.BuXCJ7M3TrYukWN0OkdeUFXGfOkZ6AYdy2D_5Y8cajg")

