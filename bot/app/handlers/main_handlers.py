from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message, CallbackQuery,
)

from bot.app.config import settings
from bot.app.text_for_handlers.main_handler_text_files import (
    CMD_START_HANDLER_TEXT,
)
from bot.app.logger.logger_file import logger
from bot.app.keyboards.Keyboard_Manager import Menu


startup_router = Router()


class MainMenu(StatesGroup):
    menu: State = State()



@startup_router.callback_query(F.data.in_(["menu"]))
async def process_menu(callback_query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(MainMenu.menu)


# Обработчик команды /start
@startup_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello! ExamBot version {settings.VERSION}")
    await message.answer(CMD_START_HANDLER_TEXT)
    await message.answer("Открыть главное меню?", reply_markup=Menu.inline_menu_button)


@startup_router.message(Command("menu"))
async def command_menu_handler(message: Message) -> None:
    await message.answer("__", reply_markup=Menu.reply_menu)
    await message.answer("Главное меню программы", reply_markup=Menu.inline_menu)
    logger.info("command_menu_handler activated")


@startup_router.message(MainMenu.menu)
async def getting_menu(message: Message, state: FSMContext) -> None:
    await message.answer("Главное меню программы", reply_markup=Menu.reply_menu)
    await message.answer("lower keyboard", reply_markup=Menu.inline_menu)
    logger.info("command_menu_handler activated")
