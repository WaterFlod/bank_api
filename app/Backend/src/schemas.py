from pydantic import BaseModel, Field, EmailStr


class AdminDTO(BaseModel):
    id: int = Field(..., gt=0, description="Id Админа")
    full_name: str = Field(..., max_length=100, description="Имя и Фамилия Админа")
    email: EmailStr = Field(..., description="Email Админа")
    password: str = Field(..., min_length=4, max_length=20, description="Пароль Админа")


class UserSchema(BaseModel):
    full_name: str = Field(..., max_length=100, description="Имя и Фамилия Пользователя")
    email: EmailStr = Field(..., description="Email Пользователя")
    password: str = Field(..., min_length=4, max_length=20, description="Пароль Пользователя")
    

class UserDTO(UserSchema):
    id: int = Field(..., gt=0, description="Id Пользователя")


class AccountSchema(BaseModel):
    user_id: int = Field(..., gt=0, description="Id Пользователя")
    balance: int = Field(..., ge=0, description="Баланс счёта Пользователя")


class AccountDTO(AccountSchema):
    id: int = Field(..., gt=0, description="Id счёта Пользователя")

    
class TransactionSchema(BaseModel):
    transaction_id: str = Field(..., description="Id транзакции от стороннего сервиса")
    user_id: int = Field(..., gt=0, description="Id Пользователя")
    account_id: int = Field(..., gt=0, description="Id счёта Пользователя")
    amount: int = Field(..., ge=0, description="Сумма платежа")
    signature: str = Field(..., description="Уникальная подпись транзакции")


class TransactionDTO(TransactionSchema):
    id: int = Field(..., gt=0, description="Id транзакции")

    
class LoginSchema(BaseModel):
    email: EmailStr = Field(..., description="Email для авторизации")
    password: str = Field(..., min_length=4, max_length=20, description="Пароль для авторизации")

    