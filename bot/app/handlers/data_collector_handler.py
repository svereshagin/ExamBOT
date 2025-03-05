import asyncio
from typing import Any

from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from bot.app.keyboards.Keyboard_Manager import Menu
from bot.app.logger.logger_file import logger
from bot.app.services.selenium_parser.parsing_logic_aiogram import parsing_logic
from bot.app.utilities.delete_msg import delete_message_later

router = Router()

class PrepareExam(StatesGroup):
    login: State = State()
    password: State = State()
    links: State = State()



@router.message(PrepareExam.login)
async def process_login(message: Message, state: FSMContext) -> None:
    await state.update_data(login=message.text)
    response = await message.answer(f"Введён логин: {message.text}")
    asyncio.create_task(delete_message_later(response, delay=20))
    asyncio.create_task(delete_message_later(message, delay=60))
    response = await message.answer("Введите пароль")
    asyncio.create_task(delete_message_later(response, delay=60))

    await state.set_state(PrepareExam.password)


@router.message(PrepareExam.password)
async def process_password(message: Message, state: FSMContext) -> None:
    await state.update_data(password=message.text)
    response = await message.answer(f"Введён пароль: {message.text}")
    asyncio.create_task(delete_message_later(response))
    asyncio.create_task(delete_message_later(message, delay=60))
    response = await message.answer(
        "Введите ссылки на сайт. Введите 'стоп', чтобы завершить.",
        reply_markup=Menu.inline_stop_button
    )
    asyncio.create_task(delete_message_later(response))

    await state.set_state(PrepareExam.links)


@router.message(PrepareExam.links)
async def process_links(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    links = data.get("links", [])

    if message.text.lower() == "стоп":
        await state.clear()
        response = await message.answer("Вы завершили ввод ссылок.")
        asyncio.create_task(delete_message_later(response))

        response = await message.answer(f"Собранные ссылки: {links}")
        asyncio.create_task(delete_message_later(response))
    else:
        links.append(message.text)
        await state.update_data(links=links)

        response = await message.answer(
            "Ссылка добавлена. Если хотите добавить еще, просто отправьте ее. Введите 'стоп', чтобы завершить.",
            reply_markup=Menu.inline_stop_button
        )
        asyncio.create_task(delete_message_later(response))


@router.callback_query(lambda c: c.data == "stop")
async def stop_links(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer("Вы завершили ввод ссылок.")

    user_data: dict[str, Any] = await state.get_data()
    links = user_data.get("links", [])
    login = user_data.get("login")
    password = user_data.get("password")
    user_data: tuple = (login, password, links)
    logger.info(f"User data: {user_data}")

    if links:
        response0 = await callback_query.message.answer("Ссылки:")
        response = await callback_query.message.answer(', '.join(links))

        asyncio.create_task(delete_message_later(response))
        asyncio.create_task(delete_message_later(response0))
    else:
        response = await callback_query.message.answer(
            "Ссылки не были собраны."
        )
        asyncio.create_task(delete_message_later(response))

    await parsing_logic(callback_query.message, user_data)
    await state.clear()
