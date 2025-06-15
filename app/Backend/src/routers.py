import os 
import sys 
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from fastapi import APIRouter, Depends, HTTPException
from authx import TokenPayload

from typing import Annotated

import asyncio

from schemas import UserSchema, UserDTO, AccountDTO, TransactionSchema, AdminDTO, TransactionDTO

from config import admin_security, user_security
from utils import hash, get_accounts, get_transactions

from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models import UserModel, AccountModel, TransactionModel, AdminModel
from sqlalchemy import select, delete, update

router_admin = APIRouter(prefix="/admin", tags=["API админа"])
router_user = APIRouter(prefix="/users", tags=["API пользователя"])


AdminDep = Depends(admin_security.access_token_required)
UserDep = Depends(user_security.access_token_required)


SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router_admin.get("/personal_information", summary="Получить данные о себе")
async def get_personal_information(session: SessionDep, payload: TokenPayload = AdminDep):
    query = select(AdminModel)
    result = await session.execute(query)
    admins = result.scalars().all()
    result_dto = [AdminDTO.model_validate(row, from_attributes=True) for row in admins]
    for admin in result_dto:
        if admin.id == int(payload.sub):
            return admin

@router_admin.post("/create_user", summary="Создать пользователя")
async def create_user(session: SessionDep, data: UserSchema):
    new_user = UserModel(
        full_name=data.full_name,
        email=data.email,
        password=data.password,
    )
    session.add(new_user)
    await session.commit()  
    return {"access": "True", "detail": "Пользователь успешно создан"}
    


@router_admin.post("/update_user", summary="Обновить пользователя")
async def update_user(session: SessionDep, data: UserDTO):
    query = select(UserModel)
    result = await session.execute(query) 
    users = result.scalars().all()
    result_dto = [UserDTO.model_validate(row, from_attributes=True) for row in users]
    for user in result_dto:
        if user.id == data.id:
            update_user = (update(UserModel).where(UserModel.id == data.id).values(full_name=data.full_name, email=data.email, password=data.password))
            await session.execute(update_user)
            await session.commit()
            return {"succes": "True", "detail": "Пользователь успешно обновлён"}
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@router_admin.get("/get_users", summary="Получить всех пользователей")
async def get_all_users(session:SessionDep):
    query = select(UserModel)
    result = await session.execute(query) 
    users = result.scalars().all()
    return users       


@router_admin.get("/get_users/{id}", summary="Получить пользователя и его счета по id пользователя")
async def get_user(session:SessionDep, id: int):
    users = query = select(UserModel)
    result = await session.execute(query) 
    users = result.scalars().all()
    accounts = query = select(AccountModel)
    result = await session.execute(query) 
    accounts = result.scalars().all()
    query = select(TransactionModel)
    result = await session.execute(query) 
    transactions = result.scalars().all()
    result_dto = [UserDTO.model_validate(row, from_attributes=True) for row in users]
    user_data = dict()
    for user in result_dto:
        if user.id == id:
            user_data["user"] = {
                "full_name": user.full_name,
                "email": user.email,
                "password": user.password,
            }
            account_data = [AccountDTO.model_validate(row, from_attributes=True) for row in accounts]
            user_data["accounts"] = get_accounts(account_data, id)
            transaction_data = [TransactionDTO.model_validate(row, from_attributes=True) for row in transactions]
            user_data["transactions"] = get_transactions(transaction_data, id)
            return user_data
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@router_admin.delete("/delete_user", summary="Удалить пользователя")
async def delete_user(session: SessionDep, id: int):
    users = query = select(UserModel)
    result = await session.execute(query) 
    users = result.scalars().all()
    result_dto = [UserDTO.model_validate(row, from_attributes=True) for row in users]
    for user in result_dto:
        if user.id == id:
            del_user = (delete(UserModel).where(UserModel.id == id.id))
            await session.execute(del_user)
            await session.commit()   
            return {"succes": "True", "detail": "Пользователь успешно удалён"}
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@router_user.get("/personal_information", summary="Получить данные о себе")
async def get_personal_information(session:SessionDep, payload: TokenPayload = UserDep):
    query = select(UserModel)
    result = await session.execute(query) 
    users = result.scalars().all()
    result_dto = [UserDTO.model_validate(row, from_attributes=True) for row in users]
    for user in result_dto:
        if user.id == int(payload.sub):
            return {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "password": user.password,
            }


@router_user.post("/open_account", summary="Открыть новый счёт")
async def open_account(session: SessionDep, payload: TokenPayload = UserDep):
    new_account = AccountModel(
        user_id=payload.sub,
        balance=0,
    )
    session.add(new_account)
    await session.commit()
    return {"succes": "True"}


@router_user.get("/accounts", summary="Получить все счета")
async def get_all_accounts(session: SessionDep, payload: TokenPayload = UserDep):
    query = select(AccountModel)
    result = await session.execute(query) 
    accounts = result.scalars().all()
    result_dto = [AccountDTO.model_validate(row, from_attributes=True) for row in accounts]
    accounts = get_accounts(result_dto, int(payload.sub))
    if len(accounts) != 0:
        return accounts
    raise HTTPException(status_code=404, detail="Счета не найдены")


@router_user.post("/transactions", summary="Произвести платёж")
async def transaction(session:SessionDep, data: TransactionSchema):
    if data.signature == hash(data.account_id, data.amount, data.transaction_id, data.user_id):
        query = select(AccountModel)
        result = await session.execute(query) 
        accounts = result.scalars().all()
        result_dto = [AccountDTO.model_validate(row, from_attributes=True) for row in accounts]
        flag = False
        for account in result_dto:
            if account.id == data.account_id:
                flag = True
        if not flag: open_account()
        
        flag = True
        query = select(TransactionModel)
        result = await session.execute(query) 
        transactions = result.scalars().all()
        result_dto = [TransactionDTO.model_validate(row, from_attributes=True) for row in transactions]
        for transaction in result_dto:
            if transaction.transaction_id == data.transaction_id:
                flag = False
        if not flag:
            raise HTTPException(status_code=400, detail="Транзакция прошла ранее")
        
        new_transaction = TransactionModel(
            transaction_id=str(data.transaction_id),
            user_id=data.user_id,
            account_id=data.account_id,
            amount=data.amount,
            signature=data.signature,
        )
        session.add(new_transaction)
        update_account = update(AccountModel).where(AccountModel.id == data.account_id).values(balance=data.amount+AccountModel.balance)
        await session.execute(update_account)
        await session.commit()   
        return {"succes": "True"}
    
    raise HTTPException(status_code=402, detail="Транзакция не прошла")

    
@router_user.get("/transactions/get_all", summary="Получить список платежей")
async def get_all_transactions(session:SessionDep, payload: TokenPayload = UserDep): 
    query = select(TransactionModel)
    result = await session.execute(query) 
    transactions = result.scalars().all()
    resultDTO = [TransactionDTO.model_validate(row, from_attributes=True) for row in transactions]
    transactions = get_transactions(resultDTO, int(payload.sub))
    if len(transactions) != 0:
        return transactions
    raise HTTPException(status_code=404, detail="Платежи не найдены")
