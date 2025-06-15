from fastapi import FastAPI
import uvicorn

import asyncio

from routers import router_admin, router_user

from auth import router as router_login

from database import Base, engine 


app = FastAPI()


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)



app.include_router(router_login)
app.include_router(router_admin)
app.include_router(router_user)


if __name__ == '__main__':
    
    # asyncio.run(init_models())
    
    uvicorn.run("main:app", log_level="info",host="0.0.0.0", reload=True)
    
