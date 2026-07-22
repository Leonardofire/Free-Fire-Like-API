import logging
import aiohttp
from aiogram import Bot, Dispatcher, executor, types

TOKEN = "8938915066:AAF0ZGTIaOH2E4LM3wfb8qupDFUyLOniwa0"

bot = Bot(token=TOKEN, parse_mode="Markdown")
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        "👋 **Привет!**\n\n"
        "Отправь мне **UID игрока Free Fire**, и я попробую найти информацию о его профиле!"
    )

@dp.message_handler(lambda message: message.text.isdigit())
async def process_uid(message: types.Message):
    uid = message.text.strip()
    status_msg = await message.reply("🔄 *Запрашиваю данные с сервера Free Fire...*")
    
    # Публичный API для получения данных по UID
    url = f"https://freefireinfo-zy9l.onrender.com/api/v1/player-profile?uid={uid}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    basic = data.get("basicInfo", {})
                    
                    nickname = basic.get("nickname", "Неизвестно")
                    level = basic.get("level", "Н/Д")
                    likes = basic.get("liked", 0)
                    region = basic.get("region", "Н/Д")
                    
                    text = (
                        f"🎮 **Профиль игрока Free Fire**\n\n"
                        f"👤 **Никнейм:** `{nickname}`\n"
                        f"🆔 **UID:** `{uid}`\n"
                        f"⭐ **Уровень:** `{level}`\n"
                        f"👍 **Лайки:** `{likes}`\n"
                        f"🌍 **Регион:** `{region}`"
                    )
                    await status_msg.edit_text(text)
                else:
                    await status_msg.edit_text("❌ **Игрок с таким UID не найден или сервер API недоступен.**")
    except Exception as e:
        await status_msg.edit_text("⚠️ **Не удалось подключиться к серверу игры.** Попробуйте позже.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
    
