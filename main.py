import asyncio
from aiogram import Bot, Dispatcher

from handlers import user_commands
from scraper import fetch_top_cryptos
from data.database import initialize_db
from config import BOT_TOKEN, DB_PATH


async def main():
    await initialize_db(DB_PATH)

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.include_routers(
        user_commands.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)

    fetch_task = asyncio.create_task(fetch_top_cryptos())

    await dp.start_polling(bot)

    await fetch_task


if __name__ == "__main__":
    asyncio.run(main())
