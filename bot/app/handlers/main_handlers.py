from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
)

from bot.app.config import settings
from bot.app.text_for_handlers.main_handler_text_files import (
    CMD_START_HANDLER_TEXT,
)
from bot.app.logger.logger_file import logger
from bot.app.keyboards.Keyboard_Manager import Menu


startup_router = Router()


# Обработчик команды /start
@startup_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Как подавать котлеты?", reply_markup=Menu.reply_menu)
    await message.answer("lower keyboard", reply_markup=Menu.inline_menu)
    logger.info("command_start_handler activated")
    await message.answer(f"Hello! ExamBot version {settings.VERSION}")
    await message.answer(CMD_START_HANDLER_TEXT)
