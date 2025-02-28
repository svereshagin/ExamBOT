from aiogram.types import Message
from pydantic.v1.class_validators import all_kwargs
from sqlalchemy import ScalarResult

from bot.app.config import settings
from bot.app.services.report import make_resulted_report, make_telegram_report
from bot.app.services.selenium_parser.parcer import get_students_from_site
from bot.app.repositories.models import Student
from bot.app.services.Exam.form_questions import form_questions
from bot.app.repositories.CRUD import student_exams



async def command_start_handler(message: Message) -> None:
    """Returns True if the bot is running else False."""
    await message.answer(f"Hello! ExamBot version {settings.VERSION}")
    await message.answer(f"Run /command_prepare_exam to get the students out of API cite\n"
                         f"Don't forget to insert your credentials into .env file\n"
                         f"And provide links into bot/yml_files/links in .yml format"
                         f"Good luck with the exam")

async def command_prepare_exam(message: Message) -> None:
    """начало парсинга команда для бизнес логики"""
    try:
        await message.answer('Начало парсинга сайта')
        students = get_students_from_site()
        await message.answer('Операция совершенна успешно')
        await message.answer("Общее количество студентов: "+str(len(students)))
        form_questions.students = students
        form_exams = form_questions.form_groups()
        try:
            await student_exams.create_students(students=students,form_exams=form_exams)
        except Exception as e:
            print(e)
    except Exception as e:
        await message.answer('Ошибка')
        await message.answer(str(e))





async def command_start_exam(message: Message) -> None:
    """
    Основной класс для начала экзамена
    активирует таймер через класс, msg должен перехватывать мод для
    таймера
    """


async def command_students(message: Message) -> None:
    """Отсылает ведомость по ученикам:
    подключается к БД, берёт данные из неё
    отсылает в виде:
        surname: asda
        mark: 0
        turn: 0
        examination_paper: 1

    также стоит настроить на клв сдавших на 5/4/3 и не сдавших для ведомостей.
    """

    data = await student_exams.get_report()
    data = make_telegram_report(make_resulted_report(data))
    for elem in data:
        await message.answer(elem)





async def command_docs(message: Message) -> None:
    """
    Отсылает документацию по работе с ботом:
    его функциями из .yml файла
    """
    await message.answer(
        "В начале подготовьте вашего бота к использованию\n"
        "Передайте параметры в .env файл\n"
        "Запустите docker-compose.yml через make build сбилдит\n"
        "Далее make up для поднятия контейнеров\n"
        "Если необходимо, то сделайте alembic revision, команда доступна в makefile\n"
        "alembic_revision\n"
        "alembic_upgrade\n"
        "Если проблемы, то возможно, стоит сменить в .env файле host на localhost,\n"
        "сделать миграции и затем поменять обратно"
    )
    await message.answer(
        "При старте нажмите на prepare_exam и подождите парсинга и формирования данных в таблицах\n"
        "Далее нажмите на start_exam и выберите мод работы из стандартного или ваш"
    )
