import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

# Вставь сюда токен от @BotFather
TOKEN = "8938915066:AAFQZGTZla9H2E4L3wMo8QwpDFUhyLOnWa0"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "👋 Привет! Отправь мне **UID** игрока Free Fire, "
        "и я покажу информацию о профиле."
    )

@dp.message(F.text.isdigit())
async def process_uid(message: Message):
    uid = message.text
    await message.answer(
        f"🎮 **Профиль игрока**\n\n"
        f"🆔 **UID:** `{uid}`\n"
        f"Статус: Активен"
    )

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  
