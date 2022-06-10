import asyncio
import logging

from aiogram import Bot, F
from aiogram.types import BotCommand
from coursebot.apps.bot.handlers.admin import register_admin_handlers
from coursebot.apps.bot.handlers.common import register_common
from coursebot.apps.bot.handlers.common.quiz import register_quiz
from coursebot.apps.bot.handlers.common.registration import register_registration
from coursebot.apps.bot.handlers.errors.errors_handlers import register_error
from coursebot.apps.bot.middleware.bot_middleware import BotMiddleware
from coursebot.apps.bot.utils import start_up_message
from coursebot.config.logg_settings_new import init_logging
from coursebot.db import init_db
from coursebot.db.utils.backup import making_backup
from coursebot.loader import bot, dp, scheduler


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Главное меню"),
        BotCommand(command="/admin", description="Админ меню"),
    ]
    await bot.set_my_commands(commands)


async def start():
    # Настройка логирования
    init_logging(
        level="TRACE",
        steaming=True,
        write=True,
    )

    dp.startup.register(start_up_message)
    # dp.shutdown.register(on_shutdown)

    # Установка команд бота
    await set_commands(bot)
    dp.message.filter(F.chat.type == "private")
    # Инициализация бд
    await init_db()

    # Меню админа
    register_admin_handlers(dp)

    # Регистрация хэндлеров
    register_common(dp)
    register_registration(dp)
    register_quiz(dp)
    register_error(dp)

    # Регистрация middleware
    # middleware = BotMiddleware()
    # dp.message.outer_middleware(middleware)
    # dp.callback_query.outer_middleware(middleware)

    # Регистрация фильтров

    scheduler.add_job(making_backup, "interval", hours=1)
    scheduler.start()
    await dp.start_polling(bot, skip_updates=True)


def main():
    asyncio.run(start())


if __name__ == "__main__":
    main()
