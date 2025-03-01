import asyncio
from typing import List

from aiogram import Bot, Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.app.logger.logger_file import logger
from bot.app.repositories.models import Student
from bot.app.services.Exam.timer import ExamTimerPreparations

active_timers = {}
router = Router()


class TimerState(StatesGroup):
    waiting_for_time = State()


def log_and_respond(message: Message, text: str):
    logger.info(f"Chat {message.chat.id}: {text}")
    return message.answer(text)


@router.message(F.text == "/start_exam")
async def command_start_timer(message: Message, state: FSMContext):
    """Запуск режима экзамена"""
    text = (
        "Возможные режимы работы:\n"
        "1. Ввод времени на подготовку (в минутах) и общего времени экзамена.\n"
        "2. Ввод времени на подготовку (в минутах) и времени на одного студента.\n"
        "Пример 1: 10 90 - где 10 минут на подготовку и 90 минут на экзамен.\n"
        "Пример 2: 0 5 - где 0 минут на подготовку и 5 минут на одного студента."
    )
    await log_and_respond(message, text)
    await message.answer("⏳ Введите параметры таймера (например, '10 90'):")
    await state.set_state(TimerState.waiting_for_time)


@router.message(TimerState.waiting_for_time)
async def set_timer(message: Message, state: FSMContext, bot: Bot):
    """Устанавливает таймер после ввода времени пользователем"""
    try:
        args = message.text.split()
        if len(args) != 2 or not all(arg.isdigit() for arg in args):
            await message.answer("🚫 Ошибка: Введите два числа через пробел (например, '10 90').")
            return

        arg, arg2 = map(int, args)
        res = ExamTimerPreparations(mode1=(arg, arg2))

        try:
            text, res_data = await res.resulted_timer()
        except Exception as e:
            logger.error(f"Ошибка в resulted_timer: {str(e)}")
            await message.answer("⚠ Произошла ошибка при вычислении таймера. Проверьте данные и попробуйте ещё раз.")
            return

        chat_id = message.chat.id

        # Проверяем, не запущен ли уже таймер
        if chat_id in active_timers:
            active_timers[chat_id].cancel()

        # Запускаем новый таймер
        task = asyncio.create_task(countdown_timer(chat_id, res_data, bot))
        active_timers[chat_id] = task

        await log_and_respond(message, f"✅ Таймер на {res_data[0]} минут запущен! Удачи на экзамене!")
        await state.clear()
    except Exception as e:
        logger.error(f"Ошибка установки таймера: {str(e)}")
        await log_and_respond(message, "⚠ Произошла ошибка. Попробуйте ещё раз.")


async def countdown_timer(chat_id: int, res: tuple[int, int, int, int, list], bot: Bot):
    """Асинхронный таймер экзамена"""
    exam_time, student_time, preparation_time, num_students, students = res
    student_time *= 60  # Перевод в секунды

    active_timers[chat_id] = True

    if preparation_time > 0:
        await send_preparation_messages(chat_id, preparation_time, bot)

    await bot.send_message(chat_id, "⏳ Подготовка завершена. Начинаем экзамен!")
    await send_exam_messages(chat_id, students, student_time, bot)

    active_timers.pop(chat_id, None)
    await bot.send_message(chat_id, "✅ Экзамен завершен!")


async def send_preparation_messages(chat_id: int, preparation_time: int, bot: Bot):
    """Отправка сообщений о ходе подготовки"""
    await bot.send_message(chat_id, f"⏳ Начинаем подготовку! Время: {preparation_time} минут.")
    await asyncio.sleep(preparation_time * 60)


async def send_exam_messages(chat_id: int, students: List[Student], student_time: int, bot: Bot):
    """Процесс экзамена для каждого студента"""
    for student in students:
        if chat_id not in active_timers:
            return
        await bot.send_message(chat_id, f"🎓 Время для студента: {student.surname}. Начинаем!")
        await asyncio.sleep(student_time)
        await bot.send_message(chat_id, f"🚀 Время для {student.surname} вышло!")


@router.message(F.text == "/stop_exam")
async def command_stop_timer(message: Message):
    """Останавливает таймер"""
    chat_id = message.chat.id
    if chat_id in active_timers:
        try:
            del active_timers[chat_id]
            await log_and_respond(message, "🛑 Таймер остановлен!")
        except Exception as e:
            await log_and_respond(message, "🛑 Ошибка остановки таймера")
    else:
        await log_and_respond(message, "⚠ У вас нет активного таймера.")
