import logging
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command

from bot.config import BOT_TOKEN
from bot.handlers import check_imei, get_start


async def start():
    """Функция, запускающая работу бота."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.message.register(
        get_start,
        Command(commands=['start', 'run'])
    )

    dp.message.register(check_imei)
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
