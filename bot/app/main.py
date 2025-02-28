# TODO Переписать часть с Ботом

import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from bot.app.bot_instance import bot, dp, set_default_commands

# Bot token can be obtained via https://t.me/BotFather

# All handlers should be attached to the Router (or Dispatcher)


async def main() -> None:
    # run events dispatching
    await set_default_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())
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
