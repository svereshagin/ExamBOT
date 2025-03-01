from aiogram.types import Message
from bot.app.config import settings
from bot.app.services.report import make_resulted_report, make_telegram_report
from bot.app.services.selenium_parser.parcer import get_students_from_site
from bot.app.services.Exam.form_questions import form_questions, FormExam
from bot.app.repositories.CRUD import student_exams
from bot.app.logger.logger_file import logger




async def command_start_handler(message: Message) -> None:
    """Returns True if the bot is running else False."""
    logger.info('command_start_handler activated')
    await message.answer(f"Hello! ExamBot version {settings.VERSION}")
    await message.answer(f"Run /command_prepare_exam to get the students out of API cite\n"
                         f"Don't forget to insert your credentials into .env file\n"
                         f"And provide links into bot/yml_files/links in .yml format"
                         f"Good luck with the exam")


async def command_prepare_exam(message: Message) -> None:
    """начало парсинга команда для бизнес логики"""
    try:
        logger.info('command_prepare_exam activated')
        await message.answer('Начало парсинга сайта')

        # Логирование входящего сообщения
        logger.info(f'Получено сообщение: {message.text} от пользователя: {message.from_user.id}')

        students: list = get_students_from_site()
        logger.info(f'Успешно получено {len(students)} студентов из сайта.')

        await message.answer('Операция совершена успешно')
        logger.info('Парсинг прошёл успешно')
        await message.answer("Общее количество студентов: " + str(len(students)))

        form_questions.students = students
        form_exams: list[FormExam] = form_questions.form_groups()
        logger.info('command_prepare_exam: Функция form_groups() создала необходимые обьекты для работы с БД.')

        try:
            logger.info(f'Вызов функции create_students с {len(students)} студентами и {len(form_exams)} экзаменами.')
            await student_exams.create_students(students=students, form_exams=form_exams)
            logger.info('command_prepare_exam: Функция create_students выполнена успешно, студенты добавлены в БД')
        except Exception as e:
            await message.answer("Произошла ошибка при попытке добавления в БД")
            logger.error('command_prepare_exam, при попытке отправки в базу групп студентов, %s', e)
    except Exception as e:
        logger.error('Проблема при операциях: парсинг, либо формировании questions: %s', e)
        await message.answer('Проблема при операциях: парсинг сайта. Проверьте доступность сервера/данных входа/переданных ссылок')

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
    logger.info('command_students activated')





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
    logger.info('command_docs activated')