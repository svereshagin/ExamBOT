# # TODO Переписать часть с Ботом
#
if '__main__' == __name__:
    from bot.app.services.selenium_parser.parcer import get_students_from_site
    r = get_students_from_site()
    print(r)
# import asyncio
# import logging
# import sys
# from os import getenv
#
# from aiogram import Bot, Dispatcher, html
# from aiogram.client.default import DefaultBotProperties
# from aiogram.enums import ParseMode
# from aiogram.filters import CommandStart
# from aiogram.types import Message
#
# # Bot token can be obtained via https://t.me/BotFather
# TOKEN = "7084142136:AAE-P9SMdAWgMzeyl9CpV9Qvd1WVwFp1CVY"
# # All handlers should be attached to the Router (or Dispatcher)
#
# dp = Dispatcher()
#
#
# @dp.message(CommandStart())
# async def command_start_handler(message: Message) -> None:
#     """
#     This handler receives messages with `/start` command
#     """
#     # Most event objects have aliases for API methods that can be called in events' context
#     # For example if you want to answer to incoming message you can use `message.answer(...)` alias
#     # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
#     # method automatically or call API method directly via
#     # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
#     await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
#
#
# @dp.message()
# async def echo_handler(message: Message) -> None:
#     """
#     Handler will forward receive a message back to the sender
#
#     By default, message handler will handle all message types (like a text, photo, sticker etc.)
#     """
#     try:
#         # Send a copy of the received message
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         # But not all the types is supported to be copied so need to handle it
#         await message.answer("Nice try!")
#
#
# async def main() -> None:
#     # Initialize Bot instance with default bot properties which will be passed to all API calls
#     bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
#
#     # And the run events dispatching
#     await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())
# # import asyncio
# # from src.bot_instance import bot
# # from src.app.handlers.handlers import register_handlers
# # from src.database.db_sessions import reset_database
# # from src.configs.commands import tcm
# # from src.configs.keyboard_manager import initialize_keyboard_manager
# #
# #
# # async def start_bot():
# #     await reset_database()
# #     await tcm.set_start_commands()
# #     register_handlers(bot)
# #     print("Bot is running...")
# #     await bot.polling()
# #
# #
# # async def main():
# #     await initialize_keyboard_manager()
# #     await start_bot()
# #
# # if __name__ == "__main__":
# #     asyncio.run(main())
# #
# # if '__main__' == __name__:
# #     links = get_links()
# #     res = run_registration(links)
# #     print(res)
# #
# # import yaml
# #
# #
# # def get_links() -> list:
# #     with open('fastapi_app/app/links.yml', 'r', encoding='UTF-8') as file:
# #         data = yaml.safe_load(file)
# #     return data['links']
# #
# # from src.src.selenium_parser.parcer import run_registration
# #
# # if '__main__' == __name__:
# #     links = get_links()
# #     res = run_registration(links)
# #     print(res)
