import uvicorn
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware

import models, routers, dependencies
from database import engine

models.Base.metadata.create_all(bind=engine)  # 创建数据库表

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.create_data.router)
app.include_router(routers.login.router)
app.include_router(routers.users.router)
app.include_router(routers.salesman.router)
app.include_router(routers.maintenance.router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8090, reload=True, debug=True)
