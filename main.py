import uvicorn
from fastapi import FastAPI, HTTPException, status, Depends

import models, routers, dependencies
from database import engine

models.Base.metadata.create_all(bind=engine)  # 创建数据库表

app = FastAPI()

app.include_router(routers.login.router)
app.include_router(routers.users.router)
app.include_router(routers.salesmen.router)
app.include_router(routers.clients.router)
app.include_router(routers.vehicles.router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True, debug=True)
