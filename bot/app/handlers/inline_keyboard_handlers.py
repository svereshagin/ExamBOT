from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.app.handlers.data_collector_handler import PrepareExam
from bot.app.logger.logger_file import logger
from bot.app.repositories.CRUD import student_exams
from bot.app.services.report import make_telegram_report, make_resulted_report
from bot.app.text_for_handlers.main_handler_text_files import (
    CMD_DOCS_HANDLER_TEXT,
)

router = Router()


@router.message(F.text == "Документация")
async def process_docs(message: Message) -> None:
    await message.answer(CMD_DOCS_HANDLER_TEXT)
    logger.info("command_docs activated")


@router.message(F.text == "Подготовка экзамена")
async def process_prep_exam(message: Message, state: FSMContext) -> None:
    await state.set_state(PrepareExam.login)
    await message.answer("Введите логин")


@router.message(F.text == "Получить ведомости")
async def process_get_reports(message: Message) -> None:
    await message.answer("Загрузка ведомостей...")
    data = await student_exams.get_report()
    formatted_data = make_telegram_report(make_resulted_report(data))
    logger.info("process_get_reports")
    for elem in formatted_data:
        await message.answer(elem)


@router.message(F.text == "Очистить БД")
async def process_clear_db(message: Message) -> None:
    result = await student_exams.delete_all_students_for_teacher_by_telegram_id(telegram_id=message.from_user.id)
    await message.answer(f"{result['success']}\n{result['message']}")


@router.message(F.text == "Выключить клавиатуру")
async def process_remove_keyboard(message: Message) -> None:
    """Скрывает нижнюю клавиатуру."""
    await message.answer("Клавиатура скрыта.", reply_markup=ReplyKeyboardRemove())
