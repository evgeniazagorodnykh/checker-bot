from typing import Optional
from fastapi import Depends, HTTPException
from fastapi_users.manager import BaseUserManager, UserManagerDependency
from fastapi_users import UUIDIDMixin
from uuid import UUID
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.future import select
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas
from sqlalchemy.ext.asyncio import AsyncSession


from src.database import get_async_session, async_session_maker
from src.models import User


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    async def get_by_telegram_id(self, telegram_id: str) -> Optional[User]:
        async with async_session_maker() as session:  # Открываем сессию здесь
            query = select(User).where(User.telegram_id == telegram_id)
            result = await session.execute(query)
            user = result.scalars().first()
            return user

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)