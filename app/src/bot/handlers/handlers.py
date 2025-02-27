import time
from app.bot_instance import dp, bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart, Command

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Hello!")
    for i in range(15):
        await message.reply(f"turn{i}")
        time.sleep(10)
from app.src.Exam.exam_logic import ExamLogic



@dp.message(Command('prepare_exam'))
async def command_prepare_exam(message: Message) -> None:
    """подготовка к экзамену, запрос ссылок для парсинга"""
    await message.answer('true')

@dp.message(Command('update'))
async def command_update(message: Message) -> None:
    """изменить(обновить значение) у оценки учащегося"""
    await message.answer('update unit')

@dp.message(Command('exam'))
async def command_exam(message: Message) -> None:
    """Основной класс для начала экзамена"""

@dp.message(Command('students'))
async def command_students(message: Message) -> None:
    """Отсылает ведомость по ученикам:
    подключается к БД, берёт данные из неё
    отсылает в виде ученик : оценка

    также стоит настроить на клв сдавших на 5/4/3 и не сдавших для ведомостей.
    """
    pass
@dp.message(Command('docs'))
async def command_docs(message: Message) -> None:
    """Отсылает документацию по работе с ботом:
    его функциями из .yml файла
    """
    await message.answer('231')


@dp.message_handler(commands=['start_timer'])
async def start_timer(message: Message):
    chat_id = message.chat.id
    seconds = 10  # Задай нужное количество секунд
    asyncio.create_task(countdown_timer_bot(chat_id, seconds))
    await message.answer("Таймер запущен!")



async def main() -> None:
    # Запуск обработки событий
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
