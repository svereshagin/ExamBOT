from typing import Tuple

from aiogram.types import Message

from bot.app.logger.logger_file import logger
from bot.app.repositories.CRUD import student_exams
from bot.app.services.Exam.form_questions import FormExam, form_questions
from bot.app.services.selenium_parser.parcer import get_students_from_site


async def parsing_logic(message: Message, user_data: Tuple) -> None:
    try:
        logger.info("command_prepare_exam activated")
        await message.answer("Начало парсинга сайта")
        logger.info(
            f"Получено сообщение: {message.text} от пользователя: {message.from_user.id}"
        )

        students: list = get_students_from_site(user_data)
        logger.info(f"Успешно получено {len(students)} студентов из сайта.")
        await message.answer("Парсинг прошёл успешно")




        if student_exams.add_teacher(telegram_id=message.from_user.id):
            await message.answer("Вы были добавлены в БД")
        else:
            await message.answer("У вас уже есть аккаунт в базе, ученики будут прикреплены к"
                                 "существующей БД")

        form_questions.students = students
        form_exams: list[FormExam] = form_questions.form_groups()
        logger.info("Формирование групп для экзамена завершено.")

        try:
            logger.info(
                f"Добавление {len(students)} студентов и {len(form_exams)} экзаменов в БД."
            )
            await message.answer(f"Добавление {len(students)} студентов и {len(form_exams)} экзаменов в БД.")
            await student_exams.add_students(
                message.from_user.id, students=students, form_exams=form_exams, telegram_id=message.from_user.id
            )
            logger.info("Студенты успешно добавлены в БД")
            await message.answer(f"Общее количество студентов: {len(students)}")
        except Exception as e:
            logger.error(f"Ошибка при добавлении студентов в БД: {e}")
            await message.answer("Произошла ошибка при попытке добавления в БД")
    except Exception as e:
        logger.error(f"Ошибка при парсинге: {e}")
        await message.answer(
            "Ошибка при парсинге сайта. Проверьте доступность сервера и данные входа."
        )
