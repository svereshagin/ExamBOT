import asyncio
import logging
import sys
from contextlib import suppress

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from bot.app.keyboards.Keyboard_Manager import Menu

# Настройка логирования
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Инициализация бота
API_TOKEN = "7084142136:AAE-P9SMdAWgMzeyl9CpV9Qvd1WVwFp1CVY"  # Замените на ваш токен
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
dp.callback_query.middleware(CallbackAnswerMiddleware())


class PrepareExam(StatesGroup):
    login: State = State()
    password: State = State()
    links: State = State()


@dp.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    await state.set_state(PrepareExam.login)
    await message.answer("Введите логин")


@dp.message(PrepareExam.login)
async def process_login(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer(f"Введён логин: {message.text}")
    await message.answer("Введите пароль")
    await state.set_state(PrepareExam.password)


@dp.message(PrepareExam.password)
async def process_password(message: Message, state: FSMContext) -> None:
    await state.update_data(password=message.text)
    await message.answer(f"Введён пароль: {message.text}")
    await message.answer("Введите ссылки на сайт. Введите 'стоп', чтобы завершить.")
    await state.set_state(PrepareExam.links)
    await message.answer("Выберите действие:", reply_markup=Menu.inline_stop_button)


@dp.message(PrepareExam.links)
async def process_links(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    links = data.get("links", [])

    # Если введено 'стоп', завершаем ввод ссылок
    if message.text.lower() == "стоп":
        await state.clear()  # Завершаем состояние
        await message.answer("Вы завершили ввод ссылок.")
        await message.answer(f"Собранные ссылки: {links}")
    else:
        links.append(message.text)  # Добавляем новую ссылку
        await state.update_data(
            links=links
        )  # Обновляем состояние с новым списком ссылок
        await message.answer(
            "Ссылка добавлена. Если хотите добавить еще, просто отправьте ее. Введите 'стоп', чтобы завершить."
        )


@dp.callback_query(lambda c: c.data == "stop")
async def stop_links(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer("Вы завершили ввод ссылок.")
    # Получаем собранные ссылки
    data = await state.get_data()
    links = data.get("links", [])
    if links:
        await callback_query.message.answer(
            f"Собранные ссылки: {', '.join(links)}"
        )  # Соединяем ссылки в строку
    else:
        await callback_query.message.answer(
            "Ссылки не были собраны."
        )  # Если нет ссылок
    await state.clear()  # Завершаем состояние


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
