from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from bot.app.config import settings
from bot.app.services.selenium_parser.parcer import run_registration


async def command_start_handler(message: Message) -> None:
    """Returns True if the bot is running else False."""
    await message.answer(f"Hello! ExamBot version {settings.VERSION}")
    await message.answer(f"Run /command_prepare_exam to get the students out of API cite\n"
                         f"Don't forget to insert your credentials into .env file\n"
                         f"And provide links into bot/yml_files/links in .yml format"
                         f"Good luck with the exam")

async def command_prepare_exam(message: Message) -> None:
    """начало парсинга команда для бизнес логики"""
    res = run_registration()
    await message.answer('true')




async def command_start_exam(message: Message) -> None:
    """
    Основной класс для начала экзамена
    активирует таймер через класс, msg должен перехватывать мод для
    таймера
    """

async def command_students(message: Message) -> None:
    """Отсылает ведомость по ученикам:
    подключается к БД, берёт данные из неё
    отсылает в виде ученик : оценка

    также стоит настроить на клв сдавших на 5/4/3 и не сдавших для ведомостей.
    """
    pass


async def command_docs(message: Message) -> None:
    """Отсылает документацию по работе с ботом:
    его функциями из .yml файла
    """
    await message.answer('231')

