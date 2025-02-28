from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.app.config import settings
from bot.app.handlers.main_handlers import (
    command_start_handler,
    command_prepare_exam,
    command_start_exam,
    command_students,
    command_docs,
)
from aiogram.filters import CommandStart, Command
from aiogram.types import BotCommand


TOKEN = settings.TOKEN

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp.message.register(command_start_handler, CommandStart())
dp.message.register(command_prepare_exam, Command("prepare_exam"))
dp.message.register(command_start_exam, Command("command_start_exam"))
dp.message.register(command_students, Command("students"))
dp.message.register(command_docs, Command("docs"))


async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(
            command="prepare_exam",
            description="подготовить экзамен, запуск перед command_start_exam"
            "возвращает общее количество студентов",
        ),
        BotCommand(
            command="command_start_exam", description="Запустить процесс экзамена }"
        ),  # добавить в хендлер возможность принятия аргумента
        # число/mod
        # для создания разных режимов работы сервиса
        BotCommand(
            command="students", description="Возвращение ведомостей по студентам"
        ),
        BotCommand(command="docs", description="Документация по работе с ботом"),
    ]

    await bot.set_my_commands(commands)


# добавить установку меню бота


__all__ = ["bot"]
