import aiohttp
from sqlalchemy import select
from aiogram import Bot
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from aiogram import types

from bot.config import APP_URL
from src.models import User
from src.database import async_session_maker


async def get_user_token(user_id: int) -> str:
    """Получает токен для пользователя по его Telegram ID"""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{APP_URL}auth/token/telegram?telegram_id={user_id}"
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("access_token")
            else:
                return None


async def get_start(message: Message, bot: Bot):
    """Приветствие."""

    await message.answer(
        f'Привет, {message.from_user.first_name}!\n'
        'Я бот для проверки IMEI устройств\n'
        'Введите IMEI для проверки.\n',
        parse_mode='HTML'
    )


async def check_imei(message: types.Message):
    token = await get_user_token(message.from_user.id)
    if not token:
        await message.answer("Ошибка авторизации. Попробуйте позже.")
        return
    
    print(token)

    imei = message.text.strip()
    if len(imei) != 15 or not imei.isdigit():
        await message.answer("Неверный формат IMEI. Введите 15-значный номер.")
        return

    async with aiohttp.ClientSession() as session:
        print("Authorization", f"Bearer {token}")
        async with session.post(
            f"{APP_URL}api/check-imei?imei={imei}", 
            headers={
            "Authorization": f"Bearer {token}"
            },
        ) as resp:
            if resp.status == 200:
                data = await resp.json()

                imei_status = data.get("status", "неизвестно")
                device_name = data.get("deviceName", "неизвестно")
                country = data.get("purchaseCountry", "неизвестно")
                fmi_on = "Включен" if data.get("fmiOn") else "Выключен"
                lost_mode = "Да" if data.get("lostMode") else "Нет"
                
                response_text = (
                    f"📱 *Информация об устройстве:*\n"
                    f"🔹 *IMEI:* `{imei}`\n"
                    f"🔹 *Статус:* `{imei_status}`\n"
                    f"🔹 *Модель:* `{device_name}`\n"
                    f"🔹 *Страна покупки:* `{country}`\n"
                    f"🔹 *Find My iPhone:* `{fmi_on}`\n"
                    f"🔹 *Режим утери:* `{lost_mode}`"
                )
                
                await message.answer(response_text, parse_mode=ParseMode.MARKDOWN)
            else:
                await message.answer("Ошибка при проверке IMEI. Попробуйте позже.")
