from authx import AuthX, AuthXConfig

import os
from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv()

class Settings_DB(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    
    def get_db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    
settings = Settings_DB()

settings.DB_HOST = os.getenv('DB_HOST')
settings.DB_PORT = os.getenv('DB_PORT')
settings.DB_USER = os.getenv('DB_USER')
settings.DB_PASS = os.getenv('DB_PASS')
settings.DB_NAME = os.getenv('DB_NAME')


admin_auth_config = AuthXConfig()
admin_auth_config.JWT_SECRET_KEY = "ADMIN_SECRET_KEY"
admin_auth_config.JWT_ACCESS_COOKIE_NAME = "cookie_access_token"
admin_auth_config.JWT_ACCESS_CSRF_COOKIE_NAME = "csrf_access_token"
admin_auth_config.JWT_TOKEN_LOCATION = ["cookies"]
admin_auth_config.JWT_COOKIE_CSRF_PROTECT = False

admin_security = AuthX(config=admin_auth_config)


user_auth_config = AuthXConfig()
user_auth_config.JWT_SECRET_KEY = "USER_SECRET_KEY"
user_auth_config.JWT_ACCESS_COOKIE_NAME = "cookie_access_token"
user_auth_config.JWT_ACCESS_CSRF_COOKIE_NAME = "csrf_access_token"
user_auth_config.JWT_TOKEN_LOCATION = ["cookies"]
user_auth_config.JWT_COOKIE_CSRF_PROTECT = False

user_security = AuthX(config=user_auth_config)
