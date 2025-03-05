import asyncio

from aiogram.types import Message


async def delete_message_later(message: Message, delay: int = 10):
    """Удаляет сообщение через `delay` секунд."""
    await asyncio.sleep(delay)
    await message.delete()