
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.app.config import settings
# from bot.app.handlers.main_handlers import (
#     # command_start_handler,
#     command_prepare_exam,
#     command_students,
#     command_docs,
# )
from aiogram.filters import CommandStart, Command
from aiogram.types import BotCommand
from bot.app.handlers.timer_handler import command_start_timer, set_timer, command_stop_timer, TimerState
from bot.app.handlers.timer_handler import router
from bot.app.handlers.main_handlers import router as main_router

TOKEN = settings.TOKEN

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# dp.message.register(command_start_handler, CommandStart())
# dp.message.register(command_prepare_exam, Command("prepare_exam"))
# # dp.message.register(command_start_exam, Command("command_start_exam"))
# dp.message.register(command_students, Command("students"))
# dp.message.register(command_docs, Command("docs"))

dp.include_routers(main_router)
dp.include_router(router)
async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(
            command="prepare_exam",
            description="Подготовить экзамен, запуск перед командой /start_exam "
                        "возвращает общее количество студентов",
        ),
        BotCommand(
            command="start_exam", description="Запустить процесс экзамена"  # исправлено имя команды
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

