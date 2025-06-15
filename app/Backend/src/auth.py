import asyncio

from fastapi import APIRouter, HTTPException, Response, Depends

from typing import Annotated

from config import admin_security, user_security, admin_auth_config, user_auth_config

from schemas import LoginSchema, UserDTO, AdminDTO

from database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from models import UserModel, AdminModel
from sqlalchemy import select

router = APIRouter(prefix="/authentication", tags=["Аутентификация"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post("/", summary="Авторизация")
async def auth(creds:LoginSchema, response: Response, session: SessionDep):
    query = select(UserModel)
    result = await session.execute(query) 
    users = result.scalars().all()
    result_dto = [UserDTO.model_validate(row, from_attributes=True) for row in users]
    for user in result_dto:
        if creds.email == user.email and creds.password == user.password:
            token = user_security.create_access_token(uid=str(user.id))
            response.set_cookie(user_auth_config.JWT_ACCESS_COOKIE_NAME, token)
            return {"access_token": token}
    query = select(AdminModel)
    result = await session.execute(query)
    admins = result.scalars().all()
    result_dto = [AdminDTO.model_validate(row, from_attributes=True) for row in admins]
    for admin in result_dto:
        if creds.email == admin.email and creds.password == admin.password:
            token = admin_security.create_access_token(uid=str(admin.id))
            response.set_cookie(admin_auth_config.JWT_ACCESS_COOKIE_NAME, token)
            return {"access_token": token}
    raise HTTPException(status_code=401, detail="Некорректно введённые данные")


