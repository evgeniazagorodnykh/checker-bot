from uuid import UUID
from fastapi import Depends, FastAPI, HTTPException
from fastapi_users.authentication import JWTStrategy
from fastapi_users import FastAPIUsers

from src.manager import UserManager, get_user_manager
from src.models import User
from src.router import router as router_api 
from src.auth import auth_backend, fastapi_users
from src.schemas import UserCreate, UserRead, UserUpdate
from src.config import SECRET_KEY


app = FastAPI(
    title="Telegram Bot IMEI"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

@app.post("/auth/token/telegram")
async def get_token_by_telegram_id(
    telegram_id: str, 
    user_manager: UserManager = Depends(get_user_manager)
):
    user = await user_manager.get_by_telegram_id(telegram_id)

    if not user:
        print("Пользователь не найден")
        raise HTTPException(status_code=404, detail="User not found")

    jwt_strategy = JWTStrategy(secret=SECRET_KEY, lifetime_seconds=3600)
    token = await jwt_strategy.write_token(user)

    return {"access_token": token, "token_type": "bearer"}

app.include_router(router_api)
