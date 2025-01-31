from uuid import UUID
from fastapi_users import schemas

class UserRead(schemas.BaseUser[UUID]):
    telegram_id: str

class UserUpdate(schemas.BaseUserUpdate):
    telegram_id: str

class UserCreate(schemas.BaseUserCreate):
    telegram_id: str