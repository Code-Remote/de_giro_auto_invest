import asyncio
import os

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


class TelegramBotService:
    def __init__(self):
        self.token = os.environ.get('TELEGRAM_TOKEN')
        self.chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        self.bot = Bot(
            token=self.token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )

    async def send_message(self, message: str):
        async with self.bot:
            await self.bot.send_message(self.chat_id, text=message)

    def send_message_sync(self, message: str):
        asyncio.run(self.send_message(message))
