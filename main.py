import asyncio
import logging
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

# Ваш токен бота
TOKEN = "8938915066:AAF0ZGTIaOH2E4LM3wfb8qupDFUyLOniwa0"

bot = Bot(token=TOKEN, parse_mode="Markdown")
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "👋 **Привет!**\n\n"
        "Отправь мне **UID игрока Free Fire**, и я загружу реальную информацию о профиле!"
    )

@dp.message(F.text.isdigit())
async def process_uid(message: Message):
    uid = message.text.strip()
    await message.answer("🔄 *Получаю данные с сервера Free Fire...*")
    
    # Публичный API для получения информации по UID Free Fire
    api_url = f"https://freefireinfo-zy9l.onrender.com/api/v1/player-profile?uid={uid}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Разбираем полученные данные
                    basic_info = data.get("basicInfo", {})
                    nickname = basic_info.get("nickname", "Неизвестно")
                    level = basic_info.get("level", "Н/Д")
                    region = basic_info.get("region", "Н/Д")
                    likes = basic_info.get("liked", 0)
                    
                    text = (
                        f"🎮 **Профиль игрока Free Fire**\n\n"
                        f"👤 **Никнейм:** `{nickname}`\n"
                        f"🆔 **UID:** `{uid}`\n"
                        f"⭐ **Уровень:** `{level}`\n"
                        f"👍 **Лайки:** `{likes}`\n"
                        f"🌍 **Регион:** `{region}`"
                    )
                    await message.answer(text)
                else:
                    await message.answer("❌ **Игрок с таким UID не найден или сервер недоступен.**")
    except Exception as e:
        await message.answer("⚠️ **Ошибка при получении данных.** Попробуйте позже.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
