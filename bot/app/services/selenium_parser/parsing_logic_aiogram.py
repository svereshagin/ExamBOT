import asyncio
from typing import Tuple
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from bot.app.logger.logger_file import logger
from bot.app.repositories.CRUD import student_exams
from bot.app.services.Exam.form_questions import FormExam, form_questions
from bot.app.services.selenium_parser.parcer import get_students_from_site


async def fetch_students(user_data: Tuple) -> list:
    """Функция для парсинга студентов с сайта."""
    logger.info("Запуск парсинга сайта")
    return await asyncio.to_thread(get_students_from_site, user_data)


async def add_teacher_to_db(telegram_id: int) -> None:
    """Функция для добавления учителя в БД."""
    logger.info("Добавление учителя в БД")
    await student_exams.add_teacher(telegram_id=telegram_id)


async def add_students_to_db(students: list, form_exams: list[FormExam], telegram_id: int) -> None:
    """Функция для добавления студентов и экзаменов в БД."""
    logger.info(f"Добавление {len(students)} студентов и {len(form_exams)} экзаменов в БД")
    await student_exams.add_students(students=students, form_exams=form_exams, telegram_id=telegram_id)


async def parsing_logic(message: Message, user_data: Tuple) -> None:
    try:
        logger.info("command_prepare_exam activated")
        await message.answer("Начало парсинга сайта")
        logger.info(f"Получено сообщение: {message.text} от пользователя: {message.from_user.id}")

        # Запускаем парсинг в фоне
        students_task = asyncio.create_task(fetch_students(user_data))
        teacher_task = asyncio.create_task(add_teacher_to_db(message.from_user.id))

        students = await students_task  # Ждём завершения парсинга

        if not students:
            logger.warning("Парсинг завершён, но студентов не найдено.")
            await message.answer("Парсинг завершён, но студентов не найдено.")
            return

        logger.info(f"Успешно получено {len(students)} студентов из сайта.")
        await message.answer("Парсинг прошёл успешно")

        await teacher_task  # Дожидаемся добавления учителя в БД
        logger.info("Учитель успешно добавлен в БД")

        # Формирование вопросов – выполняется в основном потоке
        form_questions.students = students
        form_exams = form_questions.form_groups()
        logger.info("Формирование вопросов завершено.")

        # Запускаем добавление студентов в БД в фоне
        add_students_task = asyncio.create_task(
            add_students_to_db(students, form_exams, message.from_user.id)
        )

        await message.answer(f"Общее количество студентов: {len(students)}")
        await add_students_task  # Ждём завершения добавления в БД

        logger.info("Студенты успешно добавлены в БД")
        await message.answer("Все данные успешно добавлены!")

    except TelegramBadRequest as e:
        logger.error(f"Ошибка отправки сообщения: {e}")
    except Exception as e:
        logger.error(f"Ошибка при выполнении парсинга: {e}")
        await message.answer("Ошибка при парсинге сайта. Проверьте доступность сервера и данные входа.")
