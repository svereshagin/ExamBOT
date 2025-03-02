# TODO Переписать часть с Ботом
import asyncio
import logging
import sys
from contextlib import suppress

from bot.app.bot_instance import bot, dp, set_default_commands


async def main() -> None:
    await set_default_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    with suppress(KeyboardInterrupt):
        asyncio.run(main())

