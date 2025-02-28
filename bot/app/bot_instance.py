from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.app.config import settings
from bot.app.handlers.main_handlers import (
    command_start_handler, command_prepare_exam,
    command_start_exam, command_students, command_docs)

TOKEN = settings.TOKEN


dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp.register_message_handler(command_start_handler, commands=["start"])
dp.register_message_handler(command_prepare_exam, commands=["prepare_exam"])
dp.register_message_handler(command_start_exam, commands=["command_start_exam"])
dp.register_message_handler(command_students, commands=["students"])
dp.register_message_handler(command_docs, commands=["docs"])


#добавить установку меню бота


__all__ = ["bot"]
