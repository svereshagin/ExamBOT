from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.app.handlers.data_collector_handler import PrepareExam

router = Router()


@router.callback_query(F.data.in_(["docs"]))
async def process_docs(callback_query: CallbackQuery) -> None:
    from bot.app.bot_instance import bot

    await bot.delete_message(
        callback_query.message.chat.id, callback_query.message.message_id
    )
    await callback_query.answer("Docs")
    await callback_query.message.answer("the docs")


@router.callback_query(F.data.in_(["prep_exam"]))
async def process_docs(callback_query: CallbackQuery, state: FSMContext) -> None:
    from bot.app.bot_instance import bot

    await bot.delete_message(
        callback_query.message.chat.id, callback_query.message.message_id
    )
    await state.set_state(PrepareExam.login)
    await callback_query.message.answer("Введите логин")

@router.callback_query(F.data.in_(["start_exam"]))
async def process_docs(callback_query: CallbackQuery) -> None:
    from bot.app.bot_instance import bot

    await bot.delete_message(
        callback_query.message.chat.id, callback_query.message.message_id
    )
    await callback_query.answer("Docs")
    await callback_query.message.answer("the docs")


@router.callback_query(F.data.in_(["get_reports"]))
async def process_docs(callback_query: CallbackQuery) -> None:
    from bot.app.bot_instance import bot

    await bot.delete_message(
        callback_query.message.chat.id, callback_query.message.message_id
    )
    await callback_query.answer("get_reports")
    await callback_query.message.answer("the docs")


@router.callback_query(F.data.in_(["activate_menu_keyboard"]))
async def process_docs(callback_query: CallbackQuery) -> None:
    from bot.app.bot_instance import bot

    await bot.delete_message(
        callback_query.message.chat.id, callback_query.message.message_id
    )
    await callback_query.answer("Docs")
    await callback_query.message.answer("the docs")


@router.callback_query(F.data.in_(["clear_db"]))
async def command_clear_db(callback: CallbackQuery):
    # Логика для очистки БД
    await callback.message.answer("База данных очищена")
