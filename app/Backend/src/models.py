from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

from typing import Annotated

import datetime

intpk = Annotated[int, mapped_column(primary_key=True)]


class UserModel(Base):
    __tablename__ = "user"
    
    id: Mapped[intpk]
    full_name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]


class AdminModel(Base):
    __tablename__ = "admin"
    
    id: Mapped[intpk]
    full_name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    

class AccountModel(Base):
    __tablename__ = "account"
    
    id: Mapped[intpk]
    balance: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    

class TransactionModel(Base):
    __tablename__ = "transaction"
    
    id: Mapped[intpk]
    transaction_id: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id", ondelete="CASCADE"))
    amount: Mapped[int]
    signature: Mapped[str]
    accept_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))