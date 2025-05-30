from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from bot.app.config import settings
from aiogram.filters import Command
from aiogram.types import BotCommand
from bot.app.handlers.timer_handler import (
    command_start_timer,
    set_timer,
    command_stop_timer,
    TimerState,
)
from bot.app.handlers.timer_handler import router
from bot.app.handlers.main_handlers import startup_router as main_router
from bot.app.handlers.inline_keyboard_handlers import (
    router as inline_kb_router,
)
from bot.app.handlers.under_keyboard_handler import router as under_kb_router
from bot.app.handlers.data_collector_handler import router as data_collector_router

TOKEN = settings.TOKEN


dp = Dispatcher()
dp.callback_query.middleware(CallbackAnswerMiddleware())
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp.include_routers(main_router)
dp.include_router(router)
dp.include_router(inline_kb_router)
dp.include_router(under_kb_router)
dp.include_router(data_collector_router)


async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(command="menu", description="Показать главное меню"),
        BotCommand(
            command="prepare_exam",
            description="Подготовить экзамен, запуск перед командой /start_exam "
            "возвращает общее количество студентов",
        ),
        BotCommand(
            command="start_exam",
            description="Запустить процесс экзамена",  # исправлено имя команды
        ),
        BotCommand(
            command="students", description="Возвращение ведомостей по студентам"
        ),
        BotCommand(command="docs", description="Документация по работе с ботом"),
        BotCommand(command="start_timer", description="Запустить таймер"),
        BotCommand(command="stop_timer", description="Остановить таймер"),
    ]

    await bot.set_my_commands(commands)


dp.message.register(command_start_timer, Command("start_timer"))
dp.message.register(set_timer, TimerState.waiting_for_time)
dp.message.register(command_stop_timer, Command("stop_timer"))
dp.message.register(command_stop_timer, Command("skip"))

# добавить установку меню бота


__all__ = ["bot", "dp"]
