import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from supabase import Client, create_client

from config_reader import config

# from handlers import admin_console, all_events, common, today, tomorrow
from handlers import admin_console, all_events, common, free_events, today

supabase: Client = create_client(config.supabase_url, config.supabase_key)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(
        config.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    dp.include_routers(
        common.router,
        admin_console.router,
        all_events.router,
        today.router,
        # tomorrow.router,
        free_events.router,
    )

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
